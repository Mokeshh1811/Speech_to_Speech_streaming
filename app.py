from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tracemalloc

tracemalloc.start()

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "static/videos/"
TRANSLATION_FOLDER = "static/translations/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSLATION_FOLDER, exist_ok=True)

# Supported languages
languages = {
    'ar': 'Arabic',
    'bn': 'Bengali',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'hi': 'Hindi',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'jv': 'Javanese',
    'ko': 'Korean',
    'mr': 'Marathi',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'ta': 'Tamil',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'zh': 'Chinese'
}



def extract_audio_from_video(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


def extract_text_from_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    return text


def translate_text(text, target_language):
    translator = Translator()
    translated = translator.translate(text, dest=target_language)
    return translated.text


def text_to_audio(text, audio_path, lang):
    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)


def merge_audio_with_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Trim audio if it's longer than the video
    if audio.duration > video.duration:
        audio = audio.subclip(0, video.duration)

    # Set audio to video and save
    video_with_audio = video.set_audio(audio)
    video_with_audio.write_videofile(output_path, codec="libx264", audio_codec="aac")


@app.route("/", methods=["GET", "POST"])
def index():
    original_video_preview = None
    translated_video_preview = None
    translated_video_path = None

    if request.method == "POST":
        # Handle video upload
        if "video" not in request.files or request.files["video"].filename == "":
            flash("No video file uploaded!", "error")
            return redirect(url_for("index"))

        video_file = request.files["video"]
        video_filename = video_file.filename
        video_path = os.path.join(UPLOAD_FOLDER, video_filename)
        video_file.save(video_path)

        # Show original video preview
        original_video_preview = url_for('static', filename=f'videos/{video_filename}')

        target_language = request.form.get("language")
        if not target_language:
            flash("No language selected!", "error")
            return redirect(url_for("index"))

        try:
            # Process video for translation
            audio_path = os.path.join(TRANSLATION_FOLDER, "extracted_audio.wav")
            extract_audio_from_video(video_path, audio_path)

            text = extract_text_from_audio(audio_path)

            translated_text = translate_text(text, target_language)

            translated_audio_path = os.path.join(TRANSLATION_FOLDER, "translated_audio.wav")
            text_to_audio(translated_text, translated_audio_path, target_language)

            translated_video_path = os.path.join(UPLOAD_FOLDER, "output_video.mp4")
            merge_audio_with_video(video_path, translated_audio_path, translated_video_path)

            # Show translated video preview
            translated_video_preview = url_for('static', filename='videos/output_video.mp4')

        except Exception as e:
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics("lineno")

            flash(f"Error processing video: {str(e)}", "error")
            print("[ Top 10 memory allocation locations ]")
            for stat in top_stats[:10]:
                print(stat)
            return redirect(url_for("index"))

        flash("Video processed successfully!", "success")

    return render_template(
        "index.html",
        languages=languages,
        original_video_preview=original_video_preview,
        translated_video_preview=translated_video_preview,
    )


@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
# from flask import Flask, render_template, request, flash, redirect, url_for, send_file
# import os
# from moviepy.editor import VideoFileClip, AudioFileClip
# import speech_recognition as sr
# from googletrans import Translator
# from gtts import gTTS
# from pydub import AudioSegment
# import tracemalloc

# tracemalloc.start()

# app = Flask(__name__)
# app.secret_key = "supersecretkey"

# UPLOAD_FOLDER = "static/videos/"
# TRANSLATION_FOLDER = "static/translations/"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(TRANSLATION_FOLDER, exist_ok=True)

# # Supported languages
# languages = {
#     'ar': 'Arabic',
#     'bn': 'Bengali',
#     'de': 'German',
#     'el': 'Greek',
#     'en': 'English',
#     'es': 'Spanish',
#     'fr': 'French',
#     'hi': 'Hindi',
#     'id': 'Indonesian',
#     'it': 'Italian',
#     'ja': 'Japanese',
#     'jv': 'Javanese',
#     'ko': 'Korean',
#     'mr': 'Marathi',
#     'pl': 'Polish',
#     'pt': 'Portuguese',
#     'ro': 'Romanian',
#     'ru': 'Russian',
#     'ta': 'Tamil',
#     'tr': 'Turkish',
#     'uk': 'Ukrainian',
#     'zh': 'Chinese'
# }


# def extract_audio_from_video(video_path, audio_path):
#     """
#     Extract audio from a video file and save it as a separate audio file.
#     """
#     video = VideoFileClip(video_path)
#     if not video.audio:
#         raise ValueError("The video file does not contain an audio track.")

