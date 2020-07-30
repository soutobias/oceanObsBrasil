
-- Criacao tabela ASCAT - MySQL DataBase Type

CREATE TABLE ascat (
	sat VARCHAR(10),
	datahora TIMESTAMP,
	lat FLOAT(6,4),
	lon FLOAT(6,4),
	wspd FLOAT(5,2),
	wdir INTEGER,
	PRIMARY KEY (sat, datahora,lat,lon)
);