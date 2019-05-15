use final_project;
-- ask about nid

load data local infile 'csv/Genres.csv' into table genres
fields terminated by ','
lines terminated by '\n';

load data local infile 'csv/Networks.csv' into table networks
fields terminated by ','
lines terminated by '\n';

load data local infile 'csv/Creators.csv' into table creators
fields terminated by ';'
lines terminated by '\n';

load data local infile 'csv/CW.csv' into table contentwarnings
fields terminated by ','
lines terminated by '\n';

load data local infile 'csv/Tags.csv' into table tags
fields terminated by ','
lines terminated by '\n';

load data local infile 'csv/Shows.csv' into table shows
fields terminated by ';'
lines terminated by '\n';

-- load data local infile 'csv/Streams.csv' into table showsStreams
-- fields terminated by ','
-- lines terminated by '\n';


