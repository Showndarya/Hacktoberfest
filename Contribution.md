# Contribution to Vocabulary Builder

## File Name
Each word must be in a different file named [your-word-name].json.

## File Path
Add the word to an existing folder corresponding to the starting letter of the word or create a folder.

## JSON File 

The file must contain 3 keys
> word: Your word

> definitions: One or more definitions in an array

> parts of speech: One of the 8 parts of speech the word belongs to

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
	"definition-3",
    ],
    "parts-of-speech": "parts-of-speeech-of-your-word"
}
```
