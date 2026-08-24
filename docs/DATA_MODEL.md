# Datenmodell und ERD

```mermaid
erDiagram
  ADMIN_UNIT ||--o{ ADMIN_UNIT : contains
  ADMIN_UNIT ||--o{ STREET : governs
  ADMIN_UNIT ||--o{ PARCEL : contains
  ADMIN_UNIT ||--o{ BUILDING : contains
  ADMIN_UNIT ||--o{ ADDRESS : assigns
  ADMIN_UNIT ||--o{ CADASTRAL_DISTRICT : governs
  CADASTRAL_DISTRICT ||--o{ CADASTRAL_SECTION : contains
  CADASTRAL_SECTION ||--o{ PARCEL : contains
  PARCEL ||--o{ PARCEL_OWNERSHIP_RECORD : has_protected_history
  PARCEL }o--o{ BUILDING : overlaps
  BUILDING ||--o{ ENTRANCE : has
  STREET o|--o{ ADDRESS : names
  BUILDING o|--o{ ADDRESS : locates
  ENTRANCE o|--o{ ADDRESS : targets
  CHANGE_REQUEST }o--|| USER : requested_by
  SOURCE_RECORD }o--|| OBJECT : documents
  AUDIT_EVENT }o--|| OBJECT : records
```

Adress-ID, Gebäude-ID und Grundstücks-ID sind niemals austauschbar. Lesbare Kennungen wie `SY-DI-MD-ADR-000001` helfen im Betrieb, während UUIDs die unveränderliche technische Identität bilden. Kennungsteile dürfen keine geheimen oder personenbezogenen Informationen kodieren.

Das SQL-Modell liegt in `db/migrations`. PostGIS nutzt WGS 84 (`EPSG:4326`) für Austausch und Speicherung im Pilot. Für amtliche Vermessung muss Syrien ein geeignetes nationales Referenzsystem und Transformationsregeln verbindlich wählen.

Die Erfassungsreihenfolge ist Katasterbezirk → Flur → Flurstück → Gebäude → Eingang/Adresse. Flur-, Flurstücks- und Gebäudegrundflächen werden technisch aus der Geometrie berechnet. Vor der vermessungsfachlichen Freigabe sind diese Werte nur vorläufig.

Eigentümer- oder Berechtigtenangaben liegen als zeitlich versionierte, besonders geschützte Akte getrennt vom Kartenobjekt. Öffentliche Karten-, Such- und Partnerexporte erhalten diese Daten nicht.
