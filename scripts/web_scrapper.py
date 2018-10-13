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
from difflib import SequenceMatcher
from string import ascii_uppercase

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
    cant_process = []

    soup = BeautifulSoup(html_doc, 'html.parser')

    sections = soup.findAll("section", {"class": "gramb"})
    # print(sections, len(sections))

    for section in sections:
        full_definition = {
            "word": None,
            "definitions": list(),
            "parts-of-speech": None
        }

        # parse part of speech
        try:
            part_of_speech = section.find('span').string.title()
        except Exception as e:
            print("No string argument for ", word)
            cant_process.append((word, "Missing"))
            continue

        # add parsed part of speech and word to model
        if part_of_speech in PARTS_OF_SPEECH and part_of_speech not in found_pos:
            full_definition["word"] = word.title()
            full_definition["parts-of-speech"] = part_of_speech
            found_pos.append(part_of_speech)
        # non existing parts of speech
        else:
            if part_of_speech not in found_pos:
                print("Skipping, unknown part-of-speech: ", word, part_of_speech)
            else:
                print("Word have more than one definition: ", word)
            cant_process.append((word, part_of_speech))
            continue

        # parse definitions
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
    return result, cant_process


def create_json_file(word, definition):
    """
    Function creates new json file with word definition if doesn't exist
    """
    first_letter = word[0]
    subdir_path = os.path.join(ROOT_DIR, first_letter)
    fname_path = os.path.join(subdir_path, word + ".json")

    short_definition = os.path.join(subdir_path, word.split('_')[0] + ".json")

    # rename old file name structure
    if os.path.exists(short_definition):
        with open(short_definition, 'r') as f:
            existing_def = json.load(f)
            new_pos = definition.get("parts-of-speech")
            file_pos = existing_def.get("parts-of-speech").title()

            if new_pos == file_pos:
                update_defs(definition, existing_def)
                print("Removing old definition format", word + ".json")
                os.remove(short_definition)

    # create if doesnt exist or update id exists
    if not os.path.exists(fname_path):
        with open(fname_path, 'w') as f:
            print("Creating definition for ", word + ".json")
            json.dump(definition, f, indent=4)
    else:
        with open(fname_path, 'r') as f:
            existing_def = json.load(f)
            existing_def = update_defs(definition, existing_def)

            with open(fname_path, 'w') as file:
                print("Updating definitions for ", word + ".json")
                json.dump(existing_def, file, indent=4)


def update_defs(def_given, def_existing):
    """
    Updates existing definitions and add if new definition found
    """
    new_defs = def_given.get("definitions")
    file_defs = def_existing.get("definitions")

    # check if definitions are not the same
    for wdef in new_defs:
        if similar(wdef, file_defs) > 0.9:
            file_defs.append(wdef)

    def_existing["definitions"] = file_defs
    return def_existing


def similar(a, b):
    """
    String similarity check
    """
    return SequenceMatcher(None, a, b).ratio()


def generate(input_words):
    """
    Function returns definitions of inputed words
    """
    new_definitions = {}
    final_couldnt_parse = []
    print("Starting... ")

    for word in input_words:
        url = build_api_url(word)
        content = download_page(url)
        if content is not None:
            results, couldnt_parse = parse_html(word, content)

            if len(couldnt_parse) > 0:
                final_couldnt_parse.append(couldnt_parse)

            for wdef in results:
                acurate_fname = word.title() + "_" + wdef.get('parts-of-speech').lower()
                new_definitions[acurate_fname] = wdef

        print("processed ", word)
        time.sleep(3)  # just to be not suspicious :)

    for word, definition in new_definitions.items():
        create_json_file(word, definition)

    print("Couldnt parse files, try manually", final_couldnt_parse)


def getListOfFiles(dirName):
    """
    Create a list of file and sub directories
    """
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def list_of_files(subfolder_names_string=None):
    """
    Returns list of file names from dirs A to Z or other if specified
    :param subfolder_names_string: "ABCDMNOXYZ" or other sequence
    """
    result_words = list()

    if subfolder_names_string is None:
        subfolder_names_string = ascii_uppercase

    for c in subfolder_names_string:
        w = getListOfFiles(os.path.join(ROOT_DIR, c))

        for path in w:
            filename, file_extension = os.path.splitext(path)
            json_file_name = filename.split('/')[-1]

            # missing or wrong file extension
            if file_extension != ".json":
                new_path = os.path.join(os.path.dirname(filename), json_file_name.title() + ".json")
                os.rename(path, new_path)

            # rename filename if starts with lower letter
            if json_file_name[0].islower():
                new_path = os.path.join(os.path.dirname(filename), json_file_name.title() + ".json")
                os.rename(path, new_path)

            # add only word to final list
            if '_' in json_file_name:
                pass
                # result_words.append(json_file_name.split('_')[0])
            else:
                # print("FASFF")
                result_words.append(json_file_name)

    return result_words


if __name__ == "__main__":
    words = ['your', 'list', 'of', 'word']

    words = list_of_files()
    # print(words)
    # print(len(words))

    # generate(words)
