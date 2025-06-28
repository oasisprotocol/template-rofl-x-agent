"""Configuration management for the twitter persona bot."""

import logging
import os
from typing import List

from dotenv import load_dotenv

from src.models.types import Settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

load_dotenv()

def load_settings() -> Settings:
    """Load settings from environment variables.
    
    Returns:
        Configured Settings object
        
    Raises:
        ValueError: If required environment variables are missing
    """
    required_vars = {
        "SYSTEM_PROMPT": "Bot persona/personality description",
        "TWITTER_BEARER_TOKEN": "Twitter Bearer token",
        "TWITTER_API_KEY": "Twitter API key",
        "TWITTER_API_SECRET": "Twitter API secret",
        "TWITTER_ACCESS_TOKEN": "Twitter access token",
        "TWITTER_ACCESS_TOKEN_SECRET": "Twitter access token secret",
        "OPENAI_API_KEY": "OpenAI API key"
    }
    
    missing_vars: List[str] = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var} ({description})")
            
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables:\n" + 
            "\n".join(f"  - {var}" for var in missing_vars)
        )
    
    return Settings(
        system_prompt=os.getenv("SYSTEM_PROMPT"),
        twitter_bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        twitter_api_key=os.getenv("TWITTER_API_KEY"),
        twitter_api_secret=os.getenv("TWITTER_API_SECRET"),
        twitter_access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        twitter_access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    )

__all__ = ["load_settings"]