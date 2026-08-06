# Datenmodell und ERD

```mermaid
erDiagram
  ADMIN_UNIT ||--o{ ADMIN_UNIT : contains
  ADMIN_UNIT ||--o{ STREET : governs
  ADMIN_UNIT ||--o{ PARCEL : contains
  ADMIN_UNIT ||--o{ BUILDING : contains
  ADMIN_UNIT ||--o{ ADDRESS : assigns
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
