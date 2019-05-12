use final_project;

-- TRUNCATE TABLE networks, shows, creators, showsCreators;

-- Inserting sample data

insert into networks (name)
values ("HBO"), ("NBC"), ("BBC"), ("AMC"), ("Netflix");

insert into shows (title, year, nid, genre, script, description) 
values ("Game of Thrones", 2011, 1, "Fantasy",  "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=game-of-thrones",
        "Nine noble families fight for control over the mythical lands of Westeros, while an ancient enemy returns after being dormant for thousands of years."),
        ("Friends", 1994, 2, "Sitcom", "https://fangj.github.io/friends/",
        "Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan."),
        ("Sherlock", 2010, 3, "Crime", "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=sherlock",
        "A modern update finds the famous sleuth and his doctor partner solving crime in 21st century London."),
        ("Breaking Bad", 2008, 4, "Drama", "https://filmschoolrejects.com/wp-content/uploads/2017/05/Screenplay-Breaking_Bad-Pilot.pdf",
        "A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family's future."),
        ("Black Mirror", 2011, 5, "Science Fiction", "https://www.springfieldspringfield.co.uk/episode_scripts.php?tv-show=black-mirror-2011",
        "Featuring stand-alone dramas -- sharp, suspenseful, satirical tales that explore techno-paranoia -- 'Black Mirror' is a contemporary reworking of 'The Twilight Zone' with stories that tap into the collective unease about the modern world. ")
        ;

insert into contentwarnings(name)
value("Sex & Nudity"),("Violence & Gore"),("Profanity"),("Alcohol"), ("Drugs & Smoking");

insert into showsCWs(sid,cwid)
values(1,1),(3,2),(2,5),(2,4),(4,2),(4,1),(4,5),(3,3);

insert into creators(name)
values('Mark Gatiss'),('Steven Moffat'),('Vince Gilligan'),('David Crane'),('Marta Kauffman'),('David Benioff'),('D. B. Weiss'),('Charlie Brooker');

insert into showsCreators(sid,cid)
values (3,1),(3,2),(4,3),(2,4),(2,5),(1,6),(1,7),(5,8);

-- Check
-- select * from networks;
-- select * from shows;
select * from contentwarnings;
select * from showsCWs;