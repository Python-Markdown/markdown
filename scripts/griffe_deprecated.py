"""Griffe extension for `@markdown.util.deprecated` decorator support."""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING

from griffe import Docstring, Extension
from griffe.docstrings.dataclasses import DocstringSectionAdmonition

if TYPE_CHECKING:
    from griffe import Class, Function, ObjectNode


def _deprecated(obj: Class | Function) -> str | None:
    for decorator in obj.decorators:
        if decorator.callable_path == "markdown.util.deprecated":
            return ast.literal_eval(str(decorator.value.arguments[0]))
    return None


class DeprecatedExtension(Extension):
    """Griffe extension for `@markdown.util.deprecated` decorator support."""

    def _insert_message(self, obj: Function | Class, message: str) -> None:
        if not obj.docstring:
            obj.docstring = Docstring("", parent=obj)
        sections = obj.docstring.parsed
        sections.insert(0, DocstringSectionAdmonition(kind="warning", text=message, title="Deprecated"))

    def on_class_instance(self, node: ast.AST | ObjectNode, cls: Class) -> None:  # noqa: ARG002
        """Add section to docstrings of deprecated classes."""
        if message := _deprecated(cls):
            self._insert_message(cls, message)
            cls.labels.add("deprecated")

    def on_function_instance(self, node: ast.AST | ObjectNode, func: Function) -> None:  # noqa: ARG002
        """Add section to docstrings of deprecated functions."""
        if message := _deprecated(func):
            self._insert_message(func, message)
            func.labels.add("deprecated")
