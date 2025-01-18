import subprocess
import gtts
from pydub import AudioSegment

def extract_audio_from_video(video_file, output_audio_file):
    """
    Extract audio from a video file and save it as WAV.
    """
    command = [
        "ffmpeg", 
        "-i", video_file, 
        "-q:a", "0", 
        "-map", "a", 
        output_audio_file
    ]
    subprocess.run(command)


def text_to_audio(text, output_audio_file, duration_match_audio):
    """
    Convert text to audio and ensure the audio duration matches the original audio.
    """
    tts = gtts.gTTS(text=text, lang='en')  # Adjust the language code as per the target language
    temp_audio_file = "temp_audio.mp3"
    tts.save(temp_audio_file)

    # Convert to WAV
    temp_audio_wav = "temp_audio.wav"
    command = ["ffmpeg", "-i", temp_audio_file, temp_audio_wav]
    subprocess.run(command)
    
    # Adjust duration
    original_audio = AudioSegment.from_file(duration_match_audio)
    generated_audio = AudioSegment.from_file(temp_audio_wav)
    
    adjusted_audio = generated_audio.set_duration(len(original_audio))
    adjusted_audio.export(output_audio_file, format="wav")
