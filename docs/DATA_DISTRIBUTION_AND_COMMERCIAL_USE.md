# Datenbereitstellung für Post, Rettungsdienste und Kartendienste

## Öffentlicher Export

Die Plattform stellt ausschließlich freigegebene amtliche Adressen als GeoJSON bereit:

```text
GET /api/v1/exports/addresses.geojson
```

Enthalten sind Adress-ID, formatierte Adresse, Hausnummer, Postleitzahl, Eingangspunkt, Koordinate, Qualität und Status. Eigentümer, Bewohner, Telefonnummern, Dokumente und interne Sicherheitsangaben werden niemals in diesen Export aufgenommen.

## Google Maps

Staatliche oder kommunale Stellen mit hochwertigen Daten und den erforderlichen Weitergaberechten können sich als Google Maps Content Partner bewerben. Das Portal akzeptiert unter anderem Straßen, Adressen, Postleitzahlen und Verwaltungsgrenzen. Eine Aufnahme ist eine Entscheidung von Google und wird nicht durch unseren Export garantiert.

Der vorbereitete Endpunkt:

```text
GET /api/v1/exports/google-content-partner.geojson
```

liefert nur freigegebene Adressen. Vor Übermittlung müssen Format, Rechte, ODbL-Abhängigkeiten und Google-Inhaltsanforderungen geprüft werden. Importierte OpenStreetMap-Geometrien werden nicht automatisch als eigene amtliche Daten weiterverkauft.

## Syrische Post

Technisch sind mehrere Modelle möglich:

- staatlicher Datenaustausch auf gesetzlicher Grundlage;
- Lizenzvertrag für laufend aktualisierte Qualitätsdaten;
- kostenpflichtige API mit Verfügbarkeits- und Aktualitätsgarantie;
- gemeinsame Finanzierung der Erfassung und Pflege.

Ob ein Verkauf zulässig und sinnvoll ist, entscheiden Eigentümer des Registers, syrische Post, zuständige Ministerien und Rechtsberater. Jede Auslieferung erhält Empfänger, Rechtsgrundlage, Filter, Datensatzanzahl, Prüfsumme, Freigabe und Zeitpunkt.

## Objektakten

Jede importierte Straße und jedes Gebäude besitzt eine dauerhafte Objektakte mit:

- Aktennummer;
- Objektart und Objektkennung;
- zuständiger Verwaltungseinheit;
- Quelle und Qualitätsstufe;
- aktuellem Prüfstatus;
- Hausnummernvorgängen;
- Änderungs- und Auditverlauf.

Dadurch bleiben Informationen in der Datenbank erhalten, auch wenn Namen, Hausnummern oder externe Kartendienste später geändert werden.
