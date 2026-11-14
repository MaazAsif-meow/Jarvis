import os
import time
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

SAMPLE_RATE = 16000
LISTEN_SECONDS = 5
recognizer = sr.Recognizer()


def speak(text):
    """Say the text out loud using the built-in Windows voice."""
    clean_text = text.replace("*", "").replace("#", "")
    engine = pyttsx3.init()
    engine.setProperty("rate", 175)  # speaking speed, try 150-200
    engine.say(clean_text)
    engine.runAndWait()
    engine.stop()


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