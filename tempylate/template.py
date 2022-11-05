# tempylate - Template

from __future__ import annotations

from typing import Any, cast
from collections.abc import Iterator, Sequence, Callable

from inspect import cleandoc
import ast

from collections import defaultdict
from dataclasses import dataclass


__all__ = ("Block", "extract_texts", "Template")


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

    _FUNCTION_NAME = "__tempylate_function"
    _FUNCTION_CODE = f"def {_FUNCTION_NAME}(self): ..."

    def __new__(cls, /, **kwargs: Any) -> Template:
        return cast(Template, super().__new__(type("<unknown>", (cls,), {}), **kwargs))

    def __init__(self, raw: str, template_name: str = "<unknown>") -> None:
        self.raw, self.template_name = raw, template_name
        self._texts, self._code_count = [], 0

        # コードの準備をする。
        for block in extract_texts(self.raw):
            if block.is_code:
                # ファイルから作られたテンプレートの場合は、エラー時に行が表示されるように改行を入れる。
                text = "{}{}".format("\n" * (block.line_number[0] + (
                    block.line_number[1] - block.line_number[0]
                )), cleandoc(block.text))

                # ブロック名が指定されているかを確認する。
                root = ast.parse(text, self.template_name)

                # 最後が`Expr`の場合は`Return`に置き換えて自動Returnするようにする。
                if root.body:
                    if isinstance(root.body[-1], ast.Expr):
                        root.body[-1] = ast.Return(value=root.body[-1].value)

                # コードを関数のコードに埋め込む。
                code = ast.parse(self._FUNCTION_CODE)
                assert isinstance(code, ast.Module) and isinstance(
                    code.body[-1], ast.FunctionDef | ast.AsyncFunctionDef
                )
                code.body[-1].body = root.body

                # 関数を生成する。
                ast.fix_missing_locations(code)
                namespace = dict[str, Any]()
                exec(compile(code, self.template_name, "exec"), namespace)
                self._code_count += 1
                namespace[self._FUNCTION_NAME].__name__ = f"_block{self._code_count}"
                setattr(
                    self, namespace[self._FUNCTION_NAME].__name__,
                    namespace[self._FUNCTION_NAME]
                )
                self._texts.append(namespace[self._FUNCTION_NAME])
            else:
                self._texts.append(block.text)

    def update(self, kwargs: dict[str, Any]) -> None:
        "Assign a value to the instance."
        for key, value in kwargs.items():
            setattr(self, key, value)

    def render(_tempylate_self, **kwargs: Any) -> str:
        "Renders the template."
        return "".join(
            text if isinstance(text, str) else text()
            for text in self._texts
        )