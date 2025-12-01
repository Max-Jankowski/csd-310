# Max Jankowski
# Amended from module 6

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
} #thus far this has been a copy of module 6, I will include the env file to allow program to run without 
    #modifying login code. 

def show_films(cursor, title): # defining the function to display the movies list, will be called afer each action required 
    query = """ 
        SELECT 
            film_name AS Name, 
            film_director AS Director, 
            genre_name AS Genre, 
            studio_name AS Studio
        FROM film 
        INNER JOIN genre ON film.genre_id = genre.genre_id 
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """
    #above is a multi line string that contains the query commands to display movies list as descriped 
    cursor.execute(query) # used to execute the query insructions 
    films = cursor.fetchall() #collects information 
    
    print("\n-- {} --".format(title)) #print function to display title 
    
    for film in films: # loop to provide results and display each film
        print("Film Name: {}\nDirector: {}\nGenre Name: {}\nStudio Name: {}\n".format(
            film[0], film[1], film[2], film[3]))




try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database 

    # output the connection status 
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                       config["database"]))

    input("\n\n  Press any key to continue...")

    cursor = db.cursor() # creates a cursor 
    
    show_films(cursor, "DISPLAYING FILMS") # calls show_films function to display inital data 
    
    # inserting new title and info into film table. first line defines columns and values line input information on the shining 
    insert_query = """  
        INSERT INTO film (film_name, film_director, genre_id, studio_id, film_releaseDate, film_runtime)
        VALUES ('The Shining', 'Stanley Kubrick', 1, 1, '1980', 146)
    """
    cursor.execute(insert_query)
    db.commit() # saves changes into table
    
    show_films(cursor, "DISPLAYING FILMS AFTER INSERT") #call once again to the function to display current state, with added movie
    
    # performing a query to update genre info to the alien movie
    update_query = """
        UPDATE film 
        SET genre_id = 1 
        WHERE film_name = 'Alien'
    """
    cursor.execute(update_query)
    db.commit() # once again commiting changes and saving data 

    
    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE") # calling display function to show changes 
    
    # final query request to delete movie 
    delete_query = """
        DELETE FROM film 
        WHERE film_name = 'Gladiator'
    """
    cursor.execute(delete_query)
    db.commit()
    
    show_films(cursor, "DISPLAYING FILMS AFTER DELETE") # final call to the function to show final changes in data 

# the last of the code is just the copy of the end of module 6 code 
except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """

    db.close()

# https://www.teachoo.com/22106/4582/Performing-insert--update--delete-queries-using-cursor/category/Concepts/#google_vignette
# https://stackoverflow.com/questions/54081058/how-to-insert-or-update-in-sql-using-python
# https://stackoverflow.com/questions/5243596/python-sql-query-string-formatting
# https://docs.sqlalchemy.org/en/20/tutorial/data_update.html
