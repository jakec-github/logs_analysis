# Logs Analysis

This program analyses a website database and prints 3 analyses.

1. Most popular articles
2. Authors sorted by article views
3. Dates with an error rate over 1%

## Install

Can be installed from github repository.

`git clone
https://github.com/jakec-github/logs_analysis.git`

## Usage

### Running the program

To run the analysis navigate to the logs_analysis directory and run the run.py module using python 3 eg:

`python3 run.py`

Before running the program please check the requirements section and setup the database as detailed below.

### Setting up the database

To setup the database navigate to the logs_analysis directory and use PostgreSQL to create a database named news:

`CREATE DATABASE news`

Then complete database setup by running the newsdata.sql file with the following command:

`psql -d news -f newsdata.sql`

### Additional information

The program does not require the creation of any views in the database.

A menu will prompt the user to select an analysis and then print the results to the console.

## Requirements

This program requires the python module [psycopg2](http://initd.org/psycopg/). This module is a PostgreSQL adaptor for python and can be installed using pip eg:

`pip install psycopg2`
or
`pip3 install psycopg2`
