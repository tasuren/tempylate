# tempylate - Utils

from typing import TypeVar, Any
from collections.abc import Callable

from asyncio import AbstractEventLoop, get_running_loop


__all__ = ("run_in_executor",)


ReT = TypeVar("ReT")
async def run_in_executor(
    function: Callable[[], ReT],
    loop: AbstractEventLoop | None = None,
    executor: Any = None
) -> ReT:
    """Execute the passed function in an asynchronous event loop ``run_in_executor``.

    Args:
        function: Function to execute.
        loop: The event loop to be used.
            If not specified, ``asyncio.get_running_loop`` is used to automatically get the event loop.
        executor: The executor to be used."""
    loop = loop or get_running_loop()
    return await loop.run_in_executor(executor, function)