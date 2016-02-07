drop table busdata;
create table busdata(
id bigserial,
stationid VARCHAR(20),
cartype integer,
busid VARCHAR(100),
providerid VARCHAR(20),
carid VARCHAR(50),
dutystatus integer,
busstatus integer,
routeid VARCHAR(20),
goback integer,
longitude numeric,
latitude numeric,
speed numeric,
azimuth numeric,
datatime timestamp,
etl_time timestamp,
update_time timestamp
);
create index position on busdata (longitude,latitude,datatime);
