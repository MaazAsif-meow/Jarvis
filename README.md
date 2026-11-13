# Jarvis

A personal AI assistant inspired by Iron Man's J.A.R.V.I.S., built in Python as a learning project. It is a work in progress: the current version is a text-based assistant that talks to Google's Gemini API, and I'm adding voice and real abilities in stages.

## Current features

- Terminal-based chat with an AI assistant that has a custom "Jarvis" personality
- Remembers earlier messages in the conversation (chat history)
- API key kept out of the code using a `.env` file

## Built with

- Python
- Google Gemini API (`google-genai`)
- `python-dotenv`

## How to run it

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
   (On Mac/Linux: `source venv/bin/activate`)
3. Install the dependencies:
   ```
   pip install google-genai python-dotenv
   ```
4. Get a free API key from [Google AI Studio](https://aistudio.google.com) and create a file named `.env` in the project folder containing:
   ```
   GEMINI_API_KEY=your_key_here
   ```
5. Run it:
   ```
   python jarvis.py
   ```
   Type `quit` to exit.

If you get a "model not available" error, Google has probably retired the model named in `jarvis.py`. Change the `model=` line to a current Gemini model name from the Gemini API docs.

## Roadmap

- [x] Stage 1: Text chat with memory
- [ ] Stage 2: Voice input (speech recognition) and spoken replies (text-to-speech)
- [ ] Stage 3: Abilities, such as opening apps and websites, weather, timers, and notes
- [ ] Stage 4: Simple GUI, error handling, and a demo video

## What I'm learning

This is my first larger Python project. So far I've practiced working with APIs, virtual environments, environment variables, and Git/GitHub, and I'm using it to build toward a computer science degree.

## Note

This project uses a third-party AI model through its API. The assistant's code, structure, and features are what I'm building; the language model itself is Google's.
