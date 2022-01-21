import requests
import re

#Get specific deck in list of decks. Deck Num will be the deck in the list of decks
def get_deck(names, deck_types, win_ps , cards_lists , card_counts , deck_num):
    
    name = names[deck_num]
    deck_type = deck_types[deck_num]
    win_p = win_ps[deck_num]
    card_list = cards_lists[deck_num]
    card_count = card_counts[deck_num]

    return name, deck_type , win_p , card_list , card_count

# Function that removes duplicates in list 
def remove_dup(list_main):
    return_list = []
    for i in list_main:
        if i not in return_list:
            return_list.append(i)
            
    return return_list


# Retrieve Deck Data which includes : deck name , deck type , win percent of deck , cards , # of each card , 
def retrieve_data(filename):
    deck_name , class_type , deck_win_percentage = '' , '' , ''
    deck_name_list, class_type_list , win_percent_list , lil_array , lil_array1 = [] , [] , [] , [] , []
    big_array , big_array1  = [[]] , [[]]

    with open(filename,'r') as file:

        # reading each line    
        for line in file:
            # reading each word        
            for words in line.split('href="/decks/'):
                if 'url(&quot;https://static.hsreplay.net/static/images/64x/class-icons' in words :
                    deck_name = words
                    deck_name = words.split(';);">',1)[1] 
                    deck_name = deck_name.split(';);">',1)[1]
                    deck_name = deck_name.split('</h3',1)[0]
                    deck_name_list.append(deck_name)
                if 'data-card-class=' in words :
                    class_type = words 
                    class_type = words.split('data-card-class="' , 1)[1]
                    class_type = class_type.split('"' , 1)[0]
                    class_type_list.append(class_type)
                if 'class="win-rate">' in words :
                    deck_win_percentage = words 
                    deck_win_percentage = words.split('"win-rate">' , 1)[1] 
                    deck_win_percentage = deck_win_percentage.split('<' , 1)[0] 
                    win_percent_list.append(deck_win_percentage)

            for words in line.split('href="/c'):
                if 'ards/' in words:
                    words = words.split("/" , 1)[1] 
                    words = words.split("/" , 1)[1] 
                    words = words.split('"', 1)[0] 
                    words = words.replace('-' , ' ')
                    lil_array.append(words)
                if 'href="/decks/' in words :
                    big_array.append(lil_array)
                    lil_array = []   
            big_array.append(lil_array)

            for words in line.split('class="card-icon"'):
                if 'aria-label="' in words :
                    words = words.split("style" , 1)[0] 
                    if '2' in words:
                        count = 2
                    else:
                        count = 1
                    lil_array1.append(count)
                if 'href="/decks/' in words :
                    print(2)
                    big_array1.append(lil_array1)
                    lil_array1 = [] 
            big_array1.append(lil_array1)

        # displaying the words    
        big_array = remove_dup(big_array)     
        big_array1 = remove_dup(big_array1)     
        del big_array1[0]
        del big_array[0]
        cards_list = big_array
        num_of_cards = big_array1
        return deck_name_list , class_type_list, win_percent_list, cards_list, num_of_cards

# Function that takes card's name and return information about card, will be used as function for all cards in deck
def get_card_info(card_name):

    card_cost = ''
    card_type = ''
    card_description = ''
    card_health = ''
    card_attack = ''


    data = requests.get( 'https://api.hearthstonejson.com/v1/91456/all/cards.collectible.json' ).json()

    for card in data:
        card_name_api = card['name']['enUS']
        card_name_api = card_name_api.lower()
        card_name_api = card_name_api.replace('-' , ' ')
        card_name_api = card_name_api.replace('(' , '')
        card_name_api = card_name_api.replace(')' , '')
        if card_name_api == card_name:
            print('Got card')
            try:
                card_description = card['text']['enUS']
                
            except  KeyError as ke:
                card_description = ''
            try:
                card_cost =  card['cost'] 
                
            except  KeyError as ke:
                card_cost =  'none' 
            try:
                card_type = card['type']
                
            except  KeyError as ke:
                card_type = 'none'
            try:
                card_health = card['health']
                
            except KeyError as ke:
                card_health = ''
            try:
                card_attack = card['attack']
                
            except KeyError as ke:
                card_attack = ''

    return card_name_api , card_cost , card_type , card_description, card_health , card_attack

#########################################################
### Following Functions for Pushing cards to Database ###
#########################################################

def push_card_data(deck_list):
    insert_list = []
    for card_list in deck_list:
        for card in card_list:
            card_name , card_cost , card_type , card_description, card_health , card_attack = get_card_info(card)
            value_ = (card_name , card_cost , card_type , card_description, card_health , card_attack)
            insert_list.append(value_)
    return insert_list


# Defining main function
def main():

    filename = 'two_decks-text.txt'

    deck_name_list , class_type_list , deck_win_percentage_list , card_names_lists , card_count_list= retrieve_data(filename)

    deck_name , class_type , deck_win_percentage, card_names, card_count = get_deck(deck_name_list , class_type_list , deck_win_percentage_list , card_names_lists , card_count_list, 0)

    cards = push_card_data(card_names_lists)
    


  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()