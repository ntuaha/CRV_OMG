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
longitude real,
latitude real,
speed real,
azimuth real,
datatime timestamp with time zone,
etl_time timestamp with time zone,
update_time timestamp with time zone
);
