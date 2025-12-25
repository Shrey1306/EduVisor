"""
AI-powered feedback generation service using OpenAI GPT.
"""

from __future__ import annotations

import openai

from .config import Config
from .metrics import LectureMetrics


class FeedbackGenerator:
    """
    Generates personalized teaching improvement suggestions using GPT.
    """
    
    SYSTEM_PROMPT = """You are an expert educational coach helping teachers improve their lecturing skills. 
Provide constructive, actionable feedback based on lecture analytics. 
Be encouraging but specific. Address the teacher directly using "you/your"."""

    USER_PROMPT_TEMPLATE = """Based on the following lecture analysis, provide personalized suggestions 
to help improve teaching effectiveness. Keep your response concise (around 200 words).

Lecture Analysis:
- Tone Modulation Score: {tone_modulation}/100 (higher = more vocal variety)
- Speaking Pace: {wpm} words per minute
- Questions Asked: {questions} questions
- Engagement Score: {engagement}% of lecture was engaging

Please provide specific, actionable suggestions for improvement."""
    
    def __init__(self, config: Config | None = None) -> None:
        self.config = config or Config.load()
    
    def generate(self, metrics: LectureMetrics) -> str:
        """Generate personalized feedback based on lecture metrics."""
        openai.api_key = self.config.openai_api_key
        
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            tone_modulation=metrics.tone_modulation_score,
            wpm=metrics.words_per_minute,
            questions=metrics.question_count,
            engagement=metrics.engagement_percentage,
        )
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )
        
        return response["choices"][0]["message"]["content"]

