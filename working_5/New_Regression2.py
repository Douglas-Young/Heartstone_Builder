from math import nan
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
from sklearn.decomposition import PCA
from collections import Counter
from auto_encoder import *
#################
### FUNCTIONS ###
#################
# function to return key for any value
def get_key(val , diction):
    for key, value in diction.items():
         if val == value:
             return key
 
    return "key doesn't exist"
def createList(r1, r2):
    return list(range(r1, r2+1))
# Split Cards Into The Stats and Description Tables
def get_card_cols(df):
    cols_dictionary = df["card_description"]
    cols_stat = df.drop("card_description" , 1)
    cards_table_stats = cols_stat.to_numpy()
    cards_table_description = cols_dictionary.to_numpy()
    return cards_table_stats , cards_table_description
def dictionary_function(numpy_arr):
    new_num_list = []
    num_list = numpy_arr.tolist()
    for x in num_list:
        x = str(x)
        y = x.split()
        for z in y:
            new_num_list.append(z)
    res = []
    for i in new_num_list:
        if i not in res:
            res.append(i)
    new_num_list = res
    #print(len(new_num_list))   #length = 846 and was 46336
    list_4675 = list(range(0, 846))
    #print(len(list_4675))      #length is also 846

    main_dict = dict(zip(list_4675, new_num_list))
    new_desc_vector = []
    new_desc_v_deck = []
    for card_x in numpy_arr:
        card_x = str(card_x)
        list_main = [0] * 846
        y = card_x.split()
        for z in y:
            key_z = get_key(z , main_dict)
            list_main[key_z] = list_main[key_z] + 1
        new_desc_vector.append(list_main)
        
    return new_desc_vector
  
def filter_cards(numpy_arr ,numpy_desc):
    i = 0 
    for card_x in numpy_arr:
        card_x[0] = int(card_x[0])
        # card_1 = card_x[1] does same thing as ID 
        if card_x[1] == 'none':
            card_x[1] = -1
        else: 
            card_x[1] = int(card_x[1])
        if card_x[2] == "SPELL":
            card_x[2] = 0
        elif card_x[2] == "MINION":
            card_x[2] = 1
        else:
            card_x[2] = 2
        card_x[3] = int(card_x[3])
        card_x[4] = int(card_x[4])
        card_x = np.append(card_x, numpy_desc[i])
        i += 1
    return numpy_arr

def run_auto_encoder(numpy_arr):
    X_train, X_test, Y_train, Y_test = train_test_split(numpy_arr, numpy_arr, test_size=0.4, random_state=42)
    sc_X = StandardScaler()
    X_trainscaled = sc_X.fit_transform(X_train)
    X_testscaled = sc_X.transform(X_test)
    Y_trainscaled = sc_X.fit_transform(Y_train)
    Y_testscaled = sc_X.transform(Y_test)

    autoencoder.fit(X_trainscaled, X_trainscaled,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(X_testscaled, X_testscaled))
    encoded_imgs = encoder.predict(X_testscaled)
    print(encoded_imgs)
    return 0
def run_PCA_(numpy_arr):
    #sc_X = StandardScaler()
    #numpy_arr = sc_X.fit_transform(numpy_arr)
    pca = PCA(n_components=1)
    #print(numpy_arr)
    numpy_arr = pca.fit_transform(numpy_arr)
    #print("PCA\n")
    #print(numpy_arr)
    #print(results.singular_values_)
    #print(numpy_arr.shape)

    return numpy_arr



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
dataframe_cards = dataframe_cards.fillna(-1)
dataframe_decks = dataframe_decks.fillna(-1)
dataframe_cards_new = dataframe_cards.drop("card_name" , 1)

cards_stats , cards_descriptions = get_card_cols(dataframe_cards_new)
dictionary_new = dictionary_function(cards_descriptions)
description_PCA = run_PCA_(dictionary_new)
#print(description_PCA)
filtered_card_stats = filter_cards(cards_stats , description_PCA)
#run_auto_encoder(filtered_card_stats)
single_val_cards = run_PCA_(filtered_card_stats)
#print(single_val_cards[1])




##############################
### SECTION 0: CARD VECTOR ###
##############################

###
# Connect card ID from Deck to card data pulled 
###

#print(dataframe_cards.iloc[0])

###############################
### PART 0: GET DECKS/CARDS ###
###############################


#####################################
### SECTION 1: RUN MLP REGRESSION ###
#####################################

### PART 0: GET INFO ###
########################

decks_and_ids = dataframe_decks.iloc[: , 0:31]
decks = decks_and_ids.iloc[: , 1:31]
target_class = dataframe_decks[['win_rate']]

#################################################
### PART 1: CONVERT TO NUMPY/STANDARDIZE DATA ###
#################################################

X = decks.to_numpy()
#print(X)
Y = target_class.to_numpy()

#sprint(X.shape)

list_1 = []
list_2 = []
card_list_deck1 = []
card_list_deck2 = []
deck_list1 = []
deck_list2 = []
i = 0
#range(len(X))
for i in range(len(X)):
    #print(i)
    for x in X[i]: 
        card_list_deck1.append(single_val_cards[x])
    #card_list_deck1_numpy = np.array(card_list_deck1)
    deck_list1.append(card_list_deck1)
    card_list_deck1 = [] 

numpy_array_1 = np.array(deck_list1)
numpy_array_1 = np.reshape(numpy_array_1 , (277,30))
#print(numpy_array_1)
#print(numpy_array_1.shape)
#print(numpy_array_1.shape)
#use numpy_array_1 as x  to 
#print(len(numpy_array_1))
#print(len(Y))

X_train, X_test, Y_train, Y_test = train_test_split(numpy_array_1, Y, test_size=0.33, random_state=42)

#sc_X = StandardScaler()
#X_trainscaled = sc_X.fit_transform(X_train)
#X_testscaled = sc_X.transform(X_test)
#Y_trainscaled = sc_X.fit_transform(Y_train)
#Y_testscaled = sc_X.transform(Y_test)

################################
### PART 2: TRAIN REGRESSION ###
################################

mlp = MLPRegressor(random_state=1, max_iter=500)
neural1 =  mlp.fit(X_train , Y_train)

#print(X_train[1])
#print(neural1.predict(X_train[1].reshape(1,-1)))
#print(Y_train[1])
for i in range(20):
    print(i)
    #print(X_test[i])
    print(neural1.predict(X_test[i].reshape(1,-1)))
    print(Y_test[i])

#X_final = sc_X.inverse_transform(Y_trainscaled)
#print(X_final[0])




########################
### Combine 30 Cards ###
########################

#print(dataframe_cards)

#id_Cards = dataframe_cards[['card_id']]
#print(id_Cards)
#id_Cards_array = id_Cards.values.tolist()