"""
Speech emotion recognition service using wav2vec2 model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from transformers import pipeline


EmotionLabel = Literal[
    "angry", "calm", "disgust", "fearful", "happy", "neutral", "sad", "surprised"
]

EngagementLevel = Literal["engaging", "non-engaging"]

ENGAGING_EMOTIONS: set[EmotionLabel] = {"calm", "happy", "surprised", "neutral"}


@dataclass
class EmotionResult:
    """Result of emotion analysis for an audio segment."""
    
    raw_scores: dict[EmotionLabel, float]
    dominant_emotion: EmotionLabel
    engagement_level: EngagementLevel
    confidence: float
    
    @property
    def is_engaging(self) -> bool:
        """Check if the dominant emotion is considered engaging."""
        return self.engagement_level == "engaging"


class EmotionAnalyzer:
    """
    Analyzes speech emotion from audio using wav2vec2.
    """
    
    MODEL_ID = "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition"
    
    def __init__(self) -> None:
        """Initialize the emotion analyzer."""
        self._pipeline = None
    
    @property
    def pipeline(self):
        """Lazy-load the classification pipeline."""
        if self._pipeline is None:
            self._pipeline = pipeline("audio-classification", model=self.MODEL_ID)
        return self._pipeline
    
    def analyze(self, audio_path: Path) -> EmotionResult:
        """Analyze the emotion in an audio file."""
        results = self.pipeline(str(audio_path))
        
        scores: dict[EmotionLabel, float] = {
            result["label"]: result["score"]
            for result in results
        }
        
        dominant_emotion = max(scores, key=lambda k: scores[k])
        confidence = scores[dominant_emotion]
        
        engagement_level: EngagementLevel = (
            "engaging" if dominant_emotion in ENGAGING_EMOTIONS else "non-engaging"
        )
        
        return EmotionResult(
            raw_scores=scores,
            dominant_emotion=dominant_emotion,
            engagement_level=engagement_level,
            confidence=confidence,
        )

