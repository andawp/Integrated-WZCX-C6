DROP TABLE if exists carinfo;
CREATE TABLE carinfo (
  id INTEGER PRIMARY KEY autoincrement,
  cpd text NOT NULL ,
  hm text NOT NULL ,
  fdj text NOT NULL ,
  email text NOT NULL ,
  wzxx text NULLABLE ,
  lastupdate DATE NULLABLE
);