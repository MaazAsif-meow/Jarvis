import asyncio
import os
import time
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

# Create a chat that remembers the conversation (during this run)
chat = client.chats.create(
    model="gemini-3.5-flash-lite",  # if this errors, check the current model name in Google AI Studio
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are Jarvis, a helpful, witty personal assistant. "
            "Keep answers short and clear. "
            "Do not use markdown, asterisks, or bullet points, because your replies are spoken aloud."
        )
    ),
)

# --- Settings ---
VOICE = "en-US-ChristopherNeural"  # change this to the British voice you chose
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
    except Exception:
        print("(Neural voice unavailable, using backup voice.)")
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