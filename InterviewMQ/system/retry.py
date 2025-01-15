import asyncio
from typing import Callable

async def _retry(self, func: Callable, *args, **kwargs):
        """
        Retry mechanism with exponential backoff.
        """
        for attempt in range(1, self.retry_limit + 1):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                wait_time = self.backoff_base * (2 ** (attempt - 1))
                print(f"Attempt {attempt} failed: {e}. Retrying in {wait_time:.2f}s...")
                await asyncio.sleep(wait_time)

        print("Retry limit reached. Giving up.")
        raise Exception("Failed to process message after retries.")