import speech_recognition as sr
from googletrans import Translator

def extract_text_from_audio(audio_file, output_text_file):
    """
    Extract text from an audio file and save it as a text file.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    
    with open(output_text_file, 'w') as f:
        f.write(text)
    return text

def translate_text(input_text, target_language, output_text_file):
    """
    Translate text to a target language and save it as a text file.
    """
    translator = Translator()
    translated = translator.translate(input_text, dest=target_language)
    
    with open(output_text_file, 'w') as f:
        f.write(translated.text)
    return translated.text