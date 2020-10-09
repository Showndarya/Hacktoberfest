import requests
from bs4 import BeautifulSoup as soup

import json
import re
import string

from typing import *

# Creates a regex to remove punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))

def crawl(url:str) -> dict:
    """
    Opens the given url and then scrapes each word from there

    url (:obj: `str`)
     * An url that looks like this: http(s)://name.com/whatever?a_given_arg
    """

    # Open the page source
    try:
        res = requests.get(url, timeout=5.75)
    except requests.exceptions.Timeout as err:
        return None

    # Read the data from the webpage
    # Using BeautifulSoup
    print(f'**{res.status_code}')
    if res.status_code == 200:
        content = res.content

        # Close connection to save RAM
        res.close()

        # Parse the HTML
        parsedContent = soup(content, 'html.parser')

        text = [i for i in parsedContent.find_all(text=True)]
        urls = [i['href'] for i in parsedContent.find_all('a', href=True)]

        # Turn it into a string
        return {
            'content': ' '.join(text),
            'urls': urls}
    else:
        print('**Could not open the specified website')
    return None

def parseText(content:str) -> Iterable['str']:
    """
    Cleans the newly crawled into seperate words
    
    content (:obj: `str`)
     * Content scraped from the given url and then
       Which is then parsed into unique words contained 
       in an iterable
    """

    # Remove punctuation
    content = regex.sub('', content)

    # Split spaces
    content = content.split(' ')

    # Turn it into a set
    vocab = set(content)

    return vocab

def saveText(vocab:Iterable, fName:str):
    """
    Saves the list or set of unique words into a json object
    """
    with open(fName, 'w') as f:
        f.write(json.dumps(list(vocab)))
    return None

if __name__ == "__main__":
    x = crawl('https://requests.readthedocs.io/en/master/')
    x = parseText(x['content'])
    x = saveText(x, 'test_file.json')