# Fenced Code Extension for Python Markdown
# =========================================

# This extension adds Fenced Code Blocks to Python-Markdown.

# See https://Python-Markdown.github.io/extensions/fenced_code_blocks
# for documentation.

# Original code Copyright 2007-2008 [Waylan Limberg](https://github.com/waylan).

# All changes Copyright 2008-2014 The Python Markdown Project

# License: [BSD](https://opensource.org/licenses/bsd-license.php)

"""
This extension adds Fenced Code Blocks to Python-Markdown.

See the [documentation](https://Python-Markdown.github.io/extensions/fenced_code_blocks)
for details.
"""

from __future__ import annotations

from textwrap import dedent
import xml.etree.ElementTree as etree
from . import Extension
from ..preprocessors import Preprocessor
from ..blockprocessors import BlockProcessor
from .codehilite import CodeHilite, CodeHiliteExtension, parse_hl_lines
from .attr_list import get_attrs_and_remainder, AttrListExtension
from ..util import parseBoolValue
from ..serializers import _escape_attrib_html
import re
from typing import TYPE_CHECKING, Any, Iterable

if TYPE_CHECKING:  # pragma: no cover
    from markdown import Markdown
    from ..blockparser import BlockParser


class FencedCodeExtension(Extension):
    def __init__(self, **kwargs):
        self.config = {
            'lang_prefix': ['language-', 'Prefix prepended to the language. Default: "language-"']
        }
        """ Default configuration options. """
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """ Add fenced code block processors to the Markdown instance. """
        md.registerExtension(self)

        # Preprocessor handles top-level fenced code blocks efficiently
        md.preprocessors.register(FencedBlockPreprocessor(md, self.getConfigs()), 'fenced_code_block', 25)

        # BlockProcessor handles fenced code blocks in nested contexts (e.g., blockquotes)
        # Priority 75 places it after HashHeaderProcessor (70) and before CodeBlockProcessor (80)
        md.parser.blockprocessors.register(
            FencedCodeBlockProcessor(md.parser, md, self.getConfigs()),
            'fenced_code_block',
            75
        )


class FencedCodeMixin:
    """
    Mixin class providing shared functionality for fenced code block processing.

    This mixin contains common methods used by both FencedBlockPreprocessor and
    FencedCodeBlockProcessor to avoid code duplication.
    """

    # List of options to convert to boolean values
    BOOL_OPTIONS = [
        'linenums',
        'guess_lang',
        'noclasses',
        'use_pygments'
    ]

    def _check_for_deps(self) -> None:
        """Check for dependent extensions (CodeHilite, AttrList)."""
        if not self.checked_for_deps:
            for ext in self.md.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.getConfigs()
                if isinstance(ext, AttrListExtension):
                    self.use_attr_list = True
            self.checked_for_deps = True

    def _handle_attrs(self, attrs: Iterable[tuple[str, str]]) -> tuple[str, list[str], dict[str, Any]]:
        """Return tuple: `(id, [list, of, classes], {configs})`"""
        id_attr = ''
        classes = []
        configs = {}
        for k, v in attrs:
            if k == 'id':
                id_attr = v
            elif k == '.':
                classes.append(v)
            elif k == 'hl_lines':
                configs[k] = parse_hl_lines(v)
            elif k in self.BOOL_OPTIONS:
                configs[k] = parseBoolValue(v, fail_on_errors=False, preserve_none=True)
            else:
                configs[k] = v
        return id_attr, classes, configs

    def _generate_html(
        self, code: str, lang: str | None, id_attr: str, classes: list[str], config: dict[str, Any]
    ) -> str:
        """Generate HTML for the fenced code block."""
        if self.codehilite_conf and self.codehilite_conf['use_pygments'] and config.get('use_pygments', True):
            local_config = self.codehilite_conf.copy()
            local_config.update(config)
            # Combine classes with `cssclass`. Ensure `cssclass` is at end
            # as Pygments appends a suffix under certain circumstances.
            # Ignore ID as Pygments does not offer an option to set it.
            if classes:
                local_config['css_class'] = '{} {}'.format(
                    ' '.join(classes),
                    local_config['css_class']
                )
            highliter = CodeHilite(
                code,
                lang=lang,
                style=local_config.pop('pygments_style', 'default'),
                **local_config
            )
            return highliter.hilite(shebang=False)
        else:
            id_str = lang_str = class_str = kv_pairs = ''
            if lang:
                prefix = self.config.get('lang_prefix', 'language-')
                lang_str = f' class="{prefix}{_escape_attrib_html(lang)}"'
            if classes:
                class_str = f' class="{_escape_attrib_html(" ".join(classes))}"'
            if id_attr:
                id_str = f' id="{_escape_attrib_html(id_attr)}"'
            if self.use_attr_list and config and not config.get('use_pygments', False):
                # Only assign key/value pairs to code element if `attr_list` extension is enabled, key/value
                # pairs were defined on the code block, and the `use_pygments` key was not set to `True`. The
                # `use_pygments` key could be either set to `False` or not defined. It is omitted from output.
                kv_pairs = ''.join(
                    f' {k}="{_escape_attrib_html(v)}"' for k, v in config.items() if k != 'use_pygments'
                )
            escaped_code = self._escape(code)
            return f'<pre{id_str}{class_str}><code{lang_str}{kv_pairs}>{escaped_code}</code></pre>'

    def _escape(self, txt: str) -> str:
        """Basic HTML escaping."""
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


