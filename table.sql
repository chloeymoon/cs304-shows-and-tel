use c9;

drop table if exists shows, networks, interviews, tags;
drop table if exists creators, scripts, streams, actors;

-- THINGS TO DO: 
-- required relationship?

-- Creating tables

create table shows (
    sid int auto_increment,
    primary key (sid),
    title varchar(30),
    description varchar(100),
    genre varchar(30), -- Q: enum(a,b,c)?? what is better?
    script varchar(100), -- adding scripts as an attribute in shows (link)
    foreign key(nid) references networks(nid)
        on delete cascade -- one show can have one network, but one network can have many shows
); 
ENGINE = InnoDB;

create table networks (
    nid int auto_increment,
    primary key (nid),
    name varchar(30)
); 
ENGINE = InnoDB;

create table interviews (
    iid int auto_increment,
    primary key (iid),
    link varchar(100),
    foreign key (sid) references shows(sid)
        on delete cascade -- interview:show is many:one
);
ENGINE = InnoDB;

create table tags (
    tid int auto_increment,
    primary key (tid),
    name varchar(30)
); 
ENGINE = InnoDB;

create table creators (
    cid int auto_increment,
    primary key (cid),
    name varchar(50),
); 
ENGINE = InnoDB;

create table streams (
    stid int auto_increment,
    primary key (stid),
    source varchar(50)
); 
ENGINE = InnoDB;

create table actors (
    aid int auto_increment,
    primary key (aid),
    name varchar(30)
); 
ENGINE = InnoDB;

-- tables for many to many relationships --

-- shows and creators
create table showsCreators (
    foreign key (sid) references shows(sid) on delete cascade,
    foreign key (cid) references creators(cid) on delete cascade,
    primary key(sid, cid)
); 
ENGINE = InnoDB;

-- shows and streams
create table showsStreams (
    foreign key (sid) references shows(sid) on delete cascade,
    foreign key (stid) references streams(stid) on delete cascade,
    primary key(sid, stid)
); 
ENGINE = InnoDB;

-- shows and actors
create table showsActors (
    foreign key (sid) references shows(sid) on delete cascade,
    foreign key (aid) references actors(aid) on delete cascade,
    primary key(sid, aid)
); 
ENGINE = InnoDB;

-- shows and tags
create table showsTags (
    foreign key (sid) references shows(sid) on delete cascade,
    foreign key (tid) references tags(tid) on delete cascade,
    primary key(sid, tid)
);
ENGINE = InnoDB;
