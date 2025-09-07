import os 
import time
import pygame
import speech_recognition as sr
from gtts import gTTS

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)

    #initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    #wait for the audio to finish playing
    print("speaking...")
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10) #small delay to prevent CPU overuse
    #stop playback and quit mixer to release the file
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    #Now safer to delete the file
    os.remove(filename)

speak("How can i help you")