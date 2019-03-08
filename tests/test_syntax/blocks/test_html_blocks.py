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

import unittest
from markdown.test_tools import TestCase


class TestHTMLBlocks(TestCase):

    def test_raw_paragraph(self):
        self.assertMarkdownRenders(
            '<p>A raw paragraph.</p>',
            '<p>A raw paragraph.</p>'
        )

    def test_raw_skip_inline_markdown(self):
        self.assertMarkdownRenders(
            '<p>A *raw* paragraph.</p>',
            '<p>A *raw* paragraph.</p>'
        )

    def test_raw_indent_one_space(self):
        self.assertMarkdownRenders(
            ' <p>A *raw* paragraph.</p>',
            # TODO: reevaluate. This matches strict rules and reference
            # implementation version 1.0.1 but not 1.0.2b8.
            '<p><p>A <em>raw</em> paragraph.</p></p>'
        )

    def test_raw_indent_four_spaces(self):
        self.assertMarkdownRenders(
            '    <p>code block</p>',
            self.dedent(
                """
                <pre><code>&lt;p&gt;code block&lt;/p&gt;
                </code></pre>
                """
            )
        )

    def test_raw_span(self):
        self.assertMarkdownRenders(
            '<span>*inline*</span>',
            '<p><span><em>inline</em></span></p>'
        )

    def test_code_span(self):
        self.assertMarkdownRenders(
            '`<em>code span</em>`',
            '<p><code>&lt;em&gt;code span&lt;/em&gt;</code></p>'
        )

    def test_multiline_raw(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>
                    A raw paragraph
                    with multiple lines.
                </p>
                """
            ),
            self.dedent(
                """
                <p>
                    A raw paragraph
                    with multiple lines.
                </p>
                """
            )
        )

    def test_blank_lines_in_raw(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>

                    A raw paragraph...

                    with many blank lines.

                </p>
                """
            ),
            self.dedent(
                """
                <p>

                    A raw paragraph...

                    with many blank lines.

                </p>
                """
            )
        )

    def test_raw_surrounded_by_Markdown(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Some *Markdown* text.

                <p>*Raw* HTML.</p>

                More *Markdown* text.
                """
            ),
            self.dedent(
                """
                <p>Some <em>Markdown</em> text.</p>
                <p>*Raw* HTML.</p>

                <p>More <em>Markdown</em> text.</p>
                """
            )
        )

    def test_raw_without_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Some *Markdown* text.
                <p>*Raw* HTML.</p>
                More *Markdown* text.
                """
            ),
            # The raw gets treated as inline HTML. This follows the rules and this lib's
            # previous behavior, but not the reference implementation. TODO: Reevaluate.
            self.dedent(
                """
                <p>Some <em>Markdown</em> text.
                <p><em>Raw</em> HTML.</p>
                More <em>Markdown</em> text.</p>
                """
            )
            # The reference implementation does this instead:
            # self.dedent(
            #     """
            #     <p>Some <em>Markdown</em> text.</p>
            #     <p>*Raw* HTML.</p>
            #     <p>More <em>Markdown</em> text.</p>
            #     """
            # )
        )

    def test_raw_with_markdown_blocks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                    Not a Markdown paragraph.

                    * Not a list item.
                    * Another non-list item.

                    Another non-Markdown paragraph.
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                    Not a Markdown paragraph.

                    * Not a list item.
                    * Another non-list item.

                    Another non-Markdown paragraph.
                </div>
                """
            )
        )

    # TODO: This fails. Fix it.
    def test_adjacent_raw_blocks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                """
            ),
            self.dedent(
                """
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                """
            )
        )

    def test_adjacent_raw_blocks_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>A raw paragraph.</p>

                <p>A second raw paragraph.</p>
                """
            ),
            self.dedent(
                """
                <p>A raw paragraph.</p>

                <p>A second raw paragraph.</p>
                """
            )
        )

    def test_nested_raw_block(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                <p>A raw paragraph.</p>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p>A raw paragraph.</p>
                </div>
                """
            )
        )

    def test_nested_indented_raw_block(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                    <p>A raw paragraph.</p>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                    <p>A raw paragraph.</p>
                </div>
                """
            )
        )

    def test_nested_raw_blocks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                </div>
                """
            )
        )

    def test_nested_raw_blocks_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>

                <p>A raw paragraph.</p>

                <p>A second raw paragraph.</p>

                </div>
                """
            ),
            self.dedent(
                """
                <div>

                <p>A raw paragraph.</p>

                <p>A second raw paragraph.</p>

                </div>
                """
            )
        )
