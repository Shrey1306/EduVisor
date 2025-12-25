"""
Configuration management for external API services.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """
    Configuration holder for API keys and service credentials.
    
    Loads configuration from environment variables first, then falls back
    to config.json for local development.
    """
    
    google_cloud_key_path: str
    openai_api_key: str
    hugging_face_api_key: str
    
    # Audio processing settings
    chunk_duration_ms: int = 30000  # 30 seconds
    audio_sample_rate: int = 44100
    audio_channels: int = 2
    
    _instance: Optional[Config] = None
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> Config:
        """
        Load configuration from environment variables or config file.
        
        Environment variables take precedence:
        - GOOGLE_CLOUD_KEY_PATH
        - OPENAI_API_KEY
        - HUGGINGFACE_API_KEY
        """
        if cls._instance is not None:
            return cls._instance
            
        # Try environment variables first
        google_key = os.environ.get("GOOGLE_CLOUD_KEY_PATH")
        openai_key = os.environ.get("OPENAI_API_KEY")
        hf_key = os.environ.get("HUGGINGFACE_API_KEY")
        
        # Fall back to config.json
        if not all([google_key, openai_key, hf_key]):
            if config_path is None:
                # Look in project root data directory
                config_path = Path(__file__).parent.parent.parent.parent / "data" / "config.json"
            
            if config_path.exists():
                with open(config_path) as f:
                    data = json.load(f)
                    google_key = google_key or data.get("google_cloud_key")
                    openai_key = openai_key or data.get("openai_key")
                    hf_key = hf_key or data.get("hugging_face_key")
        
        if not google_key:
            raise ValueError("Missing Google Cloud key configuration")
        if not openai_key:
            raise ValueError("Missing OpenAI API key configuration")
        if not hf_key:
            raise ValueError("Missing Hugging Face API key configuration")
        
        cls._instance = cls(
            google_cloud_key_path=google_key,
            openai_api_key=openai_key,
            hugging_face_api_key=hf_key,
        )
        
        return cls._instance
    
    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None

