import pyttsx3
import os
import urllib.request
import json
from random import *

def main(args=None):
    letter = randint(0,25) 
    letter_char = str(chr(letter+65))

    folder_url = "https://api.github.com/repositories/108530593/contents/" + str(letter_char)
    folder_data = urllib.request.urlopen(folder_url)
    folder_json = json.load(folder_data)

    word = randint(0,len(folder_json)-1)
    word_file_name = folder_json[word].get("name")

    file_url = "https://raw.githubusercontent.com/Showndarya/Hacktoberfest/master/" + str(letter_char) +"/"+ str(word_file_name)

    file_data = urllib.request.urlopen(file_url)
    file_json = json.load(file_data)

    engine = pyttsx3.init()
    engine.setProperty('rate', 60)
    engine.setProperty('voice', 'english+f3')


    contents = ""
    number = ["First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth","Ninth","Tenth","Eleventh","Twelfth"]

    for (k,v) in file_json.items():
        if(k == "word"):
            contents = "The word is "+ v+"\n";
            engine.say("The word is "+v)
        if(k == "definitions"):
            for i in range(0,len(v)):
                contents += number[i]+ " definition is "
                contents += v[i]+"\n";
                engine.say(number[i]+ " definition is "+v[i])
            contents += str("The parts of speech is ")
        if(k == "parts-of-speech"):
            contents += str(v);
            engine.say("The parts of speech is "+str(v))


    print(contents)
    engine.runAndWait()
    

main()
