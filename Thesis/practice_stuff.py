import requests

data = requests.get( 'https://api.hearthstonejson.com/v1/91456/all/cards.collectible.json' ).json()
#https://api.hearthstonejson.com/v1/25770/all/cards.collectible.json

for card in data:
        card_name_api = card['name']['enUS']
        card_name_api = card_name_api.lower()
        card_name_api = card_name_api.replace('-' , ' ')
        card_name_api = card_name_api.replace('(' , '')
        card_name_api = card_name_api.replace(')' , '')
        if 'flurry rank 1' == card_name_api:
                print('yas')
                card_description = card['text']['enUS']
                print(card_description)
        #print(card_name_api)
                #print(card['name']['enUS'], card['type'], card['cost'] , card['text']['enUS'])
                #print('Good')
