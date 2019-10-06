import os 
import string

rootdir = '.'
dir_list = list(string.ascii_uppercase)

for dir_name in dir_list:
    for subdir, dirs, files in os.walk(dir_name):
        print(f'Current directory: {rootdir}/{dir_name}')
        for file in files:
            old_name = os.path.join(subdir, file)
            print(old_name)

            if file.islower():
                new_name = os.path.join(subdir, file.capitalize())
                print('=================================')
                print(f'Old filename {old_name}')
                print(f'New filename {new_name}')
                print('=================================')
                os.rename(old_name, new_name)
