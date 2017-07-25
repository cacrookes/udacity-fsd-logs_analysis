#!/usr/bin/etc python3
"""
Project: Logs Analysis, for Udacity Fullstack Nanodegree
Author: Christopher Crookes

log_analysis.py generates reports from the database set in DBNAME. Run directly
to generate a report of the top 3 articles of all time by views, a ranking of
the most popular authors by views, and a list of days were over 1% of access
requests to the site were errors.

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


def __print_results(header, answers):
    """ Prints a section of a report.

        Args:
            header - (string) The section header to print

            answers - a list of strings to print, row by row
    """
    print(header)
    print('-' * len(header))
    print(*answers, sep='\n')
    print('\n')


def execute_query(query, data=[]):
    """execute_query takes an SQL query as a parameter.
        Executes the query and returns the results as a list of tuples.
       
       Args:
           query - an SQL query statement to be executed.

           data - a list of paramenters to pass to the query statement

       returns:
           A list of tuples containing the results of the query.
    """
    try:
        db, c = __db_connect()
        c.execute(query, data)
        results = c.fetchall()
        db.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def print_top_articles(limit='all'):
    """Prints out the top 3 articles of all time.
    
        Args:
          limit - specifies the number of results to return. Defaults to 'all'.  
    """
    query = """SELECT title, views
               FROM article_views
               ORDER BY views DESC"""
    
    # if a limit is specified, append limit clause to SQL query
    if limit == 'all':
        query += ';'
        results = execute_query(query)
    else:
        query += ' LIMIT %s;'
        results = execute_query(query, [limit,])

    # create a list of nicely formatted rows to print later
    answers = ['\"{}\" -- {} views'.format(title, views)
               for title, views in results]
    header = 'Top Articles By All Time Views' if limit=='all' else \
             'Top {} Articles By All Time Views'.format(limit)
    __print_results(header, answers)


def print_top_authors(limit='all'):
    """Prints a list of authors ranked by article views.
        
        Args:
          limit - specifies the number of results to return. Defaults to 'all'.
    """
    query = """SELECT author, SUM(views) AS views
               FROM article_views
               GROUP BY author
               ORDER BY views DESC"""


     # if a limit is specified, append limit clause to SQL query
    if limit == 'all':
        query += ';'
        results = execute_query(query)
    else:
        query += ' LIMIT %s;'
        results = execute_query(query, [limit,])
        
    header = 'Top Authors By All Time Views' if limit=='all' else \
             'Top {} Authors By All Time Views'.format(limit)
    # create a list of nicely formatted rows to print later
    answers = ['{} -- {} views'.format(title, views) 
               for title, views in results]
    __print_results(header, answers)


def print_error_days(threshold=1):
    """Prints out the days where more than 1% of
    logged access requests were errors.
    
        Args:
          threshold - (optional numeric value) days with an error rate 
            percentage exceeding threshold will be printed. Set to 1 by default
    """

    query = """SELECT date, error_percent
               FROM daily_error_rates
               WHERE error_percent > %s
               ORDER BY date;"""
    results = execute_query(query, [threshold,])
    header = 'Days With Over {}% Error Access Rate'.format(threshold)
    # create a list of nicely formatted rows to print later
    answers = []
    if len(results) == 0:
        answers = ['No results']
    else:
        answers = ['{0:%B %d, %Y} -- {1:.2f}% errors'
                .format(log_date, error_percent) 
                for log_date, error_percent in results]
    __print_results(header, answers)


if __name__ == '__main__':
    print_top_articles(3)
    print_top_authors()
    print_error_days()
