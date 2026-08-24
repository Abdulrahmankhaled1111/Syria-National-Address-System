# Landesweiter Syrien-Import

Quelle: Geofabrik/OpenStreetMap-Landesauszug, ODbL 1.0. Importdatum und Quellzeitpunkt stehen in `data/national/syria_catalog.sqlite`.

Importierter Arbeitsbestand:

- 343.671 Straßen- und Wegobjekte;
- 1.368.050 Gebäudeobjekte;
- 10.323 Ortsobjekte.

Der unveränderte PBF-Auszug bleibt als Quellsnapshot erhalten. Der kompakte SQLite-Index speichert Objektkennung, Namen, Typ, repräsentative Koordinate und Begrenzungsrahmen. In der produktiven PostGIS-Stufe werden zusätzlich vollständige Geometrien importiert und räumlich indiziert.

Alle Objekte besitzen zunächst `OPEN_DATA_UNVERIFIED` und Qualitätsstufe D. Der Import behauptet nicht, dass die Quelle vollständig oder amtlich ist.

Die öffentliche Suche findet landesweit:

- arabische, englische und sonstige vorhandene Straßennamen;
- amtliche, alternative, lokale, kurze und frühere Namen, soweit sie in der Quelle vorhanden sind;
- Straßennummern/Referenzen;
- Städte, Dörfer und Ortsteile;
- technische Gebäudeobjektkennungen.

Die Hausnummernvergabe ist serverseitig weiterhin auf die Verwaltungseinheit Maskanah (`au-mas`) beschränkt. Weitere Gemeinden werden erst nach erfolgreicher Pilotabnahme freigeschaltet.
