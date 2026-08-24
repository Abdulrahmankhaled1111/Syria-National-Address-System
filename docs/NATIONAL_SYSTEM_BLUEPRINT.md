# Nationaler System-Blueprint für Syrien

## Zweck und Status

Dieser Blueprint überführt die Architektur- und Sicherheitsanforderungen aus dem
Projektgespräch in den vorhandenen Codebestand. Das Repository bleibt ein
lauffähiger Pilot und darf nicht als bereits zugelassenes nationales Kataster
oder Grundbuch bezeichnet werden. Rechtswirkung entsteht erst durch syrische
Gesetze, zuständige Behörden, bestätigte Daten und formale Abnahmen.

## Zielbild

Das nationale System besteht aus drei fachlich und technisch getrennten
Schutzdomänen:

1. **Öffentliches Adressregister** – Straße, Hausnummer, Postgebiet,
   Gebäudeumriss, Eingang, öffentliche Koordinate und Verwaltungsgebiet.
2. **Internes Katasterregister** – Vermessungsdaten, Grundstücke, Gebäude,
   Qualitätsberichte, Änderungsanträge und unveröffentlichte Bestände.
3. **Besonders geschütztes Rechtsregister** – Eigentümer, Berechtigte,
   Rechtsgrundlagen, Identitätsnachweise und zugehörige Dokumente.

Zwischen den Domänen existieren ausschließlich kontrollierte, protokollierte
Beziehungen. Öffentliche APIs, Karten, PDFs und Partnerexporte dürfen niemals
Eigentümer-, Bewohner-, Identitäts- oder interne Sicherheitsdaten enthalten.

```text
Internet
  |
DDoS-Schutz -> WAF/API-Gateway -> öffentliche Karte, Suche und Exporte
                                  |
                           kontrollierte APIs
-------------------------- Sicherheitsgrenze --------------------------
Behördenzugang -> Identität + MFA + Geräteprüfung -> Fachanwendungen
                                                   -> Genehmigungsworkflow
-------------------------- Sicherheitsgrenze --------------------------
Adressregister | Katasterregister | geschütztes Rechtsregister
                         |
             unveränderbare Auditkopie -> SOC/SIEM
                         |
          Standort A <-> Standort B -> Backupstandort C
```

## Staatliche Datenhoheit

- Betriebsstandorte, Administratorenkonten, Hauptschlüssel und Backups stehen
  unter technischer und rechtlicher Kontrolle der zuständigen syrischen Stelle.
- Kein ausländischer Anbieter erhält alleinige Administratorrechte, Schlüssel,
  Fernwartungszugänge oder exklusives Betriebswissen.
- Quellcode, Builds, Konfigurationen, Datenformate und Wiederherstellungswege
  müssen vollständig prüfbar und übertragbar sein.
- Kritische Komponenten werden auf mehrere Lieferanten verteilt; Softwarepakete
  und Releases werden signiert und mit einer SBOM dokumentiert.

## Drei physisch getrennte Standorte

### Standort A – Primärbetrieb

Anwendungsdienste, interne Portale, Karten- und Suchdienste, Hauptdatenbanken,
Identitätsanbindung sowie Sicherheitsüberwachung.

### Standort B – Ausweichbetrieb

Andere Stadt, möglichst unabhängige Strom- und Telekommunikationswege,
kontinuierliche Replikation und nachgewiesene Betriebsübernahme. Zielwerte des
Piloten: RPO höchstens 15 Minuten für Registeränderungen und RTO 4 Stunden;
endgültige Werte folgen aus der staatlichen Schutzbedarfsanalyse.

### Standort C – Wiederherstellung

Verschlüsselte, unveränderbare oder offline getrennte Sicherungen mit mehreren
Datenständen und isolierter Restore-Umgebung. Es gilt 3-2-1-1-0: drei Kopien,
zwei Speichermedien, eine externe Kopie, eine unveränderbare/offline Kopie und
null ungeprüfte Wiederherstellungsfehler.

## Identität, Rollen und privilegierte Zugriffe

