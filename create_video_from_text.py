import os
import textwrap
import numpy as np
from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import (
    VideoClip,
    AudioFileClip,
    concatenate_audioclips,
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
    ImageClip
)

# --- TTS generation ---
def generate_tts(text, filename="tts.wav"):
    tmp_mp3 = "temp.mp3"
    tts = gTTS(text)
    tts.save(tmp_mp3)

    sound = AudioSegment.from_mp3(tmp_mp3)
    sound = sound.set_frame_rate(44100).set_channels(2)
    sound.export(filename, format="wav")
    os.remove(tmp_mp3)

    print(f"✅ Audio generated: {filename}, duration: {len(sound)/1000:.2f} sec")
    return filename

# --- Create video from text ---
def create_video_from_text(
    text,
    title=None,
    background_path="Background_reddit/background.mp4",
    template_path="Reddit_template.png",
    output_video="final_video.mp4"
):
    width, height = 1280, 720
    fps = 15

    # Load background video
    bg_clip = VideoFileClip(background_path)

    # Split text into sentences
    from nltk.tokenize import sent_tokenize
    sentences = sent_tokenize(text)

    # --- Generate audio clips ---
    audio_clips = []
    durations = []

    # Title audio
    if title:
        title_audio_file = "tts_title.wav"
        generate_tts(title, title_audio_file)
        title_clip = AudioFileClip(title_audio_file)
        audio_clips.append(title_clip)
        durations.append(title_clip.duration)

    # Sentence audios
    for i, sentence in enumerate(sentences):
        audio_file = f"tts_{i}.wav"
        generate_tts(sentence, audio_file)
        clip = AudioFileClip(audio_file)
        audio_clips.append(clip)
        durations.append(clip.duration)

    total_duration = sum(durations)

    # Loop background to match total duration
    bg_clip = bg_clip.loop(duration=total_duration).resize((width, height))

    # --- Create subtitles ---
    subtitle_clips = []
    current_time = 0

    # Title template + text
    if title:
        title_audio_duration = durations[0]

        # Load template image and set duration
        template_clip = ImageClip(template_path).set_start(0).set_duration(title_audio_duration)
        template_clip = template_clip.resize(width=800)  # adjust width if needed
        template_clip = template_clip.set_position(("center", int(height*0.25)))  # lower on screen

        # Wrap title text
        wrapped_title = "\n".join(textwrap.wrap(title, width=30))
        temp_txt_clip = TextClip(
            wrapped_title,
            fontsize=36,
            color="white",
            font="Arial-Bold",
            method="caption",
            size=(int(template_clip.w*0.9), None)
        )
        vertical_offset = int(template_clip.h/2 - temp_txt_clip.h/2)

        title_text_clip = temp_txt_clip.set_position((
            "center",
            int(height*0.25 + vertical_offset)
        )).set_start(0).set_duration(title_audio_duration)

        subtitle_clips.extend([template_clip, title_text_clip])
        current_time += title_audio_duration

    # Normal subtitles for the rest of the sentences
    for i, sentence in enumerate(sentences):
        wrapped_text = "\n".join(textwrap.wrap(sentence, width=60))
        txt_clip = TextClip(
            wrapped_text,
            fontsize=40,
            color="white",
            method="caption",
            size=(int(width*0.9), None)
        ).set_position(("center", "center")).set_start(current_time).set_duration(durations[i + (1 if title else 0)])
        subtitle_clips.append(txt_clip)
        current_time += durations[i + (1 if title else 0)]

    # Combine video, subtitles, and audio
    final_audio = concatenate_audioclips(audio_clips)
    final_video = CompositeVideoClip([bg_clip, *subtitle_clips]).set_audio(final_audio)

    # Render final video
    final_video.write_videofile(output_video, fps=fps)

    # Cleanup temporary audio files
    if title:
        os.remove("tts_title.wav")
    for i in range(len(sentences)):
        os.remove(f"tts_{i}.wav")

    print(f"✅ Done! Saved as {output_video}")

if __name__ == "__main__":
    # For testing purposes
    reddit_title = input("Enter Reddit title:\n> ")
    reddit_text = input("Enter Reddit story:\n> ")
    create_video_from_text(reddit_text, title=reddit_title)
