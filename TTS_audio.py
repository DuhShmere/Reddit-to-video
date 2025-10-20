from gtts import gTTS

def generate_tts(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    print(f"✅ Saved TTS audio as {filename}")
