-- This file handles the initial setup of the news database for the
-- Udacity Fullstack nanodegree Logs Analysis project
-- It creates a database called news, imports the schema and mock data
-- for news from newsdata.sql, and adds custom views.

-- Create a fresh version of the news database
DROP DATABASE IF EXISTS news;
CREATE DATABASE news;
\c news

-- newsdata.sql contains the schema for news, along with mock data
\i newsdata.sql 

-- article_views displays a table of articles with their author and view count
CREATE VIEW article_views AS 
SELECT articles.title, authors.name as author, log.views
FROM articles INNER JOIN
    (SELECT path, count(*) as views
    FROM log 
    GROUP BY path) AS log
ON '/article/' || articles.slug = log.path
LEFT JOIN authors 
ON articles.author = authors.id;

-- daily_error_summary displays a table summarizing the error rate for each day
-- as a percent.
CREATE VIEW daily_error_rates AS
SELECT time::date AS date,
    100 * (COUNT(*) FILTER (WHERE status = '404 NOT FOUND') / 
           COUNT(*)::numeric) AS error_percent
FROM log
GROUP BY time::date;