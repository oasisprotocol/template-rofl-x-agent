"""Tweet generation tests."""

from unittest.mock import Mock
from src.core.tweet_generator import TweetGenerator
from src.clients.openai import OpenAIClient
from src.models.types import Settings


def create_test_settings():
    """Create test settings."""
    return Settings(
        system_prompt="Test bot",
        twitter_bearer_token="token",
        twitter_api_key="key",
        twitter_api_secret="secret",
        twitter_access_token="access",
        twitter_access_token_secret="access_secret",
        openai_api_key="openai_key"
    )


class TestTweetGeneration:
    """Test tweet generation functionality."""
    
    def test_successful_tweet_generation(self):
        """Test generating a tweet successfully."""
        settings = create_test_settings()
        mock_openai_client = Mock(spec=OpenAIClient)
        mock_openai_client.generate_tweet.return_value = "Generated tweet"
        
        generator = TweetGenerator(settings, mock_openai_client)
        tweet = generator.generate()
        
        assert tweet == "Generated tweet"
        assert len(generator.tweet_history) == 1
    
    def test_tweet_truncation(self):
        """Test tweets are truncated to 280 characters."""
        settings = create_test_settings()
        mock_openai_client = Mock(spec=OpenAIClient)
        long_content = "x" * 300
        mock_openai_client.generate_tweet.return_value = long_content
        
        generator = TweetGenerator(settings, mock_openai_client)
        tweet = generator.generate()
        
        assert tweet == long_content
        assert len(generator.tweet_history) == 1
        assert generator.tweet_history[0] == long_content
    
    def test_failed_generation(self):
        """Test handling when API fails."""
        settings = create_test_settings()
        mock_openai_client = Mock(spec=OpenAIClient)
        mock_openai_client.generate_tweet.return_value = None
        
        generator = TweetGenerator(settings, mock_openai_client)
        tweet = generator.generate()
        
        assert tweet is None
        assert len(generator.tweet_history) == 0
    
    def test_history_management(self):
        """Test tweet history is maintained correctly."""
        settings = create_test_settings()
        mock_openai_client = Mock(spec=OpenAIClient)
        
        generator = TweetGenerator(settings, mock_openai_client)
        
        for i in range(15):
            generator._add_to_history(f"Tweet {i}")
        
        assert len(generator.tweet_history) == 10
        assert generator.tweet_history[0] == "Tweet 5"
        assert generator.tweet_history[-1] == "Tweet 14"