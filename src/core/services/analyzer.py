"""
Main lecture analysis orchestrator service.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .audio import AudioProcessor
from .config import Config
from .emotion import EmotionAnalyzer
from .metrics import LectureMetrics, MetricsCalculator, Utterance
from .speech import SpeechTranscriber
from .visualization import ChartGenerator
from .ai_feedback import FeedbackGenerator


@dataclass
class AnalysisResult:
    """Complete results of lecture video analysis."""
    
    metrics: LectureMetrics
    feedback: str
    timeline_chart_html: str
    utterances: list[Utterance]
    
    def to_context(self) -> dict:
        """Convert to template rendering context."""
        return {
            "questions": self.metrics.question_count,
            "engagement_score": self.metrics.engagement_percentage,
            "tone_modulation": self.metrics.tone_modulation_score,
            "wpm": self.metrics.words_per_minute,
            "graph": self.timeline_chart_html,
            "suggestion": self.feedback,
        }


class LectureAnalyzer:
    """
    Main orchestrator for lecture video analysis.
    
    Example:
        analyzer = LectureAnalyzer()
        result = analyzer.analyze(Path("lecture.mp4"))
        print(f"Engagement: {result.metrics.engagement_percentage}%")
    """
    
    def __init__(
        self,
        config: Config | None = None,
        chunk_duration_ms: int = 30000,
    ) -> None:
        self.config = config or Config.load()
        self.chunk_duration_ms = chunk_duration_ms
        
        self._audio_processor = AudioProcessor(chunk_duration_ms=chunk_duration_ms)
        self._speech_transcriber = SpeechTranscriber(config=self.config)
        self._emotion_analyzer = EmotionAnalyzer()
        self._metrics_calculator = MetricsCalculator()
        self._chart_generator = ChartGenerator()
        self._feedback_generator = FeedbackGenerator(config=self.config)
    
    def analyze(
        self,
        video_path: Path,
        progress_callback: Callable[[str, int, int], None] | None = None,
    ) -> AnalysisResult:
        """Perform complete analysis of a lecture video."""
        try:
            # Extract audio
            if progress_callback:
                progress_callback("Extracting audio", 0, 1)
            audio_path = self._audio_processor.extract_audio(video_path)
            
            # Segment and analyze
            utterances: list[Utterance] = []
            chunks = list(self._audio_processor.segment_audio(audio_path))
            
            for i, chunk in enumerate(chunks):
                if progress_callback:
                    progress_callback("Analyzing segments", i + 1, len(chunks))
                
                transcript = self._speech_transcriber.transcribe(chunk.file_path)
                emotion = self._emotion_analyzer.analyze(chunk.file_path)
                
                utterances.append(Utterance(
                    start_time_ms=chunk.start_time_ms,
                    end_time_ms=chunk.end_time_ms,
                    transcript=transcript,
                    emotion=emotion,
                ))
            
            # Calculate metrics
            metrics = self._metrics_calculator.calculate(utterances)
            
            # Generate visualizations
            timeline_html = self._chart_generator.create_engagement_timeline(utterances)
            
            # Generate AI feedback
            feedback = self._feedback_generator.generate(metrics)
            
            return AnalysisResult(
                metrics=metrics,
                feedback=feedback,
                timeline_chart_html=timeline_html,
                utterances=utterances,
            )
            
        finally:
            self._audio_processor.cleanup()

