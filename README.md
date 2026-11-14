# Jarvis

A personal AI voice assistant inspired by Iron Man's J.A.R.V.I.S., built in Python as a learning project. It is a work in progress: right now it can listen to me, think using Google's Gemini API, and speak its replies out loud. I'm adding more abilities in stages.

<!-- Add your demo video link here, for example: [Watch the demo](https://...) -->

## Current features

- Voice input: press Enter, speak, and Jarvis turns my speech into text (typing a message also works)
- AI replies from the Gemini API, with a custom "Jarvis" personality
- Spoken replies using text-to-speech
- Remembers earlier messages during a conversation (memory resets when the program closes)
- Retries automatically if the AI server is busy
- API key kept out of the code using a `.env` file

## Built with

- Python
- Google Gemini API (`google-genai`)
- `SpeechRecognition` (uses Google's free speech-to-text service) and `sounddevice` for microphone input
- `pyttsx3` for text-to-speech (built-in Windows voices)
- `python-dotenv`

## How to run it

Tested on Windows. You need a working microphone and an internet connection.

1. Clone the repo and open the folder:
   ```
   git clone https://github.com/MaazAsif-meow/jarvis.git
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

## Roadmap

- [x] Stage 1: Text chat with memory
- [x] Stage 2: Voice input and spoken replies
- [ ] Calm British voice using a neural text-to-speech engine
- [ ] Stage 3: Abilities, such as opening websites and apps, weather, timers, and notes
- [ ] Memory that persists between runs
- [ ] Wake word and automatic silence detection
- [ ] Simple GUI

## What I'm learning

This is my first larger Python project. So far I've practiced working with APIs, virtual environments, environment variables, audio input and output, error handling, and Git/GitHub, and I'm using it to build toward a computer science degree.

## Note

This project uses third-party services: Google's Gemini model for the AI replies and Google's speech recognition for transcription. The assistant's code, structure, and features are what I'm building; the language model itself is Google's.