- Persönliche Konten, keine gemeinsamen Benutzer oder Administratorpasswörter.
- Starke MFA; für privilegierte Rollen Hardware-Schlüssel oder Behördenkarten.
- Rollen mindestens: Bürger, Adressbearbeitung, Vermessung, Prüfung,
  Genehmigung, Datenbankbetrieb, Sicherheitsbetrieb, Audit und Notfallbetrieb.
- Least Privilege, Funktionstrennung und räumlicher Zuständigkeitsbereich.
- Privilegierte Rechte werden begründet, zeitlich begrenzt, protokolliert und
  automatisch entzogen. Hauptschlüssel liegen in staatlich kontrollierten HSMs;
  besonders kritische Vorgänge benötigen zwei Personen.
- Sofortiges Offboarding sowie regelmäßige Rezertifizierung von Konten, Rollen
  und Geräten.

## Amtliche Fortführung und Integrität

Kein Mitarbeiter ändert den amtlichen Bestand direkt. Jede Fortführung folgt
diesem unveränderlichen Ablauf:

```text
Antrag -> Bearbeitungsbereich -> automatische Prüfung -> fachliche Prüfung
       -> Genehmigung -> digitale Signatur -> Publikation -> Historisierung
```

Für jede Änderung werden Antragsteller, Bearbeiter, Prüfer, Genehmiger,
Zeitpunkt, vorheriger und neuer Stand, Quelle und Rechtsgrundlage festgehalten.
Auditereignisse werden verkettet und zusätzlich in eine unabhängige,
append-only Sicherheitsdomäne exportiert. Datenbankadministratoren dürfen den
technischen Betrieb durchführen, aber keine amtliche Änderung genehmigen.

## Verschlüsselung und Schlüsselverwaltung

- TLS für Browser, Apps und Behördenzugänge; gegenseitiges TLS zwischen
  Diensten und Standorten.
- Verschlüsselung von Datenträgern, Datenbanken, Dokumenten, Exporten,
  Mobilgeräten und Backups.
- Haupt-, Signatur- und Zertifikatsschlüssel in HSMs, geregelte Rotation,
  Wiederherstellung und Zwei-Personen-Freigabe.
- Backup-, HSM- und Produktionsadministration verwenden getrennte Identitäten.

## Plattform und Netztrennung

Die Zielplattform verwendet gehärtetes Linux, PostgreSQL/PostGIS,
S3-kompatiblen Objektspeicher, ein zentrales Identitätsmanagement und eine
staatlich kontrollierte Private Cloud, beispielsweise auf OpenStack. Kubernetes
kann zustandsarme Anwendungsdienste ausführen; besonders sensible Datenbanken
werden separat gehärtet betrieben. Produktionsserver enthalten nur notwendige
Dienste, keine Desktopumgebung und keine privaten Programme.

Mindestens getrennte Netzzonen: Internetkante, öffentliche Dienste,
API-Übergang, Behördenzugang, Fachanwendungen, Register, Administration,
Sicherheitsüberwachung und Backups. Ein kompromittierter Büro-PC oder eine
öffentliche Kartenanwendung darf keine direkte Route zu Registerdaten besitzen.

## Erkennung, Reaktion und Widerstandsfähigkeit

Ein rund um die Uhr besetztes oder verbindlich beauftragtes SOC überwacht
Anmeldungen, Massenabfragen, Rechteänderungen, Exporte, Objektänderungen,
Malware, Ausfälle und Manipulationsversuche. Alarme müssen automatische
Begrenzungsmaßnahmen wie Sitzungsentzug, Kontosperre oder Exportstopp auslösen
können. Hinzu kommen Red-Team-Übungen, unabhängige Prüfungen, sichere
Build-Systeme, signierte Artefakte, Schwachstellenscans, Patch-Prozesse und ein
getesteter Notbetrieb ohne öffentliches Internet.

## Abbildung auf dieses Repository

