use final_project;

drop table if exists userpass;

-- create table userpass(
--        uid int auto_increment,
--        username varchar(50) not null,
--        hashed char(60),
--        unique(username),
--        index(username),
--        primary key (uid)
-- );

create table userpass(
       username varchar(50) not null primary key,
       hashed char(60)
);