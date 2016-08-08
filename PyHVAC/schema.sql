drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  date_time timestamp without time zone not null,
  mode_num text not null,
  relative_humidity integer not null,
  misting boolean not null,
  pressure integer not null,
  co2 integer not null,
  wind_speed integer not null,
  sensor_data text not null,
  actuator_data text not null
);

drop table if exists modes;
create table modes (
  id integer primary key autoincrement,
  mode_num integer not null,
  temperature integer not null,
  relative_humidity integer not null,
  misting boolean not null,
  pressure integer not null,
  co2 integer not null,
  wind_speed integer not null
);

