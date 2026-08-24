# Syrisches nationales Adress- und Geoinformationssystem – Production Candidate v0.19

Lauffähiges MVP für einen fachlich kontrollierten Adress- und Geodatenbestand. Enthalten sind dreisprachige öffentliche Suche und Verwaltung (Arabisch, Englisch, Deutsch), vereinfachte Kartenansicht, Postgebiete, Rollen, Änderungs-/Freigabeworkflow, Historisierungskonzept, verkettetes Auditlog, PostGIS-Schema, Pilotdaten, Tests, Backup/Restore und Betriebsdokumentation.

> Dies ist ein professioneller Pilot, kein rechtsverbindliches Kataster und keine behauptete landesweite Produktionsplattform.

Der vollständige, auf dieses Repository zugeschnittene Zielzustand für
Datenhoheit, Registertrennung, drei Rechenzentrumsstandorte, HSM/MFA,
Fortführungsworkflow, SOC, Backups und stufenweisen nationalen Rollout steht in
[`docs/NATIONAL_SYSTEM_BLUEPRINT.md`](docs/NATIONAL_SYSTEM_BLUEPRINT.md).

Für Behördennetze ohne Internetzugang enthält das Projekt außerdem eine
installierbare Offline-Webanwendung, ein Air-Gap-Containerpaket mit Prüfsummen
und eine getrennte Server-Installationsstrecke. Betriebsgrenzen und Übergabe:
[`docs/AIR_GAPPED_OPERATION.md`](docs/AIR_GAPPED_OPERATION.md).

## Isolierter Mitarbeiter-Assistent

Das Verwaltungsportal enthält einen dreisprachigen, lokalen Beratungsassistenten
für Arbeitsabläufe, Kataster, Adressierung, Rollen, Datenqualität, Sicherheit
und Offline-Betrieb. Er ist nur nach Mitarbeiter-Anmeldung verfügbar und nennt
die verwendeten internen Dokumente. Sein separates Wissensmodul besitzt keinen
Datenbank-, Netzwerk-, Datei- oder Aktionszugriff. Es kann daher keine Vorgänge
erstellen, verändern, genehmigen, löschen oder exportieren. Architektur und
Pflegeprozess: [`docs/STAFF_ASSISTANT.md`](docs/STAFF_ASSISTANT.md).

## Produktionsmodus

Version 0.17 führt einen abgesicherten Produktionsmodus ein. Er verweigert den
Start bei schwachem Signaturschlüssel, fehlender Host-Freigabe, ungeeigneter
Sitzungsdauer oder fehlendem Bootstrap-Administratorkennwort. Eine leere
Produktionsdatenbank erhält ausschließlich einen mit scrypt geschützten
Bootstrap-Administrator und niemals die dokumentierten Demokonten.

Zusätzlich enthalten sind:

- Login-Sperre nach wiederholten Fehlversuchen,
- zeitlich begrenzte signierte Sitzungen,
- Host-Header-Prüfung und strenge Browser-Sicherheitsheader,
- TLS-Reverse-Proxy-Konfiguration,
- Container ohne Root-Rechte und ohne Linux-Capabilities,
- maschinenlesbare Bereitschafts- und Auditkettenprüfung,
- konsistente Backups mit SHA-256-Manifest und Integritätsprüfung,
- strukturierte Protokolle mit Request-ID,
- gesondertes Werkzeug zur sicheren Benutzerbereitstellung.

Der Production-Readiness-Gate bleibt absichtlich geschlossen, solange der
Anwendungsadapter noch SQLite statt PostgreSQL/PostGIS verwendet, Demokonten
aktiv sind oder fachliche Daten nicht staatlich bestätigt wurden. Details:
`deploy/PRODUCTION-READINESS.md`.

Das bereitgestellte syrische Emblem wird ohne weißen Bildhintergrund einheitlich
in der öffentlichen Kartenplattform, im Verwaltungsportal und in den
PDF-Objektakten verwendet.

## Nummerierungsgebiet Maskanah

Der aktuelle kommunale Arbeitsbestand enthält 320 Straßenobjekte und 172
Gebäudeobjekte. Für alle 172 derzeit erfassten Gebäude wurde ein
nachvollziehbarer Hausnummernvorschlag gespeichert. Die Zuordnung verwendet die
nächstgelegene Straße, die Reihenfolge entlang des Straßenverlaufs und getrennte
gerade/ungerade Straßenseiten. Der Lauf ist als `MUNICIPAL_REVIEW` gespeichert.
Erst Prüfung und Genehmigung durch die zuständigen Rollen erzeugen eine amtliche
Adresse.

