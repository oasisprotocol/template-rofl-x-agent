"""Main entry point for the twitter persona bot."""

import asyncio
import logging
import signal
import sys
from typing import Optional

from src.config import load_settings
from src.core.persona_bot import PersonaBot

logger = logging.getLogger(__name__)

# Reduce noise from httpx logger
logging.getLogger("httpx").setLevel(logging.WARNING)


class GracefulShutdown:
    """Handle graceful shutdown on SIGINT/SIGTERM."""
    
    def __init__(self):
        self.shutdown_event = asyncio.Event()
        self.bot: Optional[PersonaBot] = None
        
    def handle_signal(self, signum: int, frame: Optional[object]) -> None:
        """Handle shutdown signals.
        
        Args:
            signum: Signal number
            frame: Current stack frame
        """
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown_event.set()
        
    async def wait_for_shutdown(self) -> None:
        """Wait for shutdown signal."""
        await self.shutdown_event.wait()
        
    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)


async def main() -> None:
    """Run the twitter persona bot."""
    shutdown_handler = GracefulShutdown()
    shutdown_handler.setup_signal_handlers()
    
    try:
        # Load configuration
        settings = load_settings()
        logger.info("Twitter Persona Bot starting...")
        
        # Initialize bot
        bot = PersonaBot(settings)
        shutdown_handler.bot = bot
        
        # Create bot task
        bot_task = asyncio.create_task(bot.run())
        shutdown_task = asyncio.create_task(shutdown_handler.wait_for_shutdown())
        
        # Wait for either bot completion or shutdown signal
        done, pending = await asyncio.wait(
            [bot_task, shutdown_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        
        # Cancel pending tasks
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
                
        # If bot task completed with error, re-raise it
        for task in done:
            if task == bot_task and task.exception():
                raise task.exception()
                
    except asyncio.TimeoutError:
        logger.error("Bot operation timed out")
        sys.exit(1)
    except asyncio.CancelledError:
        logger.info("Bot operation cancelled")
    except Exception as e:
        logger.error(f"Bot error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Twitter Persona Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())