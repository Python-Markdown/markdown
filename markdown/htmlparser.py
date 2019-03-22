# -*- coding: utf-8 -*-
"""
Python Markdown

A Python implementation of John Gruber's Markdown.

Documentation: https://python-markdown.github.io/
GitHub: https://github.com/Python-Markdown/markdown/
PyPI: https://pypi.org/project/Markdown/

Started by Manfred Stienstra (http://www.dwerg.net/).
Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
Currently maintained by Waylan Limberg (https://github.com/waylan),
Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

Copyright 2007-2019 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from __future__ import unicode_literals
from . import util
try:
    import HTMLParser as parser
except ImportError:
    from html import parser
import re

# Monkeypatch HTMLParser to only accept `?>` to close Processing Instructions.
parser.piclose = re.compile(r'\?>')
# Monkeypatch HTMLParser to only recognize entity references with a closing semicolon.
parser.entityref = re.compile(r'&([a-zA-Z][-.a-zA-Z0-9]*);')


class HTMLExtractor(parser.HTMLParser):
    """
    Extract raw HTML from text.

    The raw HTML is stored in the `htmlStash` of the Markdown instance passed
    to `md` and the remaining text is stored in `cleandoc` as a list of strings.
    """

    def __init__(self, md, *args, **kwargs):
        if util.PY3 and 'convert_charrefs' not in kwargs:
            kwargs['convert_charrefs'] = False
        # This calls self.reset
        parser.HTMLParser.__init__(self, *args, **kwargs)  # TODO: Use super when we drop PY2 support
        self.md = md

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.inraw = False
        self.stack = []  # When inraw==True, stack contains a list of tags
        self._cache = []
        self.cleandoc = []
        parser.HTMLParser.reset(self)  # TODO: Use super when we drop PY2 support

    def close(self):
        """Handle any buffered data."""
        parser.HTMLParser.close(self)  # TODO: Use super when we drop PY2 support
        # Handle any unclosed tags.
        if len(self._cache):
            self.cleandoc.append(self.md.htmlStash.store(''.join(self._cache)))
            self._cache = []

    @property
    def line_offset(self):
        """Returns char index in self.rawdata for the start of the current line. """
        if self.lineno > 1:
            return re.match(r'([^\n]*\n){{{}}}'.format(self.lineno-1), self.rawdata).end()
        return 0

    def at_line_start(self):
        """
        Returns True if current position is at start of line.

        Allows for up to three blank spaces at start of line.
        """
        if self.offset == 0:
            return True
        if self.offset > 3:
            return False
        # Confirm up to first 3 chars are whitespace 
        return self.rawdata[self.line_offset:self.offset].strip() == ''

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)

        if self.at_line_start() and self.md.is_block_level(tag) and not self.inraw:
            # Started a new raw block
            self.inraw = True
            if len(self.cleandoc):
                # Insert blank line between this and previous line.
                self.cleandoc.append('\n')

        text = self.get_starttag_text()
        if self.inraw:
            self._cache.append(text)
        else:
            self.cleandoc.append(text)

    def handle_endtag(self, tag):
        # Attempt to extract actual tag from raw source text
        start = self.line_offset + self.offset
        m = parser.endendtag.search(self.rawdata, start)
        if m:
            text = self.rawdata[start:m.end()]
        else:
            # Failed to extract from raw data. Assume well formed and lowercase.
            text = '</{0}>'.format(tag)

        if tag in self.stack:
            while self.stack:
                if self.stack.pop() == tag:
                    break
        if self.inraw and len(self.stack) == 0:
            # End of raw block
            self.inraw = False
            self._cache.append(text)
            self.cleandoc.append(self.md.htmlStash.store(''.join(self._cache)))
            # Insert blank line between this and next line. TODO: make this conditional??
            self.cleandoc.append('\n\n')
            self._cache = []
        elif self.inraw:
            self._cache.append(text)
        else:
            self.cleandoc.append(text)

    def handle_data(self, data):
        if self.inraw:
            self._cache.append(data)
        else:
            self.cleandoc.append(data)

    def handle_empty_tag(self, data, is_block):
        """ Handle empty tags (`<data>`). """
        if self.inraw:
            # Append this to the existing raw block
            self._cache.append(data)
        elif self.at_line_start() and is_block:
            # Handle this as a standalone raw block
            self.cleandoc.append(self.md.htmlStash.store(data))
            # Insert blank line between this and next line.
            self.cleandoc.append('\n\n')
        else:
            self.cleandoc.append(data)

    def handle_startendtag(self, tag, attrs):
        self.handle_empty_tag(self.get_starttag_text(), is_block=self.md.is_block_level(tag))

    def handle_charref(self, name):
        self.handle_empty_tag('&#{};'.format(name), is_block=False)

    def handle_entityref(self, name):
        self.handle_empty_tag('&{};'.format(name), is_block=False)

    def handle_comment(self, data):
        self.handle_empty_tag('<!--{}-->'.format(data), is_block=True)

    def handle_decl(self, data):
        self.handle_empty_tag('<!{}>'.format(data), is_block=True)

    def handle_pi(self, data):
        self.handle_empty_tag('<?{}?>'.format(data), is_block=True)

    def unknown_decl(self, data):
        end = ']]>' if data.startswith('CDATA[') else ']>'
        self.handle_empty_tag('<![{}{}'.format(data, end), is_block=True)
