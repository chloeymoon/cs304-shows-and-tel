create database if not exists final_project;
use final_project;

SET FOREIGN_KEY_CHECKS = 0;
drop table if exists showsCreators, showsActors, showsStreams, showsTags, showsCWs, showsGenres;
drop table if exists interviews, scripts, streams, networks, contentwarnings;
drop table if exists shows, creators, streams, actors, tags, genres, userpass, likes; 
SET FOREIGN_KEY_CHECKS = 0;


-- Tables

-- For Log in
create table userpass(
        uid int auto_increment,
        username varchar(50) not null,
        hashed char(60) not null,
        primary key (uid)
)
ENGINE = InnoDB;

-- likes table
create table likes (
    sid int(10),
    uid int(10),
    foreign key (sid) references shows (sid),
    foreign key (uid) references userpass (uid),
    primary key (sid, uid)
)
ENGINE = InnoDB; 


create table networks (
    nid int auto_increment,
    primary key (nid),
    name varchar(30) not null
)
ENGINE = InnoDB;

-- many to many because one show can have multiple content warnings and one content warning can have many shows
create table contentwarnings (
    cwid int auto_increment,
    primary key (cwid),
    name varchar(50)
)
ENGINE = InnoDB;


create table tags (
    tid int auto_increment,
    primary key (tid),
    val varchar(50),
    name ENUM('length', 'pace', 'type'),
    sid int,
    foreign key(sid) references shows(sid) on delete cascade
)
ENGINE = InnoDB;

create table creators (
    cid int auto_increment,
    primary key (cid),
    name varchar(60)
)
ENGINE = InnoDB;

create table genres (
    gid int auto_increment,
    primary key (gid),
    name varchar(50)
)
ENGINE = InnoDB;

create table shows (
    sid int auto_increment,
    primary key (sid),
    title varchar(30),
    description varchar(1000),
    year int,
    script varchar(100), -- adding scripts as an attribute in shows (link)
    nid int,
    foreign key(nid) references networks(nid) on delete cascade
        -- one show can have one network, but one network can have many shows
)
ENGINE = InnoDB;


-- TABLES FOR MANY TO MANY RELATIONSHIPS --

-- shows and creators
create table showsCreators (
    sid int,
    cid int,
    foreign key (sid) references shows(sid) on delete cascade,
    foreign key (cid) references creators(cid) on delete cascade,
    primary key(sid, cid)
)
ENGINE = InnoDB;

-- shows and genres
create table showsGenres (
    sid int,
    gid int,
    foreign key (sid) references shows(sid) on delete cascade,
    foreign key (gid) references genres(gid) on delete cascade,
    primary key(sid, gid)
)
ENGINE = InnoDB;

create table showsCWs (
    sid int,
    cwid int,
    foreign key (sid) references shows(sid) on delete cascade,
    foreign key (cwid) references contentwarnings(cwid) on delete cascade,
    primary key(sid, cwid)
)
ENGINE = InnoDB;


-- loading csv files

load data local infile 'csv/Genres.csv' into table genres
fields terminated by ','
lines terminated by '\n'
(name)
set gid = NULL;

load data local infile 'csv/Networks.csv' into table networks
fields terminated by ','
lines terminated by '\n'
(name)
set nid = NULL;

load data local infile 'csv/CW.csv' into table contentwarnings
fields terminated by ','
lines terminated by '\n'
(name)
set cwid = NULL;

load data local infile 'csv/Tags.csv' into table tags
fields terminated by ','
lines terminated by '\n'
(val, name, sid)
set tid = NULL;

load data local infile 'csv/Creators.csv' into table creators
fields terminated by ','
lines terminated by '\n'
(name)
set cid = NULL;

load data local infile 'csv/ShowsCreators.csv' into table showsCreators
fields terminated by ','
lines terminated by '\n';

load data local infile 'csv/ShowsCWs.csv' into table showsCWs
fields terminated by ','
lines terminated by '\n';

load data local infile 'csv/ShowsGenres.csv' into table showsGenres
fields terminated by ','
lines terminated by '\n';

load data local infile 'csv/Shows.csv' into table shows
fields terminated by ';'
lines terminated by '\n'
(title, description, year, script, nid)
set sid = NULL;

ALTER TABLE shows ADD COLUMN numLikes int not null default 0;