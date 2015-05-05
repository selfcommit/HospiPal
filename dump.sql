BEGIN;
CREATE TABLE "HospiPal_person" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "ssn" integer NOT NULL UNIQUE,
    "date_of_birth" date NOT NULL,
    "gender" varchar(1) NOT NULL,
    "first_name" varchar(33) NOT NULL,
    "last_name" varchar(33) NOT NULL,
    "street1" varchar(255) NOT NULL,
    "street2" varchar(255) NOT NULL,
    "city" varchar(255) NOT NULL,
    "state" varchar(255) NOT NULL,
    "zipcode" varchar(255) NOT NULL,
    "telephone" varchar(33) NOT NULL
)
;
CREATE TABLE "HospiPal_supportstaff" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "person_id" integer NOT NULL REFERENCES "HospiPal_person" ("id"),
    "salary_amount" integer,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_skill" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(33) NOT NULL
)
;
CREATE TABLE "HospiPal_surgeon_skills" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "surgeon_id" integer NOT NULL,
    "skill_id" integer NOT NULL REFERENCES "HospiPal_skill" ("id"),
    UNIQUE ("surgeon_id", "skill_id")
)
;
CREATE TABLE "HospiPal_surgeon" (
    "person_id" integer NOT NULL PRIMARY KEY REFERENCES "HospiPal_person" ("id"),
    "salary_amount" integer,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_physician" (
    "person_id" integer NOT NULL PRIMARY KEY REFERENCES "HospiPal_person" ("id"),
    "skill_id" integer NOT NULL REFERENCES "HospiPal_skill" ("id"),
    "ownership" bool NOT NULL,
    "salary_amount" integer,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_nurse" (
    "person_id" integer NOT NULL PRIMARY KEY REFERENCES "HospiPal_person" ("id"),
    "years_experience" integer NOT NULL,
    "skill_id" integer NOT NULL REFERENCES "HospiPal_skill" ("id"),
    "grade" varchar(1) NOT NULL,
    "salary_amount" integer,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_chief" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "physician_id" integer NOT NULL REFERENCES "HospiPal_physician" ("person_id"),
    "dept" varchar(33) NOT NULL
)
;
CREATE TABLE "HospiPal_theater" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(33) NOT NULL,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_nursingunit" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "number" integer NOT NULL,
    "available" bool NOT NULL
)
;
CREATE TABLE "HospiPal_nursingroom" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "unit_id" integer NOT NULL REFERENCES "HospiPal_nursingunit" ("id"),
    "color" varchar(5) NOT NULL,
    "available" bool NOT NULL
)
;
CREATE TABLE "HospiPal_bed" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "room_id" integer NOT NULL REFERENCES "HospiPal_nursingroom" ("id"),
    "letter" varchar(1) NOT NULL,
    "available" bool NOT NULL
)
;
CREATE TABLE "HospiPal_patient" (
    "person_id" integer NOT NULL PRIMARY KEY REFERENCES "HospiPal_person" ("id"),
    "primary_id" integer NOT NULL REFERENCES "HospiPal_physician" ("person_id"),
    "hdl" varchar(33) NOT NULL,
    "ldl" varchar(33) NOT NULL,
    "tri" varchar(33) NOT NULL,
    "blood_sugar" varchar(33) NOT NULL,
    "needs_surgery" bool NOT NULL,
    "date_admitted" datetime NOT NULL,
    "date_discharged" datetime,
    "attending_nurse_id" integer REFERENCES "HospiPal_nurse" ("person_id"),
    "bed_id" integer REFERENCES "HospiPal_bed" ("id"),
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_illness_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(33) NOT NULL,
    "category" varchar(1) NOT NULL,
    "description" varchar(255) NOT NULL
)
;
CREATE TABLE "HospiPal_illness" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name_id" integer NOT NULL REFERENCES "HospiPal_illness_type" ("id"),
    "patient_id" integer NOT NULL REFERENCES "HospiPal_patient" ("person_id"),
    "date_added" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_surgery_type_skills" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "surgery_type_id" integer NOT NULL,
    "skill_id" integer NOT NULL REFERENCES "HospiPal_skill" ("id"),
    UNIQUE ("surgery_type_id", "skill_id")
)
;
CREATE TABLE "HospiPal_surgery_type" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(33) NOT NULL,
    "category" varchar(1) NOT NULL,
    "anatomical_location" varchar(33) NOT NULL,
    "special_needs" varchar(33) NOT NULL,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_surgery_nurses" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "surgery_id" integer NOT NULL,
    "nurse_id" integer NOT NULL REFERENCES "HospiPal_nurse" ("person_id"),
    UNIQUE ("surgery_id", "nurse_id")
)
;
CREATE TABLE "HospiPal_surgery_surgeons" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "surgery_id" integer NOT NULL,
    "surgeon_id" integer NOT NULL REFERENCES "HospiPal_surgeon" ("person_id"),
    UNIQUE ("surgery_id", "surgeon_id")
)
;
CREATE TABLE "HospiPal_surgery" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "surgery_type_id" integer NOT NULL REFERENCES "HospiPal_surgery_type" ("id"),
    "date_performed" datetime NOT NULL,
    "patient_id" integer NOT NULL REFERENCES "HospiPal_patient" ("person_id"),
    "theater_id" integer NOT NULL REFERENCES "HospiPal_theater" ("id"),
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_consultation" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "patient_id" integer NOT NULL REFERENCES "HospiPal_patient" ("person_id"),
    "doctor_id" integer NOT NULL REFERENCES "HospiPal_physician" ("person_id"),
    "date_of_consult" datetime NOT NULL,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_medication" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(33) NOT NULL,
    "quantity_on_hand" integer NOT NULL,
    "quantity_on_order" integer NOT NULL,
    "unit_cost" integer NOT NULL,
    "year_to_date" datetime NOT NULL,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_medication_interaction" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "prescribed_drug_id" integer NOT NULL REFERENCES "HospiPal_medication" ("id"),
    "interfering_drug_id" integer NOT NULL REFERENCES "HospiPal_medication" ("id"),
    "interaction" varchar(1) NOT NULL
)
;
CREATE TABLE "HospiPal_prescription" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "medication_id" integer NOT NULL REFERENCES "HospiPal_medication" ("id"),
    "prescriber_id" integer NOT NULL REFERENCES "HospiPal_physician" ("person_id"),
    "patient_id" integer NOT NULL REFERENCES "HospiPal_patient" ("person_id"),
    "dosage" varchar(33) NOT NULL,
    "frequency" varchar(33) NOT NULL,
    "date_added" datetime NOT NULL,
    "date_updated" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_contract_skills" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "contract_id" integer NOT NULL,
    "skill_id" integer NOT NULL REFERENCES "HospiPal_skill" ("id"),
    UNIQUE ("contract_id", "skill_id")
)
;
CREATE TABLE "HospiPal_contract" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "surgeon_id" integer NOT NULL REFERENCES "HospiPal_surgeon" ("person_id"),
    "years" integer NOT NULL
)
;
CREATE TABLE "HospiPal_schedule" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id"),
    "object_id" integer unsigned NOT NULL,
    "shift" datetime NOT NULL
)
;
CREATE TABLE "HospiPal_corporation" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" varchar(33) NOT NULL UNIQUE,
    "headquarters" varchar(33) NOT NULL,
    "percent" integer NOT NULL
)
;

COMMIT;
