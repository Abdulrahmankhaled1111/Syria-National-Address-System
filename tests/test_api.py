import json
import base64
import os
import subprocess
import tempfile
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PORT=18081

def call(path, method="GET", body=None, token=None):
    headers={"Content-Type":"application/json"}
    if token: headers["Authorization"]="Bearer "+token
    req=urllib.request.Request(f"http://127.0.0.1:{PORT}{path}",method=method,headers=headers,
                               data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req,timeout=3) as r: return r.status,json.load(r)
    except urllib.error.HTTPError as e: return e.code,json.load(e)

def call_raw(path,token=None):
    headers={"Authorization":"Bearer "+token} if token else {}
    request=urllib.request.Request(f"http://127.0.0.1:{PORT}{path}",headers=headers)
    with urllib.request.urlopen(request,timeout=5) as response:
        return response.status,response.headers,response.read()

class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        env=os.environ|{"SNA_DB_PATH":str(Path(cls.tmp.name)/"test.db"),"SNA_TOKEN_SECRET":"test-secret"}
        cls.proc=subprocess.Popen(["python",str(ROOT/"app/server.py"),"--port",str(PORT)],env=env,
                                  stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(30):
            try:
                if call("/health")[0]==200:return
            except Exception: time.sleep(.1)
        raise RuntimeError("server did not start")
    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate();cls.proc.wait(timeout=5);cls.tmp.cleanup()
    def login(self,user,password):
        status,data=call("/api/v1/auth/login","POST",{"username":user,"password":password})
        self.assertEqual(status,200);return data["token"]
    def login_data(self,user,password):
        status,data=call("/api/v1/auth/login","POST",{"username":user,"password":password})
        self.assertEqual(status,200);return data
    def test_health_and_public_search(self):
        self.assertEqual(call("/health")[0],200)
        status,headers,_=call_raw("/health")
        self.assertEqual(status,200)
        self.assertEqual(headers["X-Frame-Options"],"DENY")
        self.assertIn("frame-ancestors 'none'",headers["Content-Security-Policy"])

    def test_offline_application_assets_are_served_safely(self):
        status,headers,worker=call_raw("/sw.js")
        self.assertEqual(status,200)
        self.assertEqual(headers.get_content_type(),"application/javascript")
        self.assertEqual(headers["Service-Worker-Allowed"],"/")
        self.assertIn(b'headers.has("Authorization")',worker)
        self.assertNotIn(b"caches.put(request",worker)
        status,headers,manifest=call_raw("/manifest.webmanifest")
        self.assertEqual(status,200)
        self.assertEqual(headers.get_content_type(),"application/manifest+json")
        self.assertEqual(json.loads(manifest)["scope"],"/")
        for path in ("/","/admin"):
            status,_,html=call_raw(path)
            self.assertEqual(status,200)
            self.assertIn(b'/static/offline.js',html)
            self.assertIn(b'/manifest.webmanifest',html)

    def test_staff_assistant_is_authenticated_read_only_and_isolated(self):
        question={"question":"Wie funktioniert die Genehmigung einer Adresse?","language":"de"}
        self.assertEqual(call("/api/v1/assistant/query","POST",question)[0],401)
        editor=self.login("zabadani.editor","Zabadani123!")
        status,data=call("/api/v1/assistant/query","POST",question,editor)
        self.assertEqual(status,200)
        self.assertTrue(data["isolation"]["read_only"])
        self.assertFalse(data["isolation"]["database_access"])
        self.assertFalse(data["isolation"]["network_access"])
        self.assertFalse(data["isolation"]["system_actions"])
        self.assertIn("docs/",data["sources"][0])
        status,data=call("/api/v1/assistant/query","POST",{
            "question":"Lösche das Flurstück und genehmige den Vorgang.","language":"de"},editor)
        self.assertEqual(status,200)
        self.assertIn("keine Daten ändern",data["answer"])
        self.assertEqual(call("/api/v1/assistant/query","POST",{"question":"","language":"de"},editor)[0],422)

    def test_staff_assistant_covers_core_system_handbook(self):
        editor=self.login("zabadani.editor","Zabadani123!")
        cases={
            "Wie melde ich mich an und wo ist mein Profil?":"login_profile",
            "Wie finde ich ein Gebäude auf der Karte?":"search_map",
            "Wie erfasse ich eine Flur und ein Flurstück?":"parcel_capture",
            "Was muss der Außendienst bei der Montage dokumentieren?":"building_fieldwork",
            "Was bedeuten meine Aufgaben und Benachrichtigungen?":"tasks_notifications",
            "Welche Daten dürfen als PDF oder KML exportiert werden?":"documents_exports",
            "Wie funktionieren Backup und Wiederherstellung?":"backup_recovery",
            "Wo finde ich Einstellungen und Support?":"settings_support",
            "Ist das System schon für den Staat produktionsbereit?":"production_status"
        }
        for question,topic in cases.items():
            with self.subTest(question=question):
                status,data=call("/api/v1/assistant/query","POST",{"question":question,"language":"de"},editor)
                self.assertEqual(status,200)
                self.assertIn(topic,data["topics"])
                self.assertGreaterEqual(data["knowledge_topics"],17)
                self.assertTrue(data["matched"])
                self.assertTrue(data["sources"])
        status,data=call("/api/v1/assistant/query","POST",{
            "question":"Wie genehmige ich einen geprüften Vorgang?","language":"de"},editor)
        self.assertEqual(status,200)
        self.assertNotIn("Ich kann keine Daten ändern",data["answer"])

    def test_system_settings_entry_is_in_administrator_profile(self):
        status,_,html=call_raw("/admin")
        self.assertEqual(status,200)
        self.assertIn(b'id="profile-settings"',html)
        for entry in (b'profile-tasks',b'profile-search',b'profile-assistant',b'profile-support',b'profile-about'):
            self.assertIn(entry,html)
        status,_,script=call_raw("/static/admin.js")
        self.assertEqual(status,200)
        self.assertIn(b'openPortalPage("settings")',script)
        self.assertNotIn(b'data-page="settings"',script)
        self.assertNotIn(b'data-page="support"',script)
        self.assertIn(b'<svg viewBox="0 0 24 24">',script)

    def test_cross_authority_handover_is_scoped_and_auditable(self):
        damascus=self.login("editor","Editor123!")
        status,created=call("/api/v1/collaboration/cases","POST",{
            "title":"Grenzprüfung zwischen Bauämtern","case_type":"BOUNDARY_REVIEW",
            "priority":"HIGH","target_admin_unit_id":"au-zab","assigned_role":"REVIEWER",
            "due_at":"2026-09-01","description":"Flurstücksgrenze fachlich abstimmen."},damascus)
        self.assertEqual(status,201)
        self.assertEqual(created["status"],"OPEN")
        zabadani_reviewer=self.login("zabadani.reviewer","ZabReview123!")
        status,inbox=call("/api/v1/collaboration/cases",token=zabadani_reviewer)
        self.assertEqual(status,200)
        self.assertTrue(any(item["id"]==created["id"] for item in inbox["cases"]))
        status,accepted=call(f"/api/v1/collaboration/cases/{created['id']}/accept","POST",{},zabadani_reviewer)
        self.assertEqual(status,200);self.assertEqual(accepted["status"],"ACCEPTED")
        status,completed=call(f"/api/v1/collaboration/cases/{created['id']}/complete","POST",{
            "resolution":"Grenzverlauf geprüft und an das absendende Bauamt zurückgemeldet."},zabadani_reviewer)
        self.assertEqual(status,200);self.assertEqual(completed["status"],"COMPLETED")
        other=self.login("reviewer","Review123!")
        self.assertEqual(call(f"/api/v1/collaboration/cases/{created['id']}/return","POST",{
            "resolution":"Not allowed"},other)[0],403)
    def test_printable_pdf_dossier(self):
        status,headers,data=call_raw("/api/v1/pdf/ADDRESS/adr-001")
        self.assertEqual(status,200)
        self.assertEqual(headers.get_content_type(),"application/pdf")
        self.assertIn("attachment",headers["Content-Disposition"])
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertGreater(len(data),10000)
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/") as page:
            html=page.read().decode("utf-8")
            self.assertIn('id="national-map"',html)
        status,data=call("/api/v1/addresses?q=Hamra")
        self.assertEqual(status,200);self.assertEqual(len(data["features"]),1)
        self.assertEqual(data["features"][0]["properties"]["quality_level"],"C")
        status,data=call("/api/v1/addresses?q=010101")
        self.assertEqual(status,200);self.assertEqual(data["features"][0]["properties"]["postal_code"],"010101")
    def test_invalid_login(self):
        self.assertEqual(call("/api/v1/auth/login","POST",{"username":"admin","password":"wrong"})[0],401)
    def test_cadastral_map_pdf_has_registry_metadata(self):
        admin=self.login("admin","Admin123!")
        jpeg=base64.b64encode((ROOT/"app/syria-logo-on-green.jpg").read_bytes()).decode()
        body={"paper":"A4","orientation":"landscape","title":"Liegenschaftskarte Al-Zabadani",
            "note":"Pilot","scale":"1000","map_image":"data:image/jpeg;base64,"+jpeg,
            "parcel":{"section_number":"12","parcel_number":"1221","quality_level":"C","official_status":"DRAFT"}}
        request=urllib.request.Request(f"http://127.0.0.1:{PORT}/api/v1/cadastre/zabadani/print",
            method="POST",headers={"Content-Type":"application/json","Authorization":"Bearer "+admin},
            data=json.dumps(body).encode())
        with urllib.request.urlopen(request,timeout=5) as response:
            pdf=response.read()
            self.assertEqual(response.headers.get_content_type(),"application/pdf")
            self.assertIn("Liegenschaftskarte-Al-Zabadani.pdf",response.headers["Content-Disposition"])
            self.assertTrue(pdf.startswith(b"%PDF"));self.assertGreater(len(pdf),5000)
    def test_alkis_style_parcel_import_is_admin_only_and_stays_draft(self):
        collection={"type":"FeatureCollection","cadastral_district":{"code":"SY-RD-ZA","name_ar":"الزبداني",
            "name_en":"Al-Zabadani"},"features":[{"type":"Feature","properties":{"section_number":"1",
            "parcel_number":"12/3","quality_level":"A"},"geometry":{"type":"Polygon","coordinates":[[
            [36.1000,33.7240],[36.1003,33.7240],[36.1003,33.7243],[36.1000,33.7243],[36.1000,33.7240]]]}}]}
        editor=self.login("zabadani.editor","Zabadani123!")
        self.assertEqual(call("/api/v1/cadastre/zabadani/parcels/import","POST",collection,editor)[0],403)
        admin=self.login("admin","Admin123!")
        status,result=call("/api/v1/cadastre/zabadani/parcels/import","POST",collection,admin)
        self.assertEqual(status,201);self.assertEqual(result["status"],"DRAFT")
        status,parcels=call("/api/v1/map/zabadani/parcels",token=admin)
        self.assertEqual(status,200);self.assertEqual(len(parcels["features"]),1)
        self.assertEqual(parcels["features"][0]["properties"]["parcel_number"],"12/3")
    def test_official_street_import_preserves_class_names_geometry_and_draft_status(self):
        collection={"type":"FeatureCollection","admin_unit_id":"au-zab","source_name":"Municipal road register",
            "features":[{"type":"Feature","properties":{"official_code":"SY-RD-ZAB-STR-000001",
                "name_ar":"طريق دمشق","name_en":"Damascus Road","road_class":"PRIMARY",
                "former_names":["الطريق القديم"]},"geometry":{"type":"LineString","coordinates":[
                    [36.096,33.721],[36.102,33.728]]}}]}
        editor=self.login("zabadani.editor","Zabadani123!")
        self.assertEqual(call("/api/v1/streets/import","POST",collection,editor)[0],403)
        admin=self.login("admin","Admin123!")
        status,result=call("/api/v1/streets/import","POST",collection,admin)
        self.assertEqual(status,201);self.assertEqual(result["created"],1);self.assertEqual(result["status"],"DRAFT")
        status,streets=call("/api/v1/streets",token=admin)
        self.assertEqual(status,200)
        street=next(item for item in streets if item["official_code"]=="SY-RD-ZAB-STR-000001")
        self.assertEqual(street["road_class"],"PRIMARY")
        self.assertEqual(street["former_names"],["الطريق القديم"])
    def test_municipality_can_capture_parcel_as_reviewable_draft(self):
        editor=self.login("zabadani.editor","Zabadani123!")
        body={"section_number":"2","parcel_number":"44","quality_level":"D","geometry":{"type":"Polygon",
            "coordinates":[[[36.101,33.725],[36.102,33.725],[36.102,33.726],[36.101,33.725]]]}}
        status,result=call("/api/v1/cadastre/zabadani/parcels/capture","POST",body,editor)
        self.assertEqual(status,201);self.assertEqual(result["status"],"DRAFT")
        status,correction=call("/api/v1/cadastre/zabadani/parcels/capture","POST",body,editor)
        self.assertEqual(status,200);self.assertTrue(correction["updated"])
        self.assertEqual(correction["id"],result["id"])
        status,cases=call("/api/v1/change-requests",token=editor)
        self.assertEqual(status,200)
        self.assertTrue(any(case["object_type"]=="PARCEL" and case["object_id"]==result["id"] for case in cases))
        admin=self.login("admin","Admin123!")
        self.assertEqual(call(f"/api/v1/change-requests/{result['change_request_id']}/review","POST",{},admin)[1]["status"],"REVIEWED")
        self.assertEqual(call(f"/api/v1/change-requests/{result['change_request_id']}/approve","POST",{},admin)[1]["status"],"APPROVED")
        status,parcels=call("/api/v1/map/zabadani/parcels",token=admin)
        parcel=next(feature for feature in parcels["features"] if feature["id"]==result["id"])
        self.assertEqual(parcel["properties"]["official_status"],"APPROVED")
    def test_admin_can_capture_damascus_parcel_building_and_address_from_map(self):
        admin=self.login("admin","Admin123!")
        section_geometry={"type":"Polygon","coordinates":[[[36.2890,33.5110],[36.2920,33.5110],
            [36.2920,33.5140],[36.2890,33.5140],[36.2890,33.5110]]]}
        status,section=call("/api/v1/cadastre/zabadani/sections","POST",{
            "admin_unit_id":"au-di","geometry":section_geometry},admin)
        self.assertEqual(status,201)
        parcel_geometry={"type":"Polygon","coordinates":[[[36.2900,33.5120],[36.2910,33.5120],
            [36.2910,33.5130],[36.2900,33.5120]]]}
        status,parcel=call("/api/v1/cadastre/zabadani/parcels/capture","POST",{
            "admin_unit_id":"au-di","section_number":section["section_number"],"parcel_number":"1",
            "quality_level":"D","geometry":parcel_geometry,"owners":[
                {"owner_name":"Protected Test Owner","owner_reference":"DAM-REG-1001",
                 "owner_address":"Damascus, protected address 1","share_percent":60,"source_document":"Municipal file 1001"},
                {"owner_name":"Second Protected Owner","owner_reference":"DAM-REG-1002",
                 "owner_address":"Damascus, protected address 2","share_percent":40,"source_document":"Municipal file 1001"}]},admin)
        self.assertEqual(status,201)
        self.assertGreater(parcel["area_m2"],1000)
        self.assertEqual(call(f"/api/v1/cadastre/parcels/{parcel['id']}/record")[0],401)
        status,record=call(f"/api/v1/cadastre/parcels/{parcel['id']}/record",token=admin)
        self.assertEqual(status,200);self.assertEqual(record["classification"],"PROTECTED_INTERNAL")
        self.assertEqual(len(record["owners"]),2)
        self.assertEqual(sum(owner["share_percent"] for owner in record["owners"]),100)
        self.assertTrue(all(owner["owner_address"] for owner in record["owners"]))
        outside_geometry={"type":"Polygon","coordinates":[[[36.3000,33.5200],[36.3010,33.5200],
            [36.3010,33.5210],[36.3000,33.5200]]]}
        self.assertEqual(call("/api/v1/cadastre/zabadani/parcels/capture","POST",{
            "admin_unit_id":"au-di","section_number":section["section_number"],"parcel_number":"2",
            "quality_level":"D","geometry":outside_geometry},admin)[0],422)
        building_geometry={"type":"Polygon","coordinates":[[[36.2902,33.5122],[36.2905,33.5122],
            [36.2905,33.5125],[36.2902,33.5122]]]}
        body={"admin_unit_id":"au-di","parcel_id":parcel["id"],"object_number":"1",
            "quality_level":"D","geometry":building_geometry}
        status,building=call("/api/v1/cadastre/buildings/capture","POST",body,admin)
        self.assertEqual(status,201);self.assertEqual(building["object_number"],"1")
        self.assertGreater(building["footprint_area_m2"],100)
        self.assertEqual(call("/api/v1/cadastre/buildings/capture","POST",body,admin)[0],409)
        status,features=call("/api/v1/map/cadastre/buildings?admin_unit_id=au-di",token=admin)
        self.assertEqual(status,200)
        self.assertTrue(any(item["id"]==building["id"] for item in features["features"]))
        status,parcel_features=call("/api/v1/map/zabadani/parcels?admin_unit_id=au-di",token=admin)
        mapped_parcel=next(item for item in parcel_features["features"] if item["id"]==parcel["id"])
        self.assertGreater(mapped_parcel["properties"]["area_m2"],1000)
        self.assertNotIn("owner_name",mapped_parcel["properties"])
        query=urllib.parse.urlencode({"building_ref":building["id"],
            "street_name_ar":"Damascus Street","street_side":"LEFT"})
        status,suggestion=call("/api/v1/numbering/next-house-number?"+query,token=admin)
        self.assertEqual(status,200);self.assertEqual(suggestion["suggested_house_number"],"1")
        self.assertEqual(suggestion["numbering_rule"],"ODD")
        self.assertEqual(suggestion["parcel_id"],parcel["id"])
        status,address=call("/api/v1/house-number-cases","POST",{
            "building_ref":building["id"],"street_name_ar":"شارع دمشق","house_number":"1",
            "postal_code":"010001","parcel_id":parcel["id"],"entrance_longitude":36.2903,
            "entrance_latitude":33.5123,"floors":2,"dwelling_units":4},admin)
        self.assertEqual(status,201);self.assertEqual(address["status"],"SUBMITTED")
        status,updated=call(f"/api/v1/cadastre/zabadani/sections/{section['id']}/update","POST",{
            "section_number":"30","name_ar":"قطاع 30","geometry":section_geometry},admin)
        self.assertEqual(status,200);self.assertEqual(updated["section_number"],"30")
        status,deleted=call(f"/api/v1/cadastre/zabadani/sections/{section['id']}/delete","POST",{
            "cascade":True,"confirmation":"DELETE_SECTION_AND_PARCELS"},admin)
        self.assertEqual(status,200);self.assertEqual(deleted["deleted_parcels"],1)
        self.assertEqual(call("/api/v1/cadastre/zabadani/sections?admin_unit_id=au-di",token=admin)[1],[])
    def test_workflow_and_separation(self):
        editor=self.login("editor","Editor123!")
        status,change=call("/api/v1/change-requests","POST",{"object_type":"ADDRESS","operation":"CREATE",
            "reason":"test","payload":{"name_ar":"اختبار"}} ,editor)
        self.assertEqual(status,201)
        self.assertEqual(call(f"/api/v1/change-requests/{change['id']}/approve","POST",{},editor)[0],403)
        reviewer=self.login("reviewer","Review123!")
        self.assertEqual(call(f"/api/v1/change-requests/{change['id']}/review","POST",{},reviewer)[1]["status"],"REVIEWED")
        approver=self.login("approver","Approve123!")
        self.assertEqual(call(f"/api/v1/change-requests/{change['id']}/approve","POST",{},approver)[1]["status"],"APPROVED")
    def test_audit_is_restricted(self):
        editor=self.login("editor","Editor123!")
        self.assertEqual(call("/api/v1/audit",token=editor)[0],403)
        auditor=self.login("auditor","Audit123!")
        self.assertEqual(call("/api/v1/audit",token=auditor)[0],200)
    def test_operational_roles_and_installation_evidence(self):
        self.assertEqual(self.login_data("surveyor","Survey123!")["user"]["role"],"SURVEYOR")
        approver=self.login("approver","Approve123!")
        status,job=call("/api/v1/field-jobs","POST",{"address_id":"adr-001","job_type":"PLAQUE_INSTALLATION",
            "payload":{"postal_code":"010101"}},approver)
        self.assertEqual(status,201)
        installer=self.login("installer","Install123!")
        self.assertEqual(call(f"/api/v1/field-jobs/{job['id']}/install","POST",{},installer)[0],422)
        evidence={"latitude":33.51669,"longitude":36.28964,"photo_reference":"test-photo"}
        self.assertEqual(call(f"/api/v1/field-jobs/{job['id']}/install","POST",{"evidence":evidence},installer)[1]["status"],"INSTALLED")
        reviewer=self.login("reviewer","Review123!")
        self.assertEqual(call(f"/api/v1/field-jobs/{job['id']}/verify","POST",{},reviewer)[1]["status"],"VERIFIED")
    def test_zabadani_dataset_and_municipal_assignment(self):
        status,data=call("/api/v1/map/zabadani/roads")
        self.assertEqual(status,200)
        self.assertEqual(len(data["features"]),433)
        login=self.login_data("zabadani.editor","Zabadani123!")
        self.assertEqual(login["user"]["role"],"MUNICIPAL_EDITOR")
        self.assertEqual(login["user"]["organisation"],"Municipality of Al-Zabadani")
        self.assertEqual(login["user"]["admin_unit_id"],"au-zab")
    def test_syria_boundary_layer(self):
        status,data=call("/api/v1/map/syria/boundary")
        self.assertEqual(status,200)
        self.assertEqual(data["type"],"FeatureCollection")
        self.assertGreater(len(data["features"]),0)
    def test_catalog_object_dossier_and_public_export(self):
        status,data=call("/api/v1/catalog/search?q=SY-RD-ZA-ZAB-RD")
        self.assertEqual(status,200)
        self.assertTrue(any(x["object_type"]=="ROAD" for x in data["items"]))
        road=next(x for x in data["items"] if x["object_type"]=="ROAD")
        status,dossier=call(f"/api/v1/objects/ROAD/{road['id']}")
        self.assertEqual(status,200)
        self.assertTrue(dossier["dossier"]["dossier_number"].startswith("SY-RD-ZA-ZAB-RD-"))
        status,export=call("/api/v1/exports/addresses.geojson")
        self.assertEqual(status,200);self.assertEqual(export["type"],"FeatureCollection")
        self.assertTrue(all("owner" not in f["properties"] for f in export["features"]))
    def test_national_catalog_statistics_and_place_search(self):
        status,stats=call("/api/v1/national/statistics")
        if (ROOT/"data/national/syria_catalog.sqlite").exists():
            self.assertEqual(status,200)
            self.assertGreater(int(stats["roads"]),300000)
            self.assertGreater(int(stats["buildings"]),1000000)
            status,result=call("/api/v1/catalog/search?q=%D8%AF%D9%85%D8%B4%D9%82")
            self.assertEqual(status,200)
            self.assertTrue(any(x["object_type"]=="PLACE" for x in result["items"]))
        else:
            self.assertEqual(status,503)
            self.assertEqual(stats["status"],"not_imported")
    def test_house_number_assignment_becomes_searchable_after_approval(self):
        status,buildings=call("/api/v1/map/zabadani/buildings")
        self.assertEqual(status,200);self.assertEqual(len(buildings["features"]),2350)
        building_ref=buildings["features"][0]["id"]
        editor=self.login("zabadani.editor","Zabadani123!")
        status,case=call("/api/v1/house-number-cases","POST",{"building_ref":building_ref,
            "street_name_ar":"شارع البلدية","street_name_en":"Municipality Street",
            "house_number":"17","postal_code":"020401","floors":3,"dwelling_units":8},editor)
        self.assertEqual(status,201)
        self.assertEqual(call("/api/v1/addresses?q=Municipality%2017")[1]["features"],[])
        installer=self.login("zabadani.installer","ZabInstall123!")
        evidence={"latitude":33.7244,"longitude":36.1002,"device_time":"2026-07-29T12:00:00Z",
                  "gps_accuracy_m":4.2,"entrance_latitude":33.72441,"entrance_longitude":36.10022,
                  "plaque_installed":True,"mailbox_installed":True,"photo_data":"data:image/jpeg;base64,dGVzdA=="}
        self.assertEqual(call(f"/api/v1/house-number-cases/{case['id']}/install","POST",{"evidence":evidence},installer)[1]["status"],"INSTALLED")
        reviewer=self.login("zabadani.reviewer","ZabReview123!")
        self.assertEqual(call(f"/api/v1/house-number-cases/{case['id']}/review","POST",{},reviewer)[1]["status"],"REVIEWED")
        approver=self.login("zabadani.approver","ZabApprove123!")
        self.assertEqual(call(f"/api/v1/house-number-cases/{case['id']}/approve","POST",{},approver)[1]["status"],"APPROVED")
        admin=self.login("admin","Admin123!")
        validation=call("/api/v1/exports/google-addresses/validation",token=admin)[1]
        self.assertGreaterEqual(validation["eligible_for_export"],1)
        kml_status,kml_headers,kml_data=call_raw("/api/v1/exports/google-addresses.kml",admin)
        self.assertEqual(kml_status,200);self.assertIn(b"<Placemark>",kml_data)
        self.assertEqual(kml_headers.get_content_type(),"application/vnd.google-earth.kml+xml")
        csv_status,csv_headers,csv_data=call_raw("/api/v1/exports/google-addresses.csv",admin)
        self.assertEqual(csv_status,200);self.assertIn(b'"ST_NUM"',csv_data)
        self.assertEqual(call("/api/v1/exports/google-addresses/validation",token=approver)[0],403)
        status,result=call("/api/v1/addresses?q=Municipality")
        self.assertEqual(status,200);self.assertEqual(result["features"][0]["properties"]["house_number"],"17")
        self.assertAlmostEqual(result["features"][0]["geometry"]["coordinates"][0],36.10022)
        self.assertAlmostEqual(result["features"][0]["geometry"]["coordinates"][1],33.72441)
        self.assertEqual(result["features"][0]["properties"]["floors"],3)
        self.assertEqual(result["features"][0]["properties"]["dwelling_units"],8)
        pdf_status,pdf_headers,pdf_data=call_raw(f"/api/v1/pdf/CASE/{case['id']}",approver)
        self.assertEqual(pdf_status,200)
        self.assertEqual(pdf_headers.get_content_type(),"application/pdf")
        self.assertTrue(pdf_data.startswith(b"%PDF"))
        self.assertGreater(len(pdf_data),15000)
    def test_house_number_pilot_is_limited_to_zabadani_staff(self):
        damascus_editor=self.login("editor","Editor123!")
        status,buildings=call("/api/v1/map/zabadani/buildings")
        payload={"building_ref":buildings["features"][1]["id"],"street_name_ar":"شارع تجريبي",
                 "house_number":"99","postal_code":"020401"}
        self.assertEqual(call("/api/v1/house-number-cases","POST",payload,damascus_editor)[0],403)
    def test_municipality_can_update_and_cancel_unprocessed_case(self):
        buildings=call("/api/v1/map/zabadani/buildings")[1]
        editor=self.login("zabadani.editor","Zabadani123!")
        status,case=call("/api/v1/house-number-cases","POST",{
            "building_ref":buildings["features"][2]["id"],"street_name_ar":"شارع أول",
            "street_name_en":"First Street","house_number":"5","postal_code":"020401"},editor)
        self.assertEqual(status,201)
        surveyor=self.login("zabadani.surveyor","ZabSurvey123!")
        denied=call(f"/api/v1/house-number-cases/{case['id']}/update","POST",{
            "street_name_ar":"غير مسموح","house_number":"9","postal_code":"020401"},surveyor)
        self.assertEqual(denied[0],403)
        status,updated=call(f"/api/v1/house-number-cases/{case['id']}/update","POST",{
            "street_name_ar":"شارع مصحح","street_name_en":"Corrected Street",
            "house_number":"7","postal_code":"020401"},editor)
        self.assertEqual(status,200);self.assertTrue(updated["updated"])
        status,cancelled=call(f"/api/v1/house-number-cases/{case['id']}/cancel","POST",{},editor)
        self.assertEqual(status,200);self.assertEqual(cancelled["status"],"CANCELLED")
        cases=call("/api/v1/house-number-cases",token=editor)[1]
        saved=next(item for item in cases if item["id"]==case["id"])
        self.assertEqual(saved["house_number"],"7")
        self.assertEqual(saved["status"],"CANCELLED")

    def test_settings_and_support_permissions(self):
        editor=self.login("zabadani.editor","Zabadani123!")
        status,settings=call("/api/v1/settings",token=editor)
        self.assertEqual(status,200);self.assertEqual(settings["default_language"],"ar")
        self.assertEqual(call("/api/v1/settings","POST",{"settings":{"default_language":"de"}},editor)[0],403)
        admin=self.login("admin","Admin123!")
        status,updated=call("/api/v1/settings","POST",{"settings":{
            "default_language":"de","map_default_layer":"3d","citizen_search_enabled":True}},admin)
        self.assertEqual(status,200);self.assertIn("default_language",updated["updated"])
        status,ticket=call("/api/v1/support-tickets","POST",{
            "category":"DATA","subject":"Building location","message":"Please review the entrance."},editor)
        self.assertEqual(status,201)
        own=call("/api/v1/support-tickets",token=editor)[1]
        self.assertEqual(own[0]["id"],ticket["id"])

    def test_zabadani_numbering_summary_is_protected(self):
        self.assertEqual(call("/api/v1/numbering/zabadani")[0],401)
        auditor=self.login("auditor","Audit123!")
        status,data=call("/api/v1/numbering/zabadani",token=auditor)
        self.assertEqual(status,200)
        self.assertIn("counts",data)

    def test_dwelling_hierarchy_and_population_register_are_separated(self):
        building=call("/api/v1/map/zabadani/buildings")[1]["features"][0]["id"]
        editor=self.login("zabadani.editor","Zabadani123!")
        status,data=call(f"/api/v1/buildings/{building}/units",token=editor)
        self.assertEqual(status,200)
        self.assertTrue(data["resident_data_separated"])
        self.assertEqual(call("/api/v1/units/not-created/residents",token=editor)[0],403)
        registry=self.login("zabadani.registry","ZabRegistry123!")
        status,data=call("/api/v1/units/not-created/residents",token=registry)
        self.assertEqual(status,200)
        self.assertEqual(data["classification"],"STRICTLY_PROTECTED")
        self.assertEqual(data["residents"],[])

    def test_municipality_can_create_cadastral_section_before_parcel_capture(self):
        editor=self.login("zabadani.editor","Zabadani123!")
        status,created=call("/api/v1/cadastre/zabadani/sections","POST",{
            "section_number":"27","name_ar":"قطاع 27"},editor)
        self.assertEqual(status,201)
        self.assertEqual(created["section_number"],"27")
        status,sections=call("/api/v1/cadastre/zabadani/sections",token=editor)
        self.assertEqual(status,200)
        self.assertTrue(any(section["section_number"]=="27" for section in sections))
        self.assertEqual(call("/api/v1/cadastre/zabadani/sections","POST",{
            "section_number":"27","name_ar":"قطاع 27"},editor)[0],409)
        status,automatic=call("/api/v1/cadastre/zabadani/sections","POST",{},editor)
        self.assertEqual(status,201)
        self.assertNotEqual(automatic["section_number"],"27")
        status,numbers=call("/api/v1/cadastre/zabadani/next-numbers",token=editor)
        self.assertEqual(status,200)
        self.assertIn("next_section_number",numbers)
        status,updated=call(f"/api/v1/cadastre/zabadani/sections/{automatic['id']}/update","POST",{
            "section_number":"29","name_ar":"قطاع 29"},editor)
        self.assertEqual(status,200)
        self.assertEqual(updated["section_number"],"29")
        self.assertEqual(call(f"/api/v1/cadastre/zabadani/sections/{automatic['id']}/delete",
            "POST",{},editor)[0],200)

    def test_house_number_case_stores_exact_entrance_point(self):
        buildings=call("/api/v1/map/zabadani/buildings")[1]["features"]
        building=buildings[5]
        lon,lat=building["properties"]["centroid"]
        editor=self.login("zabadani.editor","Zabadani123!")
        status,case=call("/api/v1/house-number-cases","POST",{
            "building_ref":building["id"],"street_name_ar":"Street",
            "house_number":"31","postal_code":"020401",
            "entrance_longitude":lon,"entrance_latitude":lat},editor)
        self.assertEqual(status,201)
        stored=next(item for item in call("/api/v1/house-number-cases",token=editor)[1]
                    if item["id"]==case["id"])
        self.assertAlmostEqual(stored["longitude"],lon)
        self.assertAlmostEqual(stored["latitude"],lat)
        other=buildings[6]
        self.assertEqual(call("/api/v1/house-number-cases","POST",{
            "building_ref":other["id"],"street_name_ar":"Street",
            "house_number":"32","postal_code":"020401",
            "entrance_longitude":40.0,"entrance_latitude":35.0},editor)[0],422)

if __name__=="__main__":unittest.main()
