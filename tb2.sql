-- (A) USERS TABLE
CREATE TABLE employee (
  uid INTEGER,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  email TEXT NOT NULL,
  bu TEXT NOT NULL,
  PRIMARY KEY("uid" AUTOINCREMENT)
);

CREATE INDEX `idx_fname`
  ON `employee` (`lname`);

CREATE UNIQUE INDEX `idx_email`
  ON `employee` (`email`);

-- (B) DUMMY DATA
INSERT INTO "employee" VALUES
(1,'สุชิรา','j1@doe.com','TPBR'),
(2,'สุชาติ','j2@doe.com','TPBR'),
(3,'ปนัดดา','j3@doe.com','TPBR'),
(4,'เอกชัย','j4@doe.com','TPBR'),
(5,'เอกพล','j5@doe.com','TPBR');
