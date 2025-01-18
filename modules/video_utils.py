from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for
import os
from moviepy import VideoFileClip, AudioFileClip
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import asyncio
import tracemalloc

tracemalloc.start()

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/videos/"
TRANSLATION_FOLDER = "static/translations/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSLATION_FOLDER, exist_ok=True)

def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def extract_text_from_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text

async def translate_text(text, target_language):
    translator = Translator()
    translated = await translator.translate(text, dest=target_language)
    return translated.text

def text_to_audio(text, audio_path):
    tts = gTTS(text=text, lang='en')
    tts.save(audio_path)

def merge_audio_with_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)  # Correctly load the audio file
    final_video = video.set_audio(audio)
    final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "video" not in request.files or request.files["video"].filename == "":
            flash("No video file uploaded!", "error")
            return redirect(url_for("index"))

        video_file = request.files["video"]
        video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
        video_file.save(video_path)

        target_language = request.form.get("language")
        if not target_language:
            flash("No language selected!", "error")
            return redirect(url_for("index"))

        try:
            audio_path = os.path.join(TRANSLATION_FOLDER, "extracted_audio.wav")
            extract_audio_from_video(video_path, audio_path)

            text = extract_text_from_audio(audio_path)

            translated_text = asyncio.run(translate_text(text, target_language))

            translated_audio_path = os.path.join(TRANSLATION_FOLDER, "translated_audio.wav")
            text_to_audio(translated_text, translated_audio_path)

            output_video_path = os.path.join(UPLOAD_FOLDER, "output_video.mp4")
            merge_audio_with_video(video_path, translated_audio_path, output_video_path)

        except Exception as e:
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')

            flash(f"Error processing video: {str(e)}", "error")
            print("[ Top 10 memory allocation locations ]")
            for stat in top_stats[:10]:
                print(stat)
            return redirect(url_for("index"))

        flash("Video processed successfully!", "success")
        return send_from_directory(UPLOAD_FOLDER, "output_video.mp4", as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
