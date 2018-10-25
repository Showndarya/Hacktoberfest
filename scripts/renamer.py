from pathlib import Path

project_path = Path(__file__).resolve().parent.parent
dirs = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for alphabet in dirs:
	words_dir = project_path/alphabet
	for json_file in words_dir.glob('*.json'):
		if json_file.stem[0].islower():
			json_file.rename(Path(json_file.parent,json_file.stem.capitalize()+'.json'))
			# print (json_file,json_file.stem.capitalize()+'.json')