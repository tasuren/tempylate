# tempylate - Template

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from collections.abc import Iterator, Iterable

from inspect import cleandoc
import ast

import asyncio

from .exceptions import LoadBlockError
from .builtins import builtins as default_builtins
from .types import BlockFunction

if TYPE_CHECKING:
    from .manager import Manager


__all__ = ("extract_texts", "Template")


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
                tentative = line
                may = True
        elif may:
            may = False
        # blockを書き込んでいく。
        now += character
    yield (tentative, line), block, now


_FUNCTION = "def __tempylate_function(<args>): ..."
_FUNCTION_ASYNC = f"async {_FUNCTION}"


class Template:
    """Class for storing template strings.
    This class can be used to render templates.

    Args:
        raw: The template string.
        builtins: A dictionary containing the names and values of built-in variables that can be used from the beginning at rendering time.
        manager: Instance of the Manager class. This argument is used when creating a template from Manager and does not have to be used.
        loop: Event Loop.
        executor: The executor to use with ``loop.run_in_executor``."""

    raw: str
    "Template string."
    builtins: dict[str, Any]
    "A dictionary containing variables that can be used by default in the template."
    manager: Manager | None
    "Instance of the Manager class used to create the template."
    blocks: dict[str, BlockFunction]
    "A dictionary in which the functions of the block are stored."
    loop: asyncio.AbstractEventLoop | None = None
    "Event Loop."
    executor: Any = None
    "The executor to use with ``loop.run_in_executor``."
    prepared: bool = False
    "Whether or not :meth:`.prepare` has already been executed."

    def __init__(
        self, raw: str, builtins: dict[str, Any] | None = None, manager: Manager | None = None,
        loop: asyncio.AbstractEventLoop | None = None, executor: Any = None
    ):
        self.raw, self.builtins, self.manager = raw, builtins or {}, manager
        self.blocks, self.loop, self.executor = {}, loop, executor
        self._objects: list[str | BlockFunction] = []
        self.builtins.update(default_builtins)

        if self.manager is not None:
            self.loop, self.executor = self.manager.loop, self.manager.executor

    def prepare(
        self, args: Iterable[str] = (), template_name: str | None = None,
        async_mode: bool = False
    ) -> None:
        """Prepare a template.
        Running this will store the blocks in the template as a function in :var:`.blocks`.
        This can be done all at once.

        Args:
            args: An iterable that returns the names of variables that can be used in a block of templates.
            template_name: The name to be displayed in case of an error. If not specified, `"<unknown>"` is used.
            async_mode: Whether the function of the block to be generated should be a coroutine function or not.

        Notes:
            This is done automatically when :meth:`.render` or :meth:`.aiorender` is executed."""
        if self.prepared:
            raise LoadBlockError("The block has already been loaded.")
        self.prepared = True

        # テンプレートの文字列からブロックを取り出していく。
        name = ""
        for index, ((first, _), is_block, text) in enumerate(extract_texts(self.raw)):
            if is_block:
                text = cleandoc(text)
                # ファイルから作られたテンプレートの場合は、エラー時に行が表示されるように改行を入れる。
                if template_name is None:
                    template_name = "<unknown>"
                else:
                    text = "{}{}".format("\n"*(first-1), text)

                # ブロック名が指定されているかを確認する。
                root = ast.parse(text, template_name)
                for node in ast.walk(root):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        if node.func.id != "name":
                            continue

                        if not node.args:
                            raise LoadBlockError("The `name` function does not have a name argument.")
                        if not isinstance(node.args[0], ast.Constant) \
                                or not isinstance(node.args[0].value, str):
                            raise LoadBlockError("Passed to the `name` function is not a string.")
                        name = node.args[0].value
                if not name:
                    name = f"block{index}"

                # 最後が`Expr`の場合は`Return`に置き換えて自動Returnするようにする。
                if root.body:
                    if isinstance(root.body[-1], ast.Expr):
                        root.body[-1] = ast.Return(value=root.body[-1].value)

                # コードを関数のコードに埋め込む。
                code = ast.parse((_FUNCTION_ASYNC if async_mode else _FUNCTION
                ).replace("<args>", ",".join(args)))
                assert isinstance(code, ast.Module) and isinstance(
                    code.body[-1], ast.FunctionDef | ast.AsyncFunctionDef
                )
                code.body[-1].body = root.body

                # 関数を生成する。
                ast.fix_missing_locations(code)
                namespace: dict[str, Any] = {}
                exec(compile(code, template_name, "exec"), namespace)
                self.blocks[name] = namespace["__tempylate_function"]
                self.blocks[name].__name__ = name
                self._objects.append(self.blocks[name])
            else:
                self._objects.append(text)

    def _set_builtins_default(self, kwargs):
        # `.builtins`をデフォルトに設定します。
        for key, value in self.builtins.items():
            kwargs.setdefault(key, value)

    def _prepare(self, kwargs, template_name, async_mode):
        # `.prepare`が一度も実行されていない時のみ`.prepare`を実行します。
        self._set_builtins_default(kwargs)
        if not self.prepared:
            self.prepare(kwargs.keys(), template_name, async_mode)

    def render(self, template_name: str | None = None, **kwargs: Any) -> str:
        """Renders the template.

        Args:
            template_name: The name of the template.
            **kwargs: A dictionary of names and values of variables to be passed to the template."""
        self._prepare(kwargs, template_name, False)
        return "".join(
            obj if isinstance(obj, str) else obj(**kwargs) or "" # type: ignore
            for obj in self._objects
        )

    async def aiorender(
        self, template_name: str | None = None, load_block_run_in_executor: bool = True,
        executor: Any = None, **kwargs: Any
    ) -> str:
        """Asynchronous template rendering.

        Args:
            load_block_run_in_executor: Whether the block should be loaded using `loop.run_in_executor`.
                If your blocks are often huge and complex, you may want to enable this.
                This is because it may take longer to load the blocks.
            executor: Used in ``executor`` when the argument ``load_block_run_in_executor`` is ``True``.
            template_name: The name of the template.
            **kwargs: A dictionary of names and values of variables to be passed to the template."""
        if load_block_run_in_executor:
            self._prepare_loop()
            if not self.prepared:
                assert self.loop is not None
                if self.manager is not None:
                    executor = self.manager.executor
                await self.loop.run_in_executor(
                    executor, lambda: self._prepare(kwargs, template_name, True)
                )
        else:
            self._prepare(kwargs, template_name, True)

        return "".join([
            obj if isinstance(obj, str) else await obj(**kwargs) or "" # type: ignore
            for obj in self._objects if not print(obj)
        ])

    def _prepare_loop(self):
        # イベントループを準備します。
        if self.loop is None:
            self.loop = asyncio.get_running_loop()

    def execute(self, block_name: str, **kwargs: Any) -> str:
        """Execute another block.

        Args:
            block_name: The name of the block.
            **kwargs: The keyword arguments to be passed to the block function.

        Raises:
            KeyError: Occurs when a block is not found."""
        self._set_builtins_default(kwargs)
        return self.blocks[block_name](**kwargs) # type: ignore

    async def aioexecute(self, block_name: str, **kwargs: Any) -> str:
        "Asynchronous version of :meth:`.execute`."
        return await self.execute(block_name, **kwargs) # type: ignore