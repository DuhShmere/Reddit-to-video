from gtts import gTTS
from pydub import AudioSegment
import os

def generate_tts(text, filename="tts.wav"):
    """Generate TTS audio using gTTS and export as WAV."""
    tmp_mp3 = "temp.mp3"
    tts = gTTS(text)
    tts.save(tmp_mp3)

    sound = AudioSegment.from_mp3(tmp_mp3)
    sound = sound.set_frame_rate(44100).set_channels(2)
    sound.export(filename, format="wav")

    os.remove(tmp_mp3)
    print(f"✅ Audio generated: {filename}, duration: {len(sound)/1000:.2f} sec")
    return filename
