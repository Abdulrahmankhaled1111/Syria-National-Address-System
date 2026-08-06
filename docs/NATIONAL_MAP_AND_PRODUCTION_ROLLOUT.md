# Landeskarte und Weg zum Produktionsbetrieb

## Stand v0.5

Die Anwendung besitzt eine landesweite interaktive Syrien-Karte mit Zoomen, Verschieben, Kartenklick, Koordinatenanzeige, Ebenenschalter, Adresssuche, Hausnummernebene und dem detaillierteren Maskanah-Arbeitsbestand.

Für die lokale Demonstration werden nur die vom Menschen aktuell betrachteten Standardkacheln von OpenStreetMap geladen. Es erfolgt kein Vorabladen und kein Massendownload. Die sichtbare Attribution bleibt erhalten.

## Produktionsbetrieb

Die öffentlichen OSM-Kachelserver bieten keine Verfügbarkeitsgarantie und sind nicht für den landesweiten staatlichen Produktivbetrieb vorgesehen. Der syrische Zielbetrieb benötigt:

- staatlich kontrollierte Vektor-Kachelserver;
- einen regelmäßig aktualisierten, lizenzkonformen OSM-Basisdatenbestand;
- getrennte amtliche Overlays für Adressen, Hausnummern, Gebäude, Eingänge und Verwaltungsgrenzen;
- eigenen Geocoding- und Routingdienst;
- Kachelcache und regional redundante Bereitstellung;
- Offline-Pakete ausschließlich aus eigenen oder ausdrücklich dafür lizenzierten Quellen;
- arabischen Kartenstil sowie englische und deutsche Bedienoberflächen.

## Keine erfundenen amtlichen Daten

Eine Basiskarte zeigt Straßen, ersetzt aber keine amtliche Erfassung. Hausnummern werden pro Gemeinde nach Feldprüfung, Beschluss und Freigabe publiziert. Bis dahin zeigt die Plattform nur den jeweiligen Qualitäts- und Prüfstatus.

## Stufenplan

1. Verbindliche Staats-/Gouvernorats-/Gemeindegrenzen importieren.
2. Jede Gemeinde als eigene Organisation und Zuständigkeit anlegen.
3. Offene Straßen als Arbeitsbestand importieren.
4. Kommunale Feldteams bestätigen Straßen, Namen, Gebäude und Eingänge.
5. Hausnummernplanung und öffentliche Anhörung durchführen.
6. Genehmigen, Bescheide drucken, Schilder produzieren und Montage nachweisen.
7. Provinzweise Abnahme; erst danach national veröffentlichen.

Die Softwarebasis kann landesweit sein, während der amtliche Datenbestand kontrolliert Gemeinde für Gemeinde wächst.
