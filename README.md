# Jarvis

A personal AI voice assistant inspired by Iron Man's J.A.R.V.I.S., built in Python as a learning project. It listens to me, thinks using Google's Gemini API, speaks back in a calm British voice, can open apps and websites, and remembers things between sessions. It is a work in progress and I'm adding features in stages.

<!-- Add your demo video link here, for example: [Watch the demo](https://...) -->

## Current features

- Voice input: press Enter, speak, and Jarvis turns my speech into text (typing a message also works)
- AI replies from the Gemini API, with a custom "Jarvis" personality
- Spoken replies in a calm British neural voice (falls back to a built-in Windows voice if offline)
- Tool calling: the AI can tell the time, open websites, search Google, and open desktop apps (WhatsApp, Discord, Spotify and more)
- A custom voice-triggered routine that opens my usual apps and websites in one go
- Persistent memory: remembers facts about me and recent conversations between runs, and can forget things when asked. Memory is stored locally in JSON files and is not uploaded to GitHub
- Retries automatically if the AI server is busy
- API key kept out of the code using a `.env` file

## Built with

- Python
- Google Gemini API (`google-genai`), including function (tool) calling
- `SpeechRecognition` (uses Google's free speech-to-text service) and `sounddevice` for microphone input
- `edge-tts` and `pygame` for a British neural text-to-speech voice, with `pyttsx3` (built-in Windows voices) as a backup
- `python-dotenv`

## How to run it

Tested on Windows. You need a working microphone and an internet connection.

1. Clone the repo and open the folder:
   ```
   git clone https://github.com/MaazAsif-Meow/jarvis.git
   cd jarvis
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Get a free API key from [Google AI Studio](https://aistudio.google.com) and create a file named `.env` in the project folder containing:
   ```
   GEMINI_API_KEY=your_key_here
   ```
5. Run it:
   ```
   python jarvis.py
   ```
   Press Enter to speak (Jarvis listens for 5 seconds), or type a message. Say or type `quit` to exit.

If you get a "model not available" error, Google has probably retired the model named in `jarvis.py`. Change the `model=` line to a current Gemini model name from the Gemini API docs.

The app launch list in `jarvis.py` is set up for the apps on my own computer, so edit the `APPS`, `KNOWN_SITES`, and routine lists to match yours.

## How it works

1. Microphone audio is recorded and converted to text.
2. The text goes to Gemini along with Jarvis's instructions and saved memory.
3. If the request needs an action, Gemini calls one of the Python functions I wrote (open an app, search, remember a fact), and Jarvis replies using the result.
4. The reply is converted to speech and played.

## Roadmap

- [x] Stage 1: Text chat with memory
- [x] Stage 2: Voice input and spoken replies
- [x] Calm British voice using a neural text-to-speech engine
- [x] Stage 3: Tool calling, with websites, apps, and a custom routine
- [x] Memory that persists between runs
- [ ] More tools: timers, notes, and weather
- [ ] Wake word and automatic silence detection
- [ ] Simple GUI

## What I'm learning

This is my first larger Python project. So far I've practiced working with APIs, virtual environments, environment variables, audio input and output, function calling, file handling with JSON, error handling, and Git/GitHub, and I'm using it to build toward a computer science degree.

## Note

This project uses third-party services: Google's Gemini model for the AI replies, Google's speech recognition for transcription, and Microsoft's voices through `edge-tts`. The assistant's code, structure, and features are what I'm building; the language model and voices are theirs.
