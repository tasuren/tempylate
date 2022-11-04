# tempylate - Template

from typing import Any
from collections.abc import Iterator, Iterable

from dataclasses import dataclass


__all__ = ("Text", "extract_texts", "Template")


@dataclass
class Block:
    "Data class for storing the contents of retrieved strings."

    line_number: tuple[int, int]
    "A tuple of the number of lines at the beginning and end of the retrieved string."
    is_code: bool
    "Code or not."
    text: str
    "Body text."


def extract_texts(template: str) -> Iterator[Block]:
    """Extract a text of template from a string.

    Args:
        template: Target text."""
    now, may, block, line, left_new_line = "", False, False, 0, -1
    tentative = 0
    # ブロックを取得します。
    for character in template:
        if character == "\n":
            line += 1
        if left_new_line == -1 and character not in ("\n", " ", "\t"):
            left_new_line = line
        # tempylateのブロックかどうかを調べる。
        if character == "^":
            if may:
                # ブロック終了時にはそのブロックを追加する。
                yield Block((tentative, left_new_line), block, now[:-1])
                now, block, left_new_line = "", not block, -1
                continue
            else:
                if not block:
                    tentative = line
                may = True
        elif may:
            may = False
        # blockを書き込んでいく。
        now += character
    yield Block((tentative, line), block, now)


class Template:
    "This class represents a template."

    def __init__(self, raw: str) -> None:
        self.raw = raw

    def _prepare(self, keys: Iterable[str]) -> None:
        ...

    def render(_tempylate_self, **kwargs: Any) -> str:
        "Renders the template."
        self = _tempylate_self
        return