Beim Auswählen eines Gebäudes lädt die Verwaltungsoberfläche automatisch
Straßenzuordnung, nächste freie gerade/ungerade Hausnummer und die kombinierte
Anzeige `010101 Maskanah`. Neue Gebäude werden bei einem erneuten Lauf
inkrementell ergänzt; bestehende Vorschläge werden nicht neu nummeriert.

Der mobile Außendienst kann über die iPad-Kamera ein Nachweisfoto aufnehmen.
Zusammen mit GPS, Gerätezeit und der Bestätigung für Hausnummernschild und
Briefkasten wird der Einbau dauerhaft gespeichert. Danach folgen Prüfung und
Genehmigung. Die Außendienstrolle kann deaktiviert werden, ohne Datensätze oder
Auditnachweise zu entfernen.

Die Tabelle `staff_admin_scopes` ermöglicht einem Rathaus die Zuständigkeit für
mehrere festgelegte Orte. Bearbeitungen außerhalb dieser Gebiete werden
abgelehnt. Das Postleitzahlregister speichert Code und Ortsnamen getrennt in
Arabisch, Englisch und Deutsch.

Erneute, idempotente Erzeugung:

```powershell
python scripts/assign_maskanah_numbers.py --db pilot.db
```

## Satelliten- und 3D-Karte

Die öffentliche Karte verwendet MapLibre/WebGL und bietet Straßenkarte,
Satellitenbild sowie eine neig- und drehbare 3D-Gebäudeansicht. In Maskanah
werden die 172 vorhandenen Gebäudegrundrisse extrudiert und bleiben anklickbar.
Solange keine amtliche Gebäudehöhe oder Geschosszahl vorliegt, verwendet die
Darstellung sichtbar eine vorläufige Höhe von 9 Metern. Satellitenbilder werden
mit der vorgeschriebenen Quellenangabe von Esri und dessen Datenlieferanten
angezeigt. Für einen souveränen Produktionsbetrieb ist später ein eigener
staatlicher Bild- und Kacheldienst vorgesehen.

Die syrische Staatsgrenze wird als separate, kontrastreiche Vektorebene
oberhalb von Straßen-, Satelliten- und 3D-Ebenen dargestellt. Die lokale
Grenzgeometrie stammt aus geoBoundaries `SYR-ADM0-73488105` (Datensatzjahr
2017, ODbL 1.0, Quelle OpenStreetMap/Wambacher). Sie dient der Kartendarstellung
und ersetzt keine staatlich festgestellte Rechtsgrenze.

## Schnellstart ohne Installation

Voraussetzung: Python 3.11 oder neuer.

```powershell
cd pilot
python app/server.py
```

Dann öffnen:

- Öffentliche Suche: `http://127.0.0.1:8080`
- Verwaltung: `http://127.0.0.1:8080/admin`
- Gesundheitsprüfung: `http://127.0.0.1:8080/health`

Die lokale Demo-Datenbank wird beim ersten Start erzeugt. Zurücksetzen:

```powershell
python app/server.py --reset-db --init-db
```

## PDF-Objektakte

Jeder Treffer in der öffentlichen Suche hat die Schaltfläche
`PDF-Objektakte herunterladen`. Die einseitige, druckfähige PDF enthält die
öffentlichen Kerndaten, Koordinaten, Qualitäts- und Freigabestatus sowie einen
QR-Prüfwert. Eigentümer- und Bewohnerdaten werden nicht in öffentliche PDFs
aufgenommen. Nur ein Datensatz mit Status `OFFICIAL` und Freigabe der zuständigen
Stelle ist rechtsverbindlich.

## Docker-Start

Docker Desktop muss laufen:

```powershell
Copy-Item .env.example .env
# Werte in .env durch lange Zufallswerte ersetzen
docker compose up --build
```

Compose startet den Pilotdienst und initialisiert PostgreSQL 16/PostGIS mit dem Zielschema. Die unmittelbar nutzbare Demo verwendet bewusst den eingebauten lokalen Adapter; die PostGIS-Migrationen bilden das verbindliche Datenmodell für die folgende Integrationsstufe.

## Pilotkonten

| Rolle | Benutzer | Passwort |
|---|---|---|
| Editor | `editor` | `Editor123!` |
| Prüfer | `reviewer` | `Review123!` |
| Genehmiger | `approver` | `Approve123!` |
| Auditor | `auditor` | `Audit123!` |
| Admin | `admin` | `Admin123!` |
| Vermessung | `surveyor` | `Survey123!` |
| Druck/Schilder | `printoffice` | `Print123!` |
| Montageteam | `installer` | `Install123!` |
| Rathaus Maskanah | `maskanah.editor` | `Maskanah123!` |
| Vermessung Maskanah | `maskanah.surveyor` | `MaskSurvey123!` |
| Prüfung Maskanah | `maskanah.reviewer` | `MaskReview123!` |
| Genehmigung Maskanah | `maskanah.approver` | `MaskApprove123!` |
| Außendienst Maskanah | `maskanah.installer` | `MaskInstall123!` |

