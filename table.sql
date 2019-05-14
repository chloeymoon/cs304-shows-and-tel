create database if not exists final_project;
use final_project;

SET FOREIGN_KEY_CHECKS = 0;
drop table if exists showsCreators, showsActors, showsStreams, showsTags, showsCWs, showsGenres;
drop table if exists interviews, scripts, streams, networks, contentwarnings;
drop table if exists shows, creators, streams, actors, tags, genres; 
SET FOREIGN_KEY_CHECKS = 0;


-- Tables

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
    name varchar(30)
)
ENGINE = InnoDB;


create table tags (
    tid int auto_increment,
    primary key (tid),
    sid int,
    name ENUM('length', 'pace', 'type'),
    val varchar(30),
    foreign key(sid) references shows(sid) on delete cascade
)
ENGINE = InnoDB;

create table creators (
    cid int auto_increment,
    primary key (cid),
    name varchar(50)
)
ENGINE = InnoDB;

create table genres (
    gid int auto_increment,
    primary key (gid),
    name varchar(50)
)
ENGINE = InnoDB;

-- might implement in beta
create table streams (
    stid int auto_increment,
    primary key (stid),
    source varchar(50)
)
ENGINE = InnoDB;

-- create table actors (
--     aid int auto_increment,
--     primary key (aid),
--     name varchar(30)
-- )
-- ENGINE = InnoDB;

create table shows (
    sid int auto_increment,
    primary key (sid),
    nid int,
    title varchar(30),
    description varchar(1000),
    year int,
    -- genre varchar(30), -- Q: enum(a,b,c)?? what is better?
    -- cwid int, -- not right b/c many to many
    script varchar(100), -- adding scripts as an attribute in shows (link)
    foreign key(nid) references networks(nid) on delete cascade
        -- one show can have one network, but one network can have many shows
)
ENGINE = InnoDB;

-- create table interviews (
--     iid int auto_increment,
--     primary key (iid),
--     sid int,
--     link varchar(500),
--     foreign key (sid) references shows(sid) on delete cascade 
--         -- interview:show is many:one
-- )
-- ENGINE = InnoDB;


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

-- -- shows and streams
-- create table showsStreams (
--     sid int,
--     stid int,
--     foreign key (sid) references shows(sid) on delete cascade,
--     foreign key (stid) references streams(stid) on delete cascade,
--     primary key(sid, stid)
-- )
-- ENGINE = InnoDB;

create table showsCWs (
    sid int,
    cwid int,
    foreign key (sid) references shows(sid) on delete cascade,
    foreign key (cwid) references contentwarnings(cwid) on delete cascade,
    primary key(sid, cwid)
)
ENGINE = InnoDB;

-- -- shows and actors
-- create table showsActors (
--     sid int,
--     aid int,
--     foreign key (sid) references shows(sid) on delete cascade,
--     foreign key (aid) references actors(aid) on delete cascade,
--     primary key(sid, aid)
-- )
-- ENGINE = InnoDB;

-- -- shows and tags
-- create table showsTags (
--     sid int,
--     tid int,
--     foreign key (sid) references shows(sid) on delete cascade,
--     foreign key (tid) references tags(tid) on delete cascade,
--     primary key(sid, tid)
-- )
-- ENGINE = InnoDB;
