create database comp_db;

use comp_db;

create table games (
  game_id int primary key not null auto_increment,
  description varchar(50),
  create_date date
);

create table game_points (
  gp_id int primary key not null auto_increment,
  game_id int not null,
  position int not null,
  points float not null
);

create table results (
  result_id int primary key not null auto_increment,
  game_descr varchar(50) not null,
  tournament_descr varchar(50) not null,
  username varchar(50) not null,
  position int not null,
  insert_date date
);

create table tournaments (
  tournament_id int primary key not null auto_increment,
  description varchar(50) not null,
  created_by varchar(20) not null,
  creation_date date
);

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
