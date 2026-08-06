# Syrischer nationaler Objektartenkatalog v0.1

Status: fachlicher Pilotentwurf, nicht rechtsverbindlich. ALKIS-Prinzipien wie Objekttrennung, Beziehungen, kontrollierte Wertelisten, Qualität, Quellenbezug, Lebenszeit und Historisierung wurden adaptiert; deutsche Rechtsbegriffe wurden nicht übernommen.

## Gemeinsame Merkmale

Jedes amtliche Objekt besitzt eine unveränderliche UUID, eine lesbare nationale Kennung, Gültigkeitsbeginn/-ende, Version, Status, Quelle und Qualitätsstufe. Namen werden nicht in ein einziges Feld gepresst: Arabisch ist im Pilot Pflichtfeld; Englisch, Kurdisch, historische und alternative Namen sind getrennt.

Qualität:

| Code | Bedeutung |
|---|---|
| A | amtlich vermessen und fachlich geprüft |
| B | amtlich bestätigt, Messung/Genauigkeit eingeschränkt |
| C | aus Orthofoto, Luft- oder Satellitenbild abgeleitet |
| D | kommunal/Bürger gemeldet, noch nicht fachlich bestätigt |
| E | historischer oder unsicherer Bestand |

## 10000 Verwaltungsgebiet (`AdminUnit`)

- Definition: hierarchisch abgegrenzte staatliche oder kommunale Einheit.
- Geometrie: MultiPolygon.
- Pflicht: Kennung, Ebene, arabischer Name, Gültigkeit.
- Ebenen: Staat, Gouvernorat, Bezirk, Unterbezirk, Gemeinde, Ort, Stadtteil.
- Beziehung: optional genau ein Elternobjekt; Staat besitzt keines.
- Regel: Kindgeometrie muss grundsätzlich innerhalb der Elterngeometrie liegen.
- Sichtbarkeit: öffentlich.

## 20000 Straße/Weg (`Street`)

- Definition: amtlich benannter oder technisch identifizierter Verkehrsweg.
- Geometrie: MultiLineString.
- Pflicht: Kennung, zuständige Einheit, arabischer Name, Klasse, Status.
- Optional: englischer/kurdischer Name, frühere Namen.
- Sonderfall: unbenannter Weg erhält technische Kennung, aber keinen erfundenen amtlichen Namen.
- Sichtbarkeit: öffentlich.

## 30000 Adresse (`Address`)

- Definition: amtlich verwendbare Ortsangabe, getrennt von Grundstück, Gebäude und Person.
- Geometrie: Point; bevorzugt am Eingang.
- Pflicht: Kennung, Verwaltungseinheit, arabische Formatierung, Position, Qualität, Quelle.
- Beziehungen: 0..1 Straße, 0..1 Gebäude, 0..1 Eingang.
- Sonderfälle: Gebäude ohne Straße, ländliche Adresse, Eckgebäude, temporäre Adresse.
- Regel: kein Eigentümer- oder Bewohnerbezug im öffentlichen Register.
- Sichtbarkeit: öffentlich; interne Quellbelege geschützt.

## 40000 Grundstück (`Parcel`)

- Definition: katasterfachlich abgegrenzte Bodenfläche.
- Geometrie: MultiPolygon.
- Pflicht: Kennung, Verwaltungseinheit, Geometrie, Qualität, Quelle.
- Beziehung: 0..* Gebäude über explizite Zuordnung.
- Regel: Eigentum wird nicht in diesem öffentlichen Fachobjekt gespeichert.
- Sichtbarkeit: intern; vereinfachte Darstellung nach politisch-rechtlicher Entscheidung.

## 50000 Gebäude (`Building`)

- Definition: dauerhaftes oder dokumentiertes Bauwerk mit eigenem Lebenszyklus.
- Geometrie: MultiPolygon.
- Pflicht: Kennung, Verwaltungseinheit, Funktion, Status, Qualität, Quelle.
- Status: geplant, vorhanden, beschädigt, zerstört, im Wiederaufbau, stillgelegt.
- Beziehung: 0..* Eingänge; 0..* Grundstücke.
- Sichtbarkeit: Grunddaten öffentlich, sensible Zusatzdaten intern.

## 60000 Eingang (`Entrance`)

- Definition: physischer Zugang zu einem Gebäude, navigierbares Ziel für Post und Rettungsdienste.
- Geometrie: Point.
- Pflicht: Kennung, Gebäude, Position, Qualität.
- Optional: Label, Barrierefreiheit; Einsatzhinweise sind geschützt.
- Regel: Position liegt an oder nahe der Gebäudehülle.

## 61000 Nutzungseinheit (`Unit`)

- Definition: Wohnung, Geschäft, Amt oder andere selbstständig adressierbare Einheit.
- Geometrie: keine oder optional Innenraumgeometrie.
- Pflicht: Kennung, Gebäude/Eingang, Typ, Status.
- Sichtbarkeit: nicht öffentlich; keine Bewohnerdaten.
- Pilotstatus: fachlich vorgesehen, noch nicht implementiert.

## 70000 Quellen-/Qualitätsnachweis (`SourceRecord`)

- Definition: Herkunft, Erfassungszeit, Genauigkeit und Prüfung eines Fachobjekts.
- Pflicht: Objekttyp/-ID, Quelltyp, Prüfstatus.
- Regel: Qualitätsverbesserung erfordert dokumentierte Quelle.
- Sichtbarkeit: intern.

## 80000 Änderungsantrag (`ChangeRequest`)

- Definition: kontrollierter Vorschlag zur Anlage, Änderung oder Außerkraftsetzung.
- Pflicht: Objektart, Vorgang, Nutzdaten, Begründung, Antragsteller, Zeit.
- Lebenszyklus: Entwurf → eingereicht → geprüft → genehmigt/abgelehnt → publiziert → historisiert.
- Regel: Antragsteller und Genehmiger dürfen in Produktion nicht identisch sein.
- Sichtbarkeit: behördenintern.

## 81000 Auditereignis (`AuditEvent`)

- Definition: manipulationserschwerender Nachweis einer sicherheits- oder fachrelevanten Aktion.
- Pflicht: Zeit, Aktion, Objektart, Ereignishash.
- Regel: nur anhängen; Export an getrennte Sicherheitsdomäne.
- Sichtbarkeit: Auditoren/Sicherheitsbetrieb.

## 90000 Organisation/Zuständigkeit

Behörden, Zuständigkeitsräume, Mandate und Delegationen. Vor Produktivsetzung gemeinsam mit staatlichen Stellen zu modellieren; im Pilot durch Rollen abstrahiert.
