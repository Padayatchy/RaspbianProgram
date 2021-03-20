import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import ssl
import certifi
import time
import os # to remove created audio files                
import re
import json
import requests


class person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

#r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
global bool_Understood  #Boolean to identify when the program got an unknown command
def record_audio(ask=False):
    r = sr.Recognizer() # initialise a recogniser
    with sr.Microphone() as source: # microphone as source
        #print('Entered1')
        
        if ask:
            speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        #print('Entered2')
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
            print('Entered3')
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
        print(voice_data.lower()) # print what user said
        return voice_data.lower()

# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print("kiri: {0}".format(audio_string)) # print what app said
    os.remove(audio_file) # remove audio file

def respond(voice_data):
    global bool_Understood
    # 1: greeting
    if there_exists(['hey','hi','hello']):
        bool_Understood=True
        greetings = ["hey, how can I help you {0}".format(person_obj.name)]
        greet = greetings[random.randint(0,len(greetings)-1)]
        speak(greet)

    # 2: name
    if there_exists(["what is your name","what's your name","tell me your name"]):
        bool_Understood=True
        if person_obj.name:
            speak("my name is Alexis")
        else:
            speak("my name is Alexis. what's your name?")

    if there_exists(["my name is"]):
        bool_Understood=True
        person_name = voice_data.split("is")[-1].strip()
        speak("okay, i will remember that {0}".format(person_name))
        person_obj.setName(person_name) # remember name in person object

    # 3: greeting
    if there_exists(["how are you","how are you doing"]):
        bool_Understood=True
        speak("I'm very well, thanks for asking {0}".format(person_obj.name))

    # 4: time
    if there_exists(["what's the time","tell me the time","what time is it"]):
        bool_Understood=True
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time ='{0} {1}'.format(hours,minutes)
        speak(time)

    # 5: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        bool_Understood=True
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q={0}".format(search_term)
        webbrowser.get().open(url)
        speak('Here is what I found for {0} on google'.format(search_term))

    # 6: search youtube
    if there_exists(["youtube"]):
        bool_Understood=True
        search_term = voice_data.split("for")[-1]
        url = "https://www.youtube.com/results?search_query={0}".format(search_term)
        webbrowser.get().open(url)
        speak('Here is what I found for {0} on youtube'.format())
    
    # 7: search for recipe
    if there_exists(["search recipe"]):
        bool_Understood=True
        speak("What ingredient do you want to use")
        ingredient_names=record_audio()
        method = "GET"
        url = "https://api.edamam.com/search"
        cat = re.split('\s+', ingredient_names)
        if 'and' in cat:
            index = cat.index('and')
            del cat[index]
        cat = ','.join([x for x in cat if x])
        data = "?q={0}&app_id={1}&app_key={2}&count=5".format(cat, "32ee587b", "97d251eef16236c3846c00f6b4e5600d")
        #print(data)
        response = requests.request(method,url+data)
        global globalObject
        globalObject = response.json()
        #recipes=json.loads(globalObject)
        recipe_name=globalObject['hits'][0]["recipe"]['label']
        recipe_url=globalObject['hits'][0]["recipe"]['url']
        speak("I found a recipe called {0}".format(recipe_name))
        webbrowser.get().open(recipe_url)
        


    if there_exists(["exit", "quit", "goodbye"]):
        bool_Understood=True
        speak("going offline")
        exit()
    
    if bool_Understood==False:
        speak("Sorry i did not understand that command. Please say it again")

time.sleep(1)

person_obj = person()
while(1):
    bool_Understood=False
    #for index, name in enumerate(sr.Microphone.list_microphone_names()):
     #   print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
    print('Waiting...')
    voice_data = record_audio() # get the voice input
    #print('You just said {0}'.format(voice_data))
    respond(voice_data) # respond

