# Logs Analysis

This program analyses a website database and prints 3 analyses.

1) Most popular articles
2) Authors sorted by article views
3) Dates with an error rate over 1%

## Install

Can be installed from github repository.

`git clone
https://github.com/jakec-github/logs_analysis.git`

## Usage

To run the analysis run the run.py module using python 3 eg:

`python3 run.py`

Before running the program please check the requirements section.

The program does not require the creation of any views in the database.

A menu will prompt the user to select an analysis and then print the results to the console.

## Requirements

This program requires the python module [psycopg2](http://initd.org/psycopg/). This module is a PostgreSQL adaptor for python and can be installed using pip eg:

`pip install psycopg2`
or
`pip3 install psycopg2`
