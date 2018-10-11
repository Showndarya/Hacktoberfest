# Contributions to Vocabulary Builder

## File Name
The name starts with a capital letter.
One word per file.
For instance : `[FIRST-LETTER]/[Word].json`

## File Path
Add the word to an existing folder corresponding to the starting letter of the word or create a folder.

## JSON File 

The file must contain 3 keys

```
word: Your word 
```

``` 
definitions: One or more definitions in an array 
```

``` 
parts of speech: 
One of the following 8 parts of speech the word belongs to 
Noun 
Pronoun
Verb
Adverb
Adjective
Preposition
Conjunction
Interjection 
```
## One word with different parts of speech 

Add separate files of the word in different parts of speech. Name the file ```[(your-word)_(parts-of-speech)].json```.

## Example file (Word with one definition) 

```json
{
    "word": "your-word",
    "definitions": [
        "definition"
    ],
    "parts-of-speech": "parts-of-speeech-of-your-word"
}
```

## Example file (Word with more than one definition) 

```json
{
    "word": "your-word",
    "definitions": [
        "definition-1",
	"definition-2",
	"definition-3"
    ],
    "parts-of-speech": "parts-of-speeech-of-your-word"
}
```
