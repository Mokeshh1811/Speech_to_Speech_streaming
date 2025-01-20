# Speech-to-Speech Streaming Project

This repository contains the implementation of a Speech-to-Speech Streaming system that enables real-time video translation. The application extracts audio from video files, translates the speech to a selected language, and generates a new video with the translated audio.

## Features

- **Audio Extraction:** Extract audio from uploaded video files.
- **Speech Recognition:** Convert audio to text using Google Speech Recognition.
- **Language Translation:** Translate extracted text into multiple supported languages using Google Translator.
- **Text-to-Speech Conversion:** Generate translated audio using Google Text-to-Speech (gTTS).
- **Audio-Video Merging:** Combine the translated audio with the original video to create a new video.

## Supported Languages

The application supports the following languages:
- Arabic
- Bengali
- German
- Greek
- English
- Spanish
- French
- Hindi
- Indonesian
- Italian
- Japanese
- Javanese
- Korean
- Marathi
- Polish
- Portuguese
- Romanian
- Russian
- Tamil
- Turkish
- Ukrainian
- Chinese

## Technology Stack

- **Backend:** Flask
- **Audio Processing:** moviepy
- **Speech Recognition:** SpeechRecognition
- **Translation:** googletrans
- **Text-to-Speech:** gTTS

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/speech-to-speech-streaming.git
   cd speech-to-speech-streaming
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

## Usage

1. **Start the Flask server:** Run the application using the above command.
2. **Upload Video:** On the web interface, upload a video file.
3. **Select Language:** Choose the target language for translation from the dropdown menu.
4. **Download Translated Video:** After processing, preview and download the translated video.

## Requirements

Below are the required dependencies listed in `requirements.txt`:
```
Flask==2.1.2
moviepy==1.0.3
SpeechRecognition==3.8.1
googletrans==4.0.0-rc1
gTTS==2.2.3
```

## API Endpoints

| Method | Endpoint         | Description                     |
|--------|------------------|---------------------------------|
| GET    | `/`              | Render the homepage            |
| POST   | `/`              | Handle video upload and process |
| GET    | `/download/<filename>` | Download the processed video |

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or feedback, feel free to reach out:
- **Email:** your-mokesh1811@gmail.com
- **GitHub Issues:** [Open an issue]([https://github.com/your-username/speech-to-speech-streaming/issues](https://github.com/Mokeshh1811/Speech_to_Speech_streaming)

