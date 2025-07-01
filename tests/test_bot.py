"""Core bot functionality tests."""

import asyncio
from unittest.mock import Mock, patch
import pytest

from src.core.persona_bot import PersonaBot
from src.models.types import Settings


def create_test_settings():
    """Create test settings."""
    return Settings(
        system_prompt="Test bot persona",
        twitter_bearer_token="test_bearer",
        twitter_api_key="test_key",
        twitter_api_secret="test_secret",
        twitter_access_token="test_access",
        twitter_access_token_secret="test_access_secret",
        openai_api_key="test_openai_key",
        openai_model="gpt-3.5-turbo"
    )


class TestPersonaBot:
    """Test the main bot functionality."""
    
    def test_successful_tweet_flow(self):
        """Test successful generation and posting of a tweet."""
        settings = create_test_settings()
        
        with patch('src.core.persona_bot.TwitterClient') as mock_twitter, \
             patch('src.core.persona_bot.OpenAIClient') as mock_openai, \
             patch('src.core.persona_bot.TweetScheduler'):
            
            mock_twitter_instance = Mock()
            mock_twitter_instance.connect.return_value = None
            mock_twitter_instance.post_tweet.return_value = "1234567890"
            mock_twitter.return_value = mock_twitter_instance
            
            mock_openai_instance = Mock()
            mock_openai_instance.generate_tweet.return_value = "Test tweet content"
            mock_openai.return_value = mock_openai_instance
            
            bot = PersonaBot(settings)
            bot.initialize()
            result = bot.post_tweet()
            
            assert result is True
            mock_openai_instance.generate_tweet.assert_called_once()
            mock_twitter_instance.post_tweet.assert_called_once_with("Test tweet content")
    
    def test_failed_tweet_generation(self):
        """Test handling when tweet generation fails."""
        settings = create_test_settings()
        
        with patch('src.core.persona_bot.TwitterClient') as mock_twitter, \
             patch('src.core.persona_bot.OpenAIClient') as mock_openai, \
             patch('src.core.persona_bot.TweetScheduler'):
            
            mock_twitter_instance = Mock()
            mock_twitter.return_value = mock_twitter_instance
            
            mock_openai_instance = Mock()
            mock_openai_instance.generate_tweet.return_value = None
            mock_openai.return_value = mock_openai_instance
            
            bot = PersonaBot(settings)
            result = bot.post_tweet()
            
            assert result is False
            mock_twitter_instance.post_tweet.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_bot_startup_and_scheduling(self):
        """Test bot starts up and schedules tweets."""
        settings = create_test_settings()
        
        with patch('src.core.persona_bot.TwitterClient'), \
             patch('src.core.persona_bot.OpenAIClient'), \
             patch('src.core.persona_bot.TweetScheduler') as mock_scheduler_class:
            
            mock_scheduler = Mock()
            mock_scheduler.schedule_tweets = Mock()
            mock_scheduler.run_pending = Mock()
            mock_scheduler_class.return_value = mock_scheduler
            
            bot = PersonaBot(settings)
            bot.running = False
            
            with patch.object(bot, 'post_tweet') as mock_post_tweet:
                task = asyncio.create_task(bot.run())
                await asyncio.sleep(0.1)
                bot.running = False
                
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                
                mock_scheduler.schedule_tweets.assert_called_once()
                mock_post_tweet.assert_called_once()