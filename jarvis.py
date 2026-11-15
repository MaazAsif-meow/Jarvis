import asyncio
import os
import subprocess
import time
import webbrowser
from datetime import datetime
from urllib.parse import quote_plus

import edge_tts
import pygame
import pyttsx3
import sounddevice as sd
import speech_recognition as sr
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Connect to Gemini
client = genai.Client(api_key=api_key)


# ---------------------------------------------------------------
# TOOLS: normal Python functions that Jarvis is allowed to use.
# Gemini reads each function's name, type hints and docstring to
# decide when to call it, so write them clearly.
# ---------------------------------------------------------------
KNOWN_SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
    "gmail": "https://mail.google.com",
    "wikipedia": "https://www.wikipedia.org",
    "claude": "https://claude.ai",
}

APPS = {
    "whatsapp": "whatsapp:",
    "discord": "discord:",
    "spotify": "spotify:",
    "claude": "claude:",
    "vscode": "code",
    "notepad": "notepad",
    "calculator": "calc",
}


def get_current_time() -> str:
    """Get the current local date and time. Use this when the user asks what time or date it is."""
    now = datetime.now()
    return now.strftime("%A, %d %B %Y, %I:%M %p")


def open_website(site: str) -> str:
    """Open a website in the user's web browser. Use this when the user asks to open a site such as
    YouTube, Google, GitHub, Gmail or Wikipedia.

    Args:
        site: The name of the website, for example 'youtube'.
    """
    url = KNOWN_SITES.get(site.lower().strip())
    if url is None:
        return f"I don't know the website '{site}'. I can open: {', '.join(KNOWN_SITES)}."
    webbrowser.open(url)
    return f"Opened {site}."


def search_google(query: str) -> str:
    """Search Google for something and show the results in the user's browser. Use this when the
    user asks to search for or look something up on the web.

    Args:
        query: What to search for.
    """
    webbrowser.open("https://www.google.com/search?q=" + quote_plus(query))
    return f"Searched Google for '{query}'."


def open_app(app: str) -> str:
    """Open a desktop app on the user's computer. Use this when the user asks to open an app such as
    WhatsApp, Discord, Spotify, Claude, VS Code, Notepad or Calculator.

    Args:
        app: The name of the app, for example 'whatsapp'.
    """
    target = APPS.get(app.lower().strip())
    if target is None:
        return f"I don't know the app '{app}'. I can open: {', '.join(APPS)}."
    try:
        if target == "code":
            # VS Code is launched through its command-line launcher
            subprocess.Popen("code", shell=True)
        else:
            os.startfile(target)
        return f"Opened {app}."
    except OSError:
        return f"I couldn't open {app}. It may not be installed."


# ---------------------------------------------------------------
# ROUTINE: opens everything in one go. Edit these lists any time.
# ---------------------------------------------------------------
ROUTINE_APPS = ["spotify", "discord", "claude", "vscode", "whatsapp"]
ROUTINE_SITES = ["github"]
ROUTINE_GREETING = "Welcome home, sir. Starting your usual setup."


def run_routine():
    """Open all the apps and websites in the routine, one after another."""
    for app in ROUTINE_APPS:
        print("  ", open_app(app))
        time.sleep(1)  # small pause so Windows isn't overloaded
    for site in ROUTINE_SITES:
        print("  ", open_website(site))
        time.sleep(1)


def is_routine_phrase(text):
    """True if the user said something like 'wake up, daddy's home'."""
    t = text.lower()
    return "wake up" in t and "home" in t


# Create a chat that remembers the conversation (during this run)
chat = client.chats.create(
    model="gemini-3.5-flash-lite",  # if this errors, check the current model name in Google AI Studio
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are Jarvis, a helpful, witty personal assistant. "
            "Keep answers short and clear. "
            "Do not use markdown, asterisks, or bullet points, because your replies are spoken aloud. "
            "When the user asks you to do something you have a tool for, use the tool."
        ),
        tools=[get_current_time, open_website, search_google, open_app],
    ),
)

# --- Settings ---
VOICE = "en-GB-RyanNeural"  # change this to the British voice you chose
SPEECH_FILE = "jarvis_speech.mp3"
SAMPLE_RATE = 16000
LISTEN_SECONDS = 5

recognizer = sr.Recognizer()
pygame.mixer.init()


async def make_audio(text, path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(path)


def speak_fallback(text):
    """Backup voice (built-in Windows voice) if the neural voice fails."""
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def speak(text):
    """Say the text out loud with the British neural voice."""
    clean_text = text.replace("*", "").replace("#", "")
    try:
        asyncio.run(make_audio(clean_text, SPEECH_FILE))
        pygame.mixer.music.load(SPEECH_FILE)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
    except Exception as e:
        print("(Neural voice unavailable, using backup voice.)")
        print("Reason:", repr(e))
        speak_fallback(clean_text)
        

def listen():
    """Record from the microphone for a few seconds and return the text, or None."""
    print(f"Listening for {LISTEN_SECONDS} seconds... speak now.")
    recording = sd.rec(int(LISTEN_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                       channels=1, dtype="int16")
    sd.wait()
    print("Processing...")

    audio = sr.AudioData(recording.tobytes(), SAMPLE_RATE, 2)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Jarvis: Sorry, I couldn't understand that.\n")
        return None
    except sr.RequestError as e:
        print("Jarvis: Speech service problem:", e, "\n")
        return None


print("Jarvis online.")
print("Press Enter to talk, or type a message. Say or type 'quit' to exit.\n")
speak("Jarvis online.")

while True:
    typed = input("You (Enter = speak): ").strip()

    if typed == "":
        user_input = listen()
        if user_input is None:
            continue
        print("You said:", user_input)
    else:
        user_input = typed

    if user_input.lower().strip(" .!") in ["quit", "exit", "goodbye"]:
        print("Jarvis: Goodbye!")
        speak("Goodbye!")
        break

    # Shortcut: the "wake up, daddy's home" routine skips Gemini entirely
    if is_routine_phrase(user_input):
        print("Jarvis:", ROUTINE_GREETING, "\n")
        speak(ROUTINE_GREETING)
        run_routine()
        print()
        continue

    for attempt in range(3):
        try:
            response = chat.send_message(user_input)
            print("Jarvis:", response.text, "\n")
            speak(response.text)
            break
        except Exception as e:
            print(f"Jarvis: Server busy, retrying ({attempt + 1}/3)...")
            time.sleep(3)
    else:
        print("Jarvis: Sorry, I couldn't reach the server. Try again in a bit.\n")