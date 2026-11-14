import sounddevice as sd
import speech_recognition as sr

SAMPLE_RATE = 16000
SECONDS = 5

print("Listening for 5 seconds... speak now.")
recording = sd.rec(int(SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                   channels=1, dtype="int16")
sd.wait()
print("Processing...")

audio = sr.AudioData(recording.tobytes(), SAMPLE_RATE, 2)
recognizer = sr.Recognizer()

try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I couldn't understand that.")
except sr.RequestError as e:
    print("Network problem:", e)