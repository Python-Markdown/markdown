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

from markdown.test_tools import TestCase


class TestAbbr(TestCase):

    default_kwargs = {'extensions': ['abbr']}

    def test_abbr_upper(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR

                *[ABBR]: Abbreviation
                """
            ),
            self.dedent(
                """
                <p><abbr title="Abbreviation">ABBR</abbr></p>
                """
            )
        )

    def test_abbr_lower(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                abbr

                *[abbr]: Abbreviation
                """
            ),
            self.dedent(
                """
                <p><abbr title="Abbreviation">abbr</abbr></p>
                """
            )
        )

    def test_abbr_multiple(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                The HTML specification
                is maintained by the W3C.

                *[HTML]: Hyper Text Markup Language
                *[W3C]:  World Wide Web Consortium
                """
            ),
            self.dedent(
                """
                <p>The <abbr title="Hyper Text Markup Language">HTML</abbr> specification
                is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.</p>
                """
            )
        )

    def test_abbr_override(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR

                *[ABBR]: Ignored
                *[ABBR]: The override
                """
            ),
            self.dedent(
                """
                <p><abbr title="The override">ABBR</abbr></p>
                """
            )
        )

    def test_abbr_no_blank_Lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR
                *[ABBR]: Abbreviation
                ABBR
                """
            ),
            self.dedent(
                """
                <p><abbr title="Abbreviation">ABBR</abbr></p>
                <p><abbr title="Abbreviation">ABBR</abbr></p>
                """
            )
        )

    def test_abbr_no_space(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR

                *[ABBR]:Abbreviation
                """
            ),
            self.dedent(
                """
                <p><abbr title="Abbreviation">ABBR</abbr></p>
                """
            )
        )

    def test_abbr_extra_space(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR

                *[ABBR] :      Abbreviation
                """
            ),
            self.dedent(
                """
                <p><abbr title="Abbreviation">ABBR</abbr></p>
                """
            )
        )

    def test_abbr_line_break(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR

                *[ABBR]:
                    Abbreviation
                """
            ),
            self.dedent(
                """
                <p><abbr title="Abbreviation">ABBR</abbr></p>
                """
            )
        )

    def test_abbr_ignore_unmatched_case(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR abbr

                *[ABBR]: Abbreviation
                """
            ),
            self.dedent(
                """
                <p><abbr title="Abbreviation">ABBR</abbr> abbr</p>
                """
            )
        )

    def test_abbr_partial_word(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR ABBREVIATION

                *[ABBR]: Abbreviation
                """
            ),
            self.dedent(
                """
                <p><abbr title="Abbreviation">ABBR</abbr> ABBREVIATION</p>
                """
            )
        )

    def test_abbr_unused(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                foo bar

                *[ABBR]: Abbreviation
                """
            ),
            self.dedent(
                """
                <p>foo bar</p>
                """
            )
        )

    def test_abbr_double_quoted(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR

                *[ABBR]: "Abbreviation"
                """
            ),
            self.dedent(
                """
                <p><abbr title="&quot;Abbreviation&quot;">ABBR</abbr></p>
                """
            )
        )

    def test_abbr_single_quoted(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ABBR

                *[ABBR]: 'Abbreviation'
                """
            ),
            self.dedent(
                """
                <p><abbr title="'Abbreviation'">ABBR</abbr></p>
                """
            )
        )
