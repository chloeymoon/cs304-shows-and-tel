use c9;

-- Inserting example datas
insert into shows (title, year, description) 
values ("Game of Thrones",2011, "Nine noble families fight for control over the mythical lands of Westeros, while an ancient enemy returns after being dormant for thousands of years."),
        ("Friends",1994,"Follows the personal and professional lives of six twenty to thirty-something-year-old friends living in Manhattan.	"),
        ("Sherlock",2010,"A modern update finds the famous sleuth and his doctor partner solving crime in 21st century London."),
        ("Breaking Bad",2008,"A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine in order to secure his family's future.");


-- Check
select * from shows;