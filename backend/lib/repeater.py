import asyncio
import logging
from typing import Any, Callable


def repeat_on_error(retries: int = 3, delay: int = 3) -> Callable:
    """Decorator to repeat function call on error"""

    def decorator(func: Callable) -> Callable:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            for i in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if i == retries - 1:
                        raise e
                    else:
                        logging.error(f"Error in function {func.__name__}. Retrying {i+1}/{retries}")
                        await asyncio.sleep(delay)

        return wrapper

    return decorator
