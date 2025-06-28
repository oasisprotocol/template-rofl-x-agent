"""Main persona bot orchestrator."""

import asyncio
import logging

from src.clients import OpenAIClient, TwitterClient
from src.models.types import Settings

from .scheduler import TweetScheduler
from .tweet_generator import TweetGenerator

logger = logging.getLogger(__name__)


class PersonaBot:
    """Twitter persona bot that posts AI-generated tweets."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.running = False
        
        self.twitter_client = TwitterClient(
            api_key=settings.twitter_api_key,
            api_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret
        )
        
        self.openai_client = OpenAIClient(
            api_key=settings.openai_api_key,
            model=settings.openai_model
        )
        
        self.tweet_generator = TweetGenerator(settings, self.openai_client)
        self.scheduler = TweetScheduler()
        
    def initialize(self) -> None:
        """Initialize the bot and its connections."""
        logger.info("Initializing Twitter Persona Bot")
        logger.info(f"Persona: {self.settings.system_prompt}")
        logger.info(f"OpenAI Model: {self.settings.openai_model}")
        self.twitter_client.connect()
        
    def post_tweet(self) -> bool:
        """Generate and post a tweet.
        
        Returns:
            True if tweet was posted successfully, False otherwise
        """
        try:
            tweet_text = self.tweet_generator.generate()
            if not tweet_text:
                logger.error("Failed to generate tweet content")
                return False
                
            tweet_id = self.twitter_client.post_tweet(tweet_text)
            return tweet_id is not None
            
        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False
            
    async def run(self) -> None:
        """Run the bot continuously."""
        self.initialize()
        self.running = True
        
        self.post_tweet()
        
        self.scheduler.schedule_tweets(self.post_tweet)
        while self.running:
            try:
                self.scheduler.run_pending()
                await asyncio.sleep(60)
            except asyncio.CancelledError:
                logger.info("Bot operation cancelled")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                await asyncio.sleep(300)
                
        logger.info("PersonaBot stopped")