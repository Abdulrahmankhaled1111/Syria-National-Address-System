# Straßen-, Kataster- und Eigentümerdaten

## Kartenansichten

- **Straßen & Verkehrsnetz:** zeigt nur das Verkehrsnetz und Straßennamen. Katasterflächen, Objekt- und Hausnummern bleiben verborgen.
- **Kataster & Flurstücke:** zeigt Flur, Flurstücksnummer, Gebäude-Objektnummer und amtliche Hausnummer.

## Straßennamen importieren

Die Vorlage `data/templates/streets-import-example.geojson` enthält das verbindliche Austauschformat. Pro Straße werden benötigt:

- stabiler `official_code`, der nie wieder für eine andere Straße verwendet wird;
- arabischer amtlicher Name `name_ar`;
- optionaler englischer Name `name_en`;
- `road_class`: `MOTORWAY`, `TRUNK`, `PRIMARY`, `SECONDARY`, `TERTIARY`, `LOCAL`, `SERVICE` oder `PEDESTRIAN`;
- bisherige Namen als `former_names`;
- Straßenachse als `LineString` oder `MultiLineString` in WGS 84 / EPSG:4326;
- zuständige Verwaltungseinheit `admin_unit_id` und amtliche Quelle `source_name`.

Ein Systemadministrator sendet die FeatureCollection an `POST /api/v1/streets/import`. Wiederholte Importe aktualisieren anhand von `official_code`, erzeugen keine Dubletten und bleiben zunächst `DRAFT`. Erst Namens-, Geometrie- und Zuständigkeitsprüfung dürfen die Daten amtlich freigeben. `GET /api/v1/streets` liefert das interne Straßenverzeichnis rollen- und gebietsbezogen.

## Spätere Objekt- und Hausnummernzuordnung

Die Reihenfolge ist: Verwaltungseinheit → Straße → Flur → Flurstück → Gebäudeobjekt → Eingang → Hausnummer. Eine Hausnummer darf erst vergeben werden, wenn das Gebäude einem Flurstück und einer Straße zugeordnet ist. Gerade und ungerade Nummern werden getrennt nach Straßenseite vorgeschlagen.

## Mehrere Eigentümer

Ein Flurstück kann mehrere aktive Eigentümerdatensätze besitzen. Jeder Eintrag enthält Name, geschützte Anschrift, interne Registerreferenz, Anteil und Quelldokument. Die Summe darf 100 Prozent nicht überschreiten. Eigentümerdaten sind als `PROTECTED_INTERNAL` klassifiziert, erscheinen nie in öffentlichen Karten oder Adresssuchen und jeder Abruf wird protokolliert.
