"""
Service modules for lecture analysis.
"""

from .audio import AudioProcessor, AudioChunk
from .speech import SpeechTranscriber
from .emotion import EmotionAnalyzer, EmotionResult
from .metrics import MetricsCalculator, LectureMetrics, Utterance
from .visualization import ChartGenerator
from .ai_feedback import FeedbackGenerator
from .config import Config
from .analyzer import LectureAnalyzer, AnalysisResult

__all__ = [
    # Main analyzer
    "LectureAnalyzer",
    "AnalysisResult",
    # Individual services
    "AudioProcessor",
    "AudioChunk",
    "SpeechTranscriber",
    "EmotionAnalyzer",
    "EmotionResult",
    "MetricsCalculator",
    "LectureMetrics",
    "Utterance",
    "ChartGenerator",
    "FeedbackGenerator",
    "Config",
]

