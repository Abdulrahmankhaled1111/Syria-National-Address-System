# Abgeschotteter Offline-Betrieb

## Betriebsmodell

Das System kann in einem staatlichen Behördennetz ohne Verbindung zum
öffentlichen Internet betrieben werden. Browser verbinden sich ausschließlich
mit dem internen Gateway. Die Anwendung benötigt im laufenden Betrieb keine
CDNs für Programmcode; MapLibre, Styles, Logos und Fachgeometrien liegen lokal.
Externe Straßen- oder Satellitenkacheln sind im abgeschotteten Netz nicht
verfügbar. Dort wird die lokale Katasterdarstellung verwendet, bis ein
staatlicher Tile-Server mit genehmigten Daten angeschlossen ist.

Offline bedeutet hier nicht, dass jeder Browser eigenständig amtliche Daten
ändern darf. Schreibvorgänge benötigen immer einen erreichbaren lokalen
Behördenserver, damit Rollen, Vier-Augen-Prinzip, Konfliktprüfung, Signaturen und
Auditkette wirksam bleiben. Der Service Worker speichert nur Programmdateien und
öffentliche Geodaten. Geschützte API-Antworten, Tokens, Eigentümer- und
Auditdaten werden nicht im Browsercache abgelegt.

## Vertrauenswürdige Übergabe

1. Auf einer geprüften Build-Station müssen Docker und die drei freigegebenen
   Basisimages vorhanden sein.
2. `scripts/build_offline_bundle.ps1` erzeugt Images, Konfigurationen und eine
   SHA-256-Dateiliste in `output/offline-release`.
3. Das Paket wird auf einem kontrollierten Datenträger transportiert, durch
   zwei verantwortliche Personen registriert und auf Malware geprüft.
4. Auf dem Zielserver verifiziert `sha256sum -c SHA256SUMS.txt` jede Datei.
5. Geheimnisse und TLS-Schlüssel werden erst im Behördennetz eingefügt und
   niemals in das Transportpaket oder Git geschrieben.

## Voraussetzungen des Zielservers

- gehärtetes, unterstütztes Linux mit Secure Boot und verschlüsselten
  Datenträgern;
- Docker Engine mit Compose-Plugin aus einer staatlich gepflegten Paketquelle;
- mindestens zwei getrennte Netzschnittstellen oder VLANs für Nutzerzugang und
  Registerbetrieb;
- interne DNS-Auflösung und Zertifikate einer Behörden-PKI;
- getrennte Betriebs-, Backup- und Sicherheitskonten;
- Zeitsynchronisation aus einer internen vertrauenswürdigen Quelle;
- Weiterleitung unveränderbarer Logs an ein getrenntes SOC/SIEM.

## Installation

```sh
cp deploy/.env.offline.example .env
chmod 600 .env
# Werte mit staatlich freigegebenen Zufallswerten ersetzen.
mkdir -p deploy/tls
# fullchain.pem und private-key.pem aus der Behörden-PKI einfügen.
chmod 600 deploy/tls/private-key.pem
sh scripts/install_offline.sh
```

Das Skript bricht bei einer falschen Prüfsumme, fehlender Konfiguration oder
fehlenden TLS-Dateien ab. Der PostgreSQL-Dienst liegt ausschließlich im
internen Container-Netz und veröffentlicht keinen Host-Port.

## Karten im vollständig getrennten Netz

Für eine mit Geoportal.de vergleichbare Basiskarte wird zusätzlich ein eigener
Tile- und OGC-Dienst benötigt. Empfohlene Komponenten sind eine geprüfte
PostGIS-Replik, Martin/MapServer oder GeoServer und lokal erzeugte Vector Tiles.
Satellitenbilder dürfen erst nach Klärung von Lizenz, Aktualität, Staatsgrenze
und militärischen Schutzanforderungen übernommen werden. URLs öffentlicher
Kartenanbieter sind kein Bestandteil des souveränen Zielbetriebs.

## Sicherung und Wiederanlauf

- tägliche verschlüsselte Sicherung, stündliche WAL-/Änderungssicherung nach
  festgelegtem RPO und mindestens eine unveränderbare/offline Kopie;
- Sicherungsidentitäten dürfen keine Produktionsadministratoren sein;
- monatlicher automatischer Restore in eine isolierte Umgebung;
- halbjährliche vollständige Wiederanlaufübung von Standort B;
- dokumentierte Prüfsummen, Aufbewahrung, Vernichtung und Vier-Augen-Freigabe.

## Noch blockierende Produktionspunkte

Das Offline-Paket ist eine Deployment-Vorbereitung, keine staatliche
Produktionsfreigabe. Vor realem Betrieb müssen insbesondere der aktive
SQLite-Anwendungsadapter durch PostgreSQL/PostGIS ersetzt, ein staatlicher
OIDC-/MFA-Dienst angeschlossen, HSM-Signaturen implementiert, reale Daten
amtlich bestätigt sowie Penetrations-, Datenschutz-, Failover- und Restore-
Abnahmen abgeschlossen werden. Maßgeblich bleibt
`deploy/PRODUCTION-READINESS.md`.
