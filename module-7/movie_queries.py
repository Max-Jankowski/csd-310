# Max Jankowski
# copied from assignment module6
# added code for module 7

""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode

import dotenv # to use .env file
from dotenv import dotenv_values

#using our .env file
secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database 

    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                       config["database"]))

    input("\n\n  Press any key to continue...")

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)
# all about copied form last week assignment, removed the finally argument

# first query to display all studios, sorry for more then 3 I added 10 movies
print("-- DISPLAYING Studio RECORDS --") # Formated with -- to draw attention and be a seperator 
cursor = db.cursor()                    # Cursors to execute SQL commands
cursor.execute("SELECT studio_id, studio_name FROM studio") #SQL command to display all names from the studio table

studios = cursor.fetchall()

for studio in studios:
    print("Studio ID: {}\nStudio Name: {}\n".format(studio[0], studio[1])) # print query results, formating for dispaly 
                                                                        # {} acts as a place holder and the .format() inserts values retreived 
# Second query displaying all genres. Again, I added some
print("-- DISPLAYING Genre RECORDS --")
cursor = db.cursor()
cursor.execute("SELECT genre_id, genre_name FROM genre") #SQL command to show all genres from the genre table

genres = cursor.fetchall()

for genre in genres:
    print("Genre ID: {}\nGenre Name: {}\n".format(genre[0], genre[1])) #Just as the last print call, just replaced string display and variables calls

# Third query to display films with runtime less than 2 hours 
print("-- DISPLAYING Short Film RECORDS --")
cursor = db.cursor()
cursor.execute("SELECT film_name, film_runtime FROM film WHERE film_runtime < 120") #These print arguments all are pretty copy and paste 
                                                                                    # other than the SQL commands
films = cursor.fetchall()

for film in films:
    print("Film Name: {}\nRuntime: {}\n".format(film[0], film[1]))

# Last query to display film names and directors ordered by director
print("-- DISPLAYING Director RECORDS in Order --")
cursor = db.cursor()
cursor.execute("SELECT film_name, film_director FROM film ORDER BY film_director")

directors = cursor.fetchall()

for director in directors:
    print("Film Name: {}\nDirector: {}\n".format(director[0], director[1]))


    db.close() #closing the database connection