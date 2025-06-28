"""OpenAI API client wrapper."""

import logging
from typing import Optional, List, Dict

import openai

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Handles OpenAI API interactions."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key
        
    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.8,
        max_tokens: int = 100,
        max_retries: int = 3
    ) -> Optional[str]:
        """Generate a completion using the OpenAI API."""
        for attempt in range(max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                completion = response.choices[0].message.content.strip()
                return completion
                
            except Exception as e:
                logger.error(f"OpenAI API error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    import time
                    time.sleep(2 ** attempt)
                    
        return None
        
    def generate_tweet(self, prompt: str) -> Optional[str]:
        """Generate a tweet based on a prompt."""
        messages = [
            {
                "role": "system",
                "content": "You are a tweet generator. Generate only the tweet text, nothing else."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        tweet = self.generate_completion(messages)
        
        if tweet:
            tweet = tweet.strip('"\'')
            if len(tweet) > 280:
                tweet = tweet[:277] + "..."
                
        return tweet