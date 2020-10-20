# Combine JSON files in all directories into a single csv file or JSON file
# Written by Rutuparn Pawar [InputBlackBoxOutput]
# Created 20 Oct 2020

# Note: Only the first definition is used while creating combined data

import os, string, json, csv

# -----------------------------------------------------------------------------------
def combine_into_csv():
	print("\n Combining JSON files into one CSV file")
	errors = []

	for alpha in string.ascii_uppercase:
		directory = f"../{alpha}"
		for each_file in os.listdir(directory):
			try:
				with open(os.path.join(directory, each_file)) as file:
					data = json.load(file)

				try:
					os.remove("word.csv")
				except:
					pass

				with open('words.csv', 'a', newline='') as csvfile:
				    word_writer = csv.writer(csvfile, delimiter=',')
				    word_writer.writerow([data["word"], data["definitions"][0], data["parts-of-speech"]])

			except:
				errors.append(each_file)
		
	if len(errors) > 0:		
		print(f"\nAn error occured while processing the file(s): {errors}")

	print("\nDone")

def combine_into_json(outfile="words.json"):
	print("\n Combining JSON files into one JSON file")
	errors = []

	# Remove previous json file
	try:
		os.remove(outfile)
	except:
		pass

	outdata = {
		"word": [],
		"definition": [],
		"parts-of-speech": []
	}

	for alpha in string.ascii_uppercase:
		directory = f"../{alpha}"
		for each_file in os.listdir(directory):
			try:
				with open(os.path.join(directory, each_file)) as file:
					indata = json.load(file)
					outdata["word"].append(indata["word"])
					outdata["definition"].append(indata["definitions"][0])
					outdata["parts-of-speech"].append(indata["parts-of-speech"])
			except:
				errors.append(each_file)
		
	with open(outfile, 'a', newline='') as jsonfile:
		json.dump(outdata, jsonfile, indent=4)

	if len(errors) > 0:		
		print(f"\nAn error occured while processing the file(s): {errors}")

	print("\nDone")

# -----------------------------------------------------------------------------------
if __name__ == '__main__':
	# combine_into_csv()
	combine_into_json()

# -----------------------------------------------------------------------------------