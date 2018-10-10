import json
import operator
import os
import re
import subprocess

from jsonschema import Draft4Validator


def validate(vocabulary):

    # Load the schema from the same directory
    with open(os.path.join(os.path.dirname(__file__), "schema.json")) as f:
        schema = json.load(f)

    validator = Draft4Validator(schema)

    _errors = sorted(validator.iter_errors(vocabulary), key=operator.attrgetter('path'))
    error_messages = []

    # format errors to human-friendly strings
    for err in _errors:
        err_msg = []
        err_msg.append("[%s] -> %s" % ("][".join(repr(index)
                                                 for index in err.absolute_path), err.message))
        for suberror in sorted(err.context, key=operator.attrgetter('schema_path')):
            err_msg.append("  %s" % suberror.message)

        error_messages.append("\n".join(err_msg))

    return error_messages

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
            # skip schema file from travis checks
            if not changed_file == 'schema.json':
                changed_files_json.append(changed_file)

# To verify all files at once
there_was_an_error = False

# Iterate over list of changed JSON files.
for changed_file_json in changed_files_json:
    print(f"Checking file {changed_file_json}...")

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

    errors = validate(file_content)
    if errors:
        there_was_an_error = True
        for error in errors:
            print(f"🔥 Error: {error}")

if there_was_an_error:
    exit(1)