| Anforderung | Aktueller Stand | Verbindliche nächste Stufe |
|---|---|---|
| Adress-/Kataster-/Rechtstrennung | Fachmodell und geschützte Eigentumsakte vorhanden | getrennte Datenbanken, Konten und Netzzonen |
| Änderungsworkflow | Antrag, Prüfung, Genehmigung und Ablehnung implementiert | Signaturdienst und unabhängiger Publikationsdienst |
| Historisierung und Audit | Versionierungskonzept und verkettetes Auditlog | unabhängiger append-only Export in SOC-Domäne |
| Rollen und Zuständigkeit | Rollen und kommunale Scopes vorhanden | staatlicher IdP, Hardware-MFA und JIT-Administration |
| Geodaten | PostGIS-Zielschema, GeoJSON- und Pilotimporte vorhanden | Runtime vollständig von SQLite auf PostGIS umstellen |
| Öffentliche Dienste | Suche, Karte, PDF und kontrollierte Exporte vorhanden | eigene staatliche Karten-/Kacheldienste und API-Gateway |
| Hochverfügbarkeit | Zielarchitektur dokumentiert | Standorte A/B aufbauen und Failover unter Last abnehmen |
| Backup | Backup, Prüfsumme, Verifikation und Restore-Schutz vorhanden | immutable/offline Ziel C und regelmäßige Restore-Übungen |
| Plattformhärtung | Produktionsmodus, Reverse Proxy und Containerhärtung vorhanden | HSM, mTLS, SIEM, WAF/DDoS und Lieferkettenprüfung |
| Mobile Erfassung | Nachweisfoto, GPS und Außendienstprozess im Pilot | Offline-App, Geräteverwaltung und verschlüsselter Objektspeicher |

## Programmphasen und Abnahmekriterien

1. **Fach- und Rechtskonzept:** Behördenzuständigkeit, Datenschutz, Objektkatalog,
   Kennungen, Transliteration, Koordinatenreferenzsystem und Beweiswert sind
   schriftlich beschlossen.
2. **Mehrgebiets-Pilot:** mindestens vier unterschiedliche Gebiete; Datenqualität,
   Bedienbarkeit, kommunale Prozesse und Offline-Erfassung sind messbar geprüft.
3. **Sichere Plattform:** PostGIS-Runtime, staatlicher IdP/MFA, HSM, getrennte
   Register, SOC-Anbindung und Standort C sind produktionsnah abgenommen.
4. **Ausfallsicherer Betrieb:** Last-, Failover-, Restore-, Penetrations- und
   Red-Team-Tests erfüllen genehmigte RPO/RTO- und Sicherheitsziele.
5. **Provinz-Rollout:** Migration, Schulung, Support und Datenverantwortung sind
   je Provinz bestätigt; Rückfall- und Korrekturverfahren wurden geübt.
6. **Nationaler Rollout:** stufenweise Freigabe nach unabhängiger Abnahme; keine
   landesweite Aktivierung als einmaliger Big-Bang.

## Nicht zulässige Abkürzungen

Unzulässig sind ein einzelner Zentralserver, eine gemeinsame Datenbank für
öffentliche und geschützte Daten, dauerhafte Herstellerkonten, direkte
Bestandsänderungen, gemeinsam genutzte Administratoren, Backups mit denselben
Rechten wie die Produktion, Eigentümerdaten in Karten/Exporten und die
Behauptung, das System sei vollständig „unhackbar“.

## Entscheidungsregister vor Rechtswirkung

Vor einer staatlichen Freigabe müssen mindestens folgende Entscheidungen mit
verantwortlicher Stelle, Datum und Version dokumentiert werden:

- Rechtsgrundlage und federführende Behörde,
- verbindlicher syrischer Objektartenkatalog,
- nationale Kennungen und Postleitzahlregeln,
- Arabisch- und Transliterationsstandard,
- amtliches Koordinatenreferenzsystem und Transformationsregeln,
- Schutzklassen, Aufbewahrung und Löschung,
- RPO/RTO, Notbetrieb und Eskalationswege,
- zugelassene Betreiber, Lieferanten und Prüfstellen,
- Veröffentlichungspolitik für Adressen, Karten und offene Daten.

