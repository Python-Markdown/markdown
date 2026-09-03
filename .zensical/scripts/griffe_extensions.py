"""Griffe extensions."""

from __future__ import annotations

import ast
from typing import TYPE_CHECKING, Any
import textwrap

from griffe import Docstring, Extension, DocstringSectionAdmonition, DocstringSectionText, Visitor, Inspector

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

    def on_class_instance(self, node: ast.AST | ObjectNode, cls: Class, agent: Visitor | Inspector, **kwargs: Any) -> None:  # noqa: ARG002
        """Add section to docstrings of deprecated classes."""
        if message := _deprecated(cls):
            self._insert_message(cls, message)
            cls.labels.add("deprecated")

    def on_function_instance(self, node: ast.AST | ObjectNode, func: Function, agent: Visitor | Inspector, **kwargs: Any) -> None:  # noqa: ARG002
        """Add section to docstrings of deprecated functions."""
        if message := _deprecated(func):
            self._insert_message(func, message)
            func.labels.add("deprecated")


class PriorityTableExtension(Extension):
    """ Griffe extension to insert a table of processor priority in specified functions. """

    def __init__(self, paths: list[str] | None = None) -> None:
        super().__init__()
        self.paths = paths

    def linked_obj(self, value: str, path: str) -> str:
        """ Wrap object name in reference link. """
        return f'[`{value}`][{path}.{value}]'

    def on_function_instance(self, node: ast.AST | ObjectNode, func: Function, agent: Visitor | Inspector, **kwargs: Any) -> None:  # noqa: ARG002
        """Add table to specified function docstrings."""
        if self.paths and func.path not in self.paths:
            return  # skip objects that were not selected

        # Table header
        data = [
            'Class Instance | Name | Priority',
            '-------------- | ---- | :------:'
        ]

        # Extract table body from source code of function.
        for obj in node.body:
            # Extract the arguments passed to `util.Registry.register`.
            if isinstance(obj, ast.Expr) and isinstance(obj.value, ast.Call) and obj.value.func.attr == 'register':
                _args = obj.value.args
                cls = self.linked_obj(_args[0].func.id, func.path.rsplit('.', 1)[0])
                name = _args[1].value
                priority = str(_args[2].value)
                if func.name == ('build_inlinepatterns'):
                    # Include Pattern: first arg passed to class
                    if isinstance(_args[0].args[0], ast.Constant):
                        # Pattern is a string
                        value = f'`"{_args[0].args[0].value}"`'
                    else:
                        # Pattern is a variable
                        value = self.linked_obj(_args[0].args[0].id, func.path.rsplit('.', 1)[0])
                    cls = f'{cls}({value})'
                data.append(f'{cls} | `{name}` | `{priority}`')

        table = '\n'.join(data)
        body = (
            f"Return a [`{func.returns.canonical_name}`][{func.returns.canonical_path}] instance which contains "
            "the following collection of classes with their assigned names and priorities.\n\n"
            f"{table}"
        )

        # Add to docstring.
        if not func.docstring:
            func.docstring = Docstring("", parent=func)
        sections = func.docstring.parsed
        sections.append(DocstringSectionText(body, title="Priority Table"))
