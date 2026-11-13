import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
 
# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
 
# Connect to Gemini
client = genai.Client(api_key=api_key)
 
# Create a chat that remembers the conversation
chat = client.chats.create(
    model="gemini-3.5-flash-lite",  # if this errors, check the current model name in Google AI Studio
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are Jarvis, a helpful, witty personal assistant. "
            "Keep answers short and clear."
        )
    ),
)
 
print("Jarvis online. Type 'quit' to exit.\n")
 
while True:
    user_input = input("You: ")
 
    if user_input.lower() in ["quit", "exit"]:
        print("Jarvis: Goodbye!")
        break
 
    response = chat.send_message(user_input)
    print("Jarvis:", response.text, "\n")