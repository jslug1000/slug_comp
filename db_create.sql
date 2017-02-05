create database comp_db;

use comp_db;

create table games (
  game_id int primary key not null auto_increment,
  tournament_id int not null,
  description varchar(50) not null,
  create_date datetime,
  -- this should change to be user_id
  created_by varchar(20)
);

create table game_points (
  gp_id int primary key not null auto_increment,
  game_id int not null,
  position int not null,
  points float not null
);

create table results (
  result_id int primary key not null auto_increment,
  session_id int not null,
  game_id int not null,
  tournament_id int not null,
  user_id int not null,
  position int not null,
  game_setup_time datetime not null,
  results_confirmed_time datetime
);

create table game_sessions (
  session_id int primary key not null auto_increment,
  game_id int not null,
  tournament_id int not null,
  created_by int not null
);

create table tournaments (
  tournament_id int primary key not null auto_increment,
  description varchar(50) not null,
  -- this should be changed to be user_id
  created_by varchar(20) not null,
  creation_date date
);

-- maybe change this to be 'competitors'
create table users (
  user_id int primary key not null auto_increment,
  username varchar(20) not null,
  name varchar(45) not null,
  password varchar(45) not null
);

create table tournament_players (
  player_id int primary key not null auto_increment,
  user_id int not null,
  tournament_id int not null,
  entered_by int not null,
  added_at date
);
