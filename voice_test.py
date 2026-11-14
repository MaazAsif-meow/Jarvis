import asyncio
import edge_tts
import pygame

VOICE = "en-US-ChristopherNeural"
FILE = "voice_test.mp3"


async def make_audio(text, path):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(path)


text = "Good evening, sir. Jarvis at your service."
asyncio.run(make_audio(text, FILE))

pygame.mixer.init()
pygame.mixer.music.load(FILE)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
pygame.mixer.quit()