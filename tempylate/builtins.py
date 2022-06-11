# tempylate - Builtins

from typing import Any
from collections.abc import Callable, Coroutine

from html import escape
import textwrap

from collections import defaultdict
from os import stat

from .utils import run_in_executor


__all__ = ("include", "aioinclude", "escape", "textwrap", "CS", "builtins")


_include_caches: defaultdict[str, list] = defaultdict(lambda : [0, None])
def include(path: str, __tempylate_cached: bool = False) -> str:
    """Include other file.

    Args:
        path: The path to a file.

    Notes: Use the last modified date of the file to cache it."""
    mtime = stat(path).st_mtime
    cached = False
    if mtime != _include_caches[path][0]:
        cached = True
        _include_caches[path][0] = mtime
        with open(path, "r") as f:
            _include_caches[path][1] = f.read()
    if __tempylate_cached:
        return _include_caches[path][1], cached # type: ignore
    return _include_caches[path][1]


def aioinclude(path: str, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, str]:
    """This is an asynchronous version of :func:`tempylate.builtins.include`.  
    This is using the :func:`utils.run_in_executor`.

    Args:
        path: The path to a file.
        *args: Argument passed to :func:`tempylate.utils.run_in_executor` following ``function``.
        **kwargs: Keyword arguments to be passed to :func:`tempylate.utils.run_in_executor`."""
    cached = kwargs.pop("__tempylate_cached", False)
    return run_in_executor(
        lambda: include(path, cached),
        *args, **kwargs
    )


CS = "^^"
"""This is just a constant with two caret signs in it.  
Use this when you want to use two caret signs side by side in a string defined in the Python code in the block."""


builtins: dict[str, Callable[..., Any]] = {
    name: globals()[name] for name in __all__ if name != "builtins"
}
"A dictionary of what is in ``tempylate.builtins``."