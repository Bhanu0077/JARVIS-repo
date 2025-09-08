import datetime
import os
import pygame
import speech_recognition as sr
from gtts import gTTS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Google Calendar API scope
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# ------------------ SPEAK FUNCTION ------------------
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

# ------------------ VOICE INPUT ------------------
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

# ------------------ GOOGLE CALENDAR FUNCTION ------------------
def get_calendar_events(max_results=10):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        return events
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

# ------------------ MAIN PROGRAM ------------------
text = get_audio().lower()

# Simple responses
if "hello" in text:
    speak("Hello, how can I assist you?")

elif "what is your name" in text:
    speak("My name is Jarvis")

elif "how are you" in text:
    speak("I am fine, thank you, and you?")

# Google Calendar integration
elif "show my event" in text or "my calendar" in text:
    events = get_calendar_events(5)
    if not events:
        speak("You have no upcoming events.")
    else:
        speak(f"You have {len(events)} upcoming events.")
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "No title")
            speak(f"{summary} at {start}")

else:
    speak("I did not understand that.")
