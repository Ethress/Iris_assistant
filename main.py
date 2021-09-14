import gtts
import os
import datetime
import time

# import pyttsx3
from playsound import playsound
import speech_recognition as sr
# /!\ pydub library not used
import re
import requests
# import json       # /!\ Not used
# import subprocess     # /!\ Not used
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

# Playing video VCl
import pafy
import vlc

r = sr.Recognizer()     # Initialize recognizer

########################################

# TYPICAL FUNCTIONS CALLED-OUT
# tts = gtts.gTTS("Test Athena", lang="fr")
# print(gtts.lang.tts_lang())  # Prints all available languages (comment)
# tts.save("helloW.mp3")      # Save audio file
# playsound("helloW.mp3")     # Plays audio
# os.remove("helloW.mp3")     # Removes audio from file

AI_name = "Iris"    # Changes name of AI in script + conditions


def disconnection_msg():
    disconnect = gtts.gTTS(AI_name + " disconnected, goodbye sir")
    disconnect.save("DscGreeting.mp3")
    playsound("DscGreeting.mp3")
    os.remove("DscGreeting.mp3")


def give_time():
    current_time = datetime.datetime.now()      # Using the datetime module
    time_txt = gtts.gTTS("It's currently" + str(current_time.hour) + "hour and" + str(current_time.minute) + "minutes")
    time_txt.save("GiveTime.mp3")
    playsound("GiveTime.mp3")
    os.remove("GiveTime.mp3")


def take_note(str1):
    # todo Modify str1 to account for outside commands
    file = open(r"User_notes", "a+")
    file.write(str1)
    file.write("\n")
    file.close()


def read_note():
    # todo Modify str1 to account for outside commands + finish function
    file = open(r"User_notes", "r")
    file.readline(0)      # Reads one line
    file.readlines()    # Reads all lines
    file.close()


def play_yt_music():
    music_name = text.replace("play ", "")      # Remove 'play' command from YT video name
    query_string = urllib.parse.urlencode({"search_query": music_name})
    format_url = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", format_url.read().decode())
    # clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    print(clip2)

    video = pafy.new(clip2)
    best = video.getbest()
    playurl = best.url

    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(playurl)
    media.get_mrl()
    player.set_media(media)
    player.play()

    print("Music playing - Time elapsed :")
    time.sleep(5)
    time_elapsed = 5

    while player.is_playing():
        print("                             {} s".format(time_elapsed))
        time.sleep(30)
        time_elapsed += 30


def get_weather():
    city_name = "Paris"
    word = "weather"
    address = 'http://www.google.com/search?q='
    newword = address + word + city_name
    page = requests.get(newword)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.prettify())      # Html extracted code (beautiful)

    pattern = r'([+-]?\d+(\.\d)*)\s?°([CcFf])'  # Regex find temperature : ['+ or - number','°','C or c or F or f']
    temperatures = re.findall(pattern, str(soup))   # Format [('21', '', 'C'), ('65', '', 'F')]

    weather_prediction = gtts.gTTS("Weather in " + city_name + " is " + temperatures[0][0] + " degrees Celsius")
    # with a 50 percent chance of rain
    weather_prediction.save("GiveWeather.mp3")
    playsound("GiveWeather.mp3")
    os.remove("GiveWeather.mp3")


def get_recipe():
    recipe_name = "raclette"
    website = 'https://www.marmiton.org/recettes/'
    search_recipe = website + recipe_name
    page = requests.get(search_recipe)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.prettify())      # Html extracted code (beautiful)

    urls_src = soup.find_all('div', {'class', 'yuRUbf'})
    url_list = []
    for val in urls_src:
        url_list.append(val.find('a')['href'])
    print(url_list)


def status():
    text = "Iris online, all systems connected"
    tts = gtts.gTTS(text)
    tts.save("speech.mp3")  # Save audio file
    playsound("speech.mp3")  # Plays audio
    os.remove("speech.mp3")  # Removes audio from file


while True:
    print("Initialize Scan")
    # print("\033[1;32;40m Bright Green  \n")     # ANSI escape format \033[ Style ; txtColor ; backColor

    with sr.Microphone() as source:
        print("Scanning . . .")

        audio_data = r.listen(source)
        try:
            text = r.recognize_google(audio_data)
        except sr.UnknownValueError:
            print("/!\\ Google did not understood audio")
            text = "Sorry sir, I did not understood"
        except sr.RequestError as e:
            print("/!\\ Could not send audio to Google")
            text = "System offline"
        print(text)

    # Repeating the sentence once
    tts = gtts.gTTS(text)
    tts.save("speech.mp3")      # Save audio file
    playsound("speech.mp3")     # Plays audio
    os.remove("speech.mp3")     # Removes audio from file

    """
    if text.startswith("ok " + AI_name):    # Listens to further instructions
        print("OKKKKK")
    """
    get_recipe()


    if "play" in text:
        play_yt_music()

    # Gives the current time
    if "what's the time" in text or \
            "what is the time" in text or \
            "what time is it" in text or \
            "give me the time" in text:
        give_time()     # Gives the time

    # if "search" in text:

    if "weather" in text:
        get_weather()

    # todo Condition for taking note
    if text != "Sorry sir, I did not understood" and text != "System offline":
        take_note(text)     # Takes notes in a txt file

    # todo Condition for reading note
    # read_note(text)     # Takes notes in a txt file

    if text == AI_name + " disconnect":    # Magic word to stop speech2txt
        break   # Gets out of while loop

disconnection_msg()      # Signals end of assistance
print("\n /!\\ Stop")


######################################################
# .--. ..-.  .-..--  .-. .-.-.-.-.-.---              #
# |- |\|| :  | ||-   `-.(  |-' | |-' |               #
# '--' ''-'  `-''    `-' `-'`--'-'   '   Used Cygnet #
######################################################


# Types of Google tts limits               Usage per limits
# -----------------------------------------------
# Request per minutes                       1 000
# Characters per minutes                    500 000
