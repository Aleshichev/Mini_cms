import asyncio
import logging

logger = logging.getLogger(__name__)


async def startup_with_retry(broker, retries: int = 10, delay: int = 5):
    for attempt in range(1, retries + 1):
        try:
            await broker.startup()
            logger.info("✅ Broker successfully started")
            return
        except Exception as e:
            logger.warning(
                f"❌ Broker startup failed (attempt {attempt}/{retries}): {e}"
            )
            if attempt == retries:
                logger.error("❌ Broker startup failed after all retries.")
                raise e
            await asyncio.sleep(delay)
