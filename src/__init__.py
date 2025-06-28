"""Twitter Persona Bot - AI-powered automated tweeting."""

from . import imghdr_mock
from .clients import TwitterClient, OpenAIClient
from .config import Settings, load_settings
from .core import PersonaBot, TweetGenerator, TweetScheduler

__version__ = "1.0.0"

__all__ = [
    'TwitterClient',
    'OpenAIClient',
    'Settings',
    'load_settings',
    'PersonaBot',
    'TweetGenerator',
    'TweetScheduler',
]