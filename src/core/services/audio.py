"""
Audio processing service for extracting and segmenting audio from videos.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from moviepy.editor import VideoFileClip
from pydub import AudioSegment


@dataclass
class AudioChunk:
    """Represents a segment of audio with timing information."""
    
    start_time_ms: int
    end_time_ms: int
    file_path: Path
    
    @property
    def duration_ms(self) -> int:
        """Duration of the chunk in milliseconds."""
        return self.end_time_ms - self.start_time_ms


class AudioProcessor:
    """
    Handles audio extraction from video files and segmentation into chunks.
    """
    
    def __init__(
        self,
        chunk_duration_ms: int = 30000,
        temp_dir: Path | None = None,
    ) -> None:
        """
        Initialize the audio processor.
        
        Args:
            chunk_duration_ms: Duration of each chunk (default: 30 seconds).
            temp_dir: Directory for temporary files.
        """
        self.chunk_duration_ms = chunk_duration_ms
        self.temp_dir = temp_dir or Path(__file__).parent.parent.parent.parent / "data" / "audio"
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_audio(self, video_path: Path) -> Path:
        """Extract audio track from a video file."""
        audio_path = self.temp_dir / "extracted_audio.wav"
        
        video = VideoFileClip(str(video_path))
        video.audio.write_audiofile(str(audio_path), logger=None)
        video.close()
        
        return audio_path
    
    def segment_audio(self, audio_path: Path) -> Iterator[AudioChunk]:
        """Segment audio file into chunks of specified duration."""
        audio = AudioSegment.from_wav(str(audio_path))
        total_duration = len(audio)
        
        current_position = 0
        chunk_index = 0
        
        while current_position < total_duration - self.chunk_duration_ms:
            end_position = current_position + self.chunk_duration_ms
            chunk = audio[current_position:end_position]
            
            chunk_path = self.temp_dir / f"chunk_{chunk_index:04d}.wav"
            chunk.export(str(chunk_path), format="wav")
            
            yield AudioChunk(
                start_time_ms=current_position,
                end_time_ms=end_position,
                file_path=chunk_path,
            )
            
            current_position = end_position
            chunk_index += 1
    
    def cleanup(self) -> None:
        """Remove all temporary audio files."""
        for file in self.temp_dir.glob("*.wav"):
            file.unlink()

