"""Main persona bot orchestrator."""

import logging
import time

from ..clients import TwitterClient, OpenAIClient
from ..config import Settings
from .tweet_generator import TweetGenerator
from .scheduler import TweetScheduler

logger = logging.getLogger(__name__)


class PersonaBot:
    """Twitter persona bot that posts AI-generated tweets."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        
        self.twitter_client = TwitterClient(
            consumer_key=settings.twitter_api_key,
            consumer_secret=settings.twitter_api_secret,
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
        self.twitter_client.connect()
        
    def post_tweet(self) -> bool:
        """Generate and post a tweet."""
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
            
    def run(self) -> None:
        """Run the bot continuously."""
        self.initialize()
        
        self.post_tweet()
        
        self.scheduler.schedule_tweets(self.post_tweet)
        
        while True:
            try:
                self.scheduler.run_pending()
                time.sleep(60)
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                time.sleep(300)