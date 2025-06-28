"""Type definitions for the twitter persona bot system."""

from dataclasses import dataclass


@dataclass
class Settings:
    """Application configuration settings."""
    
    system_prompt: str
    twitter_bearer_token: str
    twitter_api_key: str
    twitter_api_secret: str
    twitter_access_token: str
    twitter_access_token_secret: str
    openai_api_key: str
    openai_model: str = "gpt-4-turbo"