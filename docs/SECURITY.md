# Sicherheitskonzept

## Schutzbedarf

Verfügbarkeit und Integrität sind für Adressen/Kataster sehr hoch; Vertraulichkeit ist für Eigentums-, Rechts- und Personendaten sehr hoch. Das öffentliche Adressregister enthält keine Eigentümer oder Bewohner.

## Kontrollen

- MFA mit Hardware-Schlüsseln für Personal; Pilotpasswörter sind ausschließlich Demo-Daten.
- Föderiertes Behörden-Identitätsmanagement, persönliche Konten, sofortiges Offboarding.
- Least Privilege und Funktionstrennung: Editor, Reviewer, Approver, Auditor, Administrator.
- Netzwerkzonen für Internet, öffentliche Dienste, Behördenzugang, Register, Administration, Backups und SOC.
- TLS 1.3 wo möglich, gegenseitiges TLS zwischen Diensten, Verschlüsselung ruhender Datenträger und Backups.
- Schlüssel in staatlich kontrolliertem HSM; Schlüsselrotation und Zwei-Personen-Freigabe.
- Schreibzugriff auf amtlichen Bestand nur über validierten Publikationsdienst.
- Append-only Auditexport in unabhängige Sicherheitsdomäne; Zeitstempel und digitale Signaturen.
- Gehärtete Linux-Baselines, signierte Artefakte, SBOM, Schwachstellenscans und zeitgebundene Adminrechte.
- Rate Limits, WAF, DDoS-Schutz, sichere Header, strikte Eingabevalidierung und Exportbegrenzung.
- 3-2-1-1-0-Backups und dokumentierte Restore-Tests.

## Offene Pflichtprüfungen vor Produktion

Bedrohungsmodell, Datenschutz-Folgenabschätzung, syrisches Rechtsgutachten, Penetrationstest, Red-Team-Übung, Lieferkettenprüfung, Betriebs- und Notfallhandbuch, RPO/RTO-Abnahme, Personalüberprüfung für kritische Rollen und unabhängige Quellcodeprüfung.

Kein System ist „unhackbar“. Ziel sind Prävention, Begrenzung, schnelle Erkennung, beweissichere Reaktion und verlässlich getestete Wiederherstellung.
