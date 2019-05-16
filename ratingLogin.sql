create database if not exists final_project;
use final_project;

drop table if exists ratings, logins;
-- alter table movie drop column rating;

create table ratings (
    sid int(10) unsigned,
    uid int(10) unsigned,
    rating double,
    foreign key (sid) references shows (sid),
    foreign key (uid) references staff (uid),
    primary key (sid, uid)
); 

create table logins(
    uid int(10) auto_increment,
    username varchar(20),
    password varchar(20),
    primary key(uid)
);

-- Example
insert into logins (username,password) values ('chloeymoon','123123'),('catocity','123123');
insert into ratings (sid, uid, rating) values (1, 1, 1), (1, 2, 2);

ALTER TABLE movie ADD COLUMN rating double;

select avg(ratings.rating) from shows
inner join ratings on shows.sid = ratings.sid group by shows.sid;