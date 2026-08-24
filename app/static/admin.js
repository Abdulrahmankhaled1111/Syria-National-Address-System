const messages={ar:{portal:"بوابة الإدارة",pilot:"مشروع العناوين والبيانات الجغرافية",public:"البحث العام",protected:"منطقة عمل محمية",headline:"إدارة التغييرات بشكل مضبوط",signedOut:"غير مسجل الدخول",login:"تسجيل الدخول",logout:"تسجيل الخروج",demoNote:"حسابات التجربة موضحة في README وليست للإنتاج.",username:"اسم المستخدم",password:"كلمة المرور",cases:"المعاملات",steps:"خطوات المراجعة",auditable:"قابل للتدقيق",change:"طلب تغيير",fourEyes:"مبدأ الشخصين",objectType:"نوع الكائن",operation:"العملية",reason:"السبب",payload:"البيانات (JSON)",submit:"إرسال",requests:"قائمة المعاملات",refresh:"تحديث",fieldJobs:"الطباعة واللوحات والتركيب",newInstall:"إنشاء أمر تركيب تجريبي",houseNumbers:"تخصيص رقم المنزل",buildingObject:"كائن المبنى",streetArabic:"اسم الشارع بالعربية",houseNumber:"رقم المنزل",postal:"الرمز البريدي",submitHouse:"إرسال للتدقيق"},
en:{portal:"Administration portal",pilot:"Address and geodata pilot",public:"Public search",protected:"Protected workspace",headline:"Manage changes under control",signedOut:"Not signed in",login:"Sign in",logout:"Sign out",demoNote:"Pilot accounts are listed in README and are not for production.",username:"Username",password:"Password",cases:"Cases",steps:"Review steps",auditable:"Auditable",change:"Change request",fourEyes:"Four-eyes principle",objectType:"Object type",operation:"Operation",reason:"Reason",payload:"Payload (JSON)",submit:"Submit",requests:"Request list",refresh:"Refresh",fieldJobs:"Print, plaques and installation",newInstall:"Create pilot installation job",houseNumbers:"Assign house number",buildingObject:"Building object",streetArabic:"Street name in Arabic",houseNumber:"House number",postal:"Postal code",submitHouse:"Submit for review"},
de:{portal:"Verwaltungsportal",pilot:"Adress- und Geodatenpilot",public:"Öffentliche Suche",protected:"Geschützter Arbeitsbereich",headline:"Änderungen kontrolliert fortführen",signedOut:"Nicht angemeldet",login:"Anmelden",logout:"Abmelden",demoNote:"Pilotkonten stehen in der README und sind nicht für Produktion bestimmt.",username:"Benutzername",password:"Passwort",cases:"Vorgänge",steps:"Prüfschritte",auditable:"Auditierbar",change:"Änderungsantrag",fourEyes:"Vier-Augen-Prinzip",objectType:"Objektart",operation:"Vorgang",reason:"Begründung",payload:"Nutzdaten (JSON)",submit:"Einreichen",requests:"Vorgangsliste",refresh:"Aktualisieren",fieldJobs:"Druck, Schilder und Montage",newInstall:"Pilot-Montageauftrag anlegen",houseNumbers:"Hausnummer vergeben",buildingObject:"Gebäudeobjekt",streetArabic:"Straßenname auf Arabisch",houseNumber:"Hausnummer",postal:"Postleitzahl",submitHouse:"Zur Prüfung einreichen"}};
Object.assign(messages.ar,{postalLocality:"الرمز والمدينة",automaticProposal:"اقتراح تلقائي محفوظ",installCapture:"تسجيل تركيب الرقم وصندوق البريد",photo:"صورة إثبات"});
Object.assign(messages.en,{postalLocality:"Postal code and locality",automaticProposal:"Stored automatic proposal",installCapture:"Capture plaque and mailbox installation",photo:"Evidence photo"});
Object.assign(messages.de,{postalLocality:"PLZ und Ort",automaticProposal:"Gespeicherter automatischer Vorschlag",installCapture:"Montage von Nummer und Briefkasten erfassen",photo:"Nachweisfoto"});
Object.assign(messages.ar,{portal:"السجل الوطني للعقارات والعناوين",pilot:"نظام المعلومات الجغرافية السوري",protected:"منطقة العمل",headline:"سجل العقارات والعناوين",cases:"المعاملات المفتوحة",steps:"مراحل الاعتماد",auditable:"سجل التدقيق"});
Object.assign(messages.en,{portal:"National Property and Address Register",pilot:"Syrian geoinformation system",protected:"Workspace",headline:"Property and address register",cases:"Open cases",steps:"Approval stages",auditable:"Audit trail"});
Object.assign(messages.de,{portal:"Nationales Liegenschafts- und Adresskataster",pilot:"Syrisches Geoinformationssystem",protected:"Arbeitsbereich",headline:"Liegenschafts- und Adresskataster",cases:"Offene Vorgänge",steps:"Freigabestufen",auditable:"Prüfprotokoll"});
Object.assign(messages.ar,{systemSettings:"إعدادات النظام"});Object.assign(messages.en,{systemSettings:"System settings"});Object.assign(messages.de,{systemSettings:"Systemeinstellungen"});
Object.assign(messages.ar,{myTasks:"مهامي",quickSearch:"البحث السريع",staffAssistant:"مساعد الموظفين",helpSupport:"المساعدة والدعم",aboutSystem:"حول النظام",productionCandidate:"مرشح للإنتاج · ليس سجلاً رسمياً بعد"});Object.assign(messages.en,{myTasks:"My tasks",quickSearch:"Quick search",staffAssistant:"Staff assistant",helpSupport:"Help and support",aboutSystem:"About the system",productionCandidate:"Production candidate · not yet an official register"});Object.assign(messages.de,{myTasks:"Meine Aufgaben",quickSearch:"Schnellsuche",staffAssistant:"Mitarbeiter-Assistent",helpSupport:"Hilfe und Support",aboutSystem:"Über das System",productionCandidate:"Produktionskandidat · noch kein amtliches Register"});
let lang=localStorage.getItem("sna_lang")||"ar";
function applyLanguage(){document.documentElement.lang=lang;document.documentElement.dir=lang==="ar"?"rtl":"ltr";document.querySelector("#language").value=lang;document.querySelectorAll("[data-i18n]").forEach(e=>e.textContent=messages[lang][e.dataset.i18n]||e.textContent);const searchLabel=lang==="ar"?"البحث العام عن العناوين":lang==="de"?"Öffentliche Adresssuche":"Public address search",helpLabel=lang==="ar"?"المساعدة والدعم":lang==="de"?"Hilfe und Support":"Help and support",profileLabel=lang==="ar"?"ملف المستخدم":lang==="de"?"Benutzerprofil":"User profile";[["#header-search",searchLabel],["#header-help",helpLabel],["#profile-toggle",profileLabel]].forEach(([selector,label])=>{const element=$(selector);if(element){element.setAttribute("aria-label",label);element.title=label}})}
document.querySelector("#language").onchange=e=>{lang=e.target.value;localStorage.setItem("sna_lang",lang);applyLanguage()};
let token=localStorage.getItem("sna_token"), role=localStorage.getItem("sna_role"),organisation=localStorage.getItem("sna_organisation");
const $=s=>document.querySelector(s), esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function show(){if(token){$("#login").classList.add("hidden");$("#dashboard").classList.remove("hidden");$("#header-profile").classList.remove("hidden");document.body.dataset.userRole=role;const roleName=role==="SYSTEM_ADMIN"?(lang==="ar"?"مدير النظام":lang==="de"?"Systemadministrator":"System administrator"):(organisation||"Stadtverwaltung"),initial=role==="SYSTEM_ADMIN"?"A":"G";$("#identity").textContent=roleName+" · "+(lang==="ar"?"مسجل":lang==="de"?"angemeldet":"signed in");$("#profile-name").textContent=roleName;$("#profile-scope").textContent=role==="SYSTEM_ADMIN"?(lang==="ar"?"الوصول الوطني":lang==="de"?"Nationaler Zugriff":"National access"):(organisation||"");$("#profile-initial").textContent=initial;$("#profile-menu-initial").textContent=initial;load()}else{$("#login").classList.remove("hidden");$("#dashboard").classList.add("hidden");$("#header-profile").classList.add("hidden");$("#profile-menu").classList.add("hidden");delete document.body.dataset.userRole;$("#identity").textContent=messages[lang].signedOut}}
$("#toggle-password").onclick=()=>{const input=$("#password"),visible=input.type==="text";input.type=visible?"password":"text";$("#toggle-password").classList.toggle("visible",!visible);const label=lang==="ar"?(visible?"إظهار كلمة المرور":"إخفاء كلمة المرور"):lang==="de"?(visible?"Passwort anzeigen":"Passwort ausblenden"):(visible?"Show password":"Hide password");$("#toggle-password").setAttribute("aria-label",label);$("#toggle-password").title=label};
$("#login-btn").onclick=async()=>{let r=await fetch("/api/v1/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({username:$("#username").value,password:$("#password").value})});let d=await r.json();if(!r.ok){$("#login-error").textContent=lang==="ar"?"فشل تسجيل الدخول. تحقق من اسم المستخدم وكلمة المرور.":lang==="de"?"Anmeldung fehlgeschlagen. Benutzername und Passwort prüfen.":"Sign-in failed. Check username and password.";return}token=d.token;role=d.user.role;organisation=d.user.organisation;localStorage.setItem("sna_token",token);localStorage.setItem("sna_role",role);localStorage.setItem("sna_organisation",organisation||"");show();await loadBuildings()};
$("#password").onkeydown=event=>{if(event.key==="Enter")$("#login-btn").click()};
$("#logout-btn").onclick=()=>{localStorage.removeItem("sna_token");localStorage.removeItem("sna_role");localStorage.removeItem("sna_organisation");token=null;role=null;organisation=null;delete document.body.dataset.userRole;$("#dashboard").classList.add("hidden");$("#dashboard").setAttribute("aria-hidden","true");$("#password").value="";$("#login-error").textContent="";show();location.reload()};
$("#profile-toggle").onclick=event=>{event.stopPropagation();const menu=$("#profile-menu"),open=menu.classList.toggle("hidden")===false;$("#profile-toggle").setAttribute("aria-expanded",String(open))};
$("#profile-menu").onclick=event=>event.stopPropagation();
$("#header-help").onclick=()=>{if(token)openPortalPage("support");else $("#username")?.focus()};
document.addEventListener("click",()=>{$("#profile-menu")?.classList.add("hidden");$("#profile-toggle")?.setAttribute("aria-expanded","false")});
$("#profile-settings").onclick=()=>{$("#profile-menu").classList.add("hidden");$("#profile-toggle").setAttribute("aria-expanded","false");openPortalPage("settings")};
$("#profile-tasks").onclick=()=>{$("#profile-menu").classList.add("hidden");openPortalPage("workflow")};
$("#profile-search").onclick=()=>{$("#profile-menu").classList.add("hidden");openPortalPage("search")};
$("#profile-support").onclick=()=>{$("#profile-menu").classList.add("hidden");openPortalPage("support")};
$("#profile-assistant").onclick=()=>{$("#profile-menu").classList.add("hidden");$("#assistant-launcher")?.click()};
$("#profile-about").onclick=()=>$("#profile-about-card").classList.toggle("hidden");
async function api(path,method="GET",body){let r=await fetch(path,{method,headers:{"Content-Type":"application/json","Authorization":"Bearer "+token,"X-Device-Time":new Date().toISOString()},body:body?JSON.stringify(body):undefined});if(r.status===401){localStorage.removeItem("sna_token");localStorage.removeItem("sna_role");token=null;role=null;show();throw Error("Sitzung abgelaufen")}return [r,await r.json()]}
async function load(){let [r,d]=await api("/api/v1/change-requests");if(!r.ok)return;$("#open-count").textContent=d.length;$("#requests").innerHTML=d.map(x=>`<article class="request"><div class="request-top"><strong>${esc(x.object_type)} · ${esc(x.operation)}</strong><b class="status-${x.status}">${esc(x.status)}</b></div><div class="meta">${esc(x.reason)}<br>${esc(x.id)}</div><div class="request-actions">${x.status==="SUBMITTED"?`<button data-action="review" data-id="${x.id}">Review</button>`:""}${x.status==="REVIEWED"?`<button data-action="approve" data-id="${x.id}">Approve</button>`:""}${["SUBMITTED","REVIEWED"].includes(x.status)?`<button data-action="reject" data-id="${x.id}">Reject</button>`:""}</div></article>`).join("")||"<p class='muted'>No cases.</p>";document.querySelectorAll("[data-action]").forEach(b=>b.onclick=async()=>{let [r,d]=await api(`/api/v1/change-requests/${b.dataset.id}/${b.dataset.action}`,"POST",{});if(!r.ok)alert(d.error+": role or state not permitted");load()});await loadJobs();await loadHouseCases();await loadProposal();await loadCollaborationHub()}
async function loadJobs(){let [r,d]=await api("/api/v1/field-jobs");if(!r.ok)return;$("#create-install-job").classList.toggle("hidden",!["APPROVER","PRINT_OFFICER","SYSTEM_ADMIN"].includes(role));$("#field-jobs").innerHTML=d.map(x=>`<article class="request"><div class="request-top"><strong>${esc(x.job_type)}</strong><b>${esc(x.status)}</b></div><div class="meta">${esc(x.name_ar)} · ${esc(x.postal_code)}<br>${esc(x.id)}</div><div class="request-actions">${x.status==="CREATED"&&role==="PRINT_OFFICER"?`<button data-job="produce" data-id="${x.id}">Produce</button>`:""}${x.status==="IN_PRODUCTION"&&role==="PRINT_OFFICER"?`<button data-job="ready" data-id="${x.id}">Ready</button>`:""}${["READY","CREATED"].includes(x.status)&&role==="INSTALLER"?`<button data-job="install" data-id="${x.id}">Install + evidence</button>`:""}${x.status==="INSTALLED"&&["MUNICIPAL_EDITOR","REVIEWER"].includes(role)?`<button data-job="verify" data-id="${x.id}">Verify</button>`:""}</div></article>`).join("")||"<p class='muted'>No field jobs.</p>";document.querySelectorAll("[data-job]").forEach(b=>b.onclick=async()=>{let body=b.dataset.job==="install"?{evidence:{latitude:33.51669,longitude:36.28964,photo_reference:"pilot-photo",captured_at:new Date().toISOString()}}:{};let [r,d]=await api(`/api/v1/field-jobs/${b.dataset.id}/${b.dataset.job}`,"POST",body);if(!r.ok)alert(d.error);loadJobs()})}
$("#submit-change").onclick=async()=>{try{let payload=JSON.parse($("#payload").value);let [r,d]=await api("/api/v1/change-requests","POST",{object_type:$("#object-type").value,operation:$("#operation").value,reason:$("#reason").value,payload});$("#form-message").textContent=r.ok?"Vorgang eingereicht: "+d.id:d.error;load()}catch(e){$("#form-message").textContent="JSON ist ungültig."}};
$("#create-install-job").onclick=async()=>{let [r,d]=await api("/api/v1/field-jobs","POST",{address_id:"adr-001",job_type:"PLAQUE_INSTALLATION",payload:{plaque_text_ar:"شارع الحمراء ١٢",postal_code:"010101",qr_reference:"SY-DI-MD-ADR-000001"}});if(!r.ok)alert(d.error);loadJobs()};
async function loadBuildings(){let d=await fetch("/api/v1/map/zabadani/buildings").then(r=>r.json());$("#building-ref").innerHTML=d.features.map(f=>`<option value="${esc(f.id)}">${esc(f.properties.technical_code)}</option>`).join("");$("#building-ref").onchange=loadProposal;if(token)await loadProposal()}
async function suggestHouseNumber(showMessage=true){
  const building=$("#building-ref")?.value,street=$("#street-ar")?.value.trim(),side=$("#street-side")?.value||"UNDETERMINED";
  if(!building||!street)return;
  const [response,data]=await api(`/api/v1/numbering/next-house-number?building_ref=${encodeURIComponent(building)}&street_name_ar=${encodeURIComponent(street)}&street_side=${encodeURIComponent(side)}`);
  if(!response.ok){if(showMessage)$("#house-message").textContent=data.error==="building_must_be_linked_to_parcel"?"Das Gebäude muss zuerst einem Flurstück zugeordnet werden.":data.error;return}
  $("#house-number").value=data.suggested_house_number;
  if(doorMarker)doorMarker.getElement().dataset.houseNumber=data.suggested_house_number;
  if(showMessage)$("#house-message").textContent=side==="LEFT"?`Vorschlag ${data.suggested_house_number} · linke Straßenseite · ungerade`:side==="RIGHT"?`Vorschlag ${data.suggested_house_number} · rechte Straßenseite · gerade`:`Vorschlag ${data.suggested_house_number} · fortlaufend`;
}
async function loadProposal(){if(!token||!$("#building-ref").value)return;const button=$("#submit-house-number");button.disabled=false;delete button.dataset.caseId;let [r,d]=await api("/api/v1/numbering/proposal/"+encodeURIComponent($("#building-ref").value));if(!r.ok){let [casesResponse,cases]=await api("/api/v1/house-number-cases");let existing=casesResponse.ok?cases.find(item=>item.building_ref===$("#building-ref").value&&!["CANCELLED","REJECTED"].includes(item.status)):null;if(existing){button.dataset.caseId=existing.id;button.disabled=true;$("#proposal-info").textContent=lang==="ar"?`تم إرسال هذا المبنى بالفعل · ${existing.status}`:lang==="de"?`Für dieses Gebäude wurde bereits ein Vorgang eingereicht · ${existing.status}`:`A case already exists for this building · ${existing.status}`}else{$("#proposal-info").textContent=lang==="ar"?"تسجيل جديد: أدخل الشارع ورقم المنزل.":lang==="de"?"Neue Erfassung: Straße und Hausnummer eintragen.":"New capture: enter street and house number."}return}$("#street-ar").value=d.street_name_ar;$("#house-number").value=d.house_number;$("#house-postal").value=d.postal_code;$("#house-locality").value=d.postal_label;$("#proposal-info").textContent=`${messages[lang].automaticProposal} · ${d.side} · ${d.distance_to_road_m} m · ${d.case_status}`;if(d.case_id){button.dataset.caseId=d.case_id;button.disabled=true}else{button.disabled=false}}
function readPhoto(file){return new Promise((resolve,reject)=>{if(!file)return reject(Error("photo required"));let image=new Image(),reader=new FileReader();reader.onload=()=>{image.onload=()=>{let scale=Math.min(1,900/image.width),canvas=document.createElement("canvas");canvas.width=Math.round(image.width*scale);canvas.height=Math.round(image.height*scale);canvas.getContext("2d").drawImage(image,0,0,canvas.width,canvas.height);resolve(canvas.toDataURL("image/jpeg",.65))};image.src=reader.result};reader.onerror=reject;reader.readAsDataURL(file)})}
function position(){return new Promise((resolve,reject)=>navigator.geolocation.getCurrentPosition(x=>resolve({latitude:x.coords.latitude,longitude:x.coords.longitude,accuracy:x.coords.accuracy}),reject,{enableHighAccuracy:true,timeout:20000,maximumAge:0}))}
async function captureInstallation(button){try{button.disabled=true;let file=document.querySelector(`[data-photo-for="${button.dataset.id}"]`).files[0],photo_data=await readPhoto(file),gps=await position();lastGps=gps;if(!doorPosition)setDoorPosition(gps.longitude,gps.latitude,false);let evidence={latitude:gps.latitude,longitude:gps.longitude,gps_accuracy_m:gps.accuracy,entrance_latitude:doorPosition.latitude,entrance_longitude:doorPosition.longitude,entrance_adjusted:doorPosition.adjusted,photo_data,device_time:new Date().toISOString(),plaque_installed:true,mailbox_installed:true};let [r,d]=await api(`/api/v1/house-number-cases/${button.dataset.id}/install`,"POST",{evidence});if(!r.ok)alert(d.error);await loadHouseCases()}catch(error){alert(error.message||"Nachweis konnte nicht gespeichert werden.")}finally{button.disabled=false}}
async function loadHouseCases(){let [r,d]=await api("/api/v1/house-number-cases");if(!r.ok)return;$("#house-cases").innerHTML=d.map(x=>`<article class="request"><div class="request-top"><strong>${esc(x.street_name_ar)} ${esc(x.house_number)}</strong><b>${esc(x.status)}</b></div><div class="meta">${esc(x.building_ref)} · ${esc(x.postal_code)} ${esc(x.locality_en)}</div>${x.status==="SUBMITTED"&&role==="INSTALLER"?`<div class="install-evidence"><label>${esc(messages[lang].photo)}<input type="file" accept="image/*" capture="environment" data-photo-for="${x.id}"></label><button data-install-case="${x.id}">${esc(messages[lang].installCapture)}</button></div>`:""}<div class="request-actions">${["SUBMITTED","INSTALLED"].includes(x.status)&&["REVIEWER","SYSTEM_ADMIN"].includes(role)?`<button data-house-action="review" data-id="${x.id}">Review</button>`:""}${x.status==="REVIEWED"&&["APPROVER","SYSTEM_ADMIN"].includes(role)?`<button data-house-action="approve" data-id="${x.id}">Approve</button>`:""}</div></article>`).join("")||"<p class='muted'>No house-number cases.</p>";document.querySelectorAll("[data-house-action]").forEach(b=>b.onclick=async()=>{let [r,d]=await api(`/api/v1/house-number-cases/${b.dataset.id}/${b.dataset.houseAction}`,"POST",{});if(!r.ok)alert(d.error);loadHouseCases()});document.querySelectorAll("[data-install-case]").forEach(b=>{b.dataset.id=b.dataset.installCase;b.onclick=()=>captureInstallation(b)})}
$("#submit-house-number").onclick=async()=>{const button=$("#submit-house-number");if(button.dataset.caseId){$("#house-message").textContent=lang==="ar"?"هذا المبنى موجود بالفعل في قائمة المراجعة.":lang==="de"?"Dieses Gebäude befindet sich bereits in der Prüfung.":"This building is already under review.";return}button.disabled=true;$("#house-message").textContent=lang==="ar"?"جارٍ الإرسال…":lang==="de"?"Wird eingereicht…":"Submitting…";try{let [r,d]=await api("/api/v1/house-number-cases","POST",{building_ref:$("#building-ref").value,street_name_ar:$("#street-ar").value.trim(),house_number:$("#house-number").value.trim(),postal_code:$("#house-postal").value.trim(),floors:+$("#building-floors").value,dwelling_units:+$("#building-units").value});if(r.ok){button.dataset.caseId=d.id;$("#house-message").textContent=lang==="ar"?"تم الإرسال بنجاح للمراجعة.":lang==="de"?"Erfolgreich zur Prüfung eingereicht.":"Successfully submitted for review.";await loadHouseCases();await loadProposal()}else{$("#house-message").textContent=d.error==="active_case_exists_for_building"?(lang==="ar"?"هذا المبنى موجود بالفعل في قائمة المراجعة.":lang==="de"?"Für dieses Gebäude besteht bereits ein offener Vorgang.":"An open case already exists for this building."):d.error}}finally{button.disabled=Boolean(button.dataset.caseId)}};
Object.assign(messages.ar,{locateDoor:"موقعي عند الباب",field3d:"عرض ثلاثي الأبعاد",doorPosition:"موضع باب المنزل",gpsWaiting:"حدد موقعك عند الباب.",dragDoor:"يمكن سحب العلامة إلى موضع الباب الصحيح.",gpsAccuracy:"دقة GPS"});
Object.assign(messages.en,{locateDoor:"My position at the door",field3d:"3D view",doorPosition:"House-door position",gpsWaiting:"Determine your position at the door.",dragDoor:"Drag the marker to the correct door position.",gpsAccuracy:"GPS accuracy"});
Object.assign(messages.de,{locateDoor:"Mein Standort an der Haustür",field3d:"3D-Ansicht",doorPosition:"Position der Haustür",gpsWaiting:"Standort direkt an der Haustür bestimmen.",dragDoor:"Die Markierung kann auf die genaue Haustür verschoben werden.",gpsAccuracy:"GPS-Genauigkeit"});
let fieldMap,fieldBuildings,fieldRoads,fieldNumbers,fieldSections,fieldParcels,fieldBoundary,fieldGovernorates,selectedGovernorateBoundary,doorMarker,gpsMarker,governorateStartMarker,fieldParcelOverlay,fieldNationalOverlay,field3d=false,lastGps=null,doorPosition=null,activeAdminUnitId="",refreshChangeGraphics=()=>{},focusActiveAdminArea=()=>{};
function fieldOutsideSyriaMask(boundary){
  const feature=boundary?.features?.[0]||boundary,geometry=feature?.geometry;
  if(!geometry||!["Polygon","MultiPolygon"].includes(geometry.type))return {type:"FeatureCollection",features:[]};
  const close=ring=>{
    const result=ring.map(point=>[Number(point[0]),Number(point[1])]);
    if(result.length&&String(result[0])!==String(result[result.length-1]))result.push([...result[0]]);
    return result;
  };
  const signedArea=ring=>ring.slice(0,-1).reduce((sum,point,index)=>{
    const next=ring[index+1];
    return sum+(point[0]*next[1]-next[0]*point[1]);
  },0)/2;
  const orient=(ring,counterClockwise)=>{
    const closed=close(ring);
    return (signedArea(closed)>0)===counterClockwise?closed:closed.slice().reverse();
  };
  // A regional outer ring avoids crossing the antimeridian. That keeps the
  // outside mask stable in WebGL at every zoom level and with a pitched camera.
  const world=orient([[-30,0],[90,0],[90,70],[-30,70],[-30,0]],true);
  const polygons=geometry.type==="Polygon"?[geometry.coordinates]:geometry.coordinates;
  const territoryHoles=polygons.map(polygon=>polygon?.[0]).filter(ring=>ring?.length>=4).map(ring=>orient(ring,false));
  if(!territoryHoles.length)return {type:"FeatureCollection",features:[]};
  return {type:"FeatureCollection",features:[{type:"Feature",properties:{purpose:"outside-administrative-mask"},geometry:{type:"Polygon",coordinates:[world,...territoryHoles]}}]};
}
function fieldPointInGeometry(longitude,latitude,geometry){
  const inRing=ring=>{let inside=false,j=ring.length-1;for(let i=0;i<ring.length;i++){const [x,y]=ring[i],[xj,yj]=ring[j];if((y>latitude)!==(yj>latitude)&&longitude<(xj-x)*(latitude-y)/((yj-y)||1e-15)+x)inside=!inside;j=i}return inside};
  let polygons=geometry?.coordinates||[];
  if(geometry?.type==="Polygon")polygons=[polygons];
  if(!["Polygon","MultiPolygon"].includes(geometry?.type))return false;
  return polygons.some(polygon=>polygon?.[0]&&inRing(polygon[0])&&!polygon.slice(1).some(inRing));
}
function renderFieldParcelOverlay(){
  if(!fieldMap||!fieldParcelOverlay)return;
  const width=fieldMap.getContainer().clientWidth,height=fieldMap.getContainer().clientHeight;
  fieldParcelOverlay.setAttribute("viewBox",`0 0 ${width} ${height}`);
  if(fieldMap.getZoom()<6){fieldParcelOverlay.innerHTML="";return}
  const polygonMarkup=(features,className,label,selectedValue)=>features.map(feature=>{
    const ring=feature.geometry?.type==="Polygon"?feature.geometry.coordinates?.[0]:null;if(!ring?.length)return "";
    const points=ring.map(coordinate=>fieldMap.project(coordinate));
    const path=points.map((point,index)=>`${index?"L":"M"}${point.x.toFixed(1)},${point.y.toFixed(1)}`).join("")+"Z";
    const total=points.slice(0,-1).reduce((sum,point)=>({x:sum.x+point.x,y:sum.y+point.y}),{x:0,y:0}),count=Math.max(1,points.length-1),x=(total.x/count).toFixed(1),y=(total.y/count).toFixed(1);
    const properties=feature.properties||{},active=String(label(feature))===String(selectedValue),text=className==="screen-section"?`<tspan x="${x}">Flur ${esc(properties.section_number)}</tspan>`:`<tspan x="${x}">Flur ${esc(properties.section_number)}</tspan><tspan x="${x}" dy="13">${esc(properties.parcel_number)}</tspan>`;
    return `<path class="${className}${active?" selected":""}" d="${path}"></path><text class="${className}-label" x="${x}" y="${y}">${text}</text>`;
  }).join("");
  const selectedSection=$("#workflow-section")?.value,selectedParcel=$("#house-parcel")?.value;
  const sections=polygonMarkup(fieldSections?.features||[],"screen-section",feature=>feature.properties?.section_number,selectedSection);
  const parcels=fieldMap.getZoom()>=10?polygonMarkup(fieldParcels?.features||[],"screen-parcel",feature=>feature.id,selectedParcel):"";
  fieldParcelOverlay.innerHTML=sections+parcels;
}
function renderFieldNationalOverlay(){
  if(!fieldMap||!fieldNationalOverlay||!fieldBoundary)return;
  const feature=selectedGovernorateBoundary||(fieldBoundary.features?.[0]||fieldBoundary),geometry=feature?.geometry;
  if(!geometry||!["Polygon","MultiPolygon"].includes(geometry.type)){fieldNationalOverlay.innerHTML="";return}
  const width=fieldMap.getContainer().clientWidth,height=fieldMap.getContainer().clientHeight;
  fieldNationalOverlay.setAttribute("viewBox",`0 0 ${width} ${height}`);
  const corners=[[0,0],[width,0],[width,height],[0,height]].map(point=>fieldMap.unproject(point));
  if(corners.every(point=>fieldPointInGeometry(point.lng,point.lat,geometry))){fieldNationalOverlay.innerHTML="";return}
  const polygons=geometry.type==="Polygon"?[geometry.coordinates]:geometry.coordinates;
  const clipEdge=(points,inside,intersection)=>{
    if(!points.length)return [];
    const result=[];let previous=points[points.length-1],previousInside=inside(previous);
    for(const current of points){const currentInside=inside(current);if(currentInside){if(!previousInside)result.push(intersection(previous,current));result.push(current)}else if(previousInside)result.push(intersection(previous,current));previous=current;previousInside=currentInside}
    return result;
  };
  const clipToViewport=points=>{
    const pad=2,vertical=(a,b,x)=>{const ratio=(x-a.x)/((b.x-a.x)||1e-12);return {x,y:a.y+(b.y-a.y)*ratio}},horizontal=(a,b,y)=>{const ratio=(y-a.y)/((b.y-a.y)||1e-12);return {x:a.x+(b.x-a.x)*ratio,y}};
    let clipped=clipEdge(points,point=>point.x>=-pad,(a,b)=>vertical(a,b,-pad));
    clipped=clipEdge(clipped,point=>point.x<=width+pad,(a,b)=>vertical(a,b,width+pad));
    clipped=clipEdge(clipped,point=>point.y>=-pad,(a,b)=>horizontal(a,b,-pad));
    return clipEdge(clipped,point=>point.y<=height+pad,(a,b)=>horizontal(a,b,height+pad));
  };
  const pathForRing=ring=>{const points=clipToViewport(ring.map(coordinate=>fieldMap.project(coordinate)));return points.length>=3?points.map((point,index)=>`${index?"L":"M"}${point.x.toFixed(1)},${point.y.toFixed(1)}`).join("")+"Z":""};
  const outerPaths=polygons.map(polygon=>polygon?.[0]).filter(Boolean).map(pathForRing).join("");
  const innerPaths=polygons.flatMap(polygon=>polygon?.slice(1)||[]).filter(Boolean).map(pathForRing).join("");
  fieldNationalOverlay.innerHTML=`<defs><mask id="field-scope-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="${width}" height="${height}"><rect width="${width}" height="${height}" fill="white"></rect><path d="${outerPaths}" fill="black"></path>${innerPaths?`<path d="${innerPaths}" fill="white"></path>`:""}</mask></defs><rect class="screen-scope-dim" width="${width}" height="${height}" mask="url(#field-scope-mask)"></rect>`;
}
function syncFieldBoundarySources(){
  if(!fieldMap)return;
  const activeBoundary=selectedGovernorateBoundary||(fieldBoundary?.features?.[0]||fieldBoundary);
  fieldMap.getSource("field-governorate-boundaries")?.setData(fieldGovernorates||{type:"FeatureCollection",features:[]});
  fieldMap.getSource("field-selected-admin-boundary")?.setData(activeBoundary||{type:"FeatureCollection",features:[]});
  fieldMap.getSource("field-active-outside-mask")?.setData(fieldOutsideSyriaMask(activeBoundary));
  if(fieldMap.getLayer("field-3d-governorate-boundaries"))fieldMap.setLayoutProperty("field-3d-governorate-boundaries","visibility",selectedGovernorateBoundary?"none":"visible");
}
function prepareFieldMap(){
  const form=$("#building-ref").closest(".job-panel").querySelector(".house-form"),wrapper=document.createElement("div");
  if(!$("#house-parcel"))form.children[0].insertAdjacentHTML("afterend",`<label><span>Flurstück / القطعة / Parcel</span><select id="house-parcel"><option value="">—</option></select></label>`);
  if(!$("#street-side"))$("#street-ar").closest("label").insertAdjacentHTML("afterend",`<label><span>${lang==="ar"?"جهة الشارع":lang==="de"?"Straßenseite":"Street side"}</span><select id="street-side"><option value="LEFT">${lang==="de"?"Links · ungerade 1, 3, 5":"Left · odd"}</option><option value="RIGHT">${lang==="de"?"Rechts · gerade 2, 4, 6":"Right · even"}</option><option value="UNDETERMINED">${lang==="de"?"Noch nicht bestimmt":"Not determined"}</option></select></label>`);
  if(!$("#suggest-house-number"))$("#house-number").closest("label").insertAdjacentHTML("beforeend",`<button id="suggest-house-number" class="ghost inline-suggest" type="button">${lang==="ar"?"اقتراح الرقم":lang==="de"?"Nummer vorschlagen":"Suggest number"}</button>`);
  $("#suggest-house-number").onclick=()=>suggestHouseNumber(true);
  $("#street-side").onchange=()=>suggestHouseNumber(true);
  wrapper.className="field-map-layout";
  wrapper.innerHTML=`<div class="field-map-pane"><div id="field-map"></div><div id="cadastral-toolbar" class="cadastral-toolbar visible"><div class="cad-tools"><button id="cad-themes" type="button"><svg viewBox="0 0 24 24"><path d="m12 3 8 4.5-8 4.5-8-4.5L12 3Z"></path><path d="m4 12 8 4.5 8-4.5M4 16.5l8 4.5 8-4.5"></path></svg><span>${lang==="ar"?"الطبقات":lang==="de"?"Themen":"Layers"}</span></button><button id="cad-tools" type="button"><svg viewBox="0 0 24 24"><path d="M4 7h10M18 7h2M4 12h3M11 12h9M4 17h8M16 17h4"></path><circle cx="16" cy="7" r="2"></circle><circle cx="9" cy="12" r="2"></circle><circle cx="14" cy="17" r="2"></circle></svg><span>${lang==="ar"?"الأدوات":lang==="de"?"Werkzeuge":"Tools"}</span></button></div><div class="cad-title"><span class="cad-portal-mark">SY</span><span>${lang==="ar"?"البوابة الجغرافية الوطنية السورية":lang==="de"?"Nationales Geoportal Syrien":"Syrian National Geoportal"}</span><small>${lang==="ar"?"عرض الموظفين":lang==="de"?"Mitarbeiter-GIS":"Staff GIS"}</small></div><div class="cad-search"><button id="cad-coordinates" type="button"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="7"></circle><path d="M12 2v4M12 18v4M2 12h4M18 12h4"></path><circle cx="12" cy="12" r="2"></circle></svg><span>${lang==="de"?"Koordinaten":"Coordinates"}</span></button><button id="cad-parcel" type="button"><svg viewBox="0 0 24 24"><path d="m5 5 12-2 2 15-13 3L5 5Z"></path><path d="m9 4 2 15M6 11l12-2"></path></svg><span>${lang==="de"?"Flurstück":"Parcel"}</span></button><label><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="5.5"></circle><path d="m15 15 4.5 4.5"></path></svg><input id="cad-address-query" placeholder="${lang==="ar"?"بحث عن عنوان أو شارع":lang==="de"?"Adresse, Straße oder Objekt suchen":"Search address, street or object"}"><button id="cad-address-search" type="button" aria-label="${lang==="de"?"Suche starten":"Start search"}"><svg viewBox="0 0 24 24"><path d="M5 12h13M14 8l4 4-4 4"></path></svg></button></label></div></div><div id="cad-themes-panel" class="cad-panel"><strong>${lang==="de"?"Kartenthemen":"Map layers"}</strong><small>${lang==="de"?"Fachdaten für den aktuellen Verwaltungsbereich":"Specialist data for the current scope"}</small><label><input type="checkbox" data-cad-layer="field-buildings-flat" checked> ${lang==="de"?"Gebäude":"Buildings"}</label><label><input type="checkbox" data-cad-layer="field-cadastral-roads" checked> ${lang==="de"?"Straßen und Straßennamen":"Roads and street names"}</label><label><input type="checkbox" data-cad-layer="field-cadastral-numbers" checked> ${lang==="de"?"Amtliche Hausnummern":"Official house numbers"}</label><label><input type="checkbox" data-cad-layer="field-cadastral-parcels" checked> ${lang==="de"?"Fluren und Flurstücke":"Sections and parcels"}</label></div><div id="cad-tools-panel" class="cad-panel"><strong>${lang==="de"?"Kartenwerkzeuge":"Map tools"}</strong><button id="cad-fit-city" type="button">⌂ ${lang==="ar"?"عرض النطاق الإداري":lang==="de"?"Verwaltungsbereich anzeigen":"Show administrative area"}</button><button id="cad-clear-selection" type="button">× ${lang==="de"?"Auswahl aufheben":"Clear selection"}</button></div><div id="cad-message" class="cad-message hidden"></div><div class="field-map-tools"><button id="field-locate" type="button" data-i18n="locateDoor"></button><button id="field-normal" type="button" class="ghost active">${lang==="ar"?"خريطة سوريا":lang==="de"?"Syrien-Karte":"Syria map"}</button><button id="field-cadastral" type="button" class="ghost">${lang==="ar"?"السجل":lang==="de"?"Kataster":"Register"}</button><button id="field-basemap" type="button" class="ghost">${lang==="ar"?"قمر صناعي":lang==="de"?"Satellit":"Satellite"}</button><button id="field-3d" type="button" class="ghost" data-i18n="field3d"></button></div><div id="field-data-status" class="map-quality-badge">${lang==="de"?"Hausnummernvorschläge geladen · Flurstücke nicht geladen":"House-number proposals loaded · parcels not loaded"}</div></div><aside class="field-position-card"><strong data-i18n="doorPosition"></strong><span id="field-gps-status" data-i18n="gpsWaiting"></span><code id="field-door-coordinate">—</code><small data-i18n="dragDoor"></small></aside>`;
  form.before(wrapper);
  $(".field-position-card").insertAdjacentHTML("beforeend",`<button id="field-place-door" class="point-tool-button" type="button"><span aria-hidden="true">●</span> ${lang==="ar"?"تحديد نقطة الباب على الخريطة":lang==="de"?"Haustürpunkt auf Karte setzen":"Place entrance point on map"}</button>`);
  const changeGraphics=document.createElement("section");
  changeGraphics.id="change-graphics-drawer";changeGraphics.className="change-graphics-drawer hidden collapsed";
  changeGraphics.innerHTML=`<button id="change-graphics-toggle" class="change-graphics-toggle" type="button" aria-expanded="false"><span class="map-toggle-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 3 8 4.5-8 4.5-8-4.5L12 3Z"></path><path d="m4 12 8 4.5 8-4.5M4 16.5l8 4.5 8-4.5"></path></svg></span><strong>${lang==="ar"?"رسومات التغيير":lang==="de"?"Änderungsgrafiken Homs":"Homs change graphics"}</strong><small>${lang==="de"?"Kartenart oder Objekt auswählen":"Select map type or object"}</small><i class="map-toggle-chevron"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="m6 8 4 4 4-4"></path></svg></i></button><div class="change-graphics-body"><button id="change-graphics-prev" class="change-graphics-nav" type="button" aria-label="Zurück">‹</button><div id="change-graphics-track" class="change-graphics-track"></div><button id="change-graphics-next" class="change-graphics-nav" type="button" aria-label="Weiter">›</button></div>`;
  $(".field-map-pane").append(changeGraphics);
  $("#change-graphics-toggle strong").textContent=lang==="ar"?"طبقات الخريطة":lang==="de"?"Kartenansicht":"Map view";
  $("#change-graphics-toggle small").textContent=lang==="ar"?"الطرق • السجل العقاري • الصور الجوية":lang==="de"?"Straßen • Kataster • Luftbild":"Roads • Cadastre • Imagery";
  $(".field-position-card strong").textContent=lang==="ar"?"موضع رقم المنزل عند المدخل":lang==="de"?"Position der Hausnummer an der Haustür":"House-number position at the entrance";
  const workflow=document.createElement("section");workflow.className="cadastre-workflow";workflow.innerHTML=`<div class="workflow-head"><strong>${lang==="de"?"Bauamt · Katastererfassung":"Municipal cadastre workflow"}</strong><span>Syrien → Damaskus</span></div><div class="workflow-steps"><div><b>1</b><span>${lang==="de"?"Flurgrenze zeichnen und nummerieren":"Draw and number section"}</span><select id="workflow-section"><option value="">—</option></select><button id="workflow-new-section" type="button">${lang==="de"?"Neue Flur zeichnen":"Draw new section"}</button></div><div><b>2</b><span>${lang==="de"?"Flurstück innerhalb der Flur zeichnen":"Draw parcel inside section"}</span><button id="workflow-capture-parcel" type="button">${lang==="de"?"Flurstück erfassen":"Capture parcel"}</button></div><div><b>3</b><span>${lang==="de"?"Gebäude zuordnen und Hausnummer vergeben":"Link building and assign house number"}</span><button id="workflow-assign-building" type="button">${lang==="de"?"Gebäude/Hausnummer":"Building/address"}</button></div></div><p id="workflow-message"></p>`;
  wrapper.before(workflow);
  const governoratePanel=document.createElement("section");
  governoratePanel.className="governorate-scope-panel";
  governoratePanel.innerHTML=`<div><strong>${lang==="ar"?"نطاق الإدارة":lang==="de"?"Verwaltungsbereich":"Administrative area"}</strong><small>${lang==="ar"?"كل محافظة لها رقم وصلاحيات مستقلة":lang==="de"?"Jedes Gouvernement besitzt eine eigene Kennung und getrennte Zugriffsrechte.":"Each governorate has its own code and access scope."}</small></div><select id="governorate-scope"><option value="">${lang==="ar"?"تحميل المحافظات…":lang==="de"?"Gouvernements werden geladen …":"Loading governorates …"}</option></select><button id="governorate-show" type="button">${lang==="ar"?"عرض منفصل":lang==="de"?"Allein auf Karte anzeigen":"Show separately"}</button><span id="governorate-access-note"></span>`;
  workflow.before(governoratePanel);
  let governorates=[];
  focusActiveAdminArea=(duration=0)=>{
    // Camera changes are valid while raster tiles are still loading. Waiting for
    // map.loaded() left the hard-coded pilot camera active on slow connections.
    if(!fieldMap)return;
    const selected=$("#governorate-scope")?.value||activeAdminUnitId;
    if(!selected)return;
    fieldMap.stop();fieldMap.setMaxBounds(null);
    if(selected==="ALL"){
      governorateStartMarker?.remove();governorateStartMarker=null;
      const national=fieldBoundary?.features?.[0]||fieldBoundary,bounds=new maplibregl.LngLatBounds();
      const add=value=>{if(Array.isArray(value)&&typeof value[0]==="number")bounds.extend(value);else if(Array.isArray(value))value.forEach(add)};
      if(national?.geometry)add(national.geometry.coordinates);
      if(!bounds.isEmpty())fieldMap.fitBounds(bounds,{padding:35,maxZoom:6.8,pitch:0,bearing:0,duration});
      return;
    }
    const item=governorates.find(entry=>entry.id===selected);if(!item)return;
    selectedGovernorateBoundary=fieldGovernorates?.features?.find(feature=>feature.id===selected)||selectedGovernorateBoundary;
    if(!governorateStartMarker){const element=document.createElement("div");element.className="governorate-start-marker";element.title=lang==="de"?"Startpunkt des ausgewählten Gouvernements":"Selected governorate start point";governorateStartMarker=new maplibregl.Marker({element,anchor:"center"}).setLngLat([item.longitude,item.latitude]).addTo(fieldMap)}else governorateStartMarker.setLngLat([item.longitude,item.latitude]);
    if(selectedGovernorateBoundary){
      const bounds=new maplibregl.LngLatBounds(),add=value=>{if(Array.isArray(value)&&typeof value[0]==="number")bounds.extend(value);else if(Array.isArray(value))value.forEach(add)};add(selectedGovernorateBoundary.geometry.coordinates);
      fieldMap.fitBounds(bounds,{padding:{top:90,bottom:54,left:54,right:54},maxZoom:10.8,pitch:0,bearing:0,duration});
    }else fieldMap.jumpTo({center:[item.longitude,item.latitude],zoom:item.zoom,pitch:0,bearing:0});
  };
  api("/api/v1/admin/governorates").then(([response,data])=>{
    if(!response.ok)return;
    governorates=data;
    const national=data.length>1?`<option value="ALL">${lang==="ar"?"سوريا كاملة – ١٤ محافظة":lang==="de"?"Ganz Syrien – 14 Gouvernements":"All Syria – 14 governorates"}</option>`:"";
    $("#governorate-scope").innerHTML=national+data.map(item=>`<option value="${esc(item.id)}">${esc(item.official_code)} · ${esc(lang==="ar"?item.name_ar:item.name_en)}</option>`).join("");
    if(data.length>1){const saved=localStorage.getItem("sna_active_admin_unit"),start=data.find(item=>item.id===saved)||data.find(item=>item.id==="au-di")||data[0];$("#governorate-scope").value=start.id;activeAdminUnitId=start.id}else if(data[0]){$("#governorate-scope").value=data[0].id;activeAdminUnitId=data[0].id}
    setTimeout(()=>$("#governorate-show").click(),0);
  });
  fetch("/api/v1/map/syria/governorates").then(response=>response.json()).then(data=>{
    fieldGovernorates=data;
    const selected=$("#governorate-scope")?.value;
    selectedGovernorateBoundary=selected&&selected!=="ALL"?data.features?.find(feature=>feature.id===selected)||null:null;
    syncFieldBoundarySources();
    renderFieldNationalOverlay();
    focusActiveAdminArea(0);
  });
  $("#governorate-scope").onchange=()=>$("#governorate-show").click();
  $("#governorate-show").onclick=async()=>{
    const selected=$("#governorate-scope").value;
    if(selected)localStorage.setItem("sna_active_admin_unit",selected);
    if(selected==="ALL"){
      activeAdminUnitId="ALL";
      selectedGovernorateBoundary=null;fieldMap.setMaxBounds(null);syncFieldBoundarySources();renderFieldNationalOverlay();
      focusActiveAdminArea(900);$("#governorate-access-note").textContent=lang==="de"?"Nationaler Administrator · Zugriff auf alle 14 Gouvernements":"National administrator · access to all 14 governorates";
      $(".cad-title>span:nth-child(2)").textContent=lang==="ar"?"البوابة الجغرافية الوطنية السورية":lang==="de"?"Nationales Geoportal Syrien":"Syrian National Geoportal";
      $(".workflow-head span").textContent=lang==="de"?"Syrien · 14 getrennte Verwaltungsbereiche":"Syria · 14 separate administrative areas";
      $("#active-register-label").textContent=lang==="ar"?"سوريا · السجل الوطني":lang==="de"?"Syrien · Nationales Register":"Syria · National register";
      $("#cad-fit-city").textContent=lang==="ar"?"عرض سوريا كاملة":lang==="de"?"Ganz Syrien anzeigen":"Show all Syria";
      if($("#parcel-district-label"))$("#parcel-district-label").value=lang==="de"?"Syrien · Gouvernement auswählen":"Syria · select governorate";
      if($("#cad-print-title"))$("#cad-print-title").value=lang==="de"?"Nationale Liegenschaftskarte Syrien":"Syrian national cadastral map";
      await loadBuildings();await loadSections();return;
    }
    const item=governorates.find(entry=>entry.id===selected);if(!item||!fieldMap)return;
    activeAdminUnitId=item.id;
    selectedGovernorateBoundary=fieldGovernorates?.features?.find(feature=>feature.id===item.id)||null;
    syncFieldBoundarySources();
    renderFieldNationalOverlay();
    focusActiveAdminArea(900);
    $("#governorate-access-note").textContent=`${item.official_code} · ${lang==="ar"?item.name_ar:item.name_en} · ${lang==="de"?"eigener Verwaltungsbereich":"separate administrative scope"}`;
    $(".cad-title>span:nth-child(2)").textContent=lang==="ar"?`البوابة الجغرافية · ${item.name_ar}`:lang==="de"?`Geoportal · Gouvernement ${item.name_en}`:`Geoportal · ${item.name_en} Governorate`;
    $(".workflow-head span").textContent=`Syrien → ${lang==="ar"?item.name_ar:item.name_en}`;
    $("#active-register-label").textContent=`${item.official_code} · ${lang==="ar"?item.name_ar:item.name_en}`;
    $("#cad-fit-city").textContent=lang==="ar"?`عرض ${item.name_ar}`:lang==="de"?`${item.name_en} anzeigen`:`Show ${item.name_en}`;
    if($("#parcel-district-label"))$("#parcel-district-label").value=`${item.official_code} · ${lang==="ar"?item.name_ar:item.name_en}`;
    if($("#cad-print-title"))$("#cad-print-title").value=lang==="de"?`Liegenschaftskarte ${item.name_en}`:`Cadastral map ${item.name_en}`;
    if(item.id==="au-di"){$("#house-postal").value="010001";$("#house-locality").value="010001 Damascus"}
    // Keep the camera on the selected administrative area. Loading a building
    // or the first cadastral section must never send the user back to the pilot.
    await loadBuildings();await loadSections();
  };
  $("#workflow-new-section").insertAdjacentHTML("afterend",`<div class="workflow-inline-actions"><button id="workflow-edit-section" class="ghost" type="button">${lang==="de"?"Bearbeiten":"Edit"}</button><button id="workflow-delete-section" class="ghost danger" type="button">${lang==="de"?"Löschen":"Delete"}</button></div>`);
  $("#workflow-capture-parcel").insertAdjacentHTML("afterend",`<div class="workflow-inline-actions"><button id="workflow-edit-parcel" class="ghost" type="button">${lang==="de"?"Grenze bearbeiten":"Edit boundary"}</button><button id="workflow-delete-parcel" class="ghost danger" type="button">${lang==="de"?"Flurstück löschen":"Delete parcel"}</button></div>`);
  $(".cad-title>span:nth-child(2)").textContent=lang==="ar"?"البوابة الجغرافية الوطنية السورية":lang==="de"?"Nationales Geoportal Syrien":"Syrian National Geoportal";
  form.insertAdjacentHTML("beforeend",`<label><span>${lang==="ar"?"عدد الطوابق":lang==="de"?"Etagen":"Floors"}</span><input id="building-floors" type="number" min="0" max="200" value="1"></label><label><span>${lang==="ar"?"عدد الوحدات السكنية":lang==="de"?"Wohnungen":"Dwellings"}</span><input id="building-units" type="number" min="0" max="5000" value="1"></label>`);
  applyLanguage();
  fieldMap=new maplibregl.Map({container:"field-map",style:{version:8,glyphs:"https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf",sources:{street:{type:"raster",tiles:["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],tileSize:256,maxzoom:19,attribution:"© OpenStreetMap contributors"},satellite:{type:"raster",tiles:["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],tileSize:256,maxzoom:18,attribution:"Esri, Maxar, Earthstar Geographics"}},layers:[{id:"street-field",type:"raster",source:"street"},{id:"satellite",type:"raster",source:"satellite"},{id:"field-cadastral-background",type:"background",layout:{visibility:"none"},paint:{"background-color":"#f5e5e9"}}]},center:[36.1002,33.7244],zoom:16.2,pitch:0,bearing:0,antialias:true,preserveDrawingBuffer:true,maxPitch:60,minZoom:3,maxZoom:24,scrollZoom:true,doubleClickZoom:true,dragPan:true,touchZoomRotate:true});
  fieldMap.addControl(new maplibregl.NavigationControl({showCompass:true,showZoom:true,visualizePitch:true}),"bottom-right");
  fieldMap.addControl(new maplibregl.FullscreenControl({container:document.querySelector(".field-map-pane")}),"top-right");
  fieldMap.addControl(new maplibregl.ScaleControl({maxWidth:160,unit:"metric"}),"bottom-left");
  fieldMap.scrollZoom.enable();fieldMap.doubleClickZoom.enable();fieldMap.dragPan.enable();fieldMap.touchZoomRotate.enable();
  fieldNationalOverlay=document.createElementNS("http://www.w3.org/2000/svg","svg");fieldNationalOverlay.classList.add("field-national-screen-overlay");fieldMap.getContainer().append(fieldNationalOverlay);
  fieldParcelOverlay=document.createElementNS("http://www.w3.org/2000/svg","svg");fieldParcelOverlay.classList.add("field-parcel-screen-overlay");fieldMap.getContainer().append(fieldParcelOverlay);
  fieldMap.on("move",()=>{renderFieldNationalOverlay();renderFieldParcelOverlay()});fieldMap.on("resize",()=>{renderFieldNationalOverlay();renderFieldParcelOverlay()});
  fieldMap.on("load",()=>{
    fieldMap.addSource("field-buildings",{type:"geojson",data:fieldBuildings});
    fieldMap.addSource("field-roads",{type:"geojson",data:fieldRoads});
    fieldMap.addSource("field-number-proposals",{type:"geojson",data:fieldNumbers});
    fieldMap.addSource("field-sections",{type:"geojson",data:fieldSections||{type:"FeatureCollection",features:[]}});
    fieldMap.addSource("field-parcels",{type:"geojson",data:fieldParcels});
    fieldMap.addLayer({id:"field-buildings-flat",type:"fill",source:"field-buildings",minzoom:11,layout:{visibility:"none"},paint:{"fill-color":"#aeb3b5","fill-outline-color":"#555d61","fill-opacity":0.92}});
    fieldMap.addLayer({id:"field-buildings-3d",type:"fill-extrusion",source:"field-buildings",minzoom:12,paint:{"fill-extrusion-color":"#dbc28e","fill-extrusion-height":["coalesce",["to-number",["get","height"]],["*",["to-number",["get","building_levels"]],3],9],"fill-extrusion-opacity":.82}});
    fieldMap.addLayer({id:"field-selected-building",type:"line",source:"field-buildings",minzoom:11,filter:["==",["id"],""],paint:{"line-color":"#d02f2f","line-width":4,"line-opacity":1}});
    fieldMap.addLayer({id:"field-cadastral-road-casing",type:"line",source:"field-roads",minzoom:3,layout:{visibility:"none"},paint:{"line-color":"#7a3825","line-width":["interpolate",["linear"],["zoom"],3,.5,10,3.5,17,14],"line-opacity":.9}});
    fieldMap.addLayer({id:"field-cadastral-roads",type:"line",source:"field-roads",minzoom:3,layout:{visibility:"none"},paint:{"line-color":["match",["get","road_class"],"MOTORWAY","#d34f3f","TRUNK","#e07a3f","PRIMARY","#d99535","SECONDARY","#587d9d","#718a7c"],"line-width":["interpolate",["linear"],["zoom"],3,.7,10,2,17,10.5],"line-opacity":.96}});
    fieldMap.addLayer({id:"field-selected-road",type:"line",source:"field-roads",minzoom:10,filter:["==",["id"],""],paint:{"line-color":"#d8a029","line-width":["interpolate",["linear"],["zoom"],10,5,17,15],"line-opacity":0.9}});
    fieldMap.addLayer({id:"field-cadastral-labels",type:"symbol",source:"field-roads",minzoom:6,layout:{visibility:"none","symbol-placement":"line","text-field":["coalesce",["get","name_ar"],["get","name_en"],""],"text-font":["Open Sans Regular"],"text-size":["interpolate",["linear"],["zoom"],6,9,13,12,17,14]},paint:{"text-color":"#20343d","text-halo-color":"#f6f8f3","text-halo-width":2}});
    fieldMap.addLayer({id:"field-cadastral-sections",type:"fill",source:"field-sections",minzoom:6,layout:{visibility:"visible"},paint:{"fill-color":["match",["get","official_status"],"APPROVED","#dfead3","IN_REVIEW","#f2b65f","REJECTED","#e7a7a1","#f2c36f"],"fill-opacity":0.6}});
    fieldMap.addLayer({id:"field-cadastral-section-lines",type:"line",source:"field-sections",minzoom:6,layout:{visibility:"visible"},paint:{"line-color":["match",["get","official_status"],"APPROVED","#426b3a","IN_REVIEW","#a95012","REJECTED","#a23b32","#b45a16"],"line-width":["interpolate",["linear"],["zoom"],6,2.5,16,5],"line-opacity":1}});
    fieldMap.addLayer({id:"field-cadastral-section-labels",type:"symbol",source:"field-sections",minzoom:8,layout:{visibility:"visible","text-field":["concat","Flur ",["get","section_number"]],"text-font":["Open Sans Regular"],"text-size":["interpolate",["linear"],["zoom"],8,13,16,20],"text-allow-overlap":false},paint:{"text-color":"#27472d","text-halo-color":"#ffffff","text-halo-width":2}});
    fieldMap.addLayer({id:"field-cadastral-parcels",type:"fill",source:"field-parcels",minzoom:10,layout:{visibility:"visible"},paint:{"fill-color":["case",["==",["get","official_status"],"APPROVED"],"#efd9df","#f8e9cd"],"fill-opacity":0.72}});
    fieldMap.addLayer({id:"field-cadastral-parcel-lines",type:"line",source:"field-parcels",minzoom:10,layout:{visibility:"visible"},paint:{"line-color":["case",["==",["get","official_status"],"APPROVED"],"#241d20","#b15b16"],"line-width":["interpolate",["linear"],["zoom"],10,2.5,17,4],"line-opacity":1}});
    fieldMap.addLayer({id:"field-cadastral-parcel-labels",type:"symbol",source:"field-parcels",minzoom:10,layout:{visibility:"visible","text-field":["concat","Flur ",["get","section_number"],"\n",["get","parcel_number"]],"text-font":["Open Sans Regular"],"text-size":["interpolate",["linear"],["zoom"],10,12,17,16],"text-allow-overlap":true},paint:{"text-color":"#241d20","text-halo-color":"#ffffff","text-halo-width":2}});
    fieldMap.addLayer({id:"field-selected-parcel",type:"line",source:"field-parcels",minzoom:8,filter:["==",["id"],""],paint:{"line-color":"#c43d2b","line-width":5,"line-opacity":1}});
    fieldMap.addLayer({id:"field-selected-parcel-fill",type:"fill",source:"field-parcels",minzoom:8,filter:["==",["id"],""],paint:{"fill-color":"#efc96f","fill-opacity":0.48}});
    fieldMap.addSource("field-parcel-capture",{type:"geojson",data:{type:"FeatureCollection",features:[]}});
    fieldMap.addLayer({id:"field-parcel-capture-fill",type:"fill",source:"field-parcel-capture",paint:{"fill-color":"#d69424","fill-opacity":.2}});
    fieldMap.addLayer({id:"field-parcel-capture-line",type:"line",source:"field-parcel-capture",paint:{"line-color":"#b3261e","line-width":3,"line-dasharray":[2,1]}});
    fieldMap.addLayer({id:"field-parcel-capture-points",type:"circle",source:"field-parcel-capture",filter:["==",["geometry-type"],"Point"],paint:{"circle-radius":8,"circle-color":"#fff","circle-stroke-color":"#b3261e","circle-stroke-width":3}});
    fieldMap.addLayer({id:"field-parcel-capture-point-labels",type:"symbol",source:"field-parcel-capture",filter:["==",["geometry-type"],"Point"],layout:{"text-field":["get","point_number"],"text-font":["Open Sans Regular"],"text-size":11,"text-allow-overlap":true},paint:{"text-color":"#b3261e"}});
    fieldMap.addLayer({id:"field-cadastral-numbers",type:"symbol",source:"field-number-proposals",minzoom:13.5,layout:{visibility:"none","text-field":["get","house_number"],"text-font":["Open Sans Regular"],"text-size":["interpolate",["linear"],["zoom"],13.5,9,17,13],"text-allow-overlap":false,"text-padding":1},paint:{"text-color":"#15232a","text-halo-color":"#ffffff","text-halo-width":2}});
    if(fieldBoundary){
      fieldMap.addSource("field-syria-boundary",{type:"geojson",data:fieldBoundary});
      fieldMap.addSource("field-syria-outside-mask",{type:"geojson",data:fieldOutsideSyriaMask(fieldBoundary)});
      fieldMap.addLayer({id:"field-syria-outside-white",type:"fill",source:"field-syria-outside-mask",layout:{visibility:"none"},paint:{"fill-color":"#68706d","fill-opacity":.68,"fill-antialias":false}});
      fieldMap.addLayer({id:"field-syria-border-casing",type:"line",source:"field-syria-boundary",paint:{"line-color":"#ffffff","line-width":["interpolate",["linear"],["zoom"],4,6,10,4,16,3],"line-opacity":1}});
      fieldMap.addLayer({id:"field-syria-border",type:"line",source:"field-syria-boundary",paint:{"line-color":"#0b6b4c","line-width":["interpolate",["linear"],["zoom"],4,3.2,10,2.3,16,1.7],"line-opacity":1}});
    }
    fieldMap.addSource("field-governorate-boundaries",{type:"geojson",data:fieldGovernorates||{type:"FeatureCollection",features:[]}});
    const initialActiveBoundary=selectedGovernorateBoundary||(fieldBoundary?.features?.[0]||fieldBoundary);
    fieldMap.addSource("field-selected-admin-boundary",{type:"geojson",data:initialActiveBoundary||{type:"FeatureCollection",features:[]}});
    fieldMap.addSource("field-active-outside-mask",{type:"geojson",data:fieldOutsideSyriaMask(initialActiveBoundary)});
    fieldMap.addLayer({id:"field-active-outside-gray",type:"fill",source:"field-active-outside-mask",paint:{"fill-color":"#5b6560","fill-opacity":.5,"fill-antialias":true}});
    fieldMap.addLayer({id:"field-active-boundary-casing",type:"line",source:"field-selected-admin-boundary",paint:{"line-color":"#ffffff","line-width":["interpolate",["linear"],["zoom"],4,5,12,3.5,18,2.5],"line-opacity":1}});
    fieldMap.addLayer({id:"field-active-boundary",type:"line",source:"field-selected-admin-boundary",layout:{"line-join":"round","line-cap":"round"},paint:{"line-color":"#176247","line-width":["interpolate",["linear"],["zoom"],4,2.8,12,2,18,1.4],"line-opacity":1}});
    fieldMap.addLayer({id:"field-3d-governorate-boundaries",type:"line",source:"field-governorate-boundaries",layout:{visibility:"none"},paint:{"line-color":"#a65b35","line-width":2,"line-opacity":.85}});
    fieldMap.addLayer({id:"field-3d-selected-boundary",type:"line",source:"field-selected-admin-boundary",layout:{visibility:"none"},paint:{"line-color":"#176247","line-width":4,"line-opacity":1}});
    const selectFromMap=event=>{if(captureActive)return;const feature=event.features&&event.features[0];if(feature)selectFieldBuilding(String(feature.id||feature.properties?.id||""))};
    fieldMap.on("click","field-buildings-3d",selectFromMap);
    fieldMap.on("click","field-buildings-flat",selectFromMap);
    fieldMap.on("click","field-cadastral-parcels",event=>{if(captureActive)return;const feature=event.features&&event.features[0];if(feature)selectFieldParcel(String(feature.id||""))});
    fieldMap.on("click","field-cadastral-sections",async event=>{if(captureActive)return;const feature=event.features&&event.features[0],number=String(feature?.properties?.section_number||"");if(!number)return;$("#workflow-section").value=number;await prepareNextParcelNumber();renderFieldParcelOverlay();cadMessage(lang==="de"?`Flur ${number} ausgewählt · neue Flurstücke werden dieser Flur zugeordnet.`:`Section ${number} selected · new parcels will be assigned to it.`)});
    fieldMap.on("click","field-cadastral-roads",event=>{if(captureActive)return;const feature=event.features&&event.features[0];if(!feature)return;fieldMap.setFilter("field-selected-road",["==",["id"],String(feature.id||"")]);const street=feature.properties?.name_ar||feature.properties?.name_en||"";if(street)$("#street-ar").value=street;cadMessage(lang==="de"?`Straße ausgewählt: ${street||"ohne amtlichen Namen"}`:`Road selected: ${street||"unnamed"}`)});
    ["field-buildings-3d","field-buildings-flat"].forEach(layer=>{fieldMap.on("mouseenter",layer,()=>fieldMap.getCanvas().style.cursor=captureActive?"crosshair":"pointer");fieldMap.on("mouseleave",layer,()=>fieldMap.getCanvas().style.cursor=captureActive?"crosshair":"")});
    setFieldMapMode("normal");
    const initialParcel=fieldParcels?.features?.[0];if(initialParcel){fieldMap.setFilter("field-selected-parcel",["==",["id"],String(initialParcel.id)]);fieldMap.setFilter("field-selected-parcel-fill",["==",["id"],String(initialParcel.id)])}
    renderFieldNationalOverlay();
    renderFieldParcelOverlay();
    // Re-apply after the WebGL style is fully ready; this wins every startup race.
    setTimeout(()=>focusActiveAdminArea(0),0);
  });
  let satelliteVisible=false,cadastralVisible=false,mapMode="normal";
  const setFieldMapMode=mode=>{
    mapMode=mode;cadastralVisible=mode==="cadastral";satelliteVisible=mode==="satellite";field3d=mode==="3d";
    const visible=(id,value)=>fieldMap.getLayer(id)&&fieldMap.setLayoutProperty(id,"visibility",value?"visible":"none");
    visible("street-field",mode!=="satellite");visible("satellite",mode==="satellite");visible("field-cadastral-background",false);
    visible("field-syria-outside-white",mode==="roads");visible("field-active-outside-gray",mode!=="roads");visible("field-active-boundary-casing",mode!=="roads");visible("field-active-boundary",mode!=="roads");visible("field-3d-governorate-boundaries",mode!=="roads"&&!selectedGovernorateBoundary);visible("field-3d-selected-boundary",false);
    visible("field-buildings-3d",mode==="3d");visible("field-buildings-flat",mode==="cadastral");
    ["field-cadastral-sections","field-cadastral-section-lines","field-cadastral-section-labels"].forEach(id=>visible(id,mode==="cadastral"));
    ["field-cadastral-parcels","field-cadastral-parcel-lines","field-cadastral-parcel-labels","field-cadastral-numbers"].forEach(id=>visible(id,mode==="cadastral"));
    ["field-cadastral-road-casing","field-cadastral-roads","field-cadastral-labels"].forEach(id=>visible(id,mode==="normal"||mode==="cadastral"||mode==="roads"));
    if(mode==="roads"){visible("field-buildings-flat",false);visible("field-cadastral-numbers",false)}
    if(fieldMap.getLayer("street-field")){fieldMap.setPaintProperty("street-field","raster-saturation",mode==="roads"?-.35:0);fieldMap.setPaintProperty("street-field","raster-contrast",mode==="roads"?.12:0);fieldMap.setPaintProperty("street-field","raster-opacity",mode==="roads"?.92:1)}
    if(fieldMap.getLayer("field-cadastral-road-casing"))fieldMap.setPaintProperty("field-cadastral-road-casing","line-color",mode==="roads"?"#ffffff":"#7a3825");
    if(fieldMap.getLayer("field-cadastral-roads")){fieldMap.setPaintProperty("field-cadastral-roads","line-color",mode==="roads"?["match",["get","road_class"],"MOTORWAY","#c73f35","TRUNK","#d86c36","PRIMARY","#d69a32","SECONDARY","#49779a","#547867"]:"#efb66b");fieldMap.setPaintProperty("field-cadastral-roads","line-opacity",mode==="roads"?1:.96)}
    $("#cadastral-toolbar").classList.add("visible");
    [["#field-normal","normal"],["#field-cadastral","cadastral"],["#field-basemap","satellite"],["#field-3d","3d"]].forEach(([selector,value])=>$(selector)?.classList.toggle("active",mode===value));
    fieldMap.easeTo({pitch:mode==="3d"?50:0,bearing:mode==="3d"?12:0,duration:500});
    renderFieldNationalOverlay();renderFieldParcelOverlay();
  };
  const showFieldCadastral=visible=>setFieldMapMode(visible?"cadastral":"normal");
  refreshChangeGraphics=()=>{
    const drawer=$("#change-graphics-drawer");if(!drawer)return;
    drawer.classList.remove("hidden");
    const views=lang==="ar"?[["roads","خريطة طرق سوريا","الطرق السريعة والرئيسية والمحلية فقط","roads"],["cadastral","السجل العقاري والقطع","أرقام القطع والمباني والمنازل","cadastre"],["normal","الخريطة العامة","المدن والحدود الإدارية","overview"],["satellite","الصور الجوية","صور الأقمار الصناعية","imagery"]]:lang==="de"?[["roads","Straßenkarte Syrien","Nur Autobahnen, Haupt-, Neben- und Lokalstraßen","roads"],["cadastral","Kataster & Flurstücke","Flur-, Flurstücks-, Objekt- und Hausnummern","cadastre"],["normal","Übersichtskarte","Orte und Verwaltungsgrenzen","overview"],["satellite","Luftbild","Satellitenbild zur Orientierung","imagery"]]:[["roads","Syria road map","Motorways, primary, secondary and local roads only","roads"],["cadastral","Cadastre & parcels","Section, parcel, object and house numbers","cadastre"],["normal","Overview map","Places and administrative boundaries","overview"],["satellite","Aerial imagery","Satellite imagery for orientation","imagery"]];
    $("#change-graphics-track").innerHTML=views.map(([mode,title,subtitle,kind])=>`<button class="change-graphic-card" type="button" data-change-view="${mode}"><span class="change-graphic-preview preview-${kind}"><i></i><b></b><em></em></span><strong>${esc(title)}</strong><small>${esc(subtitle)}</small></button>`).join("");
    document.querySelectorAll("[data-change-view]").forEach(button=>button.onclick=()=>{document.querySelectorAll("[data-change-view]").forEach(item=>item.classList.remove("active"));button.classList.add("active");setFieldMapMode(button.dataset.changeView);$("#workflow-message").textContent=lang==="de"?`${button.querySelector("strong").textContent} ausgewählt.`:"Map view selected.";drawer.classList.add("collapsed");$("#change-graphics-toggle").setAttribute("aria-expanded","false")});
    $("#change-graphics-track")?.querySelector(`[data-change-view='${mapMode}']`)?.classList.add("active");
    return;
    const enabled=activeAdminUnitId==="au-hi";drawer.classList.toggle("hidden",!enabled);if(!enabled)return;
    const fixed=[
      ["normal","Bestandskarte","Straßen und Verwaltungsgrenzen","base"],
      ["parcels","Flurstücke","Flur und Flurstücksnummern","parcel"],
      ["buildings","Gebäudeobjekte","Gebäude und Objektakten","building"],
      ["numbers","Hausnummern","Adressen und Eingänge","number"],
      ["changes","Änderungsentwürfe","Neue und geänderte Objekte","change"]
    ];
    const objectCards=[...(fieldParcels?.features||[]).slice(0,20).map(feature=>["object-parcel",`Flur ${feature.properties?.section_number||"—"} · ${feature.properties?.parcel_number||feature.id}`,"Flurstücksakte","parcel",feature.id]),...(fieldBuildings?.features||[]).slice(0,20).map(feature=>["object-building",feature.properties?.technical_code||feature.id,"Gebäudeakte","building",feature.id])];
    $("#change-graphics-track").innerHTML=[...fixed,...objectCards].map(([mode,title,subtitle,kind,id])=>`<button class="change-graphic-card" type="button" data-change-view="${esc(mode)}" ${id?`data-object-id="${esc(id)}"`:""}><span class="change-graphic-preview preview-${kind}"><i></i><b></b><em></em></span><strong>${esc(title)}</strong><small>${esc(subtitle)}</small></button>`).join("");
    document.querySelectorAll("[data-change-view]").forEach(button=>button.onclick=()=>{
      document.querySelectorAll("[data-change-view]").forEach(item=>item.classList.remove("active"));button.classList.add("active");
      const view=button.dataset.changeView,objectId=button.dataset.objectId;
      if(view==="normal")setFieldMapMode("normal");else setFieldMapMode("cadastral");
      if(view==="numbers"&&fieldMap.getLayer("field-cadastral-numbers"))fieldMap.setLayoutProperty("field-cadastral-numbers","visibility","visible");
      if(view==="object-parcel"&&objectId)selectFieldParcel(objectId);
      if(view==="object-building"&&objectId)selectFieldBuilding(objectId);
      $("#workflow-message").textContent=lang==="de"?`${button.querySelector("strong").textContent} ausgewählt.`:"Map view selected.";
    });
    $("#change-graphics-track")?.querySelector("[data-change-view='normal']")?.classList.add("active");
  };
  $("#change-graphics-toggle").onclick=()=>{const drawer=$("#change-graphics-drawer"),collapsed=drawer.classList.toggle("collapsed");$("#change-graphics-toggle").setAttribute("aria-expanded",String(!collapsed))};
  $("#change-graphics-prev").onclick=()=>$("#change-graphics-track").scrollBy({left:-360,behavior:"smooth"});
  $("#change-graphics-next").onclick=()=>$("#change-graphics-track").scrollBy({left:360,behavior:"smooth"});
  $("#field-locate").onclick=locateAtDoor;
  $("#field-place-door").onclick=()=>{stopCapture();const button=$("#field-place-door");button.classList.add("active");fieldMap.getCanvas().style.cursor="crosshair";$("#field-gps-status").className="";$("#field-gps-status").textContent=lang==="de"?"Jetzt die genaue Haustür auf der Karte anklicken.":"Click the exact entrance on the map now.";fieldMap.once("click",event=>{const accepted=setDoorPosition(event.lngLat.lng,event.lngLat.lat,true);button.classList.remove("active");fieldMap.getCanvas().style.cursor="";if(accepted!==false){$("#field-gps-status").textContent=lang==="de"?"Haustürpunkt gesetzt · der Punkt kann verschoben werden.":"Entrance point placed · marker is draggable."}})};
  $("#field-normal").onclick=()=>setFieldMapMode("normal");
  $("#field-cadastral").onclick=()=>setFieldMapMode("cadastral");
  $("#field-basemap").onclick=()=>setFieldMapMode("satellite");
  $("#field-3d").onclick=()=>setFieldMapMode("3d");
  const cadMessage=text=>{const box=$("#cad-message");box.textContent=text;box.classList.remove("hidden");clearTimeout(cadMessage.timer);cadMessage.timer=setTimeout(()=>box.classList.add("hidden"),6500)};
  const closeCadPanels=except=>["#cad-themes-panel","#cad-tools-panel"].forEach(selector=>{if(selector!==except)$(selector).classList.remove("open")});
  $("#cad-themes").onclick=()=>{closeCadPanels("#cad-themes-panel");$("#cad-themes-panel").classList.toggle("open")};
  $("#cad-tools").onclick=()=>{closeCadPanels("#cad-tools-panel");$("#cad-tools-panel").classList.toggle("open")};
  const layerGroups={
    "field-buildings-flat":["field-buildings-flat"],
    "field-cadastral-roads":["field-cadastral-road-casing","field-cadastral-roads","field-cadastral-labels"],
    "field-cadastral-numbers":["field-cadastral-numbers"],
    "field-cadastral-parcels":["field-cadastral-sections","field-cadastral-section-lines","field-cadastral-section-labels","field-cadastral-parcels","field-cadastral-parcel-lines","field-cadastral-parcel-labels"]
  };
  document.querySelectorAll("[data-cad-layer]").forEach(input=>input.onchange=()=>{
    (layerGroups[input.dataset.cadLayer]||[]).forEach(id=>fieldMap.getLayer(id)&&fieldMap.setLayoutProperty(id,"visibility",input.checked&&cadastralVisible?"visible":"none"));
  });
  $("#cad-fit-city").onclick=()=>{closeCadPanels();$("#governorate-show").click()};
  $("#cad-clear-selection").onclick=()=>{closeCadPanels();fieldMap.getLayer("field-selected-building")&&fieldMap.setFilter("field-selected-building",["==",["id"],""]);cadMessage(lang==="de"?"Auswahl aufgehoben.":"Selection cleared.")};
  $("#cad-coordinates").onclick=()=>{closeCadPanels();cadMessage(lang==="de"?"Klicken Sie auf einen Punkt in der Karte.":"Click a point on the map.");fieldMap.once("click",event=>cadMessage(`${event.lngLat.lat.toFixed(7)}, ${event.lngLat.lng.toFixed(7)}`))};
  $("#cad-parcel").onclick=()=>{
    closeCadPanels();
    if(!fieldParcels?.official_data_loaded||!fieldParcels.features?.length){
      cadMessage(lang==="ar"?"بيانات القطع العقارية الرسمية لم تُحمّل بعد. يجب استيرادها والتحقق منها واعتمادها.":lang==="de"?"Amtliche Flurstücksdaten sind noch nicht geladen. Grenzen müssen importiert, geprüft und freigegeben werden.":"Official parcel data is not loaded. Boundaries must be imported, validated and approved.");
      return;
    }
    document.querySelector('[data-cad-layer="field-cadastral-parcels"]').checked=true;
    layerGroups["field-cadastral-parcels"].forEach(id=>fieldMap.getLayer(id)&&fieldMap.setLayoutProperty(id,"visibility","visible"));
    const bounds=new maplibregl.LngLatBounds();
    const addCoordinates=value=>{if(Array.isArray(value)&&typeof value[0]==="number")bounds.extend(value);else if(Array.isArray(value))value.forEach(addCoordinates)};
    fieldParcels.features.forEach(feature=>addCoordinates(feature.geometry.coordinates));
    if(!bounds.isEmpty())fieldMap.fitBounds(bounds,{padding:90,maxZoom:18,duration:700});
    cadMessage(`${fieldParcels.features.length} ${lang==="de"?"Flurstücke geladen und angezeigt.":"parcels loaded and displayed."}`);
  };
  const parcelSearchPanel=document.createElement("div");
  parcelSearchPanel.id="parcel-search-panel";parcelSearchPanel.className="parcel-search-panel hidden";
  parcelSearchPanel.innerHTML=`<div class="parcel-capture-head"><strong>${lang==="ar"?"البحث عن قطعة عقارية":lang==="de"?"Flurstückssuche":"Parcel search"}</strong><button id="parcel-search-close" type="button">×</button></div><label>${lang==="ar"?"المنطقة العقارية":lang==="de"?"Katasterbezirk":"Cadastral district"}<input id="parcel-district-label" value="Syrien · Gouvernement auswählen" readonly></label><label>${lang==="ar"?"القطاع":lang==="de"?"Flur":"Section"}<select id="parcel-search-section"><option value="">—</option></select></label><label>${lang==="ar"?"رقم القطعة":lang==="de"?"Flurstücksnummer":"Parcel number"}<input id="parcel-search-number" inputmode="numeric"></label><button id="parcel-search-submit" type="button">${lang==="ar"?"بحث":lang==="de"?"Suchen und anzeigen":"Search and show"}</button><div id="parcel-search-result" class="muted"></div>`;
  $(".field-map-pane").append(parcelSearchPanel);
  const refreshParcelSearch=()=>{
    const sections=[...new Set((fieldParcels?.features||[]).map(feature=>String(feature.properties?.section_number||"")).filter(Boolean))];
    $("#parcel-search-section").innerHTML=`<option value="">— ${lang==="de"?"Flur wählen":"Select section"} —</option>`+sections.sort((a,b)=>a.localeCompare(b,undefined,{numeric:true})).map(number=>`<option value="${esc(number)}">${lang==="de"?"Flur":"Section"} ${esc(number)}</option>`).join("");
  };
  $("#parcel-search-close").onclick=()=>parcelSearchPanel.classList.add("hidden");
  $("#parcel-search-submit").onclick=async()=>{
    const section=$("#parcel-search-section").value,number=$("#parcel-search-number").value.trim();
    const feature=(fieldParcels?.features||[]).find(item=>(!section||String(item.properties?.section_number)===section)&&(!number||String(item.properties?.parcel_number)===number));
    if(!feature){$("#parcel-search-result").textContent=lang==="de"?"Kein Flurstück mit dieser Kennung gefunden.":"No parcel found.";return}
    parcelSearchPanel.classList.add("hidden");showFieldCadastral(true);await selectFieldParcel(String(feature.id));
    cadMessage(`${lang==="de"?"Ausgewählt":"Selected"}: Flur ${feature.properties.section_number} · Flurstück ${feature.properties.parcel_number} · ${formatArea(feature.properties.area_m2)}`);
  };
  $("#parcel-search-number").onkeydown=event=>{if(event.key==="Enter")$("#parcel-search-submit").click()};
  $("#cad-parcel").onclick=()=>{
    closeCadPanels();
    if(!fieldParcels?.features?.length){cadMessage(lang==="de"?"Noch keine Flurstücke erfasst. Zuerst eine Flur anlegen und danach das Flurstück zeichnen.":"No parcels captured yet.");return}
    refreshParcelSearch();parcelSearchPanel.classList.remove("hidden");$("#parcel-search-section").focus();
  };
  const searchCadastre=async()=>{
    const query=$("#cad-address-query").value.trim();
    if(!query)return;
    const scope=$("#governorate-scope")?.value||"";
    const [response,data]=await api("/api/v1/catalog/search?q="+encodeURIComponent(query)+"&governorate_id="+encodeURIComponent(scope));
    if(!response.ok){cadMessage(data.error||"Search unavailable");return}
    const item=data.items?.find(entry=>Number.isFinite(+entry.longitude)&&Number.isFinite(+entry.latitude));
    if(!item){cadMessage(lang==="de"?"Kein räumliches Ergebnis gefunden.":"No spatial result found.");return}
    if(item.object_type==="BUILDING"&&[...$("#building-ref").options].some(option=>option.value===item.id))await selectFieldBuilding(item.id);
    else fieldMap.flyTo({center:[+item.longitude,+item.latitude],zoom:17,duration:700});
    cadMessage(`${item.label_ar||item.label_en||item.technical_code}`);
  };
  $("#cad-address-search").onclick=searchCadastre;
  $("#cad-address-query").onkeydown=event=>{if(event.key==="Enter"){event.preventDefault();searchCadastre()}};
  let capturePoints=[],captureMarkers=[],captureActive=false,captureTarget="parcel",captureEditSectionId=null;
  const capturePanel=document.createElement("div");
  capturePanel.id="parcel-capture-panel";capturePanel.className="parcel-capture-panel hidden";
  capturePanel.innerHTML=`<div class="parcel-capture-head"><strong>${lang==="ar"?"تسجيل قطعة عقارية":lang==="de"?"Flurstück erfassen":"Capture parcel"}</strong><button id="parcel-capture-close" type="button">×</button></div><p>${lang==="ar"?"انقر على زوايا حدود العقار بالترتيب. ثلاثة نقاط على الأقل.":lang==="de"?"Grenzpunkte der Reihe nach anklicken. Mindestens drei Punkte.":"Click boundary points in order. At least three points."}</p><div class="parcel-capture-fields"><label>${lang==="ar"?"القطاع / الحوض":lang==="de"?"Sektor / Flur":"Section"}<input id="parcel-section" maxlength="30"></label><label>${lang==="ar"?"رقم القطعة":lang==="de"?"Flurstücksnummer":"Parcel number"}<input id="parcel-number" maxlength="50"></label><label>${lang==="ar"?"جودة المصدر":lang==="de"?"Quellenqualität":"Source quality"}<select id="parcel-quality"><option value="D">D · ${lang==="de"?"örtlich erfasst":"field captured"}</option><option value="C">C · ${lang==="de"?"Luft-/Satellitenbild":"imagery"}</option><option value="B">B · ${lang==="de"?"behördlich bestätigt":"authority confirmed"}</option><option value="A">A · ${lang==="de"?"amtlich vermessen":"official survey"}</option></select></label></div><div class="parcel-capture-actions"><button id="parcel-undo" type="button">${lang==="de"?"Letzten Punkt löschen":"Undo point"}</button><button id="parcel-save" type="button">${lang==="ar"?"إرسال للمراجعة":lang==="de"?"Zur Prüfung einreichen":"Submit for review"}</button></div><small id="parcel-capture-status">0 ${lang==="de"?"Grenzpunkte":"points"}</small>`;
  $(".field-map-pane").append(capturePanel);
  capturePanel.querySelector(".parcel-capture-actions").insertAdjacentHTML("beforebegin",`<div id="parcel-owner-fields" class="parcel-owner-fields"><div class="protected-heading"><strong>${lang==="ar"?"سجل ملكية محمي":lang==="de"?"Geschützte Eigentumsakte":"Protected ownership record"}</strong><span>${lang==="de"?"nicht öffentlich":"internal only"}</span></div><label>${lang==="ar"?"المالك / صاحب الحق (اختياري)":lang==="de"?"Eigentümer / Berechtigter (optional)":"Owner / entitled party (optional)"}<input id="parcel-owner-name" maxlength="180" autocomplete="off"></label><label>${lang==="ar"?"رقم الملف أو السجل":lang==="de"?"Akten- oder Registerzeichen":"File or register reference"}<input id="parcel-owner-reference" maxlength="120" autocomplete="off"></label><label>${lang==="ar"?"الحصة بالنسبة المئوية":lang==="de"?"Anteil in Prozent":"Share in percent"}<input id="parcel-owner-share" type="number" min="0.01" max="100" step="0.01" value="100"></label><label>${lang==="ar"?"وثيقة الإثبات":lang==="de"?"Nachweisdokument":"Source document"}<input id="parcel-owner-document" maxlength="180" autocomplete="off"></label></div><div class="capture-area-card"><span>${lang==="ar"?"المساحة المحسوبة":lang==="de"?"Berechnete Fläche":"Calculated area"}</span><strong id="capture-area">—</strong><small>${lang==="de"?"Vorläufig aus der gezeichneten Grenze; amtlich erst nach Vermessungsfreigabe.":"Preliminary from the drawn boundary; official after survey approval."}</small></div>`);
  $("#parcel-undo").insertAdjacentHTML("beforebegin",`<button id="parcel-point-tool" class="point-tool-button active" type="button"><span aria-hidden="true">●</span> ${lang==="ar"?"وضع نقطة حدود":lang==="de"?"Grenzpunkt setzen":"Place boundary point"}</button>`);
  const polygonAreaM2=points=>{
    if(points.length<3)return 0;
    const meanLat=points.reduce((sum,point)=>sum+point[1],0)/points.length*Math.PI/180;
    const projected=points.map(([lng,lat])=>[lng*Math.PI/180*6371008.8*Math.cos(meanLat),lat*Math.PI/180*6371008.8]);
    return Math.abs(projected.reduce((sum,point,index)=>{const next=projected[(index+1)%projected.length];return sum+point[0]*next[1]-next[0]*point[1]},0)/2)
  };
  const formatArea=value=>!Number.isFinite(+value)?"—":+value>=10000?`${(+value/10000).toLocaleString(undefined,{maximumFractionDigits:3})} ha`:`${(+value).toLocaleString(undefined,{maximumFractionDigits:1})} m²`;
  const updateCapture=()=>{
    captureMarkers.forEach(marker=>marker.remove());captureMarkers=[];
    capturePoints.forEach((point,index)=>{const element=document.createElement("div");element.className="parcel-point-marker";element.textContent=String(index+1);const marker=new maplibregl.Marker({element,anchor:"center",draggable:true}).setLngLat(point).addTo(fieldMap);marker.on("dragend",()=>{const position=marker.getLngLat();capturePoints[index]=[+position.lng.toFixed(7),+position.lat.toFixed(7)];updateCapture()});captureMarkers.push(marker)});
    const features=capturePoints.map((point,index)=>({type:"Feature",geometry:{type:"Point",coordinates:point},properties:{point_number:String(index+1)}}));
    if(capturePoints.length>1)features.unshift({type:"Feature",geometry:{type:"LineString",coordinates:capturePoints},properties:{}});
    if(capturePoints.length>2)features.unshift({type:"Feature",geometry:{type:"Polygon",coordinates:[[...capturePoints,capturePoints[0]]]},properties:{}});
    fieldMap.getSource("field-parcel-capture")?.setData({type:"FeatureCollection",features});
    $("#parcel-capture-status").textContent=`${capturePoints.length} ${lang==="de"?"Grenzpunkte":"points"}`;
    $("#capture-area").textContent=formatArea(polygonAreaM2(capturePoints));
  };
  const stopCapture=()=>{captureActive=false;capturePoints=[];capturePanel.classList.add("hidden");fieldMap.getCanvas().style.cursor="";updateCapture()};
  const startCapture=(target="parcel")=>{closeCadPanels();showFieldCadastral(true);captureTarget=target;captureActive=true;capturePoints=[];capturePanel.classList.remove("hidden");capturePanel.classList.remove("saved");fieldMap.getCanvas().style.cursor="crosshair";updateCapture();const building=target==="building",section=target==="section";capturePanel.querySelector(".parcel-capture-head strong").textContent=lang==="de"?(section?"Flurfläche erfassen":building?"Gebäudeobjekt erfassen":"Flurstück erfassen"):(section?"Capture cadastral section":building?"Capture building object":"Capture parcel");capturePanel.querySelector(".parcel-capture-fields label:first-child").firstChild.textContent=lang==="de"?(section?"Flurnummer":building?"Flur des Grundstücks":"Sektor / Flur"):(section?"Section number":building?"Parcel section":"Section");capturePanel.querySelector(".parcel-capture-fields label:nth-child(2)").firstChild.textContent=lang==="de"?(section?"Bezeichnung (optional)":building?"Objektnummer":"Flurstücksnummer"):(section?"Name (optional)":building?"Object number":"Parcel number");$("#parcel-section").readOnly=building;$("#parcel-capture-status").textContent=lang==="de"?(section?"0 Grenzpunkte · Außengrenze der Flur anklicken":building?"0 Gebäudeecken · Gebäudegrundriss anklicken":"0 Grenzpunkte · Karte anklicken"):(section?"0 boundary points · click section boundary":building?"0 building corners · click map":"0 points · click map");cadMessage(lang==="de"?(section?"Die Außengrenze der Flur jetzt der Reihe nach auf der Karte anklicken.":building?"Gebäudeecken jetzt der Reihe nach auf der Karte anklicken.":"Grenzpunkte jetzt in der Karte anklicken."):(section?"Click the outer section boundary on the map.":building?"Click the building corners on the map.":"Click boundary points on the map."))};
  const syncCaptureOwnerFields=()=>{
    const ownerFields=$("#parcel-owner-fields");
    ownerFields.classList.toggle("hidden",captureTarget!=="parcel");
    if(!capturePanel.classList.contains("hidden")){
      $("#parcel-owner-name").value="";$("#parcel-owner-reference").value="";
      $("#parcel-owner-share").value="100";$("#parcel-owner-document").value="";
    }
  };
  new MutationObserver(syncCaptureOwnerFields).observe(capturePanel,{attributes:true,attributeFilter:["class"]});
  let workflowSections=[];
  const loadSections=async()=>{if(!activeAdminUnitId||activeAdminUnitId==="ALL"){workflowSections=[];$("#workflow-section").innerHTML=`<option value="">— ${lang==="de"?"Gouvernement auswählen":"Select governorate"} —</option>`;return}const [response,sections]=await api(`/api/v1/cadastre/zabadani/sections?admin_unit_id=${encodeURIComponent(activeAdminUnitId)}`);if(!response.ok)return;workflowSections=sections;const select=$("#workflow-section"),current=select.value;select.innerHTML=`<option value="">— ${lang==="de"?"Flur wählen":"Select section"} —</option>`+sections.map(section=>`<option value="${esc(section.section_number)}" data-id="${esc(section.id)}">Flur ${esc(section.section_number)} · ${section.parcel_count} ${lang==="de"?"Flurstücke":"parcels"}</option>`).join("");if(current&&sections.some(section=>String(section.section_number)===String(current)))select.value=current;else if(sections.length===1)select.value=sections[0].section_number;if(select.value)await prepareNextParcelNumber();renderFieldParcelOverlay()};
  const prepareNextParcelNumber=async()=>{const section=$("#workflow-section").value;if(!section||!activeAdminUnitId||activeAdminUnitId==="ALL")return;const [response,result]=await api(`/api/v1/cadastre/zabadani/next-numbers?section_number=${encodeURIComponent(section)}&admin_unit_id=${encodeURIComponent(activeAdminUnitId)}`);if(response.ok){$("#parcel-section").value=section;$("#parcel-number").value=result.next_parcel_number}};
  const focusSelectedSection=()=>{const section=workflowSections.find(item=>String(item.section_number)===String($("#workflow-section").value));if(!section?.geometry||!fieldMap)return;const bounds=new maplibregl.LngLatBounds(),add=value=>{if(Array.isArray(value)&&typeof value[0]==="number")bounds.extend(value);else if(Array.isArray(value))value.forEach(add)};add(section.geometry.coordinates);fieldMap.fitBounds(bounds,{padding:90,maxZoom:16,pitch:0,bearing:0,duration:700})};
  $("#workflow-section").onchange=async()=>{await prepareNextParcelNumber();renderFieldParcelOverlay();focusSelectedSection()};
  $("#workflow-new-section").onclick=async()=>{if(!activeAdminUnitId||activeAdminUnitId==="ALL"){$("#workflow-message").textContent=lang==="de"?"Bitte zuerst ein Gouvernement auswählen.":"Select a governorate first.";return}const [response,result]=await api(`/api/v1/cadastre/zabadani/next-numbers?admin_unit_id=${encodeURIComponent(activeAdminUnitId)}`);if(!response.ok){$("#workflow-message").textContent=result.error;return}captureEditSectionId=null;startCapture("section");$("#parcel-section").value=result.next_section_number;$("#parcel-number").value="";$("#parcel-section").focus();$("#workflow-message").textContent=lang==="de"?`Flur ${result.next_section_number}: Außengrenze auf der Karte zeichnen und anschließend speichern.`:`Section ${result.next_section_number}: draw its outer boundary and save.`};
  $("#workflow-edit-section").onclick=async()=>{const section=workflowSections.find(item=>item.section_number===$("#workflow-section").value);if(!section){$("#workflow-message").textContent=lang==="de"?"Bitte eine Flur auswählen.":"Select a section.";return}captureEditSectionId=section.id;startCapture("section");capturePoints=(section.geometry?.coordinates?.[0]||[]).slice(0,-1).map(point=>[...point]);$("#parcel-section").value=section.section_number;$("#parcel-number").value=section.name_ar||"";updateCapture();if(capturePoints.length){const bounds=new maplibregl.LngLatBounds();capturePoints.forEach(point=>bounds.extend(point));fieldMap.fitBounds(bounds,{padding:100,maxZoom:17,duration:600})}$("#workflow-message").textContent=lang==="de"?"Flurnummer oder Bezeichnung ändern und die Grenzpunkte bei Bedarf verschieben. Danach erneut speichern.":"Edit the section number, name, or boundary points and save again."};
  $("#workflow-delete-section").onclick=async()=>{const section=workflowSections.find(item=>item.section_number===$("#workflow-section").value);if(!section)return;const hasParcels=Number(section.parcel_count)>0,message=lang==="de"?(hasParcels?`Flur ${section.section_number} enthält ${section.parcel_count} Flurstücke. Als Administrator werden die Flur und alle enthaltenen Flurstücke gelöscht. Gebäude- und Adressakten bleiben erhalten. Wirklich fortfahren?`:`Flur ${section.section_number} wirklich löschen?`):`Delete section ${section.section_number}${hasParcels?` and its ${section.parcel_count} parcels`:""}?`;if(!confirm(message))return;const body=hasParcels&&role==="SYSTEM_ADMIN"?{cascade:true,confirmation:"DELETE_SECTION_AND_PARCELS"}:{};const [response,result]=await api(`/api/v1/cadastre/zabadani/sections/${section.id}/delete`,"POST",body);$("#workflow-message").textContent=response.ok?(lang==="de"?`Flur gelöscht${result.deleted_parcels?` · ${result.deleted_parcels} Flurstücke mit entfernt`:""}.`:"Section deleted."):(result.error==="section_contains_parcels"?(lang==="de"?"Diese Flur enthält Flurstücke und darf nur vom Systemadministrator vollständig gelöscht werden.":"Only the system administrator may delete a non-empty section."):result.error);if(response.ok){await loadBuildings();await loadSections()}};
  $("#workflow-capture-parcel").onclick=async()=>{const section=$("#workflow-section").value;if(!section){$("#workflow-message").textContent=lang==="de"?"Bitte zuerst eine Flur anlegen oder auswählen.":"Create or select a section first.";return}await prepareNextParcelNumber();startCapture();$("#parcel-section").value=section;$("#parcel-number").focus()};
  $("#workflow-edit-parcel").onclick=async()=>{const id=$("#house-parcel")?.value,feature=fieldParcels?.features?.find(item=>String(item.id)===String(id));if(!feature)return;startCapture();capturePoints=feature.geometry.coordinates[0].slice(0,-1).map(point=>[...point]);$("#parcel-section").value=feature.properties.section_number;$("#parcel-number").value=feature.properties.parcel_number;$("#parcel-quality").value=feature.properties.quality_level||"D";const [recordResponse,record]=await api(`/api/v1/cadastre/parcels/${encodeURIComponent(id)}/record`);if(recordResponse.ok&&record.ownership){$("#parcel-owner-name").value=record.ownership.owner_name||"";$("#parcel-owner-reference").value=record.ownership.owner_reference||"";$("#parcel-owner-share").value=record.ownership.share_percent||100;$("#parcel-owner-document").value=record.ownership.source_document||""}updateCapture();$("#workflow-message").textContent=lang==="de"?"Grenzpunkte oder geschützte Aktenangaben bearbeiten und anschließend erneut einreichen.":"Edit boundary or protected record details and submit again."};
  $("#workflow-delete-parcel").onclick=async()=>{const id=$("#house-parcel")?.value,feature=fieldParcels?.features?.find(item=>String(item.id)===String(id));if(!feature||!confirm(lang==="de"?`Entwurfsflurstück ${feature.properties.section_number}/${feature.properties.parcel_number} wirklich löschen?`:"Delete draft parcel?"))return;const [response,result]=await api(`/api/v1/cadastre/zabadani/parcels/${id}/delete`,"POST",{});$("#workflow-message").textContent=response.ok?(lang==="de"?"Flurstück gelöscht.":"Parcel deleted."):result.error;if(response.ok){await loadBuildings();await loadSections()}};
  $("#workflow-assign-building").onclick=async()=>{const parcelId=$("#house-parcel")?.value;if(!parcelId){$("#workflow-message").textContent=lang==="de"?"Bitte zuerst ein Flurstück auf der Karte auswählen.":"Select a parcel first.";return}const parcel=fieldParcels.features.find(item=>String(item.id)===String(parcelId));const [response,result]=await api(`/api/v1/cadastre/zabadani/next-numbers?section_number=${encodeURIComponent(parcel.properties.section_number)}&admin_unit_id=${encodeURIComponent(activeAdminUnitId)}`);startCapture("building");$("#parcel-section").value=parcel.properties.section_number;$("#parcel-number").value=response.ok?result.next_object_number:"";$("#parcel-number").focus();$("#workflow-message").textContent=lang==="de"?"Gebäudegrundriss zeichnen; die Objektnummer wird automatisch eindeutig vorgeschlagen.":"Draw the building footprint; a unique object number is proposed."};
  loadSections();
  const captureButton=document.createElement("button");captureButton.type="button";captureButton.textContent=lang==="ar"?"تسجيل قطعة":lang==="de"?"Flurstück erfassen":"Capture parcel";$("#cad-tools-panel").append(captureButton);captureButton.onclick=startCapture;
  const toolPanel=$("#cad-tools-panel"),toolButton=(label,action)=>{const button=document.createElement("button");button.type="button";button.className="cad-menu-tool";button.textContent=label;button.onclick=action;return button};
  let measureStart=null;
  const legendPanel=document.createElement("div");legendPanel.id="cad-legend-panel";legendPanel.className="cad-legend-panel hidden";
  legendPanel.innerHTML=`<div class="cad-legend-head"><strong>${lang==="ar"?"مفتاح الخريطة":lang==="de"?"Legende":"Legend"}</strong><button id="cad-legend-close" type="button">×</button></div><div class="cad-legend-group"><small>${lang==="de"?"Verkehr":"Transport"}</small><span><i class="legend-road motorway"></i>${lang==="de"?"Autobahn / Fernstraße":"Motorway / trunk road"}</span><span><i class="legend-road primary"></i>${lang==="de"?"Hauptstraße":"Primary road"}</span><span><i class="legend-road local"></i>${lang==="de"?"Lokalstraße":"Local road"}</span></div><div class="cad-legend-group"><small>${lang==="de"?"Kataster und Adressen":"Cadastre and addresses"}</small><span><i class="legend-area approved"></i>${lang==="de"?"Freigegebenes Flurstück":"Approved parcel"}</span><span><i class="legend-area draft"></i>${lang==="de"?"Entwurf / in Prüfung":"Draft / in review"}</span><span><i class="legend-area building"></i>${lang==="de"?"Gebäude":"Building"}</span><span><i class="legend-number">12</i>${lang==="de"?"Hausnummer":"House number"}</span></div>`;
  $(".field-map-pane").append(legendPanel);$("#cad-legend-close").onclick=()=>legendPanel.classList.add("hidden");
  const legend=()=>{closeCadPanels();legendPanel.classList.toggle("hidden")};
  const printPanel=document.createElement("div");printPanel.id="cad-print-panel";printPanel.className="cad-print-panel hidden";
  printPanel.innerHTML=`<div class="cad-print-head"><strong>${lang==="ar"?"طباعة الخريطة":lang==="de"?"Katasterkarte drucken":"Print cadastral map"}</strong><button id="cad-print-close" type="button">×</button></div><label>${lang==="de"?"Vorlage":"Template"}<select id="cad-print-template"><option value="A4 portrait">A4 Hochformat</option><option value="A4 landscape">A4 Querformat</option><option value="A3 portrait">A3 Hochformat</option><option value="A3 landscape">A3 Querformat</option></select></label><label>${lang==="de"?"Titel":"Title"}<input id="cad-print-title" maxlength="80" value="Liegenschaftskarte Al-Zabadani"></label><label>${lang==="de"?"Notiz":"Note"}<textarea id="cad-print-note" maxlength="350"></textarea></label><label>${lang==="de"?"Maßstab":"Scale"}<input id="cad-print-scale" inputmode="numeric" value="1000"></label><button id="cad-print-submit" type="button">${lang==="de"?"Druckansicht / PDF öffnen":"Open print / PDF"}</button>`;
  $(".field-map-pane").append(printPanel);
  const printFrame=document.createElement("div");printFrame.id="cad-print-frame";printFrame.className="cad-print-frame portrait hidden";$(".field-map-pane").append(printFrame);
  const printMeta=document.createElement("div");printMeta.id="cad-print-meta";printMeta.className="cad-print-meta";$(".field-map-pane").append(printMeta);
  const updatePrintFrame=()=>{const orientation=$("#cad-print-template").value.split(" ")[1];printFrame.className=`cad-print-frame ${orientation}`};
  const openPrint=()=>{closeCadPanels();printPanel.classList.remove("hidden");printFrame.classList.remove("hidden");$("#cad-print-scale").value=String(Math.max(250,Math.round(591657550.5/Math.pow(2,fieldMap.getZoom())/50)*50));updatePrintFrame()};
  $("#cad-print-template").onchange=updatePrintFrame;
  $("#cad-print-close").onclick=()=>{printPanel.classList.add("hidden");printFrame.classList.add("hidden")};
  $("#cad-print-submit").onclick=async()=>{
    const button=$("#cad-print-submit"),[paper,orientation]=$("#cad-print-template").value.split(" "),title=$("#cad-print-title").value.trim(),note=$("#cad-print-note").value.trim(),scale=$("#cad-print-scale").value.trim();
    button.disabled=true;button.textContent=lang==="de"?"PDF wird erstellt …":"Creating PDF …";
    try{
      showFieldCadastral(true);fieldMap.getLayer("field-cadastral-parcel-lines")&&fieldMap.setLayoutProperty("field-cadastral-parcel-lines","visibility","visible");
      await new Promise(resolve=>setTimeout(resolve,350));
      fieldMap.triggerRepaint();await new Promise(resolve=>fieldMap.once("render",()=>setTimeout(resolve,120)));
      const mapCanvas=fieldMap.getCanvas(),gl=mapCanvas.getContext("webgl2")||mapCanvas.getContext("webgl"),pixels=new Uint8Array(mapCanvas.width*mapCanvas.height*4);
      gl.readPixels(0,0,mapCanvas.width,mapCanvas.height,gl.RGBA,gl.UNSIGNED_BYTE,pixels);
      const raw=document.createElement("canvas");raw.width=mapCanvas.width;raw.height=mapCanvas.height;raw.getContext("2d").putImageData(new ImageData(new Uint8ClampedArray(pixels.buffer),mapCanvas.width,mapCanvas.height),0,0);
      const snapshot=document.createElement("canvas");snapshot.width=mapCanvas.width;snapshot.height=mapCanvas.height;const snapshotContext=snapshot.getContext("2d");snapshotContext.translate(0,snapshot.height);snapshotContext.scale(1,-1);snapshotContext.drawImage(raw,0,0);
      const mapRect=mapCanvas.getBoundingClientRect(),frameRect=printFrame.getBoundingClientRect(),ratioX=mapCanvas.width/mapRect.width,ratioY=mapCanvas.height/mapRect.height;
      const sx=Math.max(0,(frameRect.left-mapRect.left)*ratioX),sy=Math.max(0,(frameRect.top-mapRect.top)*ratioY),sw=Math.min(mapCanvas.width-sx,frameRect.width*ratioX),sh=Math.min(mapCanvas.height-sy,frameRect.height*ratioY);
      const crop=document.createElement("canvas");crop.width=Math.max(1,Math.round(sw));crop.height=Math.max(1,Math.round(sh));crop.getContext("2d").drawImage(snapshot,sx,sy,sw,sh,0,0,crop.width,crop.height);
      const map_image=crop.toDataURL("image/jpeg",.9),parcel=fieldParcels?.features?.[0]?.properties||{};
      const northWest=fieldMap.unproject([frameRect.left-mapRect.left,frameRect.top-mapRect.top]),southEast=fieldMap.unproject([frameRect.right-mapRect.left,frameRect.bottom-mapRect.top]),bounds=[northWest.lng,southEast.lat,southEast.lng,northWest.lat];
      const response=await fetch("/api/v1/cadastre/zabadani/print",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+token,"X-Device-Time":new Date().toISOString()},body:JSON.stringify({paper,orientation,title,note,scale,map_image,map_width:crop.width,map_height:crop.height,bounds,parcel})});
      if(!response.ok)throw Error((await response.json()).error||"PDF error");
      const link=document.createElement("a");link.href=URL.createObjectURL(await response.blob());link.download="Liegenschaftskarte-Al-Zabadani.pdf";link.click();setTimeout(()=>URL.revokeObjectURL(link.href),30000);
      printPanel.classList.add("hidden");printFrame.classList.add("hidden");cadMessage(lang==="de"?"Der helle Kartenausschnitt wurde als PDF erstellt.":"The bright map frame was exported to PDF.");
    }catch(error){cadMessage(error.message||"PDF error")}
    finally{button.disabled=false;button.textContent=lang==="de"?"PDF erstellen und herunterladen":"Create and download PDF"}
  };
  window.addEventListener("afterprint",()=>{document.body.classList.remove("printing-cadastre");printMeta.innerHTML="";fieldMap.resize()});
  const exportMap=async()=>{try{
    closeCadPanels();showFieldCadastral(true);
    fieldMap.triggerRepaint();await new Promise(resolve=>fieldMap.once("render",()=>setTimeout(resolve,120)));
    const source=fieldMap.getCanvas(),gl=source.getContext("webgl2")||source.getContext("webgl"),pixels=new Uint8Array(source.width*source.height*4);
    gl.readPixels(0,0,source.width,source.height,gl.RGBA,gl.UNSIGNED_BYTE,pixels);
    const raw=document.createElement("canvas");raw.width=source.width;raw.height=source.height;raw.getContext("2d").putImageData(new ImageData(new Uint8ClampedArray(pixels.buffer),source.width,source.height),0,0);
    const output=document.createElement("canvas");output.width=source.width;output.height=source.height;const context=output.getContext("2d");
    context.fillStyle="#ffffff";context.fillRect(0,0,output.width,output.height);context.save();context.translate(0,output.height);context.scale(1,-1);context.drawImage(raw,0,0);context.restore();
    const link=document.createElement("a");link.download=`kataster-al-zabadani-${new Date().toISOString().slice(0,10)}.png`;link.href=output.toDataURL("image/png");link.click();
    cadMessage(lang==="de"?"Helles Kartenbild vollständig gespeichert.":"Bright map image saved.");
  }catch(error){cadMessage(lang==="de"?"Kartenbild konnte nicht gespeichert werden.":"Map image export unavailable.")}};
  const startMeasure=()=>{measureStart=null;closeCadPanels();cadMessage(lang==="de"?"Ersten und zweiten Messpunkt anklicken.":"Click first and second measurement point.");fieldMap.once("click",first=>{measureStart=first.lngLat;fieldMap.once("click",second=>{const rad=Math.PI/180,a=measureStart.lat*rad,b=second.lngLat.lat*rad,dLat=(second.lngLat.lat-measureStart.lat)*rad,dLon=(second.lngLat.lng-measureStart.lng)*rad,h=Math.sin(dLat/2)**2+Math.cos(a)*Math.cos(b)*Math.sin(dLon/2)**2,distance=6371000*2*Math.atan2(Math.sqrt(h),Math.sqrt(1-h));cadMessage(`${lang==="de"?"Entfernung":"Distance"}: ${distance<1000?`${distance.toFixed(1)} m`:`${(distance/1000).toFixed(2)} km`}`)})})};
  const resetMap=()=>{closeCadPanels();stopCapture();legendPanel.classList.add("hidden");fieldMap.getLayer("field-selected-building")&&fieldMap.setFilter("field-selected-building",["==",["id"],""]);fieldMap.getLayer("field-selected-road")&&fieldMap.setFilter("field-selected-road",["==",["id"],""]);fieldMap.getLayer("field-selected-parcel")&&fieldMap.setFilter("field-selected-parcel",["==",["id"],""]);fieldMap.getLayer("field-selected-parcel-fill")&&fieldMap.setFilter("field-selected-parcel-fill",["==",["id"],""]);setFieldMapMode("normal");$("#governorate-show").click();cadMessage(lang==="de"?"Kartenansicht für den aktuellen Verwaltungsbereich zurückgesetzt.":"Map reset for the current administrative area.")};
  const menuTools=[
    toolButton("☷ "+(lang==="de"?"Legende anzeigen":"Show legend"),legend),
    toolButton("▣ "+(lang==="de"?"Drucken":"Print"),openPrint),
    toolButton("▧ "+(lang==="de"?"Bildexport":"Image export"),exportMap),
    toolButton("⌕ "+(lang==="de"?"Flurstückssuche":"Parcel search"),()=>$("#cad-parcel").click()),
    toolButton("◎ "+(lang==="de"?"Koordinatensystem":"Coordinate system"),()=>cadMessage("Erfassung: WGS 84 / EPSG:4326 · amtliche Transformation vor Vermessungsfreigabe")),
    toolButton("⌖ "+(lang==="de"?"Koordinaten anzeigen":"Show coordinates"),()=>$("#cad-coordinates").click()),
    toolButton("◩ "+(lang==="de"?"Messen":"Measure"),startMeasure),
    toolButton("✎ "+(lang==="de"?"Objekte digitalisieren":"Digitize objects"),startCapture),
    toolButton("↺ "+(lang==="de"?"Kartenansicht zurücksetzen":"Reset map view"),resetMap)
  ];
  menuTools.forEach(button=>toolPanel.insertBefore(button,toolPanel.firstChild));
  fieldMap.on("click",event=>{if(!captureActive)return;const allowed=selectedGovernorateBoundary||(fieldBoundary?.features?.[0]||fieldBoundary);if(allowed?.geometry&&!fieldPointInGeometry(event.lngLat.lng,event.lngLat.lat,allowed.geometry)){cadMessage(lang==="de"?"Grenzpunkt außerhalb des erlaubten Verwaltungsgebiets.":"Boundary point outside the permitted area.");return}capturePoints.push([+event.lngLat.lng.toFixed(7),+event.lngLat.lat.toFixed(7)]);updateCapture()});
  $("#parcel-capture-close").onclick=stopCapture;
  $("#parcel-point-tool").onclick=()=>{captureActive=true;$("#parcel-point-tool").classList.add("active");fieldMap.getCanvas().style.cursor="crosshair";cadMessage(lang==="de"?"Punktwerkzeug aktiv: Grenzpunkte der Reihe nach auf der Karte anklicken.":"Point tool active: click boundary points in order.")};
  $("#parcel-undo").onclick=()=>{capturePoints.pop();updateCapture()};
  $("#parcel-save").onclick=async()=>{
    if(capturePoints.length<3){cadMessage(lang==="de"?"Mindestens drei Grenzpunkte erforderlich.":"At least three boundary points required.");return}
    const section=$("#parcel-section").value.trim(),parcel=$("#parcel-number").value.trim();
    if(!section||(captureTarget!=="section"&&!parcel)){cadMessage(lang==="de"?"Flurnummer und die benötigte Objektnummer eintragen.":"Enter the section and required object number.");return}
    if(captureTarget==="section"){
      const payload={admin_unit_id:activeAdminUnitId,section_number:section,name_ar:parcel||`قطاع ${section}`,geometry:{type:"Polygon",coordinates:[[...capturePoints,capturePoints[0]]]},reason:`Flurerfassung ${activeAdminUnitId}`};
      const endpoint=captureEditSectionId?`/api/v1/cadastre/zabadani/sections/${captureEditSectionId}/update`:"/api/v1/cadastre/zabadani/sections";
      const [response,result]=await api(endpoint,"POST",payload);
      if(!response.ok){cadMessage(result.error);return}
      captureActive=false;capturePoints=[];fieldMap.getCanvas().style.cursor="";updateCapture();capturePanel.classList.add("hidden");
      captureEditSectionId=null;
      await loadBuildings();await loadSections();$("#workflow-section").value=result.section_number;await prepareNextParcelNumber();
      $("#workflow-message").textContent=lang==="de"?`Flur ${result.section_number} ist gespeichert · ${formatArea(result.area_m2)}. Jetzt können darin Flurstücke erfasst werden.`:`Section ${result.section_number} is stored · ${formatArea(result.area_m2)}. Parcels can now be captured inside it.`;
      return
    }
    if(captureTarget==="building"){
      const parcelId=$("#house-parcel")?.value;
      if(!parcelId){cadMessage(lang==="de"?"Zuerst das zugehörige Flurstück auswählen.":"Select the related parcel first.");return}
      const [response,result]=await api("/api/v1/cadastre/buildings/capture","POST",{admin_unit_id:activeAdminUnitId,parcel_id:parcelId,object_number:parcel,quality_level:$("#parcel-quality").value,geometry:{type:"Polygon",coordinates:[[...capturePoints,capturePoints[0]]]},reason:`Gebäudeerfassung ${activeAdminUnitId}`});
      if(!response.ok){cadMessage(result.error);return}
      captureActive=false;capturePoints=[];fieldMap.getCanvas().style.cursor="";updateCapture();capturePanel.classList.add("hidden");
      await loadBuildings();$("#building-ref").value=result.id;await selectFieldBuilding(result.id);form.scrollIntoView({behavior:"smooth",block:"start"});
      $("#workflow-message").textContent=lang==="de"?`Gebäudeobjekt ${result.object_number} ist gespeichert · Grundfläche ${formatArea(result.footprint_area_m2)}. Haustürpunkt setzen, Straße und Hausnummer eintragen und einreichen.`:`Building object ${result.object_number} saved · footprint ${formatArea(result.footprint_area_m2)}. Set the entrance point and assign the address.`;
      return
    }
    const [response,result]=await api("/api/v1/cadastre/zabadani/parcels/capture","POST",{admin_unit_id:activeAdminUnitId,section_number:section,parcel_number:parcel,
      quality_level:$("#parcel-quality").value,geometry:{type:"Polygon",coordinates:[[...capturePoints,capturePoints[0]]]},owner_name:$("#parcel-owner-name").value.trim(),owner_reference:$("#parcel-owner-reference").value.trim(),owner_share_percent:+$("#parcel-owner-share").value||100,owner_source_document:$("#parcel-owner-document").value.trim(),
      reason:`Katastererfassung ${activeAdminUnitId}`});
    if(!response.ok){cadMessage(result.error==="approved_parcel_requires_formal_change"?(lang==="de"?"Dieses Flurstück ist bereits amtlich freigegeben. Eine Änderung muss als formeller Fortführungsantrag erfolgen.":"Approved parcel requires a formal change request."):result.error);return}
    captureActive=false;capturePoints=[];fieldMap.getCanvas().style.cursor="";updateCapture();
    capturePanel.classList.add("saved");
    $("#parcel-capture-status").textContent=lang==="de"?`✓ Flurstück ${section}/${parcel} wurde ${result.updated?"korrigiert":"neu angelegt"} und gespeichert · ${formatArea(result.area_m2)} · Status ENTWURF.`:`✓ Parcel ${section}/${parcel} ${result.updated?"updated":"created"} · ${formatArea(result.area_m2)} · DRAFT.`;
    $("#parcel-section").value="";$("#parcel-number").value="";
    cadMessage(lang==="de"?`Flurstück ${section}/${parcel} ist dauerhaft gespeichert.`:`Parcel ${section}/${parcel} is permanently stored.`);
    await loadBuildings();await loadSections();await load();
  };
  if(role==="SYSTEM_ADMIN"){
    const importButton=document.createElement("button"),importFile=document.createElement("input");
    importButton.id="cad-import-open";importButton.type="button";
    importButton.textContent=lang==="ar"?"استيراد قطع GeoJSON":lang==="de"?"Flurstücke importieren":"Import parcels";
    importFile.id="cad-import-file";importFile.type="file";importFile.accept=".geojson,.json,application/geo+json,application/json";importFile.className="hidden";
    $("#cad-tools-panel").append(importButton,importFile);
    importButton.onclick=()=>importFile.click();
    importFile.onchange=async event=>{
      const file=event.target.files[0];if(!file)return;
      try{
        const collection=JSON.parse(await file.text());
        collection.cadastral_district=collection.cadastral_district||{code:"SY-RD-ZA",name_ar:"الزبداني",name_en:"Al-Zabadani"};
        const [response,result]=await api("/api/v1/cadastre/zabadani/parcels/import","POST",collection);
        if(!response.ok)throw Error(`${result.error}${result.feature_index!==undefined?` · Objekt ${result.feature_index+1}`:""}`);
        cadMessage(`${result.created} ${lang==="de"?"neu":lang==="ar"?"جديدة":"created"} · ${result.updated} ${lang==="de"?"aktualisiert":lang==="ar"?"محدثة":"updated"} · DRAFT`);
        await loadBuildings();
      }catch(error){cadMessage(error.message||"Import failed")}
      finally{event.target.value=""}
    };
  }
}
function setDoorPosition(lng,lat,adjusted=false){
  const allowed=selectedGovernorateBoundary||(fieldBoundary?.features?.[0]||fieldBoundary);
  if(allowed?.geometry&&!fieldPointInGeometry(+lng,+lat,allowed.geometry)){
    if(doorMarker&&doorPosition)doorMarker.setLngLat([doorPosition.longitude,doorPosition.latitude]);
    const status=$("#field-gps-status");if(status){status.className="accuracy-poor";status.textContent=lang==="de"?"Position außerhalb des erlaubten Verwaltungsgebiets.":"Position outside the permitted administrative area."}
    return false;
  }
  doorPosition={longitude:+lng,latitude:+lat,adjusted};
  if(!doorMarker){const el=document.createElement("div");el.className="door-marker";doorMarker=new maplibregl.Marker({element:el,draggable:true}).setLngLat([lng,lat]).addTo(fieldMap);doorMarker.on("dragend",()=>{const p=doorMarker.getLngLat();setDoorPosition(p.lng,p.lat,true)})}else doorMarker.setLngLat([lng,lat]);
  $("#field-door-coordinate").textContent=`${(+lat).toFixed(7)}, ${(+lng).toFixed(7)}`;
  if(doorMarker)doorMarker.getElement().dataset.houseNumber=$("#house-number")?.value||"";
}
function focusFieldBuilding(){if(!fieldMap||!fieldBuildings||!$("#building-ref").value)return;const feature=fieldBuildings.features.find(x=>x.id===$("#building-ref").value);if(!feature)return;const [lng,lat]=feature.properties.centroid;doorPosition=null;if(doorMarker){doorMarker.remove();doorMarker=null}if($("#field-door-coordinate"))$("#field-door-coordinate").textContent="—";if($("#field-gps-status"))$("#field-gps-status").textContent=lang==="de"?"Haustürpunkt an der Straßenseite setzen.":"Place entrance point at the street side.";fieldMap.flyTo({center:[lng,lat],zoom:17.2,pitch:48,bearing:12,duration:700})}
async function selectFieldBuilding(buildingId){
  if(!buildingId||![...$("#building-ref").options].some(option=>option.value===buildingId))return;
  $("#building-ref").value=buildingId;
  if(fieldMap.getLayer("field-selected-building"))fieldMap.setFilter("field-selected-building",["==",["id"],buildingId]);
  $("#house-message").textContent=lang==="ar"?"تم اختيار المبنى من الخريطة.":lang==="de"?"Gebäude auf der Karte ausgewählt.":"Building selected on the map.";
  await loadProposal();
  await loadObjectHierarchy();
  focusFieldBuilding();
}
async function locateAtDoor(){const status=$("#field-gps-status");status.textContent="GPS …";try{lastGps=await position();let cls=lastGps.accuracy<=10?"accuracy-good":lastGps.accuracy<=25?"accuracy-medium":"accuracy-poor";status.className=cls;status.textContent=`${messages[lang].gpsAccuracy}: ±${Math.round(lastGps.accuracy)} m`;if(!gpsMarker){const el=document.createElement("div");el.className="gps-marker";gpsMarker=new maplibregl.Marker({element:el}).setLngLat([lastGps.longitude,lastGps.latitude]).addTo(fieldMap)}else gpsMarker.setLngLat([lastGps.longitude,lastGps.latitude]);setDoorPosition(lastGps.longitude,lastGps.latitude,false);fieldMap.flyTo({center:[lastGps.longitude,lastGps.latitude],zoom:17.4,pitch:50,bearing:12,duration:800})}catch(error){status.className="accuracy-poor";status.textContent=error.message||"GPS nicht verfügbar"}}
async function loadBuildings(){
  const empty={type:"FeatureCollection",features:[]},scope=activeAdminUnitId;
  const pilotScope=scope==="au-rd"||scope==="au-zab";
  const scopeQuery=scope&&scope!=="ALL"?`?admin_unit_id=${encodeURIComponent(scope)}`:"";
  let [d,manual,roads,officialRoads,numbers,sections,parcels,boundary]=await Promise.all([
    pilotScope?fetch("/api/v1/map/zabadani/buildings").then(r=>r.json()):Promise.resolve(empty),
    token&&scopeQuery?api("/api/v1/map/cadastre/buildings"+scopeQuery).then(result=>result[1]):Promise.resolve(empty),
    pilotScope?fetch("/api/v1/map/zabadani/roads").then(r=>r.json()):Promise.resolve(empty),
    token?api("/api/v1/map/streets"+(scopeQuery||"?admin_unit_id=ALL")).then(result=>result[0].ok?result[1]:empty):Promise.resolve(empty),
    token&&scopeQuery?api("/api/v1/map/zabadani/number-proposals"+scopeQuery).then(result=>result[1]):Promise.resolve(empty),
    token&&scopeQuery?api("/api/v1/map/cadastre/sections"+scopeQuery).then(result=>result[1]):Promise.resolve(empty),
    token&&scopeQuery?api("/api/v1/map/zabadani/parcels"+scopeQuery).then(result=>result[1]):Promise.resolve({...empty,official_data_loaded:false}),
    fetch("/api/v1/map/syria/boundary").then(r=>r.json())
  ]);
  d={type:"FeatureCollection",features:[...(d.features||[]),...(manual.features||[])]};
  fieldBuildings=d;fieldRoads={type:"FeatureCollection",features:[...(roads.features||[]),...(officialRoads.features||[])]};fieldNumbers=numbers;fieldSections=sections;fieldParcels=parcels;fieldBoundary=boundary;
  $("#building-ref").innerHTML=d.features.map(f=>`<option value="${esc(f.id)}">${esc(f.properties.technical_code)}</option>`).join("");
  $("#building-ref").onchange=async()=>{const id=$("#building-ref").value,feature=fieldBuildings?.features?.find(item=>item.id===id),parcelId=feature?.properties?.parcel_id||"";if($("#house-parcel")){$("#house-parcel").value=[...$("#house-parcel").options].some(option=>option.value===parcelId)?parcelId:"";if(parcelId)selectFieldParcel(parcelId)}if(fieldMap?.getLayer("field-selected-building"))fieldMap.setFilter("field-selected-building",["==",["id"],id]);await loadProposal();await loadObjectHierarchy();focusFieldBuilding()};
  if(!fieldMap)prepareFieldMap();else{fieldMap.getSource("field-buildings")?.setData(fieldBuildings);fieldMap.getSource("field-roads")?.setData(fieldRoads);fieldMap.getSource("field-number-proposals")?.setData(fieldNumbers);fieldMap.getSource("field-sections")?.setData(fieldSections);fieldMap.getSource("field-parcels")?.setData(fieldParcels);renderFieldParcelOverlay()}
  if($("#field-data-status"))$("#field-data-status").textContent=scope==="ALL"?(lang==="de"?"Nationale Übersicht · Gouvernement auswählen":"National overview · select governorate"):fieldParcels.official_data_loaded?(lang==="de"?`${fieldNumbers.features.length} Hausnummern · ${fieldParcels.features.length} Flurstücke`:`${fieldNumbers.features.length} house numbers · ${fieldParcels.features.length} parcels`):(lang==="de"?`${fieldNumbers.features.length} Hausnummern · noch keine Flurstücke in diesem Gouvernement`:`${fieldNumbers.features.length} house numbers · no parcels in this governorate yet`);
  refreshChangeGraphics();
  if(token&&$("#building-ref").value){await loadProposal();await loadObjectHierarchy()}
}
async function loadObjectHierarchy(){
  if(!token||!$("#building-ref").value)return;
  let [response,data]=await api(`/api/v1/buildings/${encodeURIComponent($("#building-ref").value)}/units`);
  if(!response.ok){$("#unit-tree").innerHTML=`<span class="muted">${esc(data.error)}</span>`;return}
  const unitLabel=lang==="ar"?"وحدة":lang==="de"?"Wohnung/Nutzungseinheit":"Dwelling/unit";
  $("#unit-tree").innerHTML=`<div class="tree-building"><b>▣ ${esc($("#building-ref").value)}</b><span>${data.entrances.length} ${lang==="de"?"Eingänge":"entrances"} · ${data.units.length} ${lang==="de"?"Einheiten":"units"}</span></div>`+(data.units.map(unit=>`<button class="tree-unit" data-unit="${esc(unit.id)}"><span>└─ ${esc(unit.entrance_label||"—")} · ${esc(unitLabel)} ${esc(unit.unit_number)}</span><small>${esc(unit.floor_label||"")} · ${esc(unit.usage_type)} · ${esc(unit.status)}</small></button>`).join("")||`<p class="empty-register">${lang==="ar"?"لم يتم تسجيل وحدات بعد.":lang==="de"?"Noch keine Wohnungen oder Nutzungseinheiten amtlich erfasst.":"No dwellings or units recorded yet."}</p>`);
  document.querySelectorAll("[data-unit]").forEach(button=>button.onclick=()=>loadResidents(button.dataset.unit));
  $("#resident-register").classList.add("hidden");
}
async function loadResidents(unitId){
  if(!["REGISTRY_OFFICER","SYSTEM_ADMIN"].includes(role)){alert(lang==="ar"?"بيانات السكان متاحة فقط لمكتب السجل المدني.":lang==="de"?"Bewohnerdaten sind ausschließlich für die Meldebehörde freigegeben.":"Resident data is restricted to the registration authority.");return}
  let [response,data]=await api(`/api/v1/units/${encodeURIComponent(unitId)}/residents`);
  const panel=$("#resident-register");panel.classList.remove("hidden");
  if(!response.ok){panel.textContent=data.error;return}
  panel.innerHTML=`<div class="protected-heading"><b>🔒 ${lang==="de"?"Geschütztes Melderegister":"Protected population register"}</b><span>${esc(unitId)}</span></div>`+(data.residents.map(person=>`<div class="resident-row"><strong>${esc(person.family_name)}, ${esc(person.given_names)}</strong><span>${esc(person.register_number)} · ${esc(person.residence_type)} · ${esc(person.move_in_date)}</span></div>`).join("")||`<p>${lang==="de"?"Keine aktive Meldung vorhanden.":"No active registration."}</p>`);
}
function selectFieldParcel(parcelId){
  if(!parcelId)return;
  const feature=fieldParcels?.features?.find(item=>String(item.id)===String(parcelId));
  if(!feature)return;
  if($("#house-parcel"))$("#house-parcel").value=parcelId;
  if(fieldMap?.getLayer("field-selected-parcel"))fieldMap.setFilter("field-selected-parcel",["==",["id"],parcelId]);
  if(fieldMap?.getLayer("field-selected-parcel-fill"))fieldMap.setFilter("field-selected-parcel-fill",["==",["id"],parcelId]);
  renderFieldParcelOverlay();
  const p=feature.properties;
  $("#house-message").textContent=lang==="ar"?`تم اختيار القطاع ${p.section_number}، القطعة ${p.parcel_number}`:lang==="de"?`Flur ${p.section_number}, Flurstück ${p.parcel_number} ausgewählt.`:`Section ${p.section_number}, parcel ${p.parcel_number} selected.`;
  const coordinates=feature.geometry?.coordinates?.flat(2)||[];
  if(coordinates.length){const bounds=coordinates.reduce((box,point)=>box.extend(point),new maplibregl.LngLatBounds(coordinates[0],coordinates[0]));fieldMap.fitBounds(bounds,{padding:90,maxZoom:17,duration:650})}
}
window.addEventListener("resize",()=>fieldMap&&fieldMap.resize());
$("#dashboard").addEventListener("transitionend",()=>fieldMap&&fieldMap.resize());
new MutationObserver(()=>setTimeout(()=>fieldMap&&fieldMap.resize(),0)).observe($("#dashboard"),{attributes:true,attributeFilter:["class"]});
function buildPortalPages(){
  const dashboard=$("#dashboard"),children=[...dashboard.children],work=document.createElement("section");
  const [metrics,changes,fieldJobs,register]=children;
  work.id="page-work";work.className="portal-page";
  work.innerHTML=`<section class="app-launcher fiori-launchpad"><div class="launchpad-bar"><div><span class="eyebrow">${lang==="de"?"Nationales Kataster":"National register"}</span><h2>${lang==="de"?"App-Übersicht":"App overview"}</h2></div><label class="app-search"><svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="5.5"></circle><path d="m15 15 4.5 4.5"></path></svg><input id="app-search-input" type="search" placeholder="${lang==="de"?"Apps suchen":"Search apps"}"></label><div class="scope-command"><small>${lang==="de"?"Zugriffsbereich":"Access scope"}</small><strong>${esc(role==="SYSTEM_ADMIN"?(lang==="de"?"Gesamtes Staatsgebiet":"Nationwide"):(organisation||"–"))}</strong><span class="scope-secure">● ${lang==="de"?"Berechtigung aktiv":"Permission active"}</span></div></div><div class="app-groups"><section class="app-group"><h3>${lang==="de"?"Bestandsdaten":"Master data"}</h3><div class="app-grid"><button data-open-app="register" data-app-title="Kataster Adressen Flurstücke"><i><svg viewBox="0 0 24 24"><path d="M4 19V7l8-4 8 4v12"></path><path d="M8 19v-7h8v7M3 19h18"></path></svg></i><strong>${lang==="de"?"Kataster & Adressen":"Cadastre & addresses"}</strong><small>SNA_CADASTRE</small></button><button data-open-app="search" data-app-title="Suche Objekte Adressen"><i><svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="5.5"></circle><path d="m15 15 4.5 4.5"></path></svg></i><strong>${lang==="de"?"Zentrale Suche":"Central search"}</strong><small>SNA_SEARCH</small></button></div></section><section class="app-group"><h3>${lang==="de"?"Vorgänge":"Processes"}</h3><div class="app-grid"><button data-open-app="workflow" data-app-title="Vorgänge Prüfung Freigabe"><i><svg viewBox="0 0 24 24"><path d="M7 3h10v4H7zM5 5H3v16h18V5h-2"></path><path d="m8 14 2.5 2.5L16 11"></path></svg></i><strong>${lang==="de"?"Vorgänge & Prüfung":"Cases & review"}</strong><small>SNA_WORKFLOW</small></button><button data-open-app="collaboration" data-app-title="Behördenaustausch Zusammenarbeit"><i><svg viewBox="0 0 24 24"><path d="M5 8h13M15 5l3 3-3 3M19 16H6M9 13l-3 3 3 3"></path></svg></i><strong>${lang==="de"?"Behördenaustausch":"Authority exchange"}</strong><small>SNA_EXCHANGE</small></button><button data-open-app="field" data-app-title="Außendienst Vermessung Montage"><i><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"></circle><circle cx="12" cy="12" r="3"></circle><path d="M12 3.5V6M12 18v2.5M3.5 12H6M18 12h2.5"></path></svg></i><strong>${lang==="de"?"Außendienst":"Field operations"}</strong><small>SNA_FIELD</small></button></div></section><section class="app-group admin-app-group"><h3>${lang==="de"?"Administration":"Administration"}</h3><div class="app-grid"><button data-open-app="settings" data-app-title="Systemeinstellungen Administration"><i><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"></circle><path d="M19 13.5v-3l-2-.7-.7-1.7.9-1.9-2.1-2.1-1.9.9-1.7-.7-.7-2h-3l-.7 2-1.7.7-1.9-.9-2.1 2.1.9 1.9-.7 1.7-2 .7v3l2 .7.7 1.7-.9 1.9 2.1 2.1 1.9-.9 1.7.7.7 2h3l.7-2 1.7-.7 1.9.9 2.1-2.1-.9-1.9.7-1.7 2-.7Z"></path></svg></i><strong>${lang==="de"?"Systemeinstellungen":"System settings"}</strong><small>SNA_ADMIN</small></button></div></section></div></section>`;
  if(metrics)work.prepend(metrics);
  const registerPage=document.createElement("section");registerPage.id="page-register";registerPage.className="portal-page hidden";if(register)registerPage.append(register);
  const workflowPage=document.createElement("section");workflowPage.id="page-workflow";workflowPage.className="portal-page hidden";if(changes)workflowPage.append(changes);
  const fieldPage=document.createElement("section");fieldPage.id="page-field";fieldPage.className="portal-page hidden";if(fieldJobs)fieldPage.append(fieldJobs);
  const collaborationPage=document.createElement("section");collaborationPage.id="page-collaboration";collaborationPage.className="portal-page hidden";
  collaborationPage.innerHTML=`<section class="inventory-command"><div class="inventory-command-head"><div><span class="eyebrow">${lang==="de"?"Eigene Fach-App":"Separate specialist app"}</span><h2>${lang==="de"?"Behördenaustausch":"Authority exchange"}</h2><p>${lang==="de"?"Nur behördenübergreifende Aufgaben, Übergaben und Fristen.":"Only inter-authority tasks, handovers and deadlines."}</p></div><div class="scope-command"><small>${lang==="de"?"Mein Zuständigkeitsbereich":"My scope"}</small><strong id="collaboration-scope">${esc(organisation||"–")}</strong><span class="scope-secure">● ${lang==="de"?"Zugriff geschützt":"Access protected"}</span></div></div><div class="collaboration-kpis"><article><span>↔</span><div><strong id="collab-open">0</strong><small>Offene Übergaben</small></div></article><article><span>!</span><div><strong id="collab-due">0</strong><small>Fällige Fristen</small></div></article><article><span>▲</span><div><strong id="collab-urgent">0</strong><small>Hohe Priorität</small></div></article><article><span>✓</span><div><strong id="collab-completed">0</strong><small>Abgeschlossen</small></div></article></div><div class="collaboration-grid"><div class="collaboration-inbox"><div class="section-title"><h3>Gemeinsamer Behörden-Posteingang</h3><button id="refresh-collaboration" class="small ghost">↻</button></div><div id="collaboration-cases" class="collaboration-cases"></div></div><form id="collaboration-form" class="collaboration-form"><div class="section-title"><h3>Neue Behördenübergabe</h3><span>↗</span></div><label>Betreff<input id="collab-title" maxlength="180" required></label><div class="collaboration-form-row"><label>Vorgangsart<select id="collab-type"><option value="BUILDING_PERMIT">Baugenehmigung</option><option value="BOUNDARY_REVIEW">Grenzprüfung</option><option value="ADDRESS_ASSIGNMENT">Adressvergabe</option><option value="DATA_CORRECTION">Datenkorrektur</option><option value="INTER_AUTHORITY_REVIEW">Behördenprüfung</option><option value="COORDINATION">Koordination</option></select></label><label>Priorität<select id="collab-priority"><option value="NORMAL">Normal</option><option value="HIGH">Hoch</option><option value="CRITICAL">Kritisch</option><option value="LOW">Niedrig</option></select></label></div><label>Empfangende Behörde<select id="collab-target" required></select></label><div class="collaboration-form-row"><label>Zielrolle<select id="collab-role"><option value="MUNICIPAL_EDITOR">Bauamt</option><option value="SURVEYOR">Vermessung</option><option value="REVIEWER">Prüfung</option><option value="APPROVER">Freigabe</option><option value="REGISTRY_OFFICER">Meldebehörde</option></select></label><label>Frist<input id="collab-due-at" type="date"></label></div><label>Arbeitsauftrag<textarea id="collab-description" maxlength="1200"></textarea></label><button type="submit">Nachvollziehbar übergeben</button><p id="collab-message" class="muted"></p></form></div></section>`;
  const nav=document.createElement("nav");nav.className="portal-nav";
  nav.innerHTML=`<div class="portal-nav-heading"><strong>${lang==="de"?"Nationales Kataster":"National register"}</strong><small>${lang==="de"?"Getrennte Fach-Apps":"Separate specialist apps"}</small></div><button data-page="work" class="active"><i><svg viewBox="0 0 24 24"><rect x="4" y="4" width="6" height="6" rx="1.5"></rect><rect x="14" y="4" width="6" height="6" rx="1.5"></rect><rect x="4" y="14" width="6" height="6" rx="1.5"></rect><rect x="14" y="14" width="6" height="6" rx="1.5"></rect></svg></i><span>${lang==="de"?"App-Übersicht":"App overview"}</span></button><button data-page="register"><i><svg viewBox="0 0 24 24"><path d="M3 11.5 12 4l9 7.5"></path><path d="M5.5 10v10h13V10M9 20v-6h6v6"></path></svg></i><span>${lang==="de"?"Kataster & Adressen":"Cadastre & addresses"}</span></button><button data-page="workflow"><i><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"></circle><path d="m8 12 2.6 2.6L16.5 9"></path></svg></i><span>${lang==="de"?"Vorgänge & Prüfung":"Cases & review"}</span></button><button data-page="field"><i><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"></circle><circle cx="12" cy="12" r="3"></circle><path d="M12 3.5V6M12 18v2.5M3.5 12H6M18 12h2.5"></path></svg></i><span>${lang==="de"?"Außendienst":"Field operations"}</span></button><button data-page="collaboration"><i><svg viewBox="0 0 24 24"><path d="M5 8h13M15 5l3 3-3 3M19 16H6M9 13l-3 3 3 3"></path></svg></i><span>${lang==="de"?"Behördenaustausch":"Authority exchange"}</span></button><button data-page="search"><i><svg viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="5.5"></circle><path d="m15 15 4.5 4.5"></path></svg></i><span>${lang==="de"?"Suche":"Search"}</span></button><div class="portal-nav-footer"><span class="nav-status-dot"></span><small>${lang==="de"?"System verfügbar":"System available"}</small></div>`;
  dashboard.append(nav,work,registerPage,workflowPage,fieldPage,collaborationPage);
  dashboard.insertAdjacentHTML("beforeend",`
  <section id="page-search" class="portal-page hidden"><div class="panel"><div class="section-title"><h2>${lang==="ar"?"البحث في البيانات":lang==="de"?"Daten suchen und filtern":"Search and filter data"}</h2><span>${lang==="ar"?"العناوين والمباني":lang==="de"?"Adressen und Gebäude":"Addresses and buildings"}</span></div><div class="filter-grid"><label>${lang==="ar"?"نص البحث":lang==="de"?"Suchbegriff":"Search"}<input id="filter-query" placeholder="${lang==="de"?"Straße, Hausnummer, Objekt-ID …":"Street, number, object ID …"}"></label><label>${lang==="ar"?"الحالة":lang==="de"?"Status":"Status"}<select id="filter-status"><option value="">${lang==="de"?"Alle":"All"}</option><option>OFFICIAL</option><option>SUBMITTED</option><option>REVIEWED</option><option>CANCELLED</option></select></label><label>${lang==="ar"?"الرمز البريدي":lang==="de"?"Postleitzahl":"Postal code"}<input id="filter-postal" maxlength="6"></label><label>${lang==="ar"?"نوع البيانات":lang==="de"?"Datenart":"Data type"}<select id="filter-type"><option value="addresses">${lang==="de"?"Amtliche Adressen":"Official addresses"}</option><option value="cases">${lang==="de"?"Hausnummernvorgänge":"House-number cases"}</option></select></label></div><button id="run-filter">⌕ ${lang==="ar"?"بحث":lang==="de"?"Suchen":"Search"}</button><button id="clear-filter" class="ghost">${lang==="ar"?"مسح":lang==="de"?"Filter löschen":"Clear"}</button><div id="filter-results" class="filter-results"></div></div></section>
  <section id="page-settings" class="portal-page hidden"><div class="settings-grid"><div class="panel"><div class="section-title"><h2>${lang==="ar"?"إعدادات النظام":lang==="de"?"Systemeinstellungen":"System settings"}</h2><b>⚙</b></div><label>${lang==="ar"?"اللغة الافتراضية":lang==="de"?"Standardsprache":"Default language"}<select id="setting-language"><option value="ar">العربية</option><option value="en">English</option><option value="de">Deutsch</option></select></label><label>${lang==="ar"?"طبقة الخريطة":lang==="de"?"Standard-Kartenebene":"Default map layer"}<select id="setting-map"><option value="satellite">Satellite</option><option value="street">Street</option><option value="3d">3D</option></select></label><label>${lang==="ar"?"بريد الدعم":lang==="de"?"Support-E-Mail":"Support email"}<input id="setting-support-email"></label><button id="save-settings">${lang==="ar"?"حفظ":lang==="de"?"Einstellungen speichern":"Save settings"}</button><p id="settings-message" class="muted"></p></div><div class="panel"><div class="section-title"><h2>${lang==="ar"?"قائمة المواطنين":lang==="de"?"Bürgermenü":"Citizen menu"}</h2><b>☰</b></div><label class="toggle-row"><input id="setting-citizen-search" type="checkbox"><span>${lang==="ar"?"إتاحة البحث العام":lang==="de"?"Öffentliche Adresssuche anzeigen":"Show public address search"}</span></label><label class="toggle-row"><input id="setting-citizen-pdf" type="checkbox"><span>${lang==="ar"?"إتاحة ملفات PDF":lang==="de"?"Öffentliche PDF-Ausgabe erlauben":"Allow public PDF output"}</span></label><a class="button ghost settings-link" href="/" target="_blank">${lang==="ar"?"فتح بوابة المواطنين":lang==="de"?"Bürgerportal ansehen":"View citizen portal"}</a><p class="muted">${lang==="de"?"Änderungen sind nur für Systemadministratoren möglich. Gemeinden können die Einstellungen ansehen.":"Only system administrators can change these settings."}</p></div></div></section>
  <section id="page-support" class="portal-page hidden"><div class="settings-grid"><div class="panel"><div class="section-title"><h2>${lang==="ar"?"طلب دعم":lang==="de"?"Supportanfrage erstellen":"Create support request"}</h2><b>?</b></div><label>${lang==="ar"?"الفئة":lang==="de"?"Kategorie":"Category"}<select id="support-category"><option value="TECHNICAL">Technical</option><option value="DATA">Data quality</option><option value="ACCOUNT">Account</option><option value="OTHER">Other</option></select></label><label>${lang==="ar"?"الموضوع":lang==="de"?"Betreff":"Subject"}<input id="support-subject"></label><label>${lang==="ar"?"الوصف":lang==="de"?"Beschreibung":"Description"}<textarea id="support-message"></textarea></label><button id="send-support">${lang==="ar"?"إرسال":lang==="de"?"Anfrage senden":"Send request"}</button><p id="support-result"></p></div><div class="panel"><h2>${lang==="ar"?"طلباتي":lang==="de"?"Meine Anfragen":"My requests"}</h2><div id="support-list" class="requests"></div></div></div></section>`);
  $("#page-settings .settings-grid").insertAdjacentHTML("beforeend",`<div class="panel google-export-panel"><div class="section-title"><h2>${lang==="ar"?"تسليم بيانات الخرائط":lang==="de"?"Kartendaten übergeben":"Share map data"}</h2><b>↗</b></div><p>${lang==="ar"?"تصدير العناوين الرسمية المعتمدة فقط دون بيانات المالك أو السكان.":lang==="de"?"Nur freigegebene amtliche Adressen exportieren – ohne Eigentümer- oder Bewohnerdaten.":"Export approved official addresses only, without owner or resident data."}</p><div id="google-export-status" class="export-readiness">${lang==="de"?"Export wird geprüft …":"Checking export …"}</div><div class="export-actions"><button id="download-google-kml" type="button">KML · Google Maps</button><button id="download-google-csv" class="ghost" type="button">CSV · UTF-8</button></div><small>${lang==="de"?"Enthält Straße, Hausnummer, Ort, Postleitzahl, Objekt-ID und Haustürkoordinate (WGS 84). Google prüft die Übernahme selbst.":"Includes address fields, stable ID and entrance coordinate (WGS 84). Acceptance is reviewed by Google."}</small></div>`);
  nav.querySelectorAll("[data-page]").forEach(button=>button.onclick=()=>openPortalPage(button.dataset.page));
  document.querySelectorAll("[data-open-app]").forEach(button=>button.onclick=()=>openPortalPage(button.dataset.openApp));
  $("#app-search-input").oninput=event=>{const needle=event.target.value.trim().toLowerCase();document.querySelectorAll("[data-app-title]").forEach(card=>card.classList.toggle("search-hidden",needle&&!card.dataset.appTitle.toLowerCase().includes(needle)));document.querySelectorAll(".app-group").forEach(group=>group.classList.toggle("search-hidden",![...group.querySelectorAll("[data-app-title]")].some(card=>!card.classList.contains("hidden")&&!card.classList.contains("search-hidden"))))};
  $("#setting-language").closest("label").firstChild.nodeValue=lang==="ar"?"لغة واجهة المستخدم":lang==="de"?"Meine Oberflächensprache":"My interface language";
  $("#setting-language").onchange=event=>{lang=event.target.value;localStorage.setItem("sna_lang",lang);$("#language").value=lang;applyLanguage();location.reload()};
  $("#run-filter").onclick=runDataFilter;$("#clear-filter").onclick=()=>{$("#filter-query").value="";$("#filter-status").value="";$("#filter-postal").value="";runDataFilter()};
  $("#save-settings").onclick=saveSystemSettings;$("#send-support").onclick=createSupportTicket;
  $("#download-google-kml").onclick=()=>downloadProtectedExport("/api/v1/exports/google-addresses.kml","syrian-official-addresses-google.kml");
  $("#download-google-csv").onclick=()=>downloadProtectedExport("/api/v1/exports/google-addresses.csv","syrian-official-addresses-google.csv");
  $("#refresh-collaboration").onclick=loadCollaborationHub;$("#collaboration-form").onsubmit=createCollaborationCase;
}
const APP_ACCESS={
  SYSTEM_ADMIN:["work","register","workflow","field","collaboration","search","settings","support"],
  GOVERNORATE_ADMIN:["work","register","workflow","field","collaboration","search","support"],
  MUNICIPAL_EDITOR:["work","register","workflow","collaboration","search","support"],
  SURVEYOR:["work","register","field","collaboration","search","support"],
  REVIEWER:["work","workflow","collaboration","search","support"],
  APPROVER:["work","workflow","collaboration","search","support"],
  PRINT_OFFICER:["work","field","search","support"],INSTALLER:["work","field","search","support"],
  REGISTRY_OFFICER:["work","register","search","support"],AUDITOR:["work","workflow","search","support"]
};
function allowedApps(){return new Set(APP_ACCESS[role]||["work"])}
function applyAppPermissions(){
  const allowed=allowedApps();
  document.querySelectorAll("[data-page]").forEach(item=>item.classList.toggle("hidden",!allowed.has(item.dataset.page)));
  document.querySelectorAll("[data-open-app]").forEach(item=>item.classList.toggle("hidden",!allowed.has(item.dataset.openApp)));
  $(".admin-app-group")?.classList.toggle("hidden",role!=="SYSTEM_ADMIN");
  $("#profile-tasks")?.classList.toggle("hidden",!allowed.has("workflow"));$("#profile-search")?.classList.toggle("hidden",!allowed.has("search"));
  $("#profile-settings")?.classList.toggle("hidden",role!=="SYSTEM_ADMIN");
  document.querySelectorAll(".app-group").forEach(group=>group.classList.toggle("empty-group",![...group.querySelectorAll("[data-open-app]")].some(card=>!card.classList.contains("hidden"))));
  const visible=document.querySelector(".portal-page:not(.hidden)");if(visible&&!allowed.has(visible.id.replace("page-","")))openPortalPage("work");
}
function openPortalPage(name){
  if(!allowedApps().has(name))name="work";
  document.querySelectorAll(".portal-page").forEach(page=>page.classList.toggle("hidden",page.id!==`page-${name}`));
  document.querySelectorAll(".portal-nav button").forEach(button=>button.classList.toggle("active",button.dataset.page===name));
  if(name==="settings"){loadSystemSettings();loadGoogleExportStatus()}if(name==="support")loadSupportTickets();if(name==="search")runDataFilter();if(name==="collaboration")loadCollaborationHub();
  setTimeout(()=>{if(!fieldMap)return;fieldMap.resize();if(name==="register")focusActiveAdminArea(0)},0);
}
async function loadCollaborationHub(){
  if(!$("#collaboration-cases")||!token)return;
  const [[casesResponse,data],[officesResponse,offices]]=await Promise.all([api("/api/v1/collaboration/cases"),api("/api/v1/collaboration/offices")]);
  if(!casesResponse.ok)return;
  ["open","due","urgent","completed"].forEach(key=>{const element=$(`#collab-${key}`);if(element)element.textContent=data.summary[key]||0});
  if(officesResponse.ok&&$("#collab-target")&&!$("#collab-target").options.length)$("#collab-target").innerHTML=offices.map(office=>`<option value="${esc(office.id)}">${esc(lang==="ar"?office.name_ar:office.name_en)} · ${esc(office.level)}</option>`).join("");
  const labels={OPEN:"Open",ACCEPTED:"Accepted",IN_PROGRESS:"In progress",RETURNED:"Returned",COMPLETED:"Completed"};
  $("#collaboration-cases").innerHTML=data.cases.slice(0,20).map(item=>`<article class="collaboration-case priority-${item.priority.toLowerCase()}"><div class="collaboration-case-top"><span class="collaboration-type">${esc(item.case_type.replaceAll("_"," "))}</span><b>${esc(labels[item.status]||item.status)}</b></div><h4>${esc(item.title)}</h4><p>${esc(item.description||"")}</p><div class="collaboration-route"><span>${esc(lang==="ar"?item.source_name_ar:item.source_name_en)}</span><i>→</i><span>${esc(lang==="ar"?item.target_name_ar:item.target_name_en)}</span></div><div class="collaboration-meta"><span>${esc(item.priority)}</span><span>${item.due_at?`⏱ ${esc(item.due_at.slice(0,10))}`:""}</span><span>${esc(item.assigned_role)}</span></div><div class="request-actions">${["OPEN","RETURNED"].includes(item.status)?`<button data-collab-action="accept" data-id="${item.id}">${lang==="de"?"Annehmen":"Accept"}</button>`:""}${["OPEN","ACCEPTED","RETURNED"].includes(item.status)?`<button data-collab-action="start" data-id="${item.id}">${lang==="de"?"Bearbeiten":"Start"}</button>`:""}${["ACCEPTED","IN_PROGRESS"].includes(item.status)?`<button data-collab-action="complete" data-id="${item.id}">${lang==="de"?"Abschließen":"Complete"}</button>`:""}${!["COMPLETED","CANCELLED","RETURNED"].includes(item.status)?`<button class="ghost" data-collab-action="return" data-id="${item.id}">${lang==="de"?"Zurückgeben":"Return"}</button>`:""}</div></article>`).join("")||`<div class="collaboration-empty"><strong>${lang==="ar"?"لا توجد تحويلات مفتوحة":lang==="de"?"Keine Behördenübergaben vorhanden":"No authority handovers"}</strong><span>${lang==="de"?"Neue Zusammenarbeit kann rechts im Formular angelegt werden.":"Create a new handover using the form."}</span></div>`;
  document.querySelectorAll("[data-collab-action]").forEach(button=>button.onclick=()=>transitionCollaborationCase(button.dataset.id,button.dataset.collabAction));
  $("#collaboration-form").classList.toggle("hidden",!["GOVERNORATE_ADMIN","MUNICIPAL_EDITOR","SURVEYOR","REVIEWER","APPROVER","SYSTEM_ADMIN"].includes(role));
}
async function createCollaborationCase(event){event.preventDefault();const body={title:$("#collab-title").value.trim(),case_type:$("#collab-type").value,priority:$("#collab-priority").value,target_admin_unit_id:$("#collab-target").value,assigned_role:$("#collab-role").value,due_at:$("#collab-due-at").value,description:$("#collab-description").value.trim()};const [response,data]=await api("/api/v1/collaboration/cases","POST",body);$("#collab-message").textContent=response.ok?(lang==="de"?`Übergabe ${data.id} angelegt.`:`Created ${data.id}`):data.error;if(response.ok){event.target.reset();await loadCollaborationHub()}}
async function transitionCollaborationCase(id,action){let resolution="";if(["complete","return"].includes(action)){resolution=prompt(lang==="ar"?"اكتب النتيجة أو سبب الإعادة":lang==="de"?"Ergebnis oder Rückgabegrund dokumentieren":"Document result or return reason")||"";if(!resolution)return}const [response,data]=await api(`/api/v1/collaboration/cases/${id}/${action}`,"POST",{resolution});if(!response.ok)alert(data.error);await loadCollaborationHub()}
async function runDataFilter(){
  const query=$("#filter-query").value.trim(),status=$("#filter-status").value,postal=$("#filter-postal").value.trim(),type=$("#filter-type").value;
  let items=[];
  if(type==="addresses"){
    const response=await fetch(`/api/v1/addresses?q=${encodeURIComponent(query)}&status=${encodeURIComponent(status)}&postal_code=${encodeURIComponent(postal)}`),data=await response.json();
    items=data.features.map(feature=>feature.properties);
  }else{
    const [response,data]=await api("/api/v1/house-number-cases");if(!response.ok)return;
    const needle=query.toLowerCase();items=data.filter(item=>(!status||item.status===status)&&(!postal||item.postal_code===postal)&&(!needle||JSON.stringify(item).toLowerCase().includes(needle)));
  }
  $("#filter-results").innerHTML=`<p class="filter-count">${items.length} ${lang==="de"?"Treffer":"results"}</p>`+items.map(item=>`<article class="request"><div class="request-top"><strong>${esc(item.name_ar||item.street_name_ar||item.official_code)} ${esc(item.house_number||"")}</strong><b>${esc(item.official_status||item.status||"")}</b></div><div class="meta">${esc(item.official_code||item.building_ref||"")} · ${esc(item.postal_code||"")} · ${item.floors||0} ${lang==="de"?"Etagen":"floors"} · ${item.dwelling_units||0} ${lang==="de"?"Wohnungen":"units"}</div></article>`).join("");
}
async function loadSystemSettings(){let [response,data]=await api("/api/v1/settings");if(!response.ok)return;$("#setting-language").value=lang;$("#setting-map").value=data.map_default_layer||"satellite";$("#setting-support-email").value=data.support_email||"";$("#setting-citizen-search").checked=data.citizen_search_enabled==="true";$("#setting-citizen-pdf").checked=data.citizen_pdf_enabled==="true";["#setting-map","#setting-support-email","#setting-citizen-search","#setting-citizen-pdf","#save-settings"].forEach(selector=>$(selector).disabled=role!=="SYSTEM_ADMIN")}
async function saveSystemSettings(){let [response,data]=await api("/api/v1/settings","POST",{settings:{map_default_layer:$("#setting-map").value,support_email:$("#setting-support-email").value,citizen_search_enabled:$("#setting-citizen-search").checked,citizen_pdf_enabled:$("#setting-citizen-pdf").checked}});$("#settings-message").textContent=response.ok?(lang==="de"?"Einstellungen gespeichert.":"Settings saved."):data.error}
async function loadGoogleExportStatus(){const box=$("#google-export-status");if(!box)return;if(role!=="SYSTEM_ADMIN"){box.textContent=lang==="de"?"Nur der nationale Administrator darf Datenexporte erstellen.":"Only the national administrator can create exports.";$("#download-google-kml").disabled=true;$("#download-google-csv").disabled=true;return}const [response,data]=await api("/api/v1/exports/google-addresses/validation");box.textContent=response.ok?(lang==="de"?`${data.eligible_for_export} freigegeben · ${data.blocked} wegen fehlender Pflichtangaben gesperrt`:`${data.eligible_for_export} eligible · ${data.blocked} blocked`):data.error;box.classList.toggle("warning",response.ok&&data.blocked>0)}
async function downloadProtectedExport(path,filename){const response=await fetch(path,{headers:{Authorization:"Bearer "+token,"X-Device-Time":new Date().toISOString()}});if(!response.ok){const data=await response.json();alert(data.error);return}const blob=await response.blob(),url=URL.createObjectURL(blob),link=document.createElement("a");link.href=url;link.download=filename;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
async function createSupportTicket(){let [response,data]=await api("/api/v1/support-tickets","POST",{category:$("#support-category").value,subject:$("#support-subject").value,message:$("#support-message").value});$("#support-result").textContent=response.ok?`Ticket ${data.id}`:data.error;if(response.ok){$("#support-subject").value="";$("#support-message").value="";loadSupportTickets()}}
async function loadSupportTickets(){let [response,data]=await api("/api/v1/support-tickets");if(!response.ok)return;$("#support-list").innerHTML=data.map(ticket=>`<article class="request"><div class="request-top"><strong>${esc(ticket.subject)}</strong><b>${esc(ticket.status)}</b></div><div class="meta">${esc(ticket.category)} · ${esc(ticket.id)}<br>${esc(ticket.message)}</div></article>`).join("")||`<p class="muted">${lang==="de"?"Keine Anfragen vorhanden.":"No support requests."}</p>`}
async function editHouseCase(item){
  const street=prompt(lang==="ar"?"اسم الشارع":lang==="de"?"Straßenname":"Street name",item.street_name_ar);if(street===null)return;
  const number=prompt(lang==="ar"?"رقم المنزل":lang==="de"?"Hausnummer":"House number",item.house_number);if(number===null)return;
  const postal=prompt(lang==="ar"?"الرمز البريدي":lang==="de"?"Postleitzahl":"Postal code",item.postal_code);if(postal===null)return;
  const floors=prompt(lang==="ar"?"عدد الطوابق":lang==="de"?"Anzahl Etagen":"Number of floors",item.floors||0);if(floors===null)return;
  const units=prompt(lang==="ar"?"عدد الوحدات السكنية":lang==="de"?"Anzahl Wohnungen":"Number of dwellings",item.dwelling_units||0);if(units===null)return;
  const [r,d]=await api(`/api/v1/house-number-cases/${item.id}/update`,"POST",{street_name_ar:street,street_name_en:item.street_name_en,house_number:number,postal_code:postal,floors:+floors,dwelling_units:+units});
  if(!r.ok)alert(d.error);else await loadHouseCases();
}
async function cancelHouseCase(item){
  const question=lang==="ar"?"هل تريد سحب هذا الطلب؟ سيبقى محفوظاً في سجل التدقيق.":lang==="de"?"Diesen Vorgang wirklich zurückziehen? Er bleibt im Prüfprotokoll erhalten.":"Withdraw this case? It remains in the audit history.";
  if(!confirm(question))return;
  const [r,d]=await api(`/api/v1/house-number-cases/${item.id}/cancel`,"POST",{});
  if(!r.ok)alert(d.error);else await loadHouseCases();
}
async function loadHouseCases(){
  let [r,d]=await api("/api/v1/house-number-cases");if(!r.ok)return;
  const canMaintain=["MUNICIPAL_EDITOR","SYSTEM_ADMIN"].includes(role);
  $("#house-cases").innerHTML=d.map(x=>`<article class="request"><div class="request-top"><strong>${esc(x.street_name_ar)} ${esc(x.house_number)}</strong><b>${esc(x.status)}</b></div><div class="meta">${esc(x.building_ref)} · ${esc(x.postal_code)} ${esc(x.locality_en)} · ${x.floors||0} ${lang==="de"?"Etagen":"floors"} · ${x.dwelling_units||0} ${lang==="de"?"Wohnungen":"units"}</div>${x.status==="SUBMITTED"&&role==="INSTALLER"?`<div class="install-evidence"><label>${esc(messages[lang].photo)}<input type="file" accept="image/*" capture="environment" data-photo-for="${x.id}"></label><button data-install-case="${x.id}">${esc(messages[lang].installCapture)}</button></div>`:""}<div class="request-actions">${x.status==="SUBMITTED"&&canMaintain?`<button class="ghost" data-edit-case="${x.id}">${lang==="ar"?"تعديل":lang==="de"?"Bearbeiten":"Edit"}</button><button class="ghost" data-cancel-case="${x.id}">${lang==="ar"?"حذف":lang==="de"?"Löschen":"Delete"}</button>`:""}${["SUBMITTED","INSTALLED"].includes(x.status)&&["REVIEWER","SYSTEM_ADMIN"].includes(role)?`<button data-house-action="review" data-id="${x.id}">Review</button>`:""}${x.status==="REVIEWED"&&["APPROVER","SYSTEM_ADMIN"].includes(role)?`<button data-house-action="approve" data-id="${x.id}">Approve</button>`:""}</div></article>`).join("")||"<p class='muted'>No house-number cases.</p>";
  [...$("#house-cases").querySelectorAll(".request-actions")].forEach((actions,index)=>actions.insertAdjacentHTML("beforeend",`<button class="ghost" data-case-pdf="${d[index].id}">${lang==="ar"?"طباعة الملف":lang==="de"?"Akte drucken":"Print dossier"}</button>`));
  document.querySelectorAll("[data-house-action]").forEach(b=>b.onclick=async()=>{let [response,result]=await api(`/api/v1/house-number-cases/${b.dataset.id}/${b.dataset.houseAction}`,"POST",{});if(!response.ok)alert(result.error);loadHouseCases()});
  document.querySelectorAll("[data-install-case]").forEach(b=>{b.dataset.id=b.dataset.installCase;b.onclick=()=>captureInstallation(b)});
  document.querySelectorAll("[data-edit-case]").forEach(b=>b.onclick=()=>editHouseCase(d.find(x=>x.id===b.dataset.editCase)));
  document.querySelectorAll("[data-cancel-case]").forEach(b=>b.onclick=()=>cancelHouseCase(d.find(x=>x.id===b.dataset.cancelCase)));
  document.querySelectorAll("[data-case-pdf]").forEach(b=>b.onclick=()=>downloadCasePdf(b.dataset.casePdf));
}
async function downloadCasePdf(id){const response=await fetch(`/api/v1/pdf/CASE/${encodeURIComponent(id)}`,{headers:{Authorization:"Bearer "+token,"X-Device-Time":new Date().toISOString()}});if(!response.ok){const data=await response.json();alert(data.error);return}const blob=await response.blob(),url=URL.createObjectURL(blob),link=document.createElement("a");link.href=url;link.download=`${id}-object-dossier.pdf`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}
const loadBuildingsBase=loadBuildings;
loadBuildings=async()=>{await loadBuildingsBase();const select=$("#house-parcel");if(select){const current=select.value,building=fieldBuildings?.features?.find(feature=>feature.id===$("#building-ref").value),linkedParcel=building?.properties?.parcel_id||"";select.innerHTML=`<option value="">—</option>`+(fieldParcels?.features||[]).map(f=>`<option value="${esc(f.id)}">Flur ${esc(f.properties.section_number)} / Flurstück ${esc(f.properties.parcel_number)} · ${formatArea(f.properties.area_m2)}</option>`).join("");select.value=linkedParcel&&[...select.options].some(option=>option.value===linkedParcel)?linkedParcel:(current&&[...select.options].some(option=>option.value===current)?current:"");select.onchange=()=>selectFieldParcel(select.value);if(select.value)selectFieldParcel(select.value)}};
const apiBase=api;
api=(path,method="GET",body)=>{if(path==="/api/v1/house-number-cases"&&method==="POST"&&body){if(!body.parcel_id)body.parcel_id=$("#house-parcel")?.value||null;body.street_side=$("#street-side")?.value||"UNDETERMINED";if(doorPosition){body.entrance_longitude=doorPosition.longitude;body.entrance_latitude=doorPosition.latitude;body.entrance_adjusted=Boolean(doorPosition.adjusted)}}return apiBase(path,method,body)};
$("#house-number").addEventListener("input",()=>{if(doorMarker)doorMarker.getElement().dataset.houseNumber=$("#house-number").value});
loadHouseCases=async function(){
  const [response,data]=await api("/api/v1/house-number-cases");if(!response.ok)return;
  const active=data.filter(item=>!["CANCELLED","REJECTED"].includes(item.status));
  const history=data.filter(item=>["CANCELLED","REJECTED"].includes(item.status));
  const canMaintain=["MUNICIPAL_EDITOR","SYSTEM_ADMIN"].includes(role);
  const card=item=>`<article class="request case-card"><div class="request-top"><strong>${esc(item.street_name_ar)} ${esc(item.house_number)}</strong><b class="case-status">${esc(item.status)}</b></div><div class="case-object">${esc(item.building_ref)}</div><div class="meta">${esc(item.postal_code)} Al‑Zabadani · ${item.floors||0} ${lang==="de"?"Etagen":"floors"} · ${item.dwelling_units||0} ${lang==="de"?"Wohnungen":"units"}${item.parcel_id?` · ${lang==="de"?"Flurstück verknüpft":"parcel linked"}`:""}</div><div class="request-actions">${item.status==="SUBMITTED"&&canMaintain?`<button class="ghost" data-edit-case="${item.id}">${lang==="de"?"Bearbeiten":"Edit"}</button><button class="ghost" data-cancel-case="${item.id}">${lang==="de"?"Zurückziehen":"Withdraw"}</button>`:""}${["SUBMITTED","INSTALLED"].includes(item.status)&&["REVIEWER","SYSTEM_ADMIN"].includes(role)?`<button data-house-action="review" data-id="${item.id}">${lang==="de"?"Prüfen":"Review"}</button>`:""}${item.status==="REVIEWED"&&["APPROVER","SYSTEM_ADMIN"].includes(role)?`<button data-house-action="approve" data-id="${item.id}">${lang==="de"?"Freigeben":"Approve"}</button>`:""}<button class="ghost" data-case-pdf="${item.id}">${lang==="de"?"Akte drucken":"Print dossier"}</button></div></article>`;
  $("#house-cases").innerHTML=`<div class="case-section-heading"><strong>${lang==="de"?"Aktuelle Vorgänge":"Current cases"}</strong><span>${active.length}</span></div>${active.map(card).join("")||`<p class="empty-register">${lang==="de"?"Keine offenen Vorgänge.":"No open cases."}</p>`}${history.length?`<details class="case-history"><summary>${lang==="de"?"Zurückgezogene und abgelehnte Vorgänge":"Withdrawn and rejected cases"} (${history.length})</summary><div class="case-history-list">${history.map(card).join("")}</div></details>`:""}`;
  document.querySelectorAll("[data-house-action]").forEach(button=>button.onclick=async()=>{const [r,d]=await api(`/api/v1/house-number-cases/${button.dataset.id}/${button.dataset.houseAction}`,"POST",{});if(!r.ok)alert(d.error);await loadHouseCases()});
  document.querySelectorAll("[data-edit-case]").forEach(button=>button.onclick=()=>editHouseCase(data.find(item=>item.id===button.dataset.editCase)));
  document.querySelectorAll("[data-cancel-case]").forEach(button=>button.onclick=()=>cancelHouseCase(data.find(item=>item.id===button.dataset.cancelCase)));
  document.querySelectorAll("[data-case-pdf]").forEach(button=>button.onclick=()=>downloadCasePdf(button.dataset.casePdf));
};
function notificationText(){
  if(lang==="ar")return{title:"الإشعارات",submitted:"بانتظار المراجعة",reviewed:"بانتظار الاعتماد",changes:"طلبات تغيير مفتوحة",empty:"لا توجد مهام مفتوحة"};
  if(lang==="de")return{title:"Benachrichtigungen",submitted:"Zur Prüfung",reviewed:"Zur Freigabe",changes:"Offene Änderungen",empty:"Keine offenen Aufgaben"};
  return{title:"Notifications",submitted:"Awaiting review",reviewed:"Awaiting approval",changes:"Open changes",empty:"No open tasks"};
}
function initHeaderNotifications(){
  const profile=$("#header-profile");if(!profile||$("#header-notifications"))return;
  profile.insertAdjacentHTML("beforebegin",`<div id="header-notifications" class="header-notifications hidden"><button id="notification-toggle" class="notification-toggle" type="button" aria-haspopup="true" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"></path><path d="M10 21h4"></path></svg><span id="notification-badge" class="notification-badge hidden">0</span></button><div id="notification-menu" class="notification-menu hidden"><div class="notification-heading"><strong id="notification-title"></strong><span id="notification-total">0</span></div><div id="notification-list" class="notification-list"></div></div></div>`);
  const label=notificationText().title,toggle=$("#notification-toggle");toggle.setAttribute("aria-label",label);toggle.title=label;
  toggle.onclick=async event=>{event.stopPropagation();$("#profile-menu").classList.add("hidden");$("#profile-toggle").setAttribute("aria-expanded","false");const menu=$("#notification-menu"),open=menu.classList.toggle("hidden")===false;toggle.setAttribute("aria-expanded",String(open));if(open)await loadHeaderNotifications()};
  $("#notification-menu").onclick=event=>event.stopPropagation();
  $("#profile-toggle").addEventListener("click",()=>{$("#notification-menu").classList.add("hidden");toggle.setAttribute("aria-expanded","false")});
  document.addEventListener("click",()=>{$("#notification-menu")?.classList.add("hidden");toggle.setAttribute("aria-expanded","false")});
}
async function loadHeaderNotifications(){
  if(!token||!$("#notification-list"))return;const copy=notificationText();
  const [casesResult,changesResult]=await Promise.all([api("/api/v1/house-number-cases"),api("/api/v1/change-requests")]);
  const cases=casesResult[0].ok&&Array.isArray(casesResult[1])?casesResult[1]:[],changes=changesResult[0].ok&&Array.isArray(changesResult[1])?changesResult[1]:[];
  const items=[{label:copy.submitted,count:cases.filter(item=>["SUBMITTED","INSTALLED"].includes(item.status)).length},{label:copy.reviewed,count:cases.filter(item=>item.status==="REVIEWED").length},{label:copy.changes,count:changes.filter(item=>["SUBMITTED","REVIEWED"].includes(item.status)).length}],total=items.reduce((sum,item)=>sum+item.count,0);
  $("#notification-title").textContent=copy.title;$("#notification-total").textContent=String(total);$("#notification-badge").textContent=total>99?"99+":String(total);$("#notification-badge").classList.toggle("hidden",total===0);
  $("#notification-list").innerHTML=total?items.filter(item=>item.count).map(item=>`<button class="notification-item" type="button"><span>${esc(item.label)}</span><b>${item.count}</b></button>`).join(""):`<p class="notification-empty">${esc(copy.empty)}</p>`;
  document.querySelectorAll(".notification-item").forEach(button=>button.onclick=()=>{$("#notification-menu").classList.add("hidden");$("#notification-toggle").setAttribute("aria-expanded","false");openPortalPage("workflow")});
}
function syncHeaderNotifications(){const container=$("#header-notifications");if(!container)return;container.classList.toggle("hidden",!token);if(token)loadHeaderNotifications();else{$("#notification-menu").classList.add("hidden");$("#notification-badge").classList.add("hidden")}}
initHeaderNotifications();const baseShow=show;show=function(){baseShow();syncHeaderNotifications();applyAppPermissions()};
buildPortalPages();$("#refresh").onclick=load;applyLanguage();loadBuildings();show();
