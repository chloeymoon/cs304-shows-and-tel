use final_project;

load data local infile 'csv/Genres1.csv' into table genres
fields terminated by ','
lines terminated by '\n'
(name)
set gid = NULL;

load data local infile 'csv/Networks1.csv' into table networks
fields terminated by ','
lines terminated by '\n'
(name)
set nid = NULL;

load data local infile 'csv/CW1.csv' into table contentwarnings
fields terminated by ','
lines terminated by '\n'
(name)
set cwid = NULL;

load data local infile 'csv/Tags1.csv' into table tags
fields terminated by ','
lines terminated by '\n'
(name, val, sid)
set tid = NULL;

load data local infile 'csv/Shows1.csv' into table shows
fields terminated by ';'
lines terminated by '\n'
(title, description, year, script, nid)
set sid = NULL;

load data local infile 'csv/Creators1.csv' into table creators
fields terminated by ','
lines terminated by '\n'
(name)
set cid = NULL;


-- load data local infile 'csv/Streams.csv' into table showsStreams
-- fields terminated by ','
-- lines terminated by '\n';


