# Abbreviation Extension for Python-Markdown
# ==========================================

# This extension adds abbreviation handling to Python-Markdown.

# See https://Python-Markdown.github.io/extensions/abbreviations
# for documentation.

# Original code Copyright 2007-2008 [Waylan Limberg](http://achinghead.com/)
# and [Seemant Kulleen](http://www.kulleen.org/)

# All changes Copyright 2008-2014 The Python Markdown Project

# License: [BSD](https://opensource.org/licenses/bsd-license.php)

"""
This extension adds abbreviation handling to Python-Markdown.

See the [documentation](https://Python-Markdown.github.io/extensions/abbreviations)
for details.
"""

from __future__ import annotations

from . import Extension
from ..blockprocessors import BlockProcessor
from ..inlinepatterns import InlineProcessor
from ..treeprocessors import Treeprocessor
from ..util import AtomicString, deprecated
import re
import xml.etree.ElementTree as etree


class AbbrExtension(Extension):
    """ Abbreviation Extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Insert `AbbrTreeprocessor` and `AbbrBlockprocessor`. """
        treeprocessor = AbbrTreeprocessor(md)
        md.treeprocessors.register(treeprocessor, 'abbr', 7)
        md.parser.blockprocessors.register(AbbrBlockprocessor(md.parser, treeprocessor.abbrs), 'abbr', 16)


class AbbrTreeprocessor(Treeprocessor):
    """ Replace abbr text with `<abbr>` elements. """

    def __init__(self, md: Markdown | None=None):
        self.abbrs = {}
        self.RE = None
        super().__init__(md)

    def iter_element(self, el, parent=None):
        ''' Resursively iterate over elements, run regex on text and wrap matches in `abbr` tags. '''
        for child in reversed(el):
            self.iter_element(child, el)
        if text := el.text:
            for m in reversed(list(self.RE.finditer(text))):
                abbr = etree.Element('abbr', {'title': self.abbrs[m.group(0)]})
                abbr.text = AtomicString(m.group(0))
                abbr.tail = text[m.end():]
                el.insert(0, abbr)
                text = text[:m.start()]
            el.text = text
        if parent and el.tail:
            tail = el.tail
            index = list(parent).index(el) + 1
            for m in reversed(list(self.RE.finditer(tail))):
                abbr = etree.Element('abbr', {'title': self.abbrs[m.group(0)]})
                abbr.text = AtomicString(m.group(0))
                abbr.tail = tail[m.end():]
                parent.insert(index, abbr)
                tail = tail[:m.start()]
            el.tail = tail

    def run(self, root: etree.Element) -> etree.Element | None:
        ''' Step through tree to find known abbreviations. '''
        if not self.abbrs:
            # No abbrs defined. Skip running processor.
            return
        # Build and compile regex
        self.RE = re.compile(f"\\b(?:{ '|'.join(re.escape(key) for key in self.abbrs.keys()) })\\b")
        # Step through tree and modify on matches
        self.iter_element(root)
        return


class AbbrBlockprocessor(BlockProcessor):
    """ Abbreviation Blockprocessor - parse text for abbr references. """

    RE = re.compile(r'^[*]\[(?P<abbr>[^\\]*?)\][ ]?:[ ]*\n?[ ]*(?P<title>.*)$', re.MULTILINE)

    def __init__(self, parser, abbrs):
        self.abbrs = abbrs
        super().__init__(parser)

    def test(self, parent: etree.Element, block: str) -> bool:
        return True

    def run(self, parent: etree.Element, blocks: list[str]) -> bool:
        """
        Find and remove all Abbreviation references from the text.
        Each reference is added to the abbrs collection.

        """
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            abbr = m.group('abbr').strip()
            title = m.group('title').strip()
            self.abbrs[abbr] = title
            if block[m.end():].strip():
                # Add any content after match back to blocks as separate block
                blocks.insert(0, block[m.end():].lstrip('\n'))
            if block[:m.start()].strip():
                # Add any content before match back to blocks as separate block
                blocks.insert(0, block[:m.start()].rstrip('\n'))
            return True
        # No match. Restore block.
        blocks.insert(0, block)
        return False


@deprecated("This class will be removed in the future; use `AbbrTreeprocessor` instead.")
class AbbrInlineProcessor(InlineProcessor):
    """ Abbreviation inline pattern. """

    def __init__(self, pattern: str, title: str):
        super().__init__(pattern)
        self.title = title

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:
        abbr = etree.Element('abbr')
        abbr.text = AtomicString(m.group('abbr'))
        abbr.set('title', self.title)
        return abbr, m.start(0), m.end(0)


def makeExtension(**kwargs):  # pragma: no cover
    return AbbrExtension(**kwargs)
