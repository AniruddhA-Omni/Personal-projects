import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes
import wikipedia
from time import sleep
'''from gtts import gTTS
import os
from googletrans import Translator'''

# initialisation
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)     # 0 = Male voice, 1= Female voice

# functions


"""def transLate(command_text):
    translator = Translator()
    text_to_translate = translator.translate(command_text, src='en', dest='hi')
    text = str(text_to_translate.text)
    print(text)
    speak = gTTS(text=text, lang='hi', slow=False)
    speak.save("captured_voice.mp4")
    os.system("play captured_voice.mp4")"""


def intro():
    engine.say("Hey, I am LUCY")
    engine.say("What can I do for you?")
    engine.runAndWait()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            talk("I am listening now!")
            print("Listening.....")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            '''if "lucy" in command:
                command = command.replace("lucy", "")'''
            print(command)
            return command
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass


def run_lucy():
    command = take_command()
    print(command)
    if command != None:
        if "bye" in command:
            talk("Bye!")
            talk("See you again!")
            return False
        elif "play" in command:
            song = command.replace("play", "")
            talk("playing "+song)
            pywhatkit.playonyt(song)
            return True
        elif "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            print(time)
            talk("Current time is " + time)
            return True
        elif ("define" in command) or ("what is the meaning of" in command) or ("tell me about" in command):
            if "define" in command:
                word = command.replace("define", "")
                info = wikipedia.summary(word, 3)
                print(word)
                talk(info)
            elif "what is the meaning of" in command:
                word = command.replace("what is the meaning of", "")
                info = wikipedia.summary(word, 2)
                print(word)
                talk(info)
            else:
                word = command.replace("tell me about", "")
                info = wikipedia.summary(word, 3)
                print(word)
                talk(info)
            return True
        elif ("what is your name" in command) or ("who are you" in command):
            talk("I am LUCY")
            talk("My father is Mr. AJ")
            return True
        elif "are you single" in command:
            talk("I am in a relationship with Jarvis!!")
            return True
        elif "joke" in command:
            talk(pyjokes.get_joke())
            return True
        else:
            talk("Please, can you repeat again?")
            return True
    else:
        talk("Please, can you repeat again?")
        return True


# running the program
intro()
while True:
    check = run_lucy()
    if not check:
        break
    sleep(5)
