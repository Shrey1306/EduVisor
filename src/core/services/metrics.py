"""
Metrics calculation service for lecture analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .emotion import EmotionResult, ENGAGING_EMOTIONS


@dataclass
class Utterance:
    """Represents an analyzed audio segment with transcript and emotion."""
    
    start_time_ms: int
    end_time_ms: int
    transcript: str
    emotion: EmotionResult
    
    @property
    def duration_ms(self) -> int:
        return self.end_time_ms - self.start_time_ms
    
    @property
    def word_count(self) -> int:
        return len(self.transcript.split())


@dataclass
class LectureMetrics:
    """Aggregated metrics for a complete lecture analysis."""
    
    engagement_percentage: float
    tone_modulation_score: float
    words_per_minute: float
    question_count: int
    total_duration_ms: int
    utterance_count: int
    
    def to_dict(self) -> dict:
        return {
            "engagement_score": self.engagement_percentage,
            "tone_modulation": self.tone_modulation_score,
            "wpm": self.words_per_minute,
            "questions": self.question_count,
        }


class MetricsCalculator:
    """
    Calculates lecture quality metrics from analyzed utterances.
    """
    
    def calculate(self, utterances: Sequence[Utterance]) -> LectureMetrics:
        """Calculate all metrics for a set of utterances."""
        if not utterances:
            return LectureMetrics(
                engagement_percentage=0.0,
                tone_modulation_score=0.0,
                words_per_minute=0.0,
                question_count=0,
                total_duration_ms=0,
                utterance_count=0,
            )
        
        return LectureMetrics(
            engagement_percentage=self._calculate_engagement(utterances),
            tone_modulation_score=self._calculate_tone_modulation(utterances),
            words_per_minute=self._calculate_wpm(utterances),
            question_count=self._count_questions(utterances),
            total_duration_ms=utterances[-1].end_time_ms,
            utterance_count=len(utterances),
        )
    
    def _calculate_engagement(self, utterances: Sequence[Utterance]) -> float:
        engaging_count = sum(1 for u in utterances if u.emotion.is_engaging)
        return round((engaging_count / len(utterances)) * 100, 1)
    
    def _calculate_tone_modulation(self, utterances: Sequence[Utterance]) -> float:
        emotion_counts: dict[str, int] = {}
        
        for utterance in utterances:
            emotion = utterance.emotion.dominant_emotion
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        total_count = sum(emotion_counts.values())
        num_emotions = len(emotion_counts)
        
        if num_emotions == 0:
            return 0.0
        
        ideal_distribution = total_count / num_emotions
        
        total_difference = sum(
            abs(count - ideal_distribution)
            for count in emotion_counts.values()
        )
        max_difference = (
            (total_count - ideal_distribution) +
            (num_emotions - 1) * ideal_distribution
        )
        
        if max_difference == 0:
            emotion = next(iter(emotion_counts))
            return 40.0 if emotion in ENGAGING_EMOTIONS else 20.0
        
        modulation_score = (total_difference / max_difference) * 100
        return round(abs(100 - modulation_score), 1)
    
    def _calculate_wpm(self, utterances: Sequence[Utterance]) -> float:
        total_words = sum(u.word_count for u in utterances)
        total_minutes = utterances[-1].end_time_ms / 60000
        
        if total_minutes == 0:
            return 0.0
        
        return round(total_words / total_minutes, 1)
    
    def _count_questions(self, utterances: Sequence[Utterance]) -> int:
        count = sum(u.transcript.count("?") for u in utterances)
        return max(count, 1)

