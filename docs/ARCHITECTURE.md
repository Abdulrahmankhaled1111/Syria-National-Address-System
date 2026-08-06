# Architektur des syrischen Adress- und Geodatenpiloten

## Zweck und Grenze

Der Pilot beweist Fachmodell, Benutzerwege und Sicherheitsprinzipien für ein begrenztes Gebiet in Damaskus. Er ist weder ein produktives Kataster noch eine rechtsverbindliche landesweite Plattform. Vor einem Produktivbetrieb sind syrisches Recht, amtliche Zuständigkeiten, Verwaltungskennungen, Transliteration, Vermessungsregeln, Datenschutz und Bedrohungsmodell verbindlich festzulegen.

## Leitprinzipien

- Fachlich zentral: ein nationaler Objektkatalog und einheitliche Kennungen.
- Organisatorisch verteilt: Gemeinden erfassen, unabhängige Stellen prüfen und genehmigen.
- Technisch redundant: zwei Betriebsstandorte und ein logisch getrenntes, unveränderbares Backup.
- Registertrennung: öffentliche Adresse, internes Kataster und besonders geschütztes Rechts-/Eigentumsregister bleiben getrennte Sicherheitsdomänen.
- Keine direkte Bestandsänderung: Bearbeitung erfolgt ausschließlich über Änderungsanträge.
- Nachvollziehbarkeit: Versionen, Quelle, Qualität und verkettete Auditereignisse.

## Komponenten

```text
Browser / mobile Erfassung
          |
   Reverse Proxy, WAF, Rate Limits
          |
  Public API       Behördenportal
          |             |
          +--- Fach- und Workflowdienst
                         |
        +----------------+----------------+
        |                |                |
 Adressregister   Katasterregister   Audit/SIEM
 PostgreSQL       PostGIS             append-only
        |
 Karten-/OGC-Dienste und kontrollierte Exporte
```

Der Pilot fasst API und statische Oberfläche in einem kleinen Dienst zusammen. In der Skalierungsstufe werden öffentliche API, Behördenportal, Workflow, Identität, Geocoding und Kartenbereitstellung getrennt, ohne das Fachmodell zu ändern.

## Datenfluss einer Fortführung

1. Editor legt einen Antrag mit Quelle und Begründung an.
2. Automatische Regeln prüfen Pflichtfelder, Geometrie, Kennungen und Konflikte.
3. Reviewer verifiziert Fachlichkeit und Quelldokumente.
4. Eine andere Person mit Approver-Rolle genehmigt.
5. Ein Publikationsdienst erzeugt eine neue Objektversion; der alte Stand erhält `valid_to`.
6. Das Ereignis wird signiert, unveränderbar protokolliert und an berechtigte Abnehmer verteilt.

## Zielbetrieb

- Standort A: aktiver Betrieb in einem staatlich kontrollierten syrischen Rechenzentrum.
- Standort B: räumlich und netztechnisch getrennter Warm-Standby.
- Standort C: verschlüsselte, unveränderbare/offline Sicherungen.
- RPO-Ziel nach Schutzbedarfsanalyse, anfänglich höchstens 15 Minuten für Registeränderungen.
- RTO-Ziel anfänglich 4 Stunden; halbjährliche Wiederanlaufübung.
- HSM für Zertifikats- und Signaturschlüssel; zeitlich begrenzte privilegierte Zugriffe.

## Skalierungspfad

Pilotgebiet → mehrere kontrastierende Pilotgebiete → Provinzbetrieb → nationaler Rollout. Jede Stufe benötigt formale Abnahme von Datenqualität, Wiederherstellung, Sicherheit, Betrieb und Nutzerprozessen.
