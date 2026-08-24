# Isolierter Mitarbeiter-Assistent

## Zweck

Der Assistent beantwortet häufige fachliche und betriebliche Fragen auf
Arabisch, Englisch und Deutsch. Er unterstützt Beschäftigte bei Adressierung,
Kataster, Rollen, Freigabeworkflow, Datenqualität, Sicherheit und Offline-
Betrieb. Antworten sind Beratungshilfen und keine amtlichen Entscheidungen.

Die Wissensbasis `2026.08.2` deckt zusätzlich Anmeldung und Profil, Navigation,
Aufgaben und Benachrichtigungen, Karten und Suche, Flur-/Flurstückserfassung,
Gebäude und Außendienst, PDF/GeoJSON/KML/CSV-Exporte, Backup und Restore,
Systemeinstellungen, Support sowie den tatsächlichen Produktionsstatus ab.
Unbekannte Fragen erhalten eine Systemübersicht statt einer erfundenen
Detailantwort. Jede Antwort liefert Themenkennung, Quellen, Wissensversion und
den technischen Isolationsstatus.

## Technische Sicherheitsgrenze

```text
Mitarbeiter-Browser
       |
       | authentifizierte Frage, Sprache
       v
API-Gateway /api/v1/assistant/query
       |
       v
assistant_service.py
  - statische kuratierte Wissensartikel
  - keine Datenbankverbindung
  - kein Datei- oder Dokumentzugriff zur Laufzeit
  - kein Netzwerkzugriff
  - keine Werkzeuge oder Systemaktionen
       |
       v
Antwort + Quellenbezeichnungen + Isolationsstatus
```

Die API prüft lediglich, ob ein aktives Mitarbeiterkonto vorhanden ist. Weder
Frage noch Antwort werden durch den Assistenten in der Registerdatenbank
gespeichert. Das Wissensmodul erhält keine Objekt-, Eigentümer-, Personen-,
Audit- oder Sitzungsdaten. Es kann keine internen Endpunkte aufrufen.

## Aktionsverweigerung

Aufforderungen zum Ändern, Genehmigen, Löschen, Erstellen, Senden oder Exportieren
werden abgelehnt. Der Assistent darf stattdessen den zulässigen Arbeitsablauf
erklären. Die Anwendung muss diese Grenze auch dann beibehalten, wenn später ein
lokales Sprachmodell ergänzt wird: Ein Modell erhält keine Tools, Zugangsdaten,
SQL-Verbindung oder schreibenden APIs.

## Wissenspflege

Die Wissensversion steht in `app/assistant_service.py`. Jede Änderung benötigt:

1. fachliche Prüfung durch die zuständige Behörde,
2. Sicherheitsprüfung auf vertrauliche Inhalte,
3. Quellenangabe auf eine versionierte Projektdokumentation,
4. automatisierte Tests für Antwort, Authentifizierung und Aktionsverweigerung,
5. Vier-Augen-Freigabe des Releases.

Aktuell verwendet der Assistent bewusst eine deterministische lokale Suche.
Damit funktionieren Antworten ohne Internet, externe KI-Dienste oder
Datenübertragung. Ein späteres lokales Sprachmodell darf nur in einem separaten
Container ohne ausgehendes Netzwerk und mit schreibgeschützter Wissensbasis
laufen. Seine Antworten müssen weiterhin Quellen und Wissensversion anzeigen.
