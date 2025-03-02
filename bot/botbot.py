import search_json
import syn_detection
from data_utils.data_load import get_query_objects
from spellchecker import SpellChecker
import random
import requests
from googletrans import Translator

TEXT_BODY_PATH = './text/atlantis.txt'
ENTITY_DICT_PATH = 'data_utils/entity_dict.json'
greetings = syn_detection.detect_syn("hello")
responses = ["I'm sorry, I don't understand.",
             "I am unsure what you are asking me.",
             "Sorry, I only want to talk about Atlantis and Treasure",
             "Ask me about Atlantis or Treasure.",
             "Your words make no sense to me.",
             "I know nothing about that topic."]


def spell_check(input):
    """
    Takes a string and returns a string with closest related permutation that is part of the english language.

    Parameter:
        input: a string input  

    Returns:
        correct: a corrected string output 
    """
    spell = SpellChecker()
    err = input.split()
    correct = []
    for word in err:
        word = spell.correction(word)
        correct.append(spell.correction(word))
    return " ".join(correct)


def get_translate(phrase):
    """
    This function takes a phrase and returns a translated phrase.
    
    Parameter:
        phrase: a string input by the user acting as the key for keywords
        
    Returns:
        output: a string containing the translated phrase
    """
    translator = Translator()
    result = translator.translate(phrase, dest='en')
    print("translated: " + phrase.split(maxsplit=1)[1])
    return result.text

def get_coordinates(address):
    """
    This function takes an address and returns the coordinates of the address.

    Parameter:
        address: a string input by the user acting as the key for keywords
    
    Returns:
        coordinates: a list of coordinates
    """
    API_KEY = 'API KEY HERE'
    address = address.replace(' ', '+')
    params = {
        'key': API_KEY,
        'address': address
    }
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        result = data['results'][0]
        location = result['geometry']['location']
        coordinates = "Oh thats " + '{:.2f}'.format(location['lat']) + " Latititude and " + '{:.2f}'.format(location['lng'])+"Longitude"
        return coordinates
    else:
        print('Error:', data)

def get_response(query):
    """
    This function recieves the keyword dictionary, asks for user input, and returns chat bot responses. 
    User input is processed using get_query_objects(), which extracts nouns and propper nouns. 
    A for-loop iterates through each processed noun in a list and detects if the word exists in entity_dict.json. 
    If there is a match, that means there is a chat bot response for the keyword. If there is no keyword detected in the user response, 
    then the bot returns "Sorry can't help provide any information that relates to [whatever related noun the user entered]".

    Parameter:
        response: a string input by the user acting as the key for keywords
        entity_dict: a .json file generated from entity_dict.py
    
    Returns:
        output: a string containing the bots response
    """
    
    #entity_dict = get_entity_dict(ENTITY_DICT_PATH)
    if "translate" in query:
        return get_translate(query.split(maxsplit=1)[1])
    if "navigate" in query:
        return get_coordinates(query.split(maxsplit=1)[1])
    response = []
    # Find the objects in the user query
    for greeting in greetings:
        if greeting in query.lower().split():
            return "Hi! Great to meet you. Are you going to ask me some questions?"
    query_objects = get_query_objects(query)
    if query_objects is None:
        return responses[random.randint(0, len(responses) - 1)]
    else:
        response = search_json.search_noun_quest(query_objects[0], query_objects[1])
    # for obj in query_objects:
    #
    #     if obj in entity_dict:
    #         response.append(entity_dict[obj])
    #     else:
    #         # Satisfies 5 possible responses for out of topic questions
    #         return responses[random.randint(0, len(responses))]

    return " ".join(response)
