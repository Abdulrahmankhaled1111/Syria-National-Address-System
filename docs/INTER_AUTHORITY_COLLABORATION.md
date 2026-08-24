# Zusammenarbeit der Bauämter

## Arbeitsprinzip

Jede Behörde arbeitet innerhalb ihres zugewiesenen Verwaltungsgebiets. Muss ein
Fall von einer anderen Stelle geprüft oder bearbeitet werden, wird kein
uneingeschränkter Datenzugriff vergeben. Stattdessen entsteht eine
nachvollziehbare Behördenübergabe mit absendender Stelle, empfangender Stelle,
Zielrolle, Vorgangsart, Priorität, Frist und Arbeitsauftrag.

```text
OPEN → ACCEPTED → IN_PROGRESS → COMPLETED
  └──────────────→ RETURNED ──────────────┘
```

Abschluss und Rückgabe benötigen ein dokumentiertes Ergebnis. Jede Transition
wird in der Auditkette festgehalten. Beschäftigte sehen nur Vorgänge, deren
Quell- oder Zielbehörde in ihrem zugewiesenen Gebiet liegt. Nationale
Systemadministratoren besitzen technische Gesamtsicht, dürfen im Zielbetrieb
aber keine fachliche Entscheidung ersetzen.

## Unterstützte Vorgangsarten

- Baugenehmigung und behördenübergreifende Beteiligung,
- Grenz- und Vermessungsprüfung,
- Adress- und Hausnummernvergabe,
- Datenkorrektur,
- unabhängige fachliche Prüfung,
- allgemeine Koordination.

## Arbeitszentrale Bestandsdaten

Die Seite zeigt Zuständigkeitsbereich, offene Übergaben, fällige Fristen, hohe
Prioritäten und abgeschlossene Vorgänge. Der gemeinsame Posteingang stellt
Route, Zielrolle, Frist, Priorität und Status dar. Berechtigte Rollen können
neue Übergaben erstellen, annehmen, beginnen, mit Ergebnis abschließen oder mit
Begründung zurückgeben.

## Weitere Pflichtausbaustufen

Vor einem landesweiten Einsatz folgen Vertretungsregeln, Eskalationsfristen,
Anlagen mit Virenprüfung, qualifizierte Behörden-Signaturen, Benachrichtigungen,
Konflikterkennung für parallele Geometrieänderungen, organisationsbezogene
Leistungskennzahlen sowie eine kontrollierte Offline-Synchronisation signierter
Änderungspakete. Personen- und Eigentümerdaten dürfen nicht in allgemeinen
Koordinationsbeschreibungen stehen.
