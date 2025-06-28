"""OpenAI API client wrapper."""

import logging
import time
from typing import Dict, List, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Handles OpenAI API interactions."""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
        
    def generate_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.8,
        max_tokens: int = 100,
        max_retries: int = 3
    ) -> Optional[str]:
        """Generate a completion using the OpenAI API.
        
        Args:
            messages: List of message dictionaries for the chat
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens in response
            max_retries: Maximum number of retry attempts
            
        Returns:
            Generated text completion or None if failed
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
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
                    time.sleep(2 ** attempt)
                    
        return None
        
    def generate_tweet(self, prompt: str) -> Optional[str]:
        """Generate a tweet based on a prompt.
        
        Args:
            prompt: The prompt to generate a tweet from
            
        Returns:
            Generated tweet text or None if failed
        """
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