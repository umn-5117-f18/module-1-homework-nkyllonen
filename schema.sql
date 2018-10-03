
drop table person;
drop table skill;

create table person(
  person_id SERIAL PRIMARY KEY,
  name varchar(255)
);

create table skill(
  skill_id SERIAL PRIMARY KEY,
  person_id int references person,
  skill varchar(255)
);

-- insert into person (name) values ('max');
-- insert into person (name) values ('hao fei');
