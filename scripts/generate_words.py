"""
Helper script to generate JSON files in the required format

Huge thanks to Datamuse for this cool API!
Credits: Datamuse API
API Reference: https://www.datamuse.com/api/
"""

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


def get_words_starting_with(letters, limit=10):
    """
    Gets words starting with the letters provided from datamuse API abd
    creates the JSON file in the relevant directory.

    :type letters: `str`
    :param letters: can be a single letter or the starting letters of a word

    :type limit: `int`
    :param limit: number of words to be returned

    :raises: Assertion Error if the limit is over 100

    :rtype: None
    """
    if limit > 100:
        raise AssertionError('Take it easy! Sorry, Setting the limit to 100.')

    params = {
        'sp': letters+'*',  # Spelled like
        'md': 'p,d',  # metadata part of speech, defn
        'max': limit
    }
    resp = requests.get(BASE_API, params=params)
    data = resp.json()

    for entry in data:
        _generate_json(entry)


def _generate_json(data):
    """
    Generates the JSON in the required format
    :type data: `dict`
    :param data: data from datamuse API

    :rtype: None
    """

    if 'tags' not in data:
        return None
    elif data['tags'][0] not in PART_OF_SPEECH:
        return None
    else:
        if 'defs' not in data:
            return None

        pos = data['tags'][0]
        defns = data['defs']
        for defn in defns:
            # list consisting of part of speech and it's definition
            pos_def = defn.split('\t')
            if pos_def and pos_def[0] in PART_OF_SPEECH:
                word_json = {
                    "word": data['word'].capitalize(),
                    "definitions": [pos_def[1]],
                    "parts-of-speech": PART_OF_SPEECH[pos]
                }
                _create_file(word_json)


def _create_file(json_data):
    """
    Creates the JSON file in the relevant folder only if the file does
    not exist already(Meaning, duplicate words are not allowed)

    :type json_data: `dict`
    :param json_data: data in the format to be written into the file

    :raises: Assertion Error if the letter directory is not found

    :rtype: None
    """
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


if __name__== "__main__":
    """
    Main to call to master function

    Format to invoke the master func:
        get_words_starting_with(some_letter_you)
    
    Example:
        get_words_starting_with('ap')    
    """

    get_words_starting_with('Y', limit=20)