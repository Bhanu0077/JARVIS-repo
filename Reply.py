import os 
import time
import pygame
import speech_recognition as sr
from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(filename)

def get_audio():
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        said = "" 

        try:
            said = r.recognize_google(audio)
            print("You said: " + said)  
        except Exception as e:
            print("Exception: " + str(e))
        
    return said

text = get_audio()

#using if cases to respond to specific phrases
if "hello" in text.lower():
    speak("Hello, how can I assist you?")

if "what is your name" in text.lower():
    speak("my name is Jarvis")

if "how are you" in text.lower():
    speak("I am fine, thank you, and you?")

