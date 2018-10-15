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

import datetime
import json
import os
import requests
import time

from bs4 import BeautifulSoup
from difflib import SequenceMatcher
from random import shuffle, randrange
from string import ascii_uppercase, ascii_lowercase

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

to_be_created = dict()

no_definition = set()
multiple_def = set()
unknow_parts_of_speach = set()
created = set()
can_not_process = set()


start_time = datetime.datetime.now()


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

        # parse part of speech
        try:
            part_of_speech = section.find('span').string.title()
        except Exception as e:
            print("No string argument for ", word)
            can_not_process.add(word)
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
                unknow_parts_of_speach.add(word)
            else:
                print("Word have more than one definition: ", word)
                multiple_def.add(word)
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
            no_definition.add(word)
            continue

        result.append(full_definition)
    return result


total_added = 0
total_changed = 713
BATCH_ADDING = 1


def create_files():
    # print('to be created len', len(to_be_created))
    # if len(to_be_created) >= BATCH_ADDING:
    global total_changed
    print("Total changed:", total_changed)

    if total_changed >= 950:

        with open('cant_process.txt', 'a+') as cant_process, open('created.txt', 'a+') as already_created, open('no_definition.txt', 'a+') as no_def, open('multiple_def.txt', 'a+') as mult_def, open('unknow_pos.txt','a+') as unknow_pos:

            remove = to_be_created.keys()
            for fname_path, definition in to_be_created.items():

                word = fname_path.split('/')[-1].split('_')[0].title()
                created.add(word.lower())

                # create if doesnt exist or update id exists
                if not os.path.exists(fname_path):
                    with open(fname_path, 'w') as f:
                        print("Creating definition for ", word + ".json")

                        global total_added
                        total_added += 1

                        total_changed += 1

                        json.dump(definition, f, indent=4)
                else:
                    with open(fname_path, 'w') as file:
                        print("Updating definitions for ", word + ".json")
                        # global total_changed
                        total_changed += 1

                        json.dump(definition, file, indent=4)

            to_be_created.clear()

            for w in list(no_definition):
                print("no def", w)
                no_def.write("%s\n" % w)

            for w in list(multiple_def):
                print("mult_def", w)
                mult_def.write("%s\n" % w)

            for w in list(unknow_pos):
                print("unknow_pos", w)
                unknow_pos.write("%s\n" % w)

            for w in list(created):
                print("created", w)
                already_created.write("%s\n" % w)

            for w in list(can_not_process):
                print("cant_process", w)
                cant_process.write("%s\n" % w)

            no_definition.clear()
            multiple_def.clear()
            unknow_parts_of_speach.clear()
            created.clear()
            can_not_process.clear()

            print("Total added", total_added, "in", datetime.datetime.now() - start_time)


            # global total_changed
            total_changed = 0


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
            try:
                existing_def = json.load(f)
                new_pos = definition.get("parts-of-speech")
                file_pos = existing_def.get("parts-of-speech").title()

                # rename and update
                if new_pos == file_pos:
                    update_defs(definition, existing_def)
                    print("Removing old definition format", word + ".json")
                    os.remove(short_definition)
                    global total_changed
                    total_changed += 1
            except Exception as e:
                print("ERROR reading file ", e)

    # create if doesnt exist or update id exists
    if not os.path.exists(fname_path):
        to_be_created[fname_path] = definition

    else:
        with open(fname_path, 'r') as f:
            existing_def = update_defs(definition, json.load(f))
            to_be_created[fname_path] = existing_def

    create_files()


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

    input_words = list(input_words)
    for i in range(len(input_words)):
        word = input_words[i]
        url = build_api_url(word)
        content = download_page(url)

        if content is not None:
            results = parse_html(word, content)

            if len(results) == 0:
                no_definition.add(word)

            for wdef in results:
                acurate_fname = word.title() + "_" + wdef.get('parts-of-speech').lower()
                # new_definitions[acurate_fname] = wdef
                create_json_file(acurate_fname, wdef)
        else:
            no_definition.add(word)

        print(str(i + 1) + "/" + str(len(input_words) + 1), "processed", word)
        time.sleep(randrange(4, 9) * 0.12)  # just to be not suspicious :)



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


