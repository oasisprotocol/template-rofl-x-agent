"""Tweet generation logic."""

import logging
from datetime import datetime
from typing import List, Optional

from ..clients import OpenAIClient
from ..config import Settings

logger = logging.getLogger(__name__)


class TweetGenerator:
    """Handles tweet content generation."""
    
    def __init__(self, settings: Settings, openai_client: OpenAIClient):
        self.settings = settings
        self.openai_client = openai_client
        self.tweet_history: List[str] = []
        
    def generate(self) -> Optional[str]:
        """Generate a new tweet."""
        prompt = self._build_prompt()
        tweet = self.openai_client.generate_tweet(prompt)
        
        if tweet:
            self._add_to_history(tweet)
            
        return tweet
        
    def _build_prompt(self) -> str:
        """Build the prompt for tweet generation."""
        current_time = datetime.now()
        time_context = f"Current time: {current_time.strftime('%A, %B %d, %Y at %I:%M %p')}"
        
        recent_tweets_context = ""
        if self.tweet_history:
            recent = self.tweet_history[-3:]
            recent_tweets_context = "Recent tweets to avoid repetition:\n" + "\n".join(
                f"- {tweet}" for tweet in recent
            )
            
        prompt = f"""
{self.settings.system_prompt}

{time_context}

Generate an engaging tweet that:
1. Fits your persona perfectly
2. Is under 280 characters
3. Is relevant and interesting
4. Uses appropriate hashtags if relevant
5. Could spark conversation or provide value

{recent_tweets_context}

Tweet:"""
        
        return prompt
        
    def _add_to_history(self, tweet: str) -> None:
        """Add a tweet to the history."""
        self.tweet_history.append(tweet)
        if len(self.tweet_history) > 10:
            self.tweet_history.pop(0)