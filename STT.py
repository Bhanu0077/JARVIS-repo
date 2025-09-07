import os 
import time
import pygame
import speech_recognition as sr
from gtts import gTTS

def get_audio():
    r = sr.Recognizer()  # Create a Recognizer instance to recognize speech

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")  # Inform the user that the program is listening
        audio = r.listen(source)  # Capture the audio from the microphone
        said = ""  # Initialize a variable to store recognized text

        try:
            # Recognize speech using Google Web Speech API
            said = r.recognize_google(audio)
            print("You said: " + said)  # Print the recognized text
        except Exception as e:
            # Handle exceptions (like if speech was unclear or not recognized)
            print("Exception: " + str(e))
        
    return said  # Return the recognized text

# Main program starts here

print("Listening...")
get_audio()