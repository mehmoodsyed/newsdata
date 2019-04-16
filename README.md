NEWS_REPOSITORY.py
Python code news_repository.py is a reporting tool that queries the PSQL database "news" in search of the following three questions:
1) Who are the most popular article authors of all time? 
2) What are the most popular three articles of all time?
3) On which days did more than 1% of requests lead to errors?

SETUP:
This program was tested under VM. Tools used to install an manage the VM are called Vagrant and VirtualBox. Virtual Box can be 
downloaded at https://www.virtualbox.org/wiki/Download_Old_Builds_5_1 and Vagrant can be downloaded at
https://www.vagrantup.com/downloads.html
To find more detailed description on how to use the tools mentioned above please refer to following URL:
https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0

The database can be downloaded at https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
Once unzipped the file newsdata.sql need to be put in the directory where it can be accessed by the VM. Following command need
to be used to load the data:
psql -d news -f newsdata.sql

IMPLEMENTATION:
The Python code in news_repository.py relies on the following views to answer the above questions. The
VIEW #1 and #2 are used to answer the first two questions. Rest of the views are needed for the last question.

1) CREATE VIEW id_name_title_hits AS
    SELECT authors.id, authors.name, articles.title, hits FROM authors 
    LEFT JOIN articles
      ON authors.id = articles.author
        JOIN
        (SELECT path, count(path) AS hits
            FROM log
            GROUP BY log.path) AS log
            ON log.path = '/article/' || articles.slug
            ORDER BY hits DESC;

2) CREATE VIEW popular_authors AS
    SELECT authors.name, totals FROM authors
        JOIN
        (SELECT name, SUM(hits) AS totals
            FROM id_name_title_hits group by name) AS pop_authors
            ON authors.name = pop_authors.name
            ORDER BY totals DESC;

3) CREATE VIEW traffic_pattern AS
  SELECT successful_attempts.day, successful_attempts.pass, failed_attempts.fails
   FROM successful_attempts LEFT JOIN failed_attempts
       ON successful_attempts.day = failed_attempts.day
   GROUP BY successful_attempts.day, successful_attempts.pass, failed_attempts.fails;

4) CREATE VIEW successful_attempts AS
  SELECT EXTRACT(dow from time) AS dow,
       DATE_TRUNC('day',time) AS day,
       COUNT(id) AS pass
  FROM log WHERE log.status='200 OK'
  GROUP BY 1,2 ORDER BY pass DESC;

5) CREATE VIEW failed_attempts AS
  SELECT EXTRACT(dow from time) AS dow,
       DATE_TRUNC('day',time) AS day,
       COUNT(id) AS fails
  FROM log WHERE log.status='404 NOT FOUND'
  GROUP BY 1,2 ORDER BY fails DESC;

  RESOURCES USED:
  1) Instructors notes
  2) http://www.stackoverflow.com
  3) http://www.postgresqltutorial.com
  4) https://www.postgresql.org
  5) https://mode.com/blog/postgres-sql-date-functions
  6) https://dba.stackexchange.com
  and probably many more

  ISSUES:
  Probably not most elegant of the solution. 
  The last three views need simplification.
  No attempt was made to optimize the queries for speed.
