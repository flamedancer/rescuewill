drop table if exists want_todo;
create table want_todo (
  id int UNSIGNED AUTO_INCREMENT,
  title varchar(250) not null,
  hard_star TINYINT not null,
  create_time datetime DEFAULT NOW(),
  finish_time datetime,
  total_score TINYINT not null,
  get_score INT,
  satisfy_star TINYINT,
  finish_reflection VARCHAR(1000),
  status INT,
  PRIMARY KEY ( `id` )
);