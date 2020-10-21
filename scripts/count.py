import os, string, json

def word_count():
	count = {}

	for alpha in string.ascii_uppercase:
		directory = f"../{alpha}"

		count[f"{alpha}"] = len(os.listdir(directory)) 
	
	return count


def part_speech_count():
	count = {
	"Noun"         : 0,
	"Pronoun"      : 0,
	"Verb"         : 0,
	"Adverb"       : 0,
	"Adjective"    : 0,
	"Preposition"  : 0,
	"Conjunction"  : 0,
	"Interjection" : 0,
	"No data"      : 0
	}

	for alpha in string.ascii_uppercase:
		directory = f"../{alpha}"
		for each_file in os.listdir(directory):
			try:
				with open(os.path.join(directory, each_file)) as file:
					data = json.load(file)

					if data["parts-of-speech"] in count.keys():
						count[data["parts-of-speech"]] += 1
					else:
						count["No data"] += 1
			except:
				pass

	return count


if __name__ == '__main__':
	print(word_count())	
	print(part_speech_count())