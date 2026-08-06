# Postleitzahlenkonzept v0.1

Status: Pilotvorschlag, noch durch syrische Post, Kommunen und staatliche Stellen zu bestätigen.

## Empfehlung

Eine Postleitzahl ist kein Gebäude- und kein Adresskennzeichen. Sie bezeichnet ein Zustellgebiet. Eine Stadt erhält deshalb nicht zwingend nur eine Nummer: Große Städte besitzen mehrere Zustellgebiete; ein Zustellgebiet kann bei dünner Besiedlung mehrere Orte umfassen.

Für den Pilot wird ein festes sechs-stelliges, rein numerisches Format verwendet:

```text
GG SS ZZ
│  │  └─ Zustellzone (00-99)
│  └──── Postsektor (00-99)
└─────── regionale Leitkennzahl/Gouvernoratsgruppe (01-99)
```

Beispiel: `01 01 01` beziehungsweise maschinenlesbar `010101`.

Die erste Stufe dient dem nationalen Routing, die zweite dem Sortier-/Zustellsektor und die dritte dem örtlichen Zustellgebiet. Die endgültige Zuordnung darf erst nach Analyse von Bevölkerung, Straßennetz, Poststandorten, Zustellmengen und erwarteter Stadtentwicklung erfolgen.

## Wichtige Regeln

- In Datenbanken und APIs immer die Ziffern `0-9` speichern.
- Die arabische Oberfläche darf dieselbe Zahl optional als arabisch-indische Ziffern darstellen.
- Führende Nullen bleiben erhalten; Postleitzahlen sind Text, keine Rechenzahlen.
- Keine Personen-, Eigentümer-, Sicherheits- oder Gebäudedaten in die Nummer kodieren.
- Postgebietsgrenzen werden als eigene versionierte Geometrien geführt.
- Bei Verwaltungsgrenzänderungen muss eine Postleitzahl nicht automatisch geändert werden.
- Alte Codes bleiben mit Gültigkeitszeitraum und Nachfolger nachvollziehbar.
- Gebäude und Eingänge behalten ihre dauerhaften IDs, auch wenn sich die Postleitzahl ändert.

## Sprachen

Die Bedienoberfläche ist auf Arabisch, Englisch und Deutsch verfügbar. Arabisch ist die vorgeschlagene amtliche Standardsprache. Englische Transliteration unterstützt internationale Zusammenarbeit. Deutsch ist eine Bedien- und Schulungssprache, aber keine zusätzliche amtliche Schreibweise syrischer Ortsnamen.
