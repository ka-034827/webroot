PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE srdfiles (name TEXT);
INSERT INTO "srdfiles" VALUES('afile');
INSERT INTO "srdfiles" VALUES('aAfile');
INSERT INTO "srdfiles" VALUES('cCCCfile');
INSERT INTO "srdfiles" VALUES('AAbbCCfile');
INSERT INTO "srdfiles" VALUES('cfile');
INSERT INTO "srdfiles" VALUES('Mdfile');
INSERT INTO "srdfiles" VALUES('bBfile');
COMMIT;
