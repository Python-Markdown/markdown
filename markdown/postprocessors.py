# Python Markdown

# A Python implementation of John Gruber's Markdown.

# Documentation: https://python-markdown.github.io/
# GitHub: https://github.com/Python-Markdown/markdown/
# PyPI: https://pypi.org/project/Markdown/

# Started by Manfred Stienstra (http://www.dwerg.net/).
# Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
# Currently maintained by Waylan Limberg (https://github.com/waylan),
# Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

# Copyright 2007-2023 The Python Markdown Project (v. 1.7 and later)
# Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
# Copyright 2004 Manfred Stienstra (the original version)

# License: BSD (see LICENSE.md for details).

"""

Post-processors run on the text of the entire document after is has been serialized into a string.
Postprocessors should be used to work with the text just before output. Usually, they are used add
back sections that were extracted in a preprocessor, fix up outgoing encodings, or wrap the whole
document.

"""

from __future__ import annotations

from html import escape
from typing import TYPE_CHECKING, Any
from . import util
import re

if TYPE_CHECKING:  # pragma: no cover
    from markdown import Markdown


def build_postprocessors(md: Markdown, **kwargs: Any) -> util.Registry[Postprocessor]:
    """ Build the default postprocessors for Markdown. """
    postprocessors = util.Registry()
    postprocessors.register(RawHtmlPostprocessor(md), 'raw_html', 30)
    postprocessors.register(AndSubstitutePostprocessor(), 'amp_substitute', 20)
    return postprocessors


class Postprocessor(util.Processor):
    """
    Postprocessors are run after the ElementTree it converted back into text.

    Each Postprocessor implements a `run` method that takes a pointer to a
    text string, modifies it as necessary and returns a text string.

    Postprocessors must extend `Postprocessor`.

    """

    def run(self, text: str) -> str:
        """
        Subclasses of `Postprocessor` should implement a `run` method, which
        takes the html document as a single text string and returns a
        (possibly modified) string.

        """
        pass  # pragma: no cover


class RawHtmlPostprocessor(Postprocessor):
    """ Restore raw html to the document. """

    BLOCK_LEVEL_REGEX = re.compile(r'^\<\/?([^ >]+)')

    # Match regions of code (`<pre>` and `<code>` elements). A raw HTML
    # placeholder within such a region must be restored as escaped text.
    CODE_REGION_RE = re.compile(r'<(pre|code)[\s>].*?</\1\s*>', re.DOTALL)

    def run(self, text: str) -> str:
        """ Iterate over html stash and restore html. """
        def substitute_match(m: re.Match[str]) -> str:
            if key := m.group(1):
                wrapped = True
            else:
                key = m.group(2)
                wrapped = False
            if (key := int(key)) >= self.md.htmlStash.html_counter:
                return m.group(0)
            entry = self.md.htmlStash.rawHtmlBlocks[key]
            html = self.stash_to_string(entry)
            if self.in_code_region(m.string, m.start()):
                # The placeholder is within a code block. Restore the HTML as
                # escaped text so it displays as content rather than markup.
                # The code block adds a trailing newline itself and only
                # strips `tab_length` from each line, so re-indent the content
                # accordingly.
                if isinstance(entry, util.IndentedRawHtml):
                    extra = entry.indent - self.md.tab_length
                    if extra > 0:
                        # The first line is the start tag. Its indentation is
                        # already retained by the placeholder line itself (the
                        # code block only strips `tab_length` from it), so
                        # only the following lines are re-indented.
                        lines = html.split('\n')
                        html = '\n'.join([lines[0]] + [
                            ' ' * extra + line if line else line
                            for line in lines[1:]
                        ])
                if html.endswith('\n'):
                    html = html[:-1]
                return escape(html, quote=False)
            if not wrapped or self.isblocklevel(html):
                return pattern.sub(substitute_match, html)
            return pattern.sub(substitute_match, f"<p>{html}</p>")

        if self.md.htmlStash.html_counter:
            base_placeholder = util.HTML_PLACEHOLDER % r'([0-9]+)'
            pattern = re.compile(f'<p>{ base_placeholder }</p>|{ base_placeholder }')
            return pattern.sub(substitute_match, text)
        else:
            return text

    def in_code_region(self, text: str, pos: int) -> bool:
        """ Check if position `pos` in `text` is within a `<pre>` or `<code>` region. """
        return any(m.start() < pos < m.end() for m in self.CODE_REGION_RE.finditer(text))

    def isblocklevel(self, html: str) -> bool:
        """ Check is block of HTML is block-level. """
        m = self.BLOCK_LEVEL_REGEX.match(html)
        if m:
            if m.group(1)[0] in ('!', '?', '@', '%'):
                # Comment, PHP etc...
                return True
            return self.md.is_block_level(m.group(1))
        return False

    def stash_to_string(self, text: str) -> str:
        """ Convert a stashed object to a string. """
        return str(text)


class AndSubstitutePostprocessor(Postprocessor):
    """ Restore valid entities """

    def run(self, text: str) -> str:
        text = text.replace(util.AMP_SUBSTITUTE, "&")
        return text


@util.deprecated(
    "This class is deprecated and will be removed in the future; "
    "use [`UnescapeTreeprocessor`][markdown.treeprocessors.UnescapeTreeprocessor] instead."
)
class UnescapePostprocessor(Postprocessor):
    """ Restore escaped chars. """

    RE = re.compile(r'{}(\d+){}'.format(util.STX, util.ETX))

    def unescape(self, m: re.Match[str]) -> str:
        return chr(int(m.group(1)))

    def run(self, text: str) -> str:
        return self.RE.sub(self.unescape, text)
