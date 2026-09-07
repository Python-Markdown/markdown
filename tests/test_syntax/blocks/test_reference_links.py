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

Copyright 2007-2023 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

import time

from markdown.test_tools import TestCase


class TestReferenceLinks(TestCase):

    def test_reference_link(self):
        self.assertMarkdownRenders(
            '[Text][id]\n\n[id]: http://example.com',
            '<p><a href="http://example.com">Text</a></p>'
        )

    def test_reference_link_split_across_lines(self):
        self.assertMarkdownRenders(
            '[Text][id]\n\n[id]:\nhttp://example.com',
            '<p><a href="http://example.com">Text</a></p>'
        )

    def test_reference_link_with_title(self):
        self.assertMarkdownRenders(
            '[Text][id]\n\n[id]: http://example.com "Title"',
            '<p><a href="http://example.com" title="Title">Text</a></p>'
        )

    def test_reference_link_title_on_own_line(self):
        self.assertMarkdownRenders(
            '[Text][id]\n\n[id]: http://example.com\n"Title"',
            '<p><a href="http://example.com" title="Title">Text</a></p>'
        )

    def test_malformed_reference_does_not_take_quadratic_time(self):
        """
        A reference definition whose URL is missing (only trailing spaces
        after the colon) must not trigger catastrophic regex backtracking.

        See https://github.com/Python-Markdown/markdown/issues/798
        """
        text = '[id]:' + (' ' * 50000)
        start = time.time()
        self.assertMarkdownRenders(
            text, f'<p>{text}</p>', expected_attrs={'references': {}}
        )
        self.assertLess(time.time() - start, 2)
