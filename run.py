# Python 3.5.2

import psycopg2


# Name of the database
DBNAME = "news"
# When this is set to False the program quits
runner = True


# Prints the three most popular articles
def popular_articles():
    global runner

    # Opens the database
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # SQL query
    c.execute("""
    SELECT title, count(*)
    FROM log, articles
    WHERE log.path = '/article/' || articles.slug
    AND path LIKE '/article/%'
    GROUP BY 1
    ORDER BY 2 DESC
    LIMIT 3;
    """)

    # Post-processing and printing of the query
    response = c.fetchall()
    db.close()
    count = 1
    print("")
    for n in response:
        print(str(count) + ") " + n[0] + ". - " + str(n[1]) + " views")
        count += 1

    # Menu options
    print("")
    print("Enter M for the menu or Q to quit")
    option = str(input("-> ")).lower()
    if option == "q":
        runner = False


# Prints the authors sorted by article views
def author_views():
    global runner

    # Opens the database
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # SQL query
    c.execute("""
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
    """)

    # Post-processing and printing of the query
    response = c.fetchall()
    db.close()
    count = 1
    print("")
    for n in response:
        print(str(count) + ") " + n[0] + " - " + str(n[1]) + " views")
        count += 1

    # Menu options
    print("")
    print("Enter M for the menu or Q to quit")
    option = str(input("-> ")).lower()
    if option == "q":
        runner = False


# Prints any dates with an error rate over 1%
def error_rate():
    global runner

    # Opens the database
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    # SQL query
    c.execute("""
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
    """)

    # Post-processing and printing of the query
    response = c.fetchall()
    db.close()
    print("")
    for n in response:
        print(str(n[0]) + " - " + str(n[1]) + "%")
    print("")
    print("Enter M for the menu or Q to quit")
    option = str(input("-> ")).lower()
    if option == "q":
        runner = False


#  Program runner
def run():
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


run()
