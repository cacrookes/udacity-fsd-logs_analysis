# Logs Analysis

## Project Description

TODO

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

TODO