def list_of_files(subfolder_names_string, skip_fixes):
    """
    Returns list of file names from dirs A to Z or other if specified
    :param subfolder_names_string: "ABCDMNOXYZ" or other sequence
    """
    result_words = list()

    for c in subfolder_names_string:
        w = getListOfFiles(os.path.join(ROOT_DIR, c.upper()))

        for path in w:
            word = fix_json_files(path, skip_fixes=skip_fixes)
            result_words.append(word.lower())

    return result_words


def fix_json_files(path, skip_fixes):
    """
    Rename files - startin with upercase
    Delete old structure and create new correct
    Added .json if missing
    Returns (file name) word
    """
    filename, file_extension = os.path.splitext(path)
    json_file_name = filename.split('/')[-1]

    global total_changed

    if not skip_fixes:
        # Fix extension and file name
        try:
            # print(json_file_name)
            with open(path, 'r') as f:
                definition = json.load(f)
                # print(definition)
                file_pos = definition.get("parts-of-speech")

                if isinstance(file_pos, str) and file_pos.title() in PARTS_OF_SPEECH:

                    if not '_' in json_file_name:
                        jfn = json_file_name
                        json_file_name = json_file_name.title() + "_" + file_pos.lower() + ".json"
                        new_path = os.path.join(os.path.dirname(filename), json_file_name)

                        print(new_path)
                        if not os.path.exists(new_path):
                            with open(new_path, 'w') as fw:
                                print("Creating definition for ", jfn + ".json")
                                if definition:
                                    total_changed += 1
                                    json.dump(definition, fw, indent=4)

                        generate([jfn])
                        print("DELETE", os.path.exists(os.path.join(os.path.dirname(filename), jfn + file_extension)), os.path.join(os.path.dirname(filename), jfn + file_extension))
                        if os.path.exists(os.path.join(os.path.dirname(filename), jfn + file_extension)):

                            total_changed += 1
                            os.remove(os.path.join(os.path.dirname(filename), jfn + file_extension))


                    else:
                        if not "." in json_file_name:
                            json_file_name = json_file_name + ".json"
                        new_path = os.path.join(os.path.dirname(filename), json_file_name)
                    path = new_path



                else:
                    print("WRONG part of speech", type(file_pos), file_pos, json_file_name)
        except Exception as e:
            print("ERROR reading file ", e)
            print("in file ", json_file_name)

        # Fix content of file
        try:
            with open(path, 'r') as f:
                file_def = json.load(f)

                file_word = file_def.get('word').title()
                if isinstance(file_word, str):
                    file_def['word'] = file_word
                else:
                    print("WRONG TYPE OF word", type(file_word), file_word)

                file_pos = file_def.get('parts-of-speech').title()
                if isinstance(file_pos, str) and file_pos in PARTS_OF_SPEECH:
                    file_def['parts-of-speech'] = file_pos
                else:
                    print("WRONG TYPE OF part-of-speech", type(file_pos), file_pos, file_word)

                file_defs = file_def.get('definitions')
                if isinstance(file_defs, list) :
                    if len(file_defs) == 0:
                        print("EMPTY DEFINITIONS", file_defs, file_word)
                else:
                    print("WRONG TYPE OF definitions", type(file_defs), file_defs, file_word)

                with open(path, 'w') as fw:
                    # print("Writing", file_def)
                    total_changed += 1
                    json.dump(file_def, fw, indent=4)

        except Exception as e:
            print("ERROR reading file ", e, "in file ", json_file_name)
            raise Exception(e)

    # add only word to final list
    if '_' in json_file_name:
        return str(json_file_name.split('_')[0])
    else:
        return str(json_file_name)


FREEDICTIONARY_URL = "https://www.thefreedictionary.com/words-that-start-with-"


