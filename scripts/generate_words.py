import requests


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
        pass


def _generate_json(data):

    if not data['tags']:
        return None
    elif data['tags'] > 1:
        return None
    elif data['tags'][0] not in PART_OF_SPEECH:
        return None
    else:
        pos = data['tags'][0]
        return {
            "word": data['word'],
            "definitions": [
                "pleasing the senses or mind aesthetically",
                "of a very high standard; excellent"
            ],
            "parts-of-speech": PART_OF_SPEECH[pos]
        }
