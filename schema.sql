create database if not exists rescuewill;
use rescuewill;


-- drop table if exists datetask;
create table if not exists datetask (
  id int UNSIGNED AUTO_INCREMENT,
  title varchar(250) not null,
  create_time datetime DEFAULT NOW(),
  score INT not null,
  status INT,
  PRIMARY KEY ( `id` )
);


-- drop table if exists important;
create table if not exists important (
  id int UNSIGNED AUTO_INCREMENT,
  title varchar(250) not null,
  create_time datetime DEFAULT NOW(),
  deadline datetime DEFAULT NOW(),
  finish_time datetime,
  status INT,
  PRIMARY KEY ( `id` )
);

-- drop table if exists want_todo;
create table if not exists want_todo (
  id int UNSIGNED AUTO_INCREMENT,
  title varchar(250) not null,
  hard_star TINYINT not null,
  create_time datetime DEFAULT NOW(),
  finish_time datetime,
  total_score INT not null,
  get_score INT,
  satisfy_star TINYINT,
  finish_reflection VARCHAR(1000),
  status INT,
  PRIMARY KEY ( `id` )
);

-- drop table if exists memory;
create table if not exists memory (
  id int UNSIGNED AUTO_INCREMENT,
  title varchar(250) not null,
  remember_times INT DEFAULT 0,
  create_time datetime DEFAULT NOW(),
  score INT not null,
  status INT,
  PRIMARY KEY ( `id` )
);