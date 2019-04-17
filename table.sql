use c9;

drop table if exists shows, networks, interviews, tags;
drop table if exists creators, scripts, streams, actors;

-- THINGS TO DO: many-to-one or one-to-many relationships to implement
-- Foreign keys, primary keys could be a pair
-- Scott said it's too messy
-- required relationship?

-- Creating tables

create table shows (
    sid int auto_increment,
    -- foreign key (tt) references movie (tt),
    primary key (sid),
    title varchar(30),
    description varchar(100),
    genre varchar(30) -- or choose from certain + other?
); 

create table networks (
    nid int auto_increment,
    primary key (nid),
    name varchar(30),
); 

create table interviews (
    iid int auto_increment,
    -- foreign key (tt) references movie (tt),
    primary key (iid),
    link varchar(50)
); 

create table tags (
    tid int auto_increment,
    primary key (tid),
    name varchar(30)
); 

create table creators (
    cid int auto_increment,
    primary key (cid),
    name varchar(50)
); 

create table scripts (
    scid int auto_increment,
    primary key (scid),
    link varchar(50)
); 

create table streams (
    stid int auto_increment,
    primary key (stid),
    source varchar(50)
); 

create table actors (
    aid int auto_increment,
    primary key (aid),
    name varchar(30)
); 