#     video.audio.write_audiofile(audio_path)
#     return video.duration * 1000  # Return video duration in milliseconds


# def extract_text_from_audio(audio_path):
#     """
#     Extract text from an audio file using Google Speech Recognition.
#     """
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_path) as source:
#         audio_data = recognizer.record(source)
#         text = recognizer.recognize_google(audio_data)
#     return text


# def translate_text(text, target_language):
#     """
#     Translate the given text to the target language using Google Translator.
#     """
#     translator = Translator()
#     translated = translator.translate(text, dest=target_language)
#     return translated.text


# def text_to_speech_with_duration(text, audio_path, lang, target_duration):
#     """
#     Convert text to speech and adjust duration to match the target duration.
#     """
#     if target_duration == 0:
#         raise ValueError("Target duration cannot be zero.")

#     temp_audio_file = "temp_audio.mp3"
#     tts = gTTS(text=text, lang=lang)
#     tts.save(temp_audio_file)

#     audio = AudioSegment.from_mp3(temp_audio_file)
#     current_duration = len(audio)

#     if current_duration != target_duration:
#         speed_factor = current_duration / target_duration
#         if speed_factor == 0:
#             raise ValueError("Speed factor calculation resulted in zero.")
#         adjusted_audio = audio.speedup(playback_speed=speed_factor)
#         adjusted_audio.export(audio_path, format="wav")
#     else:
#         audio.export(audio_path, format="wav")

#     if os.path.exists(temp_audio_file):
#         os.remove(temp_audio_file)


# def merge_audio_with_video(video_path, audio_path, output_path):
#     """
#     Merge the translated audio with the original video.
#     """
#     video = VideoFileClip(video_path)
#     audio = AudioFileClip(audio_path)

#     if audio.duration > video.duration:
#         audio = audio.subclip(0, video.duration)

#     video_with_audio = video.set_audio(audio)
#     video_with_audio.write_videofile(output_path, codec="libx264", audio_codec="aac")


# @app.route("/", methods=["GET", "POST"])
# def index():
#     original_video_preview = None
#     translated_video_preview = None
#     translated_video_path = None

#     if request.method == "POST":
#         # Handle video upload
#         if "video" not in request.files or request.files["video"].filename == "":
#             flash("No video file uploaded!", "error")
#             return redirect(url_for("index"))

#         video_file = request.files["video"]
#         video_filename = video_file.filename
#         video_path = os.path.join(UPLOAD_FOLDER, video_filename)
#         video_file.save(video_path)

#         # Show original video preview
#         original_video_preview = url_for('static', filename=f'videos/{video_filename}')

#         target_language = request.form.get("language")
#         if not target_language:
#             flash("No language selected!", "error")
#             return redirect(url_for("index"))

#         try:
#             # Process video for translation
#             audio_path = os.path.join(TRANSLATION_FOLDER, "extracted_audio.wav")
#             video_duration = extract_audio_from_video(video_path, audio_path)

#             # Ensure video duration is valid and non-zero
#             if video_duration == 0:
#                 raise ValueError("Extracted video duration is zero.")

#             text = extract_text_from_audio(audio_path)

#             translated_text = translate_text(text, target_language)

#             translated_audio_path = os.path.join(TRANSLATION_FOLDER, "translated_audio.wav")
#             text_to_speech_with_duration(translated_text, translated_audio_path, target_language, int(video_duration))

#             translated_video_path = os.path.join(UPLOAD_FOLDER, "output_video.mp4")
#             merge_audio_with_video(video_path, translated_audio_path, translated_video_path)

#             # Show translated video preview
#             translated_video_preview = url_for('static', filename='videos/output_video.mp4')

#         except Exception as e:
#             snapshot = tracemalloc.take_snapshot()
#             top_stats = snapshot.statistics("lineno")

#             flash(f"Error processing video: {str(e)}", "error")
#             print("[ Top 10 memory allocation locations ]")
#             for stat in top_stats[:10]:
#                 print(stat)
#             return redirect(url_for("index"))

#         flash("Video processed successfully!", "success")

#     return render_template(
#         "index.html",
#         languages=languages,
#         original_video_preview=original_video_preview,
#         translated_video_preview=translated_video_preview,
#     )


# @app.route("/download/<filename>")
# def download_file(filename):
#     path = os.path.join(UPLOAD_FOLDER, filename)
#     return send_file(path, as_attachment=True)


# if __name__ == "__main__":
#     app.run(debug=True)
