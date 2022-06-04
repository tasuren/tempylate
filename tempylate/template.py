# tempylate - Template

from typing import Any
from collections.abc import Iterator

from .manager import Manager


def extract_texts(template: str) -> Iterator[tuple[tuple[int, int], bool, str]]:
    """Extract a block and text of template from a string.

    Args:
        template: Target text.

    Yields:
        This is an integer indicating how many lines are the first and last of the extracted string, a boolean indicating whether it is a block, and a tuple of the body text."""
    now, may, block, line = "", False, False, 0
    tentative = 0
    # ブロックを取得します。
    for character in template:
        if character == "\n":
            line += 1
        # tempylateのブロックかどうかを調べる。
        if character == "^":
            if may:
                # ブロック終了時にはそのブロックを追加する。
                yield (tentative, line), block, now[:-1]
                now, block = "", not block
                continue
            else:
                tentative = now
                may = True
        elif may:
            may = False
        # blockを書き込んでいく。
        now += character
    yield (tentative, line), block, now


class Template:
    """Class for storing template strings.
    This class can be used to render templates.

    Args:
        raw: The template string.
        builtins: A dictionary containing the names and values of built-in variables that can be used from the beginning at rendering time.
        manager: Instance of the Manager class. This argument is used when creating a template from Manager and does not have to be used."""

    raw: str
    "Template string."
    manager: Manager | None
    "Instance of the Manager class used to create the template."

    def __init__(
        self, raw: str, builtins: dict[str, Any] | None = None,
        manager: Manager | None = None
    ):
        self.raw, self.builtins, self.manager = raw, builtins or {}, manager

    def prepare(self) -> None:
        "Prepare a template."
        for first, _, is_block, text in extract_texts(self.raw):
            ...

    def render(self, **kwargs: Any) -> str:
        ...