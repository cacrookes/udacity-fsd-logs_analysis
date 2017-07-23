#!/usr/bin/etc python3
"""
Project: Logs Analysis, for Udacity Fullstack Nanodegree
Author: Christopher Crookes

log_analysis.py generates reports from the database set in DBNAME. Run directly to
generate a report of the top 3 articles of all time by views, a ranking of the most
popular authors by views, and a list of days were over 1% of access requests to the
site were errors.

This script can also be loaded as a module. Publically availabe functions:
- execute_query
- print_top_articles
- print_top_authors
- print_error_days
"""

import psycopg2

DBNAME = 'news'


def __db_connect():
    """ Creates and returns a connection to the database defined by DBNAME,
        as well as a cursor for the database.

        Returns:
            db, c - a tuple. The first element is a connection to the database.
                    The second element is a cursor for the database.
    """
    try:
        db = psycopg2.connect(dbname=DBNAME) 
        c = db.cursor()  # Create cursor
        return db, c
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def execute_query(query):
    """execute_query takes an SQL query as a parameter. 
        Executes the query and returns the results as a list of tuples.
       args:
           query - an SQL query statement to be executed.

       returns:
           A list of tuples containing the results of the query.
    """
    try:
        db, c = __db_connect()
        c.execute(query)
        results = c.fetchall()
        db.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def print_top_articles():
    """Prints out the top 3 articles of all time."""
    query = """SELECT title, views
               FROM article_views
               ORDER BY views DESC
               LIMIT 3;"""
    results = execute_query(query)

    header = 'Top 3 Articles by All Time Views'
    print(header)
    print('-' * len(header))
    for title, views in results:
        print('\"{}\" -- {} views'.format(title, views))
    

def print_top_authors():
    """Prints a list of authors ranked by article views."""
    query = """SELECT author, SUM(views) AS views
               FROM article_views
               GROUP BY author
               ORDER BY views DESC;"""
    results = execute_query(query)
    
    header = 'Top Authors by All Time Views'
    print(header)
    print('-' * len(header))
    for title, views in results:
        print('\"{}\" -- {} views'.format(title, views))

def print_error_days():
    """Prints out the days where more than 1% of logged access requests were errors."""
    query = "<put your SQL query here>"
    results = execute_query(query)

    # add code to print results

if __name__ == '__main__':
    print_top_articles()
    print('\n')
    print_top_authors()
    #print_error_days()
