import os
from openai import OpenAI

class SpeechTranscriber:
    """
    Handles converting spoken audio files to text using Whisper models (Groq or OpenAI).
    """
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if self.groq_api_key:
            # Groq provides a Whisper model: whisper-large-v3
            self.client = OpenAI(api_key=self.groq_api_key, base_url="https://api.groq.com/openai/v1")
            self.model_name = "whisper-large-v3"
        elif self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)
            self.model_name = "whisper-1"
        else:
            self.client = None
            self.model_name = None

    def transcribe_audio(self, file_path: str) -> str:
        """
        Transcribes the provided audio file to text.
        """
        if not self.client:
            # Fallback if API keys aren't configured
            return "[Transcriber not configured. This is a fallback transcript.]"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        try:
            with open(file_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model=self.model_name,
                    file=audio_file,
                    response_format="text"
                )
            
            # The API returns either a string (when response_format='text') or an object
            if isinstance(transcription, str):
                return transcription.strip()
            return transcription.text.strip()

        except Exception as e:
            print(f"Error during audio transcription: {e}")
            return "[Transcription failed.]"
