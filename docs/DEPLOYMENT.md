# Deployment- und Betriebskonzept

## Pilot

Docker Compose startet Webdienst und PostGIS. Der Webdienst verwendet für die sofortige lokale Demonstration eine eigene SQLite-Pilotdatenbank; PostGIS wird parallel mit dem verbindlichen Zielschema initialisiert. Die nächste Integrationsstufe ersetzt den Demo-Adapter durch einen PostGIS-Repository-Adapter, ohne API oder Fachmodell zu ändern.

## Produktionsnahe Stufe

- reproduzierbare, signierte Container in privater Registry;
- Kubernetes oder eine vergleichbare Plattform nur mit belastbarem Betriebsteam;
- PostgreSQL/PostGIS als gehärteter, hochverfügbarer Datenbankdienst außerhalb öffentlicher Netze;
- migrationsgesteuerte Releases mit Staging, Abnahme, Rollback und Vier-Augen-Freigabe;
- OpenTelemetry/Monitoring, zentrales SIEM und Alarmbereitschaft;
- MapLibre im Client; GeoServer/MapServer nur für fachlich benötigte OGC-Dienste;
- OpenSearch für skalierte Suche, sobald der Pilotbedarf PostgreSQL-Suche übersteigt.

Konfiguration und Geheimnisse werden nicht in Images oder Git gespeichert. Vor jedem Release: Migrationstest, automatisierte Tests, Restore-Test, Schwachstellenscan, Datenschutzprüfung und fachliche Stichprobe.