def list_of_words_from_web(starts_with, diff):
    """
    Downloads and parses page and returns list of words
    """
    result = list()
    urls = []

    if isinstance(starts_with, list):
        for ch in starts_with:
            urls.append(FREEDICTIONARY_URL + ch)
    else:
        urls.append(FREEDICTIONARY_URL + starts_with)

    for url in urls:
        content = download_page(url)
        print(url)

        if content is not None:
            soup = BeautifulSoup(content, 'html.parser')

            for i in range(1, 40):
                li_words = soup.findAll("li", {"data-f": str(i)})

                if len(li_words) > 0:
                    for li in li_words:
                        a = li.find('a').attrs['href'] if li.find('a') is not None else None
                        b = li.find('b').string if li.find('b') is not None else None
                        # print(a, b)

                        if a is not None and b is not None:
                            if len(a) <= 15:
                                result.append(a)

        if diff:
            if isinstance(starts_with, list):
                for ch in starts_with:
                    words_on_disk = list_of_files(ch.upper(), skip_fixes=True)
                    result = list(set(result) - set(words_on_disk))
        print(len(result))

    return result


def load_from_file_with_diff():
    words = set()
    try:
        with open('cant_process.txt', 'r') as cant_process, open('words_from_web.txt', 'r') as from_web, open('created.txt', 'r') as already_created, open('no_definition.txt', 'r') as no_def, open('multiple_def.txt', 'r') as mult_def, open('unknow_pos.txt','r') as unknow_pos:
            for item in from_web.read().strip().split('\n'):
                words.add(item.lower())

            print(len(words))

            for item in already_created.read().strip().split('\n'):
                words.discard(item.lower())
            for item in unknow_pos.read().strip().split('\n'):
                words.discard(item.lower())
            for item in mult_def.read().strip().split('\n'):
                words.discard(item.lower())
            for item in no_def.read().strip().split('\n'):
                words.discard(item.lower())
            for item in cant_process.read().strip().split('\n'):
                words.discard(item.lower())
        return words
    except:
        print("Input files doesnt exists")


if __name__ == "__main__":
    words = ['your', 'list', 'of', 'word']

    # words = list_of_files('W')
    #
    # print(words)
    # print(len(words))

    finite = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j' ]
    # finite = ['k', 'l', 'm', 'n', 'o', 'n', 'o', 'p', 'q', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u','v']
    # finite = ['w', 'x', 'y', 'z']

    words = list_of_files(finite, False)

    # print(words)
    print(len(words))

    # words = list_of_words_from_web(finite, diff=True)
    # with open('words_from_web.txt', 'w') as f:
    #     for item in words:
    #         f.write("%s\n" % item)



    # words = load_from_file_with_diff()
    #
    # print(len(words))
    # generate(words)


    # words = list_of_files("CD")
    # words = list_of_files("FGHJK")
    # words = list_of_files("LMNP")
    # words = list_of_files("QRST")

    # words = list_of_words_from_web('a')
    # words = list_of_words_from_web('b')
    # words = list_of_words_from_web('c')
    # words = list_of_words_from_web('d')
    # words = list_of_words_from_web('e')

    # words = list_of_words_from_web('f')
    # words = list_of_words_from_web('g')
    # words = list_of_words_from_web('h')
    # words = list_of_words_from_web('i')
    # words = list_of_words_from_web('j')

    # words = list_of_words_from_web('k')
    # words = list_of_words_from_web('l')
    # words = list_of_words_from_web('m')
    # words = list_of_words_from_web('n')
    # words = list_of_words_from_web('o')

    # words = list_of_words_from_web('p')
    # words = list_of_words_from_web('q')
    # words = list_of_words_from_web('r')
    # words = list_of_words_from_web('s')
    # words = list_of_words_from_web('t')

    # next

    # words = list_of_words_from_web('u')
    # words = list_of_words_from_web('v')
    # words = list_of_words_from_web('w')
    # words = list_of_words_from_web('x')
    # words = list_of_words_from_web('y')
    # words = list_of_words_from_web('z')

    # shuffle(words)
    # print(words)
    # print(len(words))
    # start_time = datetime.datetime.now()
    # generate(words)
    # print("Total time: ", datetime.datetime.now() - start_time)