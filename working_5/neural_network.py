from typing import final
import mysql.connector as mysql
import numpy as np
import pandas as pd
import pymysql
import random
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from operator import ne
from typing import NewType, final
from numpy.core.function_base import _logspace_dispatcher
from numpy.lib.nanfunctions import _nanquantile_ureduce_func
from numpy.lib.shape_base import _apply_over_axes_dispatcher
from sklearn.linear_model import LinearRegression
import itertools
from sklearn.preprocessing import StandardScaler

#from working_3_.hill_climbing_3 import Deck
#from run_models import *



## connecting to the database using 'connect()' method
## it takes 3 required parameters 'host', 'user', 'passwd'
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "thesis2021",
    database = "hearthstone"
)


##########################
### Database Beginning ###
##########################

#print(db) # it will print a connection object if everything is fine

## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()

 ## defining the Query for decks
query1 = "SELECT * FROM decks"

## getting records from the table
cursor.execute(query1)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

column_list = [ 'deck_id' , 'card1' , 'card2', 'card3' , 'card4', 'card5' , 'card6', 'card7' , 'card8', 'card9' , 'card10', 'card11' , 'card12', 'card13' , 'card14', 'card15' , 'card16', 'card17' , 'card18', 'card19' , 'card20','card21' , 'card22', 'card23' , 'card24', 'card25' , 'card26', 'card27' , 'card28', 'card29' , 'card30', 'win_rate' , 'deck_type']

dataframe_decks = pd.DataFrame(records)
dataframe_decks.columns = column_list
dataframe_decks = dataframe_decks.replace(r'^\s*$', np.nan, regex=True)

 ## defining the Query
query2 = "SELECT * FROM cards"

## getting records from the table
cursor.execute(query2)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

column_list = ['card_id' , 'card_name', 'card_cost' , 'card_type' , 'card_description', 'card_health' , 'card_attack']
dataframe_cards = pd.DataFrame(records)
dataframe_cards.columns = column_list
dataframe_cards = dataframe_cards.replace(r'^\s*$', np.nan, regex=True)
#print(dataframe_decks)


########################
### PART 0: GET INFO ###
########################

decks_and_ids = dataframe_decks.iloc[: , 0:31]
decks = decks_and_ids.iloc[: , 1:31]
target_class = dataframe_decks[['win_rate']]

#################################################
### PART 1: CONVERT TO NUMPY/STANDARDIZE DATA ###
#################################################

X = decks.to_numpy()
Y = target_class.to_numpy()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

sc_X = StandardScaler()
X_trainscaled = sc_X.fit_transform(X_train)
X_testscaled = sc_X.transform(X_test)
Y_trainscaled = sc_X.fit_transform(Y_train)
Y_testscaled = sc_X.transform(Y_test)

################################
### PART 2: TRAIN REGRESSION ###
################################

mlp = MLPRegressor(random_state=1, max_iter=500)
neural1 =  mlp.fit(X_trainscaled , Y_trainscaled)

print(X_trainscaled[0])
print(neural1.predict(X_trainscaled[0].reshape(1,-1)))
print(Y_trainscaled[0])
#X_final = sc_X.inverse_transform(Y_trainscaled)
#print(X_final[0])





########################
### Combine 30 Cards ###
########################

#print(dataframe_cards)

#id_Cards = dataframe_cards[['card_id']]
#print(id_Cards)
#id_Cards_array = id_Cards.values.tolist()






