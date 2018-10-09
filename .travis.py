import json
import os
import re
import subprocess

# Get a diff between master and current.
try:
    commit_range = os.environ["TRAVIS_COMMIT_RANGE"]
    changed_files = subprocess.check_output(["git", "diff", "--name-only", commit_range])
except KeyError:
    print("🔥 This should be run on Travis. Otherwise make sure TRAVIS_BRANCH is set.")
    exit(1)

# Filter JSON files only.
changed_files_json = []
if changed_files:
    changed_files = changed_files.decode()
    for changed_file in changed_files.split('\n'):
        if re.search(r"\.json$", changed_file):
            changed_files_json.append(changed_file)


# Iterate over list of changed JSON files.
for changed_file_json in changed_files_json:
    print(f"Checking file {changed_file_json}...")
    there_was_an_error = False

    head, tail = os.path.split(changed_file_json)
    if head[0] != tail[0]:
        there_was_an_error = True
        print("🔥 File is in the wrong folder.")

    if not os.path.basename(changed_file_json)[0].isupper():
        there_was_an_error = True
        print("🔥 File name not capitalized.")

    try:
        with open(changed_file_json) as data_file:
            unparsed_file_content = data_file.read()
            file_content = json.loads(unparsed_file_content)
    except json.decoder.JSONDecodeError:
        there_was_an_error = True
        print(f"🔥 JSON could not be parsed. Follow this link to know more : https://jsonlint.com/?json={unparsed_file_content}")

    if 'word' not in file_content:
        there_was_an_error = True
        print("🔥 Key 'word' not found.")

    if not file_content["word"]:
        there_was_an_error = True
        print("🔥 Value for 'word' appears to be empty.")

    if 'definitions' not in file_content:
        there_was_an_error = True
        print("🔥 Key 'definitions' not found.")

    if not file_content["definitions"]:
        there_was_an_error = True
        print("🔥 Value for 'definitions' appears to be empty.")

    if 'parts-of-speech' not in file_content:
        there_was_an_error = True
        print("🔥 Key 'parts-of-speech' not found.")

    if not file_content["parts-of-speech"]:
        there_was_an_error = True
        print("🔥 Value for 'parts-of-speech' appears to be empty.")

    if there_was_an_error:
        exit(1)
