import mysql.connector as mysql

# importing  all the
# functions defined in test.py
from functions_ import *


filename = 'two_decks-text.txt'
deck_name_list , class_type_list , deck_win_percentage_list , card_names_lists , card_count_list= retrieve_data(filename)
## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'passwd'
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "thesis2021",
    database = "hearthstone"
)

card_values = push_card_data(card_names_lists)



print(db) # it will print a connection object if everything is fine

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

## first we have to 'drop' the table which has already created to create it again with the 'PRIMARY KEY'
## 'DROP TABLE table_name' statement will drop the table from a database
cursor.execute("DROP TABLE cards")

## creating a table called 'cards' in the 'hearthstone' database
## card_name_api , card_cost , card_type , card_description, card_health , card_attack
cursor.execute("CREATE TABLE cards (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY , name VARCHAR(255), card_cost VARCHAR(255), card_type VARCHAR(255) , card_description VARCHAR(255) , card_health  VARCHAR(255), card_attack VARCHAR(255))")

## getting all the tables which are present in 'datacamp' database
cursor.execute("SHOW TABLES")


## creating the 'cards' table with the 'PRIMARY KEY'
#####cursor.execute("CREATE TABLE cards (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), mana_count VARCHAR(255))")

## defining the Query
query = "INSERT INTO cards (name, card_cost , card_type , card_description, card_health , card_attack) VALUES (%s, %s, %s, %s, %s, %s)"
## storing values in a variable
#####values = ("Douglas", "1")

## executing the query with values
cursor.execute(query, card_values)

## to make final output we have to run the 'commit()' method of the database object
db.commit()

####print(cursor.rowcount, "record inserted")

## defining the Query
query = "SELECT * FROM cards"

## getting records from the table
cursor.execute(query)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

## Showing the data
for record in records:
    print(record)