"""
Script that generates word definition by the input data of words and
creates new files or updates existing definitions

Before you start
    1. create new virtual environment with python3
    2. pip install requests
    3. pip install bs4

You are ready!
Just add your favourite words in the list at the end of the file and
    Run script: 'python web_scrapper.py'

Before you commit check if the word definition is appropriate

Have fun :)

"""

import json
import os
import requests
import time

from bs4 import BeautifulSoup

OXFORD_URL = "https://en.oxforddictionaries.com/definition/"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PARTS_OF_SPEECH = [
    "Noun",
    "Pronoun",
    "Verb",
    "Adverb",
    "Adjective",
    "Preposition",
    "Conjunction",
    "Interjection",
]


def build_api_url(word):
    return OXFORD_URL + word


def download_page(url):
    try:
        return requests.get(url).text
    except Exception as e:
        print("Error: Bad URL")


def parse_html(word, html_doc):
    """
    Function parses page html and gets all definitions of given word for available parts of speech
    """
    result = list()
    found_pos = []

    soup = BeautifulSoup(html_doc, 'html.parser')

    sections = soup.findAll("section", {"class": "gramb"})
    # print(sections, len(sections))

    for section in sections:
        full_definition = {
            "word": None,
            "definitions": list(),
            "parts-of-speech": None
        }

        try:
            part_of_speech = section.find('span').string.title()
        except Exception as e:
            print("No string argument ", word)
            continue
        if part_of_speech in PARTS_OF_SPEECH and part_of_speech not in found_pos:
            full_definition["word"] = word.title()
            full_definition["parts-of-speech"] = part_of_speech
            found_pos.append(part_of_speech)

        else:
            if part_of_speech not in found_pos:
                print("Skipping, unknown part-of-speech: ", part_of_speech)
            else:
                print("Word have more than one definition: ", word)
            continue

        def_parts = section.findAll("ul", {"class": "semb"})
        for def_part in def_parts:
            wdefs = def_part.findAll("span", {"class": "ind"})

            for wdef in wdefs:
                defs = full_definition.get('definitions')
                defs.append(wdef.string)
                full_definition['definitions'] = defs

        if len(full_definition.get('definitions')) == 0:
            print("No definition found: ", word)
            continue

        result.append(full_definition)
    return result


def create_json_file(word, definition):
    """
    Function creates new json file with word definition if doesn't exist
    """
    first_letter = word[0]
    subdir_path = os.path.join(ROOT_DIR, first_letter)
    fname_path = os.path.join(subdir_path, word + ".json")

    if not os.path.exists(fname_path):
        with open(fname_path, 'w') as f:
            print("Creating definition ", word + ".json")
            json.dump(definition, f, indent=4)
    else:
        with open(fname_path, 'r') as f:
            existing_def = json.load(f)
            new_defs = definition.get("definitions")
            file_defs = existing_def.get("definitions")

            # check if definitions are not the same
            for wdef in new_defs:
                if wdef not in file_defs:
                    file_defs.append(wdef)

            existing_def["definitions"] = file_defs

            with open(fname_path, 'w') as file:
                print("Updating definitions for ", word + ".json")
                json.dump(existing_def, file, indent=4)


def generate(input_words):
    """
    Function returns definitions of inputed words
    """
    new_definitions = {}
    print("Starting... ")

    for word in input_words:
        url = build_api_url(word)
        content = download_page(url)
        if content is not None:
            for wdef in parse_html(word, content):
                new_definitions[word.title() + "_" + wdef.get('parts-of-speech').lower()] = wdef

        print("processed ", word)
        time.sleep(3)  # just to be not suspicious :)

    for word, definition in new_definitions.items():
        create_json_file(word, definition)


if __name__ == "__main__":
    words = ['your', 'list', 'of', 'word']
    generate(words)
