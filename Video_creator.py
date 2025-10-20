# -*- coding: utf-8 -*-
import os
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
from TTS_audio import generate_tts

def create_text_image(text, filename="text_image.png", size=(1280, 720), bg_color=(0,0,0), text_color=(255,255,255)):
    """Create an image with the given text using Pillow."""
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("Arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    margin, offset = 100, 200
    for line in text.split("\n"):
        draw.text((margin, offset), line, font=font, fill=text_color)
        offset += font.getbbox(line)[3] + 20

    img.save(filename)
    return filename

def create_video_from_text(text):
    # Step 1: Generate TTS audio
    audio_file = "output.mp3"
    print("🔊 Generating TTS audio...")
    generate_tts(text, audio_file)

    # Step 2: Load audio
    print("🎵 Loading audio file...")
    audio_clip = AudioFileClip(audio_file)
    duration = audio_clip.duration

    # Step 3: Create text image
    print("🖼️ Creating text image...")
    text_image_file = create_text_image(text)

    # Step 4: Create video from image
    print("🎥 Creating video clip...")
    image_clip = ImageClip(text_image_file).set_duration(duration)

    # Step 5: Combine audio and video
    print("🎬 Combining audio and video...")
    final_clip = CompositeVideoClip([image_clip.set_audio(audio_clip)])

    # Step 6: Export final video with audio
    output_video = "final_video.mp4"
    print(f"💾 Exporting video to {output_video} ...")
    final_clip.write_videofile(output_video, fps=24, codec='libx264', audio_codec='aac')

    # Cleanup
    audio_clip.close()
    final_clip.close()
    os.remove(text_image_file)
    os.remove(audio_file)

    # Step 7: Auto-open video
    print("📺 Opening video...")
    os.system(f'open "{output_video}"')

    print("✅ Done!")

if __name__ == "__main__":
    user_input = input("Enter the text you want to convert to video: ")
    create_video_from_text(user_input)
