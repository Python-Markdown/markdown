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

Copyright 2007-2018 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from __future__ import unicode_literals
from markdown.test_tools import TestCase


class TestFootnotes(TestCase):

    def test_backlink_text(self):
        """Test backlink configuration."""

        self.assertMarkdownRenders(
            'paragraph[^1]\n\n[^1]: A Footnote',
            '<p>paragraph<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">back</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extensions=['footnotes'],
            extension_configs={'footnotes': {'BACKLINK_TEXT': 'back'}}
        )

    def test_footnote_separator(self):
        """Test separator configuration."""

        self.assertMarkdownRenders(
            'paragraph[^1]\n\n[^1]: A Footnote',
            '<p>paragraph<sup id="fnref-1"><a class="footnote-ref" href="#fn-1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn-1">\n'
            '<p>A Footnote&#160;<a class="footnote-backref" href="#fnref-1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extensions=['footnotes'],
            extension_configs={'footnotes': {'SEPARATOR': '-'}}
        )
