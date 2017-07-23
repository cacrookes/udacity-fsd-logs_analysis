# Logs Analysis

## Project Description

This project was created as one of the assignments for [Udacity's Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

This project creates a mock database called *news* for a fictional news website. The python script, *logs_analysis.py* queries the *news* database using psycopg2 to generate a report and print it to the screen. The report lists:
1. The top 3 all time most viewed articles on the news site.
2. A ranking of authors based on total article views.
3. A list of days where more than 1% of access requests to the site were errors.

## Requirements
This project was tested with:
- [Python 3.5.2](https://www.python.org/downloads/)
- [PostgreSQL 9.5.6](https://www.postgresql.org/download/)
- psycopg2 2.7.1
  - psycopg2 can be installed using the included **requirements.txt** file.
  - From the command line type: `pip install -r requirements.txt`

## Database Set-up
**WARNING**: If you currently have a PostreSQL database named *news*, following these steps will delete it. If you are not sure if you have a database named *news*, follow these steps to check:
- From the command line, enter: `psql -d news`
- If you see: `psql: FATAL:  database "news" does not exist`, then you are safe to proceed.
- If you don't get an error, but see a prompt similar to `news=>`, I recommend not proceeding with this set-up at this time unless you are sure you want to delete your *news* database.

To set-up the database, follow these steps:
1. In the folder containing the project files, extract **newsdata.sql**
   - From the command line, type: `tar -xvzf newsdata.tar.gz`
2. Ensure that both **database_setup.sql** and **newsdata.sql** are in the same folder.
3. In the command line, enter: `psql -f database_setup.sql`
   - This will create the *news* database, import the schema and mock data from *newsdata.sql*, and create a couple custom views as described below. 

## How to run
- Once you have successfully set-up the *news* database, you can run logs_analysis.py to generate the report.
  - From the command line type: `python3 logs_analysis.py`

## Database Structure

### Tables

- **authors**: Contains info on authors of articles
  - id: serial integer, unique identifier for each author
  - name: full name of the author
  - bio: the author's biograpy
- **articles**: Contains info on articles that appear on the news site
  - id: serial integer, unique identifier for each article
  - author: integer representing the id of the article's author
  - title: title of the article
  - slug: the article's url slug
  - lead: description of the article
  - body: the main text of the article
  - time: time the article was last updated
- **log**: Contains a log of access requests to the news site
  - id: unique identifier for the access request
  - path: relative url that was requested
  - ip: ip address that sent the request
  - method: HTTP request type. e.g. GET
  - status: request status. e.g. '200 OK', '404 NOT FOUND'
  - time: datetime field storing the time of the request

### Views

In addition to the original tables, the following views are created when running **database_setup.sql**

#### article_views
```sql
CREATE VIEW article_views AS 
SELECT articles.title, authors.name as author, log.views
FROM articles INNER JOIN
    (SELECT path, count(*) as views
    FROM log 
    GROUP BY path) AS log
ON '/article/' || articles.slug = log.path
LEFT JOIN authors 
ON articles.author = authors.id;
```

*article_views* creates a table of all articles with the name of the author and the number of times the articl was viewed on the site.
- title: title of the article
- author: full name of the article's author
- views: the number of times the article has been accessed to date 

#### daily_error_summary
```sql
CREATE VIEW daily_error_summary AS
SELECT time::date AS date,
COUNT(*) FILTER (WHERE status = '404 NOT FOUND') AS error_404,
COUNT(*) AS access_request
FROM log
GROUP BY time::date;
```

*daily_error_summary* creates a table showing the number of *404 NOT FOUND* errors and total access requests for each day.
- date: date summarized by the row
- error_404: the number of *404 NOT FOUND* errors for the site on that date
- access_requests: the total number of hits for the site, including successful and unsuccessful requests, for that day

