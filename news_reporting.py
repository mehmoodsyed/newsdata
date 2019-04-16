# !/usr/bin/env python3
#
#  Project 1 FSND
#  Submitter: Mehmood Syed
#  Date: April 14, 2019
#  Building an informative summary from database to answer following questions:
#  What are the most popular three articles of all time?
#  Who are the most popular article authors of all time?
#  On which days did more than 1% of requests lead to errors?

import psycopg2

DBNAME = "news"


#  What are the most popular three articles of all time?


def get_top3_articles():
    """Return top 3 articles. Query is using a view named id_name_title_hits"""
    db = psycopg2.connect(database=DBNAME, user="vagrant", host="/tmp/",
                          password="vagrant")
    c = db.cursor()
    c.execute("SELECT title, hits FROM id_name_title_hits LIMIT 3")
    top3 = c.fetchall()
    db.close()
    return top3


#  Who are the most popular article authors of all time?


def get_top3_authors():
    """Return top 3 authors. Query is using a view named popular_authors"""
    db = psycopg2.connect(database=DBNAME, user="vagrant", host="/tmp/",
                          password="vagrant")
    c = db.cursor()
    c.execute("SELECT * FROM popular_authors LIMIT 3")
    top3 = c.fetchall()
    db.close()
    return top3


# On which days did more than 1% of requests lead to errors?


def get_traffic_pattern():
    """Return traffic pattern with pass and fail by day.
       Query is using a view named traffic pattern which in turn
       use views failed_attempts and successful_attempts"""
    db = psycopg2.connect(database=DBNAME, user="vagrant", host="/tmp/",
                          password="vagrant")
    c = db.cursor()
    c.execute("SELECT TO_CHAR(day, 'yyyy-mm-dd'),CAST(fails AS \
              NUMERIC)/(CAST(pass AS NUMERIC)+CAST(fails AS NUMERIC))*100\
              FROM traffic_pattern WHERE CAST(fails AS NUMERIC)/(CAST(pass \
              AS numeric)+CAST(fails AS numeric)) >= 0.01")
    result = c.fetchall()
    db.close()
    return result


if __name__ == '__main__':
    results = get_top3_authors()
    # results in format name, totals
    print("Most Popular 3 Authors:")
    print("=======================")
    for i in range(0, 3):
        print(results[i][0], "----", results[i][1], "views")

    print("\n\n")
    print("Most Popular 3 Articles:")
    print("========================")
    results = get_top3_articles()
    # results in format article, views
    for i in range(0, 3):
        print('"', results[i][0], '", '"----", results[i][1], "views")
    print("\n\n")
    print("Days on which more than 1 percent of requests lead to errors:")
    print("=============================================================")
    results = get_traffic_pattern()
    print(results[0][0], "----", round(results[0][1], 1), "% " + "errors")
