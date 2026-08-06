"""Create a printable, privacy-safe PDF dossier for a registry object."""
from io import BytesIO
from pathlib import Path
import sys

APP = Path(__file__).resolve().parent
sys.path.insert(0, str(APP / "vendor"))
sys.path.insert(0, str(APP / "pdf_lib"))

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import arabic_reshaper
from bidi.algorithm import get_display

FONT_PATH = APP / "fonts" / "NotoSansArabic.ttf"
LOGO_PATH = APP / "syria-logo-on-green.jpg"
TRANSPARENT_LOGO_PATH = APP / "syria-logo-pdf.jpg"
pdfmetrics.registerFont(TTFont("NotoArabic", str(FONT_PATH)))


def ar(value):
    """Shape Arabic for right-to-left display in ReportLab."""
    return get_display(arabic_reshaper.reshape(str(value or "")))


def build_pdf(record):
    out = BytesIO()
    pdf = canvas.Canvas(out, pagesize=A4, pageCompression=1)
    width, height = A4
    green = colors.HexColor("#0B6B4C")
    ink = colors.HexColor("#153128")
    pale = colors.HexColor("#EEF4F0")
    muted = colors.HexColor("#607269")
    gold = colors.HexColor("#D9A441")

    pdf.setTitle(f"Object dossier {record.get('technical_code', '')}")
    pdf.setAuthor("Syria National Address Platform")
    pdf.setSubject("Printable public registry object dossier")

    pdf.setFillColor(green)
    pdf.rect(0, height - 86, width, 86, fill=1, stroke=0)
    pdf.drawImage(str(LOGO_PATH), 20, height - 72, width=52, height=52, preserveAspectRatio=True)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(84, height - 43, "SYRIA NATIONAL ADDRESS PLATFORM")
    pdf.setFont("NotoArabic", 13)
    pdf.drawRightString(
        width - 42,
        height - 43,
        ar("\u0627\u0644\u0645\u0646\u0635\u0629 \u0627\u0644\u0648\u0637\u0646\u064a\u0629 \u0627\u0644\u0633\u0648\u0631\u064a\u0629 \u0644\u0644\u0639\u0646\u0627\u0648\u064a\u0646"),
    )
    pdf.setFont("Helvetica", 8)
    pdf.drawString(84, height - 66, "PRINTABLE OBJECT DOSSIER - CONTROLLED COPY")

    pdf.setFillColor(ink)
    pdf.setFont("Helvetica-Bold", 23)
    pdf.drawString(42, height - 126, "OBJECT DOSSIER")
    pdf.setFont("NotoArabic", 18)
    pdf.drawRightString(
        width - 42,
        height - 126,
        ar("\u0645\u0644\u0641 \u0627\u0644\u0643\u0627\u0626\u0646"),
    )
    pdf.setStrokeColor(colors.HexColor("#DDE6E0"))
    pdf.line(42, height - 145, width - 42, height - 145)

    fields = [
        ("Dossier number", "\u0631\u0642\u0645 \u0627\u0644\u0645\u0644\u0641", record.get("dossier_number")),
        ("Object type", "\u0646\u0648\u0639 \u0627\u0644\u0643\u0627\u0626\u0646", record.get("object_type")),
        ("Technical identifier", "\u0627\u0644\u0645\u0639\u0631\u0641 \u0627\u0644\u062a\u0642\u0646\u064a", record.get("technical_code")),
        ("Arabic designation", "\u0627\u0644\u062a\u0633\u0645\u064a\u0629 \u0627\u0644\u0639\u0631\u0628\u064a\u0629", record.get("label_ar")),
        ("English designation", "\u0627\u0644\u062a\u0633\u0645\u064a\u0629 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629", record.get("label_en")),
        ("House number", "\u0631\u0642\u0645 \u0627\u0644\u0645\u0646\u0632\u0644", record.get("house_number")),
        ("Postal code", "\u0627\u0644\u0631\u0645\u0632 \u0627\u0644\u0628\u0631\u064a\u062f\u064a", record.get("postal_code")),
        ("Locality", "\u0627\u0644\u0628\u0644\u062f\u0629", record.get("locality")),
        ("Coordinates", "\u0627\u0644\u0625\u062d\u062f\u0627\u062b\u064a\u0627\u062a", record.get("coordinates")),
        ("Quality level", "\u0645\u0633\u062a\u0648\u0649 \u0627\u0644\u062c\u0648\u062f\u0629", record.get("quality_level")),
        ("Official status", "\u0627\u0644\u062d\u0627\u0644\u0629 \u0627\u0644\u0631\u0633\u0645\u064a\u0629", record.get("official_status")),
        ("Data source", "\u0645\u0635\u062f\u0631 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a", record.get("source")),
    ]

    y = height - 180
    for english, arabic, value in fields:
        if value in (None, ""):
            continue
        pdf.setFillColor(pale)
        pdf.roundRect(42, y - 28, width - 84, 33, 6, fill=1, stroke=0)
        pdf.setFillColor(muted)
        pdf.setFont("Helvetica-Bold", 7)
        pdf.drawString(54, y - 7, english.upper())
        pdf.setFont("NotoArabic", 8)
        pdf.drawRightString(width - 54, y - 7, ar(arabic))
        value = str(value)
        is_arabic = any("\u0600" <= character <= "\u06ff" for character in value)
        pdf.setFillColor(ink)
        pdf.setFont("NotoArabic" if is_arabic else "Helvetica", 10)
        pdf.drawString(54, y - 22, (ar(value) if is_arabic else value)[:90])
        y -= 40

    pdf.setFillColor(pale)
    pdf.roundRect(42, 112, width - 84, 78, 8, fill=1, stroke=0)
    pdf.setFillColor(gold)
    pdf.rect(42, 112, 6, 78, fill=1, stroke=0)
    pdf.setFillColor(ink)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(60, 170, "VALIDITY NOTICE")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(60, 153, "This record is legally authoritative only when its status is OFFICIAL and the")
    pdf.drawString(60, 140, "issuing authority has approved it. Other objects remain working records.")
    pdf.setFont("NotoArabic", 8)
    pdf.drawRightString(
        width - 60,
        123,
        ar("\u0644\u0627 \u062a\u0635\u0628\u062d \u0647\u0630\u0647 \u0627\u0644\u0648\u062b\u064a\u0642\u0629 \u0631\u0633\u0645\u064a\u0629 \u0625\u0644\u0627 \u0628\u0639\u062f \u0627\u0639\u062a\u0645\u0627\u062f \u0627\u0644\u062c\u0647\u0629 \u0627\u0644\u0645\u062e\u062a\u0635\u0629."),
    )

    qr_value = str(record.get("verification_value") or record.get("technical_code") or "SNA")
    widget = qr.QrCodeWidget(qr_value)
    bounds = widget.getBounds()
    size = 54
    drawing = Drawing(
        size,
        size,
        transform=[size / (bounds[2] - bounds[0]), 0, 0, size / (bounds[3] - bounds[1]), 0, 0],
    )
    drawing.add(widget)
    renderPDF.draw(drawing, pdf, width - 100, 35)

    pdf.setFillColor(muted)
    pdf.setFont("Helvetica", 7)
    pdf.drawString(42, 61, "Generated by SNA Platform - verify against the live registry")
    pdf.drawString(42, 47, "Public print copy - no owner or resident information included")
    pdf.setFont("Helvetica-Bold", 8)
    has_evidence=bool(record.get("details") or record.get("audit_events"))
    pdf.drawRightString(width - 42, 24, "PAGE 1 / 2" if has_evidence else "PAGE 1 / 1")
    pdf.showPage()
    if has_evidence:
        pdf.setFillColor(green);pdf.rect(0,height-70,width,70,fill=1,stroke=0)
        pdf.setFillColor(colors.white);pdf.setFont("Helvetica-Bold",14)
        pdf.drawString(42,height-42,"OBJECT RECORD · EVIDENCE AND AUDIT")
        pdf.setFont("NotoArabic",12)
        pdf.drawRightString(width-42,height-42,ar("سجل الكائن والأدلة والتدقيق"))
        y=height-100
        pdf.setFillColor(ink);pdf.setFont("Helvetica-Bold",10)
        pdf.drawString(42,y,"CAPTURE AND WORKFLOW DATA");y-=20
        for label,value in record.get("details",[]):
            if value in (None,""):continue
            pdf.setFillColor(pale);pdf.roundRect(42,y-18,width-84,24,4,fill=1,stroke=0)
            pdf.setFillColor(muted);pdf.setFont("Helvetica-Bold",7);pdf.drawString(51,y-4,str(label).upper())
            pdf.setFillColor(ink);pdf.setFont("Helvetica",8);pdf.drawString(190,y-4,str(value)[:70]);y-=30
        y-=5;pdf.setFillColor(ink);pdf.setFont("Helvetica-Bold",10)
        pdf.drawString(42,y,"TAMPER-EVIDENT AUDIT CHAIN");y-=19
        for event in record.get("audit_events",[]):
            if y<55:break
            pdf.setFillColor(pale);pdf.roundRect(42,y-17,width-84,23,4,fill=1,stroke=0)
            pdf.setFillColor(ink);pdf.setFont("Helvetica-Bold",7)
            pdf.drawString(50,y-3,f"{event.get('event_time','')}  {event.get('action','')}  {event.get('actor_id','')}")
            pdf.setFont("Helvetica",6);pdf.drawString(50,y-12,f"SHA-256: {event.get('chain_hash','')}");y-=28
        pdf.setFillColor(muted);pdf.setFont("Helvetica",7)
        pdf.drawString(42,32,"Every listed event is chained to the previous event. Verify against the live audit register.")
        pdf.setFont("Helvetica-Bold",8);pdf.drawRightString(width-42,24,"PAGE 2 / 2")
        pdf.showPage()
    pdf.save()
    out.seek(0)
    return out.getvalue()