class FencedBlockPreprocessor(FencedCodeMixin, Preprocessor):
    """ Find and extract fenced code blocks. """

    FENCED_BLOCK_RE = re.compile(
        dedent(r'''
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*                          # opening fence
            ((\{(?P<attrs>[^\n]*)\})|                                # (optional {attrs} or
            (\.?(?P<lang>[\w#.+-]*)[ ]*)?                            # optional (.)lang
            (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot)[ ]*)?) # optional hl_lines)
            \n                                                       # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                                     # the code block
            (?P=fence)[ ]*$                                          # closing fence
        '''),
        re.MULTILINE | re.DOTALL | re.VERBOSE
    )

    def __init__(self, md: Markdown, config: dict[str, Any]):
        super().__init__(md)
        self.config = config
        self.checked_for_deps = False
        self.codehilite_conf: dict[str, Any] = {}
        self.use_attr_list = False

    def run(self, lines: list[str]) -> list[str]:
        """ Match and store Fenced Code Blocks in the `HtmlStash`. """
        self._check_for_deps()

        text = "\n".join(lines)
        index = 0
        while 1:
            m = self.FENCED_BLOCK_RE.search(text, index)
            if m:
                lang, id_attr, classes, config = None, '', [], {}
                if m.group('attrs'):
                    attrs, remainder = get_attrs_and_remainder(m.group('attrs'))
                    if remainder:  # Does not have correctly matching curly braces, so the syntax is invalid.
                        index = m.end('attrs')  # Explicitly skip over this, to prevent an infinite loop.
                        continue
                    id_attr, classes, config = self._handle_attrs(attrs)
                    if len(classes):
                        lang = classes.pop(0)
                else:
                    if m.group('lang'):
                        lang = m.group('lang')
                    if m.group('hl_lines'):
                        # Support `hl_lines` outside of `attrs` for backward-compatibility
                        config['hl_lines'] = parse_hl_lines(m.group('hl_lines'))

                code = self._generate_html(m.group('code'), lang, id_attr, classes, config)

                placeholder = self.md.htmlStash.store(code)
                text = f'{text[:m.start()]}\n{placeholder}\n{text[m.end():]}'
                # Continue from after the replaced text in the next iteration.
                index = m.start() + 1 + len(placeholder)
            else:
                break
        return text.split("\n")

    # Keep handle_attrs as public method for backward compatibility
    def handle_attrs(self, attrs: Iterable[tuple[str, str]]) -> tuple[str, list[str], dict[str, Any]]:
        """ Return tuple: `(id, [list, of, classes], {configs})` """
        return self._handle_attrs(attrs)


