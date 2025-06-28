"""Twitter API client wrapper."""

import logging
from typing import Optional

from tweepy import Client, API, OAuthHandler, TweepyException

logger = logging.getLogger(__name__)


class TwitterClient:
    """Handles Twitter API interactions."""
    
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
        self._client: Optional[Client] = None
        self._api: Optional[API] = None
        
    def connect(self) -> None:
        """Initialize Twitter API connections."""
        try:
            auth = OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            
            self._client = Client(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            
            self._api = API(auth, wait_on_rate_limit=True)
            
            logger.info("Successfully connected to Twitter API")
            
        except Exception as e:
            logger.error(f"Failed to connect to Twitter API: {e}")
            raise
            
    def post_tweet(self, text: str) -> Optional[str]:
        """Post a tweet and return the tweet ID."""
        if not self._client:
            raise RuntimeError("Twitter client not connected")
            
        try:
            response = self._client.create_tweet(text=text)
            
            if response.data:
                tweet_id = response.data['id']
                logger.info(f"Successfully posted tweet: {text[:50]}...")
                logger.info(f"Tweet URL: https://twitter.com/user/status/{tweet_id}")
                return tweet_id
                
        except TweepyException as e:
            logger.error(f"Twitter API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error posting tweet: {e}")
            
        return None
        
    def verify_credentials(self) -> bool:
        """Verify that the credentials are valid."""
        if not self._api:
            return False
            
        try:
            self._api.verify_credentials()
            return True
        except Exception:
            return False