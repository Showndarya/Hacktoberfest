import requests
import os
import json


BASE_API = 'https://api.datamuse.com/words/'
PART_OF_SPEECH = {
    'adj': 'Adjective',
    'adv': 'Adverb',
    'n': 'Noun',
    'v': 'Verb'
}


def get_words_starting_with(letter, limit=10):

    if limit > 100:
        print ('Take it easy! Sorry, Setting the limit to 100.')
        limit = 100

    params = {
        'sp': letter+'*',  # Spelled like
        'md': 'p,d',  # metadata part of speech, defn
        'max': limit
    }
    resp = requests.get(BASE_API, params=params)
    data = resp.json()

    for data in resp:
        _generate_json(data)


def _generate_json(data):

    if not data['tags']:
        return None
    elif data['tags'][0] not in PART_OF_SPEECH:
        return None
    else:
        pos = data['tags'][0]
        defns = data['defs']
        for defn in defns:
            # list consisting of part of speech and it's definition
            pos_def = defn.split('\t')
            if pos_def and pos_def[0] in PART_OF_SPEECH:
                word_json = {
                    "word": data['word'],
                    "definitions": [pos_def[1]],
                    "parts-of-speech": PART_OF_SPEECH[pos]
                }
                _create_folder(word_json)


def _create_folder(json_data):

    letter = json_data['word'][0].upper()
    current_path = os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.abspath(os.path.join(current_path, os.pardir))

    directory_entries = os.listdir('.')
    if letter in directory_entries:
        file_name = json_data['word'].capitalize() + '.json'
        letter_file_path = os.path.join(parent_directory, letter)
        path = os.path.join(letter_file_path, file_name)
        letter_files = [letter_file.lower()
                        for letter_file in os.listdir(letter_file_path)]
        if file_name.lower() not in letter_files:
            with open(path, 'w') as fp:
                json.dump(json_data, fp)
    else:
        raise AssertionError('Letter: {} directory not found'.format(letter))