def build_cadastral_map_pdf(data):
    """Build an official-looking, privacy-safe cadastral map extract."""
    paper=A3 if data.get("paper")=="A3" else A4
    if data.get("orientation")=="landscape":
        paper=landscape(paper)
    width,height=paper
    out=BytesIO();pdf=canvas.Canvas(out,pagesize=paper,pageCompression=1)
    green=colors.HexColor("#245B43");ink=colors.HexColor("#172820")
    gold=colors.HexColor("#B89B62");line=colors.HexColor("#CBD5CF");pale=colors.HexColor("#F3F6F4")
    pdf.setTitle(data.get("title") or "Liegenschaftskarte Al-Zabadani")
    pdf.setAuthor("Nationales syrisches Liegenschafts- und Adresskataster")
    margin=30;header_h=88;footer_h=130
    pdf.setFillColor(colors.white);pdf.rect(0,0,width,height,fill=1,stroke=0)
    pdf.setFillColor(green);pdf.rect(0,height-header_h,width,header_h,fill=1,stroke=0)
    pdf.drawImage(str(TRANSPARENT_LOGO_PATH),margin,height-70,width=52,height=52,
                  preserveAspectRatio=True,mask="auto")
    pdf.setFillColor(colors.white);pdf.setFont("Helvetica-Bold",13)
    pdf.drawString(94,height-27,"NATIONALES LIEGENSCHAFTS- UND ADRESSKATASTER")
    pdf.setFont("NotoArabic",11)
    pdf.drawRightString(width-margin,height-49,ar("السجل الوطني السوري للعقارات والعناوين"))
    pdf.setFont("Helvetica",7.5);pdf.drawString(94,height-66,"AMTLICHER KARTENAUSZUG · PILOTGEBIET AL-ZABADANI")
    map_y=footer_h+margin;map_h=height-header_h-map_y-16;map_w=width-2*margin
    bounds=data.get("bounds") or []
    if len(bounds)!=4 or bounds[0]>=bounds[2] or bounds[1]>=bounds[3]:
        rings=[item["geometry"]["coordinates"][0] for item in data.get("parcels",[]) if item.get("geometry",{}).get("type")=="Polygon"]
        points=[point for ring in rings for point in ring]
        if points:
            xs=[point[0] for point in points];ys=[point[1] for point in points]
            pad=max(max(xs)-min(xs),max(ys)-min(ys),.0005)*2
            bounds=[min(xs)-pad,min(ys)-pad,max(xs)+pad,max(ys)+pad]
        else:bounds=[36.08,33.70,36.13,33.75]
    west,south,east,north=map(float,bounds)
    def xy(point):
        return margin+(point[0]-west)/(east-west)*map_w,map_y+(point[1]-south)/(north-south)*map_h
    def paths(geometry):
        kind=geometry.get("type");coordinates=geometry.get("coordinates") or []
        if kind=="LineString":return [coordinates]
        if kind=="MultiLineString":return coordinates
        if kind=="Polygon":return coordinates
        if kind=="MultiPolygon":return [ring for polygon in coordinates for ring in polygon]
        return []
    def draw_lines(features,color_value,line_width):
        pdf.setStrokeColor(color_value);pdf.setLineWidth(line_width)
        for feature in features:
            for sequence in paths(feature.get("geometry") or {}):
                if len(sequence)<2:continue
                path=pdf.beginPath();x,y=xy(sequence[0]);path.moveTo(x,y)
                for point in sequence[1:]:x,y=xy(point);path.lineTo(x,y)
                pdf.drawPath(path,stroke=1,fill=0)
    pdf.setFillColor(colors.HexColor("#FAF9F4"));pdf.rect(margin,map_y,map_w,map_h,fill=1,stroke=0)
    pdf.saveState();clip=pdf.beginPath();clip.rect(margin,map_y,map_w,map_h);pdf.clipPath(clip,stroke=0)
    draw_lines(data.get("roads",[]),colors.HexColor("#B9BDBA"),5)
    draw_lines(data.get("roads",[]),colors.white,3.2)
    pdf.setFillColor(colors.HexColor("#B8BCBA"));pdf.setStrokeColor(colors.HexColor("#606864"));pdf.setLineWidth(.45)
    for feature in data.get("buildings",[]):
        for ring in paths(feature.get("geometry") or {}):
            if len(ring)<3:continue
            path=pdf.beginPath();x,y=xy(ring[0]);path.moveTo(x,y)
            for point in ring[1:]:x,y=xy(point);path.lineTo(x,y)
            path.close();pdf.drawPath(path,stroke=1,fill=1)
    for item in data.get("parcels",[]):
        approved=item.get("official_status")=="APPROVED"
        pdf.setFillColor(colors.HexColor("#F1DDE2" if approved else "#F8E9CD"))
        pdf.setStrokeColor(colors.HexColor("#25201F" if approved else "#B15B16"));pdf.setLineWidth(1.4)
        for ring in paths(item.get("geometry") or {}):
            if len(ring)<3:continue
            path=pdf.beginPath();x,y=xy(ring[0]);path.moveTo(x,y)
            for point in ring[1:]:x,y=xy(point);path.lineTo(x,y)
            path.close();pdf.drawPath(path,stroke=1,fill=1)
            center_x=sum(point[0] for point in ring[:-1])/max(1,len(ring)-1)
            center_y=sum(point[1] for point in ring[:-1])/max(1,len(ring)-1)
            lx,ly=xy([center_x,center_y]);pdf.setFillColor(ink);pdf.setFont("Helvetica-Bold",7)
            pdf.drawCentredString(lx,ly+2,str(item.get("section_number","")))
            pdf.drawCentredString(lx,ly-7,str(item.get("parcel_number","")))
    pdf.restoreState()
    pdf.setStrokeColor(colors.HexColor("#66756F"));pdf.setLineWidth(.7);pdf.rect(margin,map_y,map_w,map_h,fill=0,stroke=1)
    title=data.get("title") or "Liegenschaftskarte Al-Zabadani"
    parcel=data.get("parcel") or {}
    pdf.setFillColor(ink);pdf.setFont("Helvetica-Bold",12);pdf.drawString(margin,footer_h+13,title[:80])
    pdf.setFont("Helvetica-Bold",8);pdf.setFillColor(green)
    pdf.drawString(margin,footer_h-5,"KATASTERBEZIRK")
    pdf.drawString(margin+175,footer_h-5,"FLUR / FLURSTÜCK")
    pdf.drawString(margin+330,footer_h-5,"QUALITÄT / STATUS")
    pdf.setFillColor(ink);pdf.setFont("Helvetica",9)
    pdf.drawString(margin,footer_h-20,"SY-RD-ZA · Al-Zabadani")
    pdf.drawString(margin+175,footer_h-20,f"{parcel.get('section_number','-')} / {parcel.get('parcel_number','-')}")
    pdf.drawString(margin+330,footer_h-20,f"{parcel.get('quality_level','-')} / {parcel.get('official_status','-')}")
    pdf.setStrokeColor(line);pdf.line(margin,footer_h-30,width-margin,footer_h-30)
    pdf.setFillColor(ink);pdf.setFont("Helvetica",7.5)
    pdf.drawString(margin,footer_h-44,f"Maßstab 1:{data.get('scale','-')} · Koordinatenreferenz WGS 84 (EPSG:4326) · Erstellt {data.get('created_at','')}")
    note=(data.get("note") or "").strip()
    if note:pdf.drawString(margin,footer_h-57,("Hinweis: "+note)[:150])
    pdf.setFillColor(gold);pdf.rect(margin,19,5,26,fill=1,stroke=0)
    pdf.setFillColor(ink);pdf.setFont("Helvetica",7)
    pdf.drawString(margin+12,35,"Dieser Auszug enthält keine Eigentümer- oder Bewohnerdaten.")
    pdf.drawString(margin+12,24,"DRAFT/Qualitätsstufe C ist nicht mit einer amtlich vermessenen Grenze der Qualitätsstufe A gleichzusetzen.")
    pdf.setFont("Helvetica-Bold",7);pdf.drawRightString(width-margin,24,"SEITE 1 / 1")
    pdf.showPage();pdf.save();out.seek(0);return out.getvalue()