class FencedCodeBlockProcessor(FencedCodeMixin, BlockProcessor):
    """
    Process fenced code blocks in nested contexts (e.g., blockquotes).

    This BlockProcessor complements FencedBlockPreprocessor by handling
    fenced code blocks that are only revealed after block-level processing
    (such as stripping '>' from blockquotes).
    """

    # Pattern to detect start of fenced code block
    FENCED_START_RE = re.compile(
        r'^(?P<fence>(?:~{3,}|`{3,}))[ ]*'           # opening fence
        r'((\{(?P<attrs>[^\n]*)\})|'                  # optional {attrs} or
        r'(\.?(?P<lang>[\w#.+-]*)[ ]*)?'             # optional (.)lang
        r'(hl_lines=(?P<quot>"|\')'                  # optional hl_lines
        r'(?P<hl_lines>.*?)(?P=quot)[ ]*)?)?$'
    )

    # Pattern to detect end of fenced code block
    FENCED_END_RE = re.compile(r'^(?P<fence>(?:~{3,}|`{3,}))[ ]*$')

    def __init__(self, parser: BlockParser, md: Markdown, config: dict[str, Any]):
        super().__init__(parser)
        self.md = md
        self.config = config
        self.checked_for_deps = False
        self.codehilite_conf: dict[str, Any] = {}
        self.use_attr_list = False

    def test(self, parent: etree.Element, block: str) -> bool:
        """Test if block starts with a fenced code opening."""
        return self.FENCED_START_RE.match(block.split('\n', 1)[0]) is not None

    def run(self, parent: etree.Element, blocks: list[str]) -> bool | None:
        """Process the fenced code block."""
        self._check_for_deps()

        block = blocks.pop(0)
        lines = block.split('\n')
        first_line = lines[0]
        m_start = self.FENCED_START_RE.match(first_line)

        if not m_start:
            # Should not happen since test() passed, but be safe
            blocks.insert(0, block)
            return False

        opening_fence = m_start.group('fence')
        fence_char = opening_fence[0]
        fence_len = len(opening_fence)

        # Extract language/attrs from opening fence
        lang, id_attr, classes, config = None, '', [], {}
        if m_start.group('attrs'):
            attrs, remainder = get_attrs_and_remainder(m_start.group('attrs'))
            if remainder:
                # Invalid attrs syntax, don't process as fenced code
                blocks.insert(0, block)
                return False
            id_attr, classes, config = self._handle_attrs(attrs)
            if len(classes):
                lang = classes.pop(0)
        else:
            if m_start.group('lang'):
                lang = m_start.group('lang')
            if m_start.group('hl_lines'):
                config['hl_lines'] = parse_hl_lines(m_start.group('hl_lines'))

        # Find the closing fence
        code_lines: list[str] = []
        found_end = False

        # Check remaining lines in current block
        for i, line in enumerate(lines[1:], start=1):
            m_end = self.FENCED_END_RE.match(line)
            if m_end:
                end_fence = m_end.group('fence')
                # Closing fence must use same char and be at least as long
                if end_fence[0] == fence_char and len(end_fence) >= fence_len:
                    found_end = True
                    # Any content after closing fence in this block?
                    if i + 1 < len(lines):
                        remainder = '\n'.join(lines[i + 1:])
                        if remainder.strip():
                            blocks.insert(0, remainder)
                    break
            code_lines.append(line)

        # If not found in current block, consume subsequent blocks
        while not found_end and blocks:
            next_block = blocks.pop(0)
            next_lines = next_block.split('\n')
            for i, line in enumerate(next_lines):
                m_end = self.FENCED_END_RE.match(line)
                if m_end:
                    end_fence = m_end.group('fence')
                    if end_fence[0] == fence_char and len(end_fence) >= fence_len:
                        found_end = True
                        # Any content after closing fence?
                        if i + 1 < len(next_lines):
                            remainder = '\n'.join(next_lines[i + 1:])
                            if remainder.strip():
                                blocks.insert(0, remainder)
                        break
                code_lines.append(line)
            if not found_end:
                # Add blank line between blocks (they were separated by \n\n)
                code_lines.append('')

        if not found_end:
            # No closing fence found, treat as regular content
            blocks.insert(0, block)
            return False

        # Build code content
        code_content = '\n'.join(code_lines)
        if code_content and not code_content.endswith('\n'):
            code_content += '\n'

        # Generate HTML and store in HtmlStash
        html = self._generate_html(code_content, lang, id_attr, classes, config)
        placeholder = self.md.htmlStash.store(html)

        # Create placeholder element
        p = etree.SubElement(parent, 'p')
        p.text = placeholder

        return True


def makeExtension(**kwargs):  # pragma: no cover
    return FencedCodeExtension(**kwargs)
