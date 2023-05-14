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

from markdown.test_tools import TestCase


class TestBadge(TestCase):

    def test_with_lists(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                - List

                    List {{ note "Badge" }}

                - Paragraph

                    Paragraph
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>
                <p>List</p>
                <p>
                List
                <span class="badge note">
                <span class="badge-title">Badge</span>
                </span>
                </p>
                <li>
                <p>Paragraph</p>
                <p>Paragraph</p>
                </li>
                </ul>
                '''
            ),
            extensions=['badge']
        )

    def test_definition_list(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                Term

                :   Definition {{ note "Badge" }}

                    More text

                :   Another
                    definition

                    Even more text
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>
                <p>
                Definition
                <span class="badge note">
                <span class="badge-title">Badge</span>
                </span>
                </p>
                <p>More text</p>
                </dd>
                <dd>
                <p>Another
                definition</p>
                <p>Even more text</p>
                </dd>
                </dl>
                '''
            ),
            extensions=['badge', 'def_list']
        )

    def test_with_preceding_text(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                foo **foo** {{ note "Badge" }}
                '''
            ),
            self.dedent(
                '''
                <p>foo
                <strong>foo</strong>
                <span class="badge note">
                <span class="badge-title">Badge</span>
                </span>
                </p>
                '''
            ),
            extensions=['badge']
        )
