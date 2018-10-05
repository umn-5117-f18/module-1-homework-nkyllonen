drop table person;

create table person(
  person_id SERIAL PRIMARY KEY,
  time_stamp varchar(255),
  name varchar(255),
  color varchar(255),
  music varchar(255),
  breed varchar(255),
  terms text
);
