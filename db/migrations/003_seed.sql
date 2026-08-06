BEGIN;
INSERT INTO sna.admin_unit(id,official_code,level,parent_id,name_ar,name_en) VALUES
 ('10000000-0000-0000-0000-000000000001','SY','COUNTRY',NULL,'الجمهورية العربية السورية','Syrian Arab Republic'),
 ('10000000-0000-0000-0000-000000000002','SY-DI','GOVERNORATE','10000000-0000-0000-0000-000000000001','دمشق','Damascus'),
 ('10000000-0000-0000-0000-000000000003','SY-DI-MD','MUNICIPALITY','10000000-0000-0000-0000-000000000002','مدينة دمشق','Damascus City'),
 ('10000000-0000-0000-0000-000000000004','SY-DI-MD-SH','NEIGHBOURHOOD','10000000-0000-0000-0000-000000000003','الشعلان','Al-Shaalan');
INSERT INTO sna.street(id,official_code,admin_unit_id,name_ar,name_en,centreline) VALUES
 ('20000000-0000-0000-0000-000000000001','SY-DI-MD-STR-000001','10000000-0000-0000-0000-000000000004',
  'شارع الحمراء','Al-Hamra Street',ST_Multi(ST_GeomFromText('LINESTRING(36.2889 33.5162,36.2904 33.5172)',4326)));
INSERT INTO sna.building(id,official_code,admin_unit_id,geom,function_code,lifecycle_status,floors,quality_level,source_type) VALUES
 ('30000000-0000-0000-0000-000000000001','SY-DI-MD-BLD-000001','10000000-0000-0000-0000-000000000004',
  ST_Multi(ST_GeomFromText('POLYGON((36.2895 33.5166,36.2898 33.5166,36.2898 33.5168,36.2895 33.5168,36.2895 33.5166))',4326)),
  'RESIDENTIAL_MIXED','EXISTING',4,'C','ORTHOPHOTO');
INSERT INTO sna.entrance(id,official_code,building_id,label,geom,quality_level) VALUES
 ('40000000-0000-0000-0000-000000000001','SY-DI-MD-ENT-000001','30000000-0000-0000-0000-000000000001','A',
  ST_SetSRID(ST_Point(36.28964,33.51669),4326),'C');
INSERT INTO sna.address(id,official_code,street_id,building_id,entrance_id,admin_unit_id,house_number,postal_code,formatted_ar,formatted_en,position,quality_level,source_type) VALUES
 ('50000000-0000-0000-0000-000000000001','SY-DI-MD-ADR-000001','20000000-0000-0000-0000-000000000001',
  '30000000-0000-0000-0000-000000000001','40000000-0000-0000-0000-000000000001','10000000-0000-0000-0000-000000000004',
  '12','010101','شارع الحمراء ١٢، الشعلان، دمشق','12 Al-Hamra Street, Al-Shaalan, Damascus',
  ST_SetSRID(ST_Point(36.28964,33.51669),4326),'C','ORTHOPHOTO');
COMMIT;
