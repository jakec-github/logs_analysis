#!/usr/bin/env python3

import psycopg2


# Name of the database
DBNAME = "news"
# When this is set to False the program quits
runner = True


def execute_query(query):
    """ Execute_query takes an SQL query as a parameter.
    Executes the query and returns the results as a list of tuples """
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        response = c.fetchall()
        db.close()
        return response
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if c is not None:
            db.close()


def menu_options():
    """ Menu to display after a query """
    global runner

    print("")
    print("Enter M for the menu or Q to quit")
    option = str(input("-> ")).lower()
    if option == "q":
        runner = False


def popular_articles():
    """ Prints the three most popular articles """

    # Retrieves data
    query = """
    SELECT title, numViews
    FROM articles,
        (select path, count(path) as numViews
                       from log
                       where status like '%200%'
                       group by log.path) as log
    WHERE log.path = '/article/' || articles.slug
    AND path LIKE '/article/%'
    ORDER BY numViews DESC
    LIMIT 3;
    """
    response = execute_query(query)

    # Post-processing and printing of the query
    count = 1
    print("")
    for title, numViews in response:
        print("{}) {}. - {} views".format(str(count), title, str(numViews)))
        count += 1

    menu_options()


def author_views():
    """ Prints the authors sorted by article views """

    # Retrieves data
    query = """
    SELECT name, views
    FROM authors,
    (
      SELECT author, count(*) as views FROM log, articles
      WHERE log.path = '/article/' || articles.slug
      AND path LIKE '/article/%'
      GROUP BY 1
    ) AS viewcount
    WHERE author = authors.id
    ORDER BY views DESC;
    """
    response = execute_query(query)

    # Post-processing and printing of the query
    count = 1
    print("")
    for name, numViews in response:
        print("{}) {} - {} views".format(str(count), name, str(numViews)))
        count += 1

    menu_options()


def error_rate():
    """ Prints any dates with an error rate over 1% """

    # Retrieves data
    query = """
    SELECT * FROM (
      SELECT requests.date,
      ROUND(fails.number*1.0/requests.number*100.0, 2)
      AS failure_percentage
      FROM (
        SELECT DATE(time) AS date, count(*) AS number FROM log
        WHERE log.status SIMILAR TO '(4|5)%'
        GROUP BY date
        ORDER BY number DESC
      ) AS fails JOIN
      (
        SELECT DATE(time) AS date, count(*) AS number FROM log
        GROUP BY date
        ORDER BY number DESC
      )AS requests
      ON fails.date = requests.date
      ORDER BY failure_percentage DESC
    ) AS results
    WHERE failure_percentage > 1;
    """
    response = execute_query(query)

    # Post-processing and printing of the query
    print("")
    for date, errors in response:
        print("{} - {}%".format(str(date), str(errors)))

    menu_options()


def run():
    """ Program runner """
    global runner
    while runner:
        print("")
        print("Select an option by number")
        print("")
        print("1 > View 3 most popular articles")
        print("2 > View authors by popularity")
        print("3 > View days with dates with error rate over 1%")
        print("")
        print("Enter Q to quit")

        # Handles menu options
        menu = True
        while menu:
            option = input("-> ").lower()
            if option == "1":
                popular_articles()
                menu = False
            elif option == "2":
                author_views()
                menu = False
            elif option == "3":
                error_rate()
                menu = False
            elif option == str("q"):
                runner = False
                menu = False
            else:
                print("")
                print("Invalid response")
                print("")


if __name__ == '__main__':
    run()
