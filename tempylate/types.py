# tempylate - Types

from typing import TypeAlias, Any
from collections.abc import Callable, Coroutine


__all__ = ("BlockFunction",)


BlockFunction: TypeAlias = Callable[..., str | Coroutine[Any, Any, str]]
"The function type of the block."