Diese Zugangsdaten sind öffentlich dokumentierte Testwerte und dürfen nie in Produktion verwendet werden.

## API-Kern

- `GET /api/v1/addresses?q=...` – öffentliche GeoJSON-Suche
- `GET /api/v1/addresses/{id}` – Adressdetail
- `POST /api/v1/auth/login` – Pilot-Anmeldung
- `GET|POST /api/v1/change-requests` – Vorgänge
- `POST /api/v1/change-requests/{id}/review|approve|reject` – Workflow
- `GET /api/v1/audit` – nur Auditor/Admin
- `GET|POST /api/v1/field-jobs` – Dorfpläne, Briefe, Schilder und Montage
- `POST /api/v1/field-jobs/{id}/produce|ready|install|verify` – rollenbasierter Außendienstprozess
- `GET /api/v1/map/maskanah/buildings` – 172 ungeprüfte Gebäudeobjekte
- `GET|POST /api/v1/house-number-cases` – kontrollierte Hausnummernvergabe
- `POST /api/v1/house-number-cases/{id}/review|approve|reject` – Prüfung und Veröffentlichung
- `GET /api/v1/catalog/search?q=...` – Suche über Straßen, Gebäude, Aktennummern und Adressen
- `GET /api/v1/objects/{ROAD|BUILDING}/{id}` – dauerhafte Objektakte
- `GET /api/v1/exports/addresses.geojson` – freigegebener öffentlicher Datenaustausch
- `GET /api/v1/national/statistics` – landesweiter Importstatus
- `GET /api/v1/national/objects/{ROAD|BUILDING|PLACE}/{id}` – nationales Arbeitsobjekt

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Datensicherung

Mit laufendem Compose-Stack:

```powershell
docker compose --profile operations run --rm backup
```

Restore ist absichtlich nicht automatisch. Prüfsumme, exaktes Ziel und ausdrückliche Variable `CONFIRM_RESTORE=YES` sind erforderlich. Wiederherstellungen zuerst in isolierter Umgebung testen.

## Projektstruktur

```text
app/                 API und Weboberflächen
db/migrations/       PostgreSQL/PostGIS-Schema, Rollen, Pilotdaten
docs/                Architektur, Objektkatalog, ERD, Sicherheit, Deployment
scripts/             Backup und Restore
tests/               automatisierte API-/Workflow-Tests
docker-compose.yml   reproduzierbarer Pilot-Stack
```

## Fachliche Entscheidungen

- Adresse, Gebäude, Eingang und Grundstück sind getrennte Objekte.
- Arabische Namen sind Pflicht; weitere Sprachformen werden separat geführt.
- Eindeutige UUID plus lesbare nationale Kennung.
- Quelle und Qualitätsstufe A–E sind Teil jedes relevanten Objekts.
- Postleitzahlen bezeichnen versionierte Zustellgebiete und bleiben von Adress-/Gebäude-IDs getrennt.
- Alte Stände werden nicht überschrieben, sondern zeitlich versioniert.
- Amtliche Änderungen durchlaufen Antrag, Prüfung, Genehmigung und Publikation.
- Öffentliche Adressen enthalten keine Eigentümer- oder Bewohnerdaten.

Die Grundlagen stammen aus den im Projektgespräch ausgewerteten ALKIS-Prinzipien, wurden aber auf ein modernes syrisches Modell angepasst. Das ursprünglich erwähnte PDF lag in dieser lokalen Projektkopie nicht vor; daher enthält der Katalog keine ungeprüften Seitenzitate und muss vor Rechtswirkung mit dem Original sowie syrischen Fachstellen abgeglichen werden.

## Nächste Stufe

1. Fachliche Workshops mit syrischen Kataster-, Kommunal-, Post-, Rettungs-, Rechts- und Sprachfachleuten.
2. Verbindliche Verwaltungsstruktur, Kennungssystematik, Transliteration und nationales Koordinatenreferenzsystem.
3. PostGIS-Adapter, OIDC/MFA, signierte Genehmigungen und echte Kartenkacheln.
4. Offline-Erfassungs-App und Datenqualitätsdashboard.
5. Pilot in vier kontrastierenden Gebieten, Sicherheitsprüfung und Restore-Übung.
6. Erst nach messbarer Pilotabnahme schrittweiser nationaler Rollout.
