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
try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


class HTMLExtractor(HTMLParser):
    """
    Extract raw HTML from text.

    The raw HTML is stored in the `htmlStash` of the Markdown instance passed
    to `md` and the remaining text is stored in `cleandoc` as a list of strings.
    """

    def __init__(self, md, *args, **kwargs):
        # This calls self.reset
        HTMLParser.__init__(self, *args, **kwargs)  # TODO: Use super when we drop PY2 support
        self.md = md

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.inraw = False
        self.stack = []  # When inraw==True, stack contains a list of tags
        self._cache = []
        self.cleandoc = []
        HTMLParser.reset(self)  # TODO: Use super when we drop PY2 support

    def close(self):
        """Handle any buffered data."""
        HTMLParser.close(self)  # TODO: Use super when we drop PY2 support
        # Handle any unclosed tags.
        if len(self._cache):
            self.cleandoc.append(self.md.htmlStash.store(''.join(self._cache)))
            self._cache = []

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)

        line, col = self.getpos()
        if col < 4 and self.md.is_block_level(tag) and not self.inraw:
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
            self.cleandoc.append('\n')
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

    def handle_comment(self, data):
        text = '<!--{}-->'.format(data)
        line, col = self.getpos()
        if self.inraw:
            # Append this to the existing raw block
            self._cache.append(text)
        else:
            # Handle this as a standalone raw block
            self.cleandoc.append(self.md.htmlStash.store(text))
