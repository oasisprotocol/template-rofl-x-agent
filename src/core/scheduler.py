"""Tweet scheduling logic."""

import logging
from typing import Callable

import schedule

logger = logging.getLogger(__name__)


class TweetScheduler:
    """Handles tweet scheduling."""
    
    def __init__(self):
        pass
        
    def schedule_tweets(self, tweet_callback: Callable) -> None:
        """Schedule tweets every hour."""
        schedule.every(1).hours.do(tweet_callback)
        logger.info("Scheduled to tweet every hour")
        
    def run_pending(self) -> None:
        """Run any pending scheduled tasks."""
        schedule.run_pending()