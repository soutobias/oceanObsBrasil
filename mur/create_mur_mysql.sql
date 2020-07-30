CREATE TABLE mur (
datahora TIMESTAMP,
lat FLOAT(5,2),
lon FLOAT(5,2),
sst FLOAT(5,3),
PRIMARY KEY(datahora, lat, lon)
)