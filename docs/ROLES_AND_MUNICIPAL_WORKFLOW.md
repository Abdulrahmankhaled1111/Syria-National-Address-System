# Rollen und Gemeindeprozess v0.1

| Rolle | Darf erfassen | Darf prüfen | Darf genehmigen | Druck/Schilder | Montage | Audit |
|---|---:|---:|---:|---:|---:|---:|
| Bürger/Melder | Hinweise | nein | nein | nein | nein | eigene Meldung |
| Gemeindeerfasser | Adressen/Gebäudeentwurf | nein | nein | Auftrag vorschlagen | nein | eigene Vorgänge |
| Vermesser | Geometrie/Qualität | fachliche Messprüfung | nein | nein | nein | eigene Vorgänge |
| Prüfer | Korrekturen zurückgeben | ja | nein | nein | Montage prüfen | Fachvorgänge |
| Genehmiger | nein | geprüfte Fälle | ja | Auftrag freigeben | nein | Genehmigungen |
| Druck-/Schilderstelle | nein | Produktionsdaten | nein | ja | nein | eigene Aufträge |
| Montageteam | nein | Auftrag/Adresse | nein | nein | GPS, Foto, Zeit | eigene Aufträge |
| Auditor | nein | nein | nein | nein | nein | vollständig, nur lesend |
| Systemadministrator | Technik, nicht Fachentscheid | nein | nur Notfall im Pilot | Technik | Technik | technischer Zugriff |

Produktiv dürfen Systemadministratoren keine fachlichen Genehmigungen erteilen. Der Pilot erlaubt dies ausschließlich für Tests und kennzeichnet es im Auditlog.

## Durchgängiger Vorgang

```text
Erfassung → Prüfung → Genehmigung → Dorfplan/Brief → Schildproduktion
→ Montage mit GPS und Foto → kommunale Verifikation → amtlich montiert
```

Jede Personalzuordnung ist an Organisation, Verwaltungsgebiet und Gültigkeitszeitraum gebunden. Ein Gemeindemitarbeiter darf somit nicht automatisch Daten einer anderen Gemeinde bearbeiten.

## Geplante Druckprodukte

- Dorfübersichtsplan mit Straßen, Gebäuden, Eingängen und Hausnummern
- straßenweise Montageliste
- offizieller Adressbescheid/Benachrichtigungsbrief
- Schildproduktionsdatei mit arabischem Namen, Hausnummer, Postleitzahl und QR-Prüfcode
- Montageauftrag mit Route
- Abschlussprotokoll mit Foto, Position, Zeit und ausführender Person
