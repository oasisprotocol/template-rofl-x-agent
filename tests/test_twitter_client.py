"""Twitter client tests."""

import pytest
from unittest.mock import Mock, patch
from src.clients.twitter import TwitterClient
from src.models.types import Settings


def create_test_settings():
    """Create test settings."""
    return Settings(
        system_prompt="Test bot",
        twitter_bearer_token="bearer",
        twitter_api_key="key",
        twitter_api_secret="secret",
        twitter_access_token="access",
        twitter_access_token_secret="access_secret",
        openai_api_key="openai_key"
    )


class TestTwitterClient:
    """Test Twitter API client."""
    
    @patch('tweepy.Client')
    def test_successful_tweet_post(self, mock_tweepy):
        """Test successful tweet posting."""
        mock_client = Mock()
        mock_client.create_tweet.return_value = Mock(data={"id": "123", "text": "Test"})
        mock_tweepy.return_value = mock_client
        
        settings = create_test_settings()
        twitter = TwitterClient(
            api_key=settings.twitter_api_key,
            api_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret
        )
        twitter._client = mock_client
        result = twitter.post_tweet("Test tweet")
        
        assert result == "123"
        mock_client.create_tweet.assert_called_once_with(text="Test tweet")
    
    def test_no_client_connection(self):
        """Test posting without connecting first."""
        settings = create_test_settings()
        twitter = TwitterClient(
            api_key=settings.twitter_api_key,
            api_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret
        )
        
        with pytest.raises(RuntimeError, match="Twitter client not connected"):
            twitter.post_tweet("Test tweet")
    
    def test_api_error_handling(self):
        """Test handling of Twitter API errors."""
        settings = create_test_settings()
        twitter = TwitterClient(
            api_key=settings.twitter_api_key,
            api_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret
        )
        twitter._client = Mock()
        twitter._client.create_tweet.side_effect = Exception("API Error")
        
        result = twitter.post_tweet("Test tweet")
        
        assert result is None