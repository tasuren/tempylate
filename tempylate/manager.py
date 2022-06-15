# tempylate - Manager

from typing import Generic, TypeVar, Any
from collections.abc import Callable, Iterable

from asyncio import AbstractEventLoop

from .template import Template
from .builtins import builtins


__all__ = ("Manager",)


TemplateT = TypeVar("TemplateT", bound=Template, covariant=True)
class Manager(Generic[TemplateT]):
    """This class manages templates.
    Rendering with it will save cache and thus improve operating speed.

    Args:
        builtins: A dictionary containing the names and values of variables that are available by default in the template.
        adjustors: This function is called each time a template is rendered.
            The function is passed an instance (``self``) of the template :class:`tempylate.template.Template` and a dictionary containing the names and values of variables to pass to the template.
        cls: Template class used for template rendering.
            Defaults to :class:`tempylate.template.Template`.
        loop: Event loop used for asynchronous rendering.
        executor: An executor used for asynchronous rendering."""

    def __init__(
        self, builtins: dict[str, Any] | None = None,
        adjustors: list[Callable[[TemplateT, dict[str, Any]], Any]] | None = None,
        cls: type[TemplateT] | None = None, loop: AbstractEventLoop | None = None,
        executor: Any = None
    ):
        self.builtins, self.adjustors = builtins or {}, adjustors or []
        self.cls, self.loop, self.executor = cls or Template, loop, executor
        self.caches: dict[str, Template] = {}

    def _prepare_template(self, raw, template_name, kwargs):
        # キャッシュの用意をする。
        if kwargs.pop("__tempylate_cached", False) or template_name not in self.caches:
            self.caches[template_name] = self.cls(raw, self.builtins, self)
        # Adjustorを実行する。
        for adjustor in self.adjustors:
            adjustor(self.caches[template_name], kwargs)

        return self.caches[template_name]

    def render(self, raw: str, template_name: str, **kwargs: Any) -> str:
        """Renders the passed template.

        Args:
            raw: Template string.
            template_name: The name of the template to be rendered.
                This is the name to be assigned to the cache and must be unique for each template.
            **kwargs: Keyword argument passed to :meth:`tempylate.template.Template.render`."""
        return self._prepare_template(raw, template_name, kwargs) \
            .render(template_name, **kwargs)

    async def aiorender(
        self, raw: str, template_name: str, *args, **kwargs: Any
    ) -> str:
        """This is an asynchronous version of :meth:`.render`.

        Args:
            raw: Template string.
            template_name: The name of the template to be rendered.
                This is the name to be assigned to the cache and must be unique for each template.
            *args: Argument passed to :meth:`tempylate.template.Template.aiorender`.
            **kwargs: Keyword argument passed to :meth:`tempylate.template.Template.aiorender`."""
        return await self._prepare_template(raw, template_name, kwargs) \
            .aiorender(template_name, *args, **kwargs)

    def render_from_file(self, path: str, **kwargs: Any) -> str:
        """Render the template from file.

        Args:
            path: The path to the template file.
            **kawrgs: Keyword argument passed to :meth:`.render`."""
        content, cached = builtins["include"](path, True)
        kwargs["__tempylate_cached"] = cached
        return self.render(content, path, **kwargs)

    async def aiorender_from_file(
        self, path: str, *args, aioinclude_args: Iterable[Any] = (),
        aioinclude_kwargs: dict[str, Any] | None = None, **kwargs: Any
    ) -> str:
        """This is an asynchronous version of :meth:`.render_from_file`.

        Args:
            path: The path to the template file.
            *args: Arguments passed to :meth:`tempylate.builtins.aioinclude`.
            **kwargs: Keyword argument passed to :meth:`.aiorender`."""
        aioinclude_kwargs = aioinclude_kwargs or {}
        aioinclude_kwargs.setdefault("loop", self.loop)
        aioinclude_kwargs.setdefault("executor", self.executor)
        content, cached = await builtins["aioinclude"](
            path, *aioinclude_args, __tempylate_cached=True, **aioinclude_kwargs
        )
        kwargs["__tempylate_cached"] = cached
        return await self.aiorender(content, path, *args, **kwargs)