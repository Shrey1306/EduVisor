"""
Speech-to-text transcription service using Google Cloud Speech API.
"""

from __future__ import annotations

from pathlib import Path

from google.cloud import speech

from .config import Config


class SpeechTranscriber:
    """
    Transcribes audio files to text using Google Cloud Speech-to-Text.
    """
    
    def __init__(
        self,
        config: Config | None = None,
        sample_rate: int = 44100,
        channel_count: int = 2,
    ) -> None:
        """Initialize the transcriber with Google Cloud credentials."""
        self.config = config or Config.load()
        self.sample_rate = sample_rate
        self.channel_count = channel_count
        self._client: speech.SpeechClient | None = None
    
    @property
    def client(self) -> speech.SpeechClient:
        """Lazy-load the Speech client."""
        if self._client is None:
            self._client = speech.SpeechClient.from_service_account_json(
                self.config.google_cloud_key_path
            )
        return self._client
    
    def transcribe(self, audio_path: Path) -> str:
        """Transcribe an audio file to text."""
        with open(audio_path, "rb") as f:
            audio_content = f.read()
        
        audio = speech.RecognitionAudio(content=audio_content)
        
        recognition_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code="en-US",
            sample_rate_hertz=self.sample_rate,
            audio_channel_count=self.channel_count,
            enable_automatic_punctuation=True,
        )
        
        response = self.client.recognize(config=recognition_config, audio=audio)
        
        transcripts = []
        for result in response.results:
            if result.alternatives:
                transcripts.append(result.alternatives[0].transcript)
        
        return " ".join(transcripts)

