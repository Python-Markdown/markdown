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


class TestMdInHTML(TestCase):

    default_kwargs = {'extensions': ['md_in_html']}

    def test_md1_paragraph(self):
        self.assertMarkdownRenders(
            '<p markdown="1">*foo*</p>',
            '<p><em>foo</em></p>'
        )

    def test_md1_p_linebreaks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p markdown="1">
                *foo*
                </p>
                """
            ),
            self.dedent(
                """
                <p>
                <em>foo</em>
                </p>
                """
            )
        )

    def test_md1_p_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p markdown="1">

                *foo*

                </p>
                """
            ),
            self.dedent(
                """
                <p>

                <em>foo</em>

                </p>
                """
            )
        )

    def test_md1_div(self):
        self.assertMarkdownRenders(
            '<div markdown="1">*foo*</div>',
            self.dedent(
                """
                <div>
                <p><em>foo</em></p>
                </div>
                """
            )
        )

    def test_md1_div_linebreaks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">
                *foo*
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p><em>foo</em></p>
                </div>
                """
            )
        )

    def test_md1_div_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">

                *foo*

                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p><em>foo</em></p>
                </div>
                """
            )
        )

    def test_md1_div_multi(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">

                *foo*

                __bar__

                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p><em>foo</em></p>
                <p><strong>bar</strong></p>
                </div>
                """
            )
        )

    def test_md1_div_nested(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">

                <div markdown="1">
                *foo*
                </div>

                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <div>
                <p><em>foo</em></p>
                </div>
                </div>
                """
            )
        )

    def test_md1_div_multi_nest(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">

                <div markdown="1">
                <p markdown="1">*foo*</p>
                </div>

                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <div>
                <p><em>foo</em></p>
                </div>
                </div>
                """
            )
        )

    def test_md1_mix(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">
                A _Markdown_ paragraph before a raw child.

                <p markdown="1">A *raw* child.</p>

                A _Markdown_ tail to the raw child.
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p>A <em>Markdown</em> paragraph before a raw child.</p>
                <p>A <em>raw</em> child.</p>
                <p>A <em>Markdown</em> tail to the raw child.</p>
                </div>
                """
            )
        )

    def test_md1_deep_mix(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">

                A _Markdown_ paragraph before a raw child.

                A second Markdown paragraph.

                <div markdown="1">

                A *raw* child.

                <p markdown="1">*foo*</p>

                Raw child tail.

                </div>

                A _Markdown_ tail to the raw child.

                A second tail item

                <p markdown="1">More raw.</p>

                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p>A <em>Markdown</em> paragraph before a raw child.</p>
                <p>A second Markdown paragraph.</p>
                <div>
                <p>A <em>raw</em> child.</p>
                <p><em>foo</em></p>
                <p>Raw child tail.</p>
                </div>
                <p>A <em>Markdown</em> tail to the raw child.</p>
                <p>A second tail item</p>
                <p>More raw.</p>
                </div>
                """
            )
        )

    def test_md1_div_raw_inline(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">

                <em>foo</em>

                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p><em>foo</em></p>
                </div>
                """
            )
        )

    def test_no_md1_paragraph(self):
        self.assertMarkdownRenders(
            '<p>*foo*</p>',
            '<p>*foo*</p>'
        )

    def test_no_md1_nest(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">
                A _Markdown_ paragraph before a raw child.

                <p>A *raw* child.</p>

                A _Markdown_ tail to the raw child.
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p>A <em>Markdown</em> paragraph before a raw child.</p>
                <p>A *raw* child.</p>
                <p>A <em>Markdown</em> tail to the raw child.</p>
                </div>
                """
            )
        )

    def test_md_span_paragraph(self):
        self.assertMarkdownRenders(
            '<p markdown="span">*foo*</p>',
            '<p><em>foo</em></p>'
        )

    def test_md_block_paragraph(self):
        self.assertMarkdownRenders(
            '<p markdown="block">*foo*</p>',
            self.dedent(
                """
                <p>
                <p><em>foo</em></p>
                </p>
                """
            )
        )

    def test_md_span_div(self):
        self.assertMarkdownRenders(
            '<div markdown="span">*foo*</div>',
            '<div><em>foo</em></div>'
        )

    def test_md_block_div(self):
        self.assertMarkdownRenders(
            '<div markdown="block">*foo*</div>',
            self.dedent(
                """
                <div>
                <p><em>foo</em></p>
                </div>
                """
            )
        )

    def test_md_span_nested_in_block(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="block">
                <div markdown="span">*foo*</div>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <div><em>foo</em></div>
                </div>
                """
            )
        )

    def test_md_block_nested_in_span(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="span">
                <div markdown="block">*foo*</div>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <div><em>foo</em></div>
                </div>
                """
            )
        )

    def test_md1_nested_in_nomd(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                <div markdown="1">*foo*</div>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <div markdown="1">*foo*</div>
                </div>
                """
            )
        )

    def test_md1_single_quotes(self):
        self.assertMarkdownRenders(
            "<p markdown='1'>*foo*</p>",
            '<p><em>foo</em></p>'
        )

    def test_md1_no_quotes(self):
        self.assertMarkdownRenders(
            '<p markdown=1>*foo*</p>',
            '<p><em>foo</em></p>'
        )

    def test_md_no_value(self):
        self.assertMarkdownRenders(
            '<p markdown>*foo*</p>',
            '<p><em>foo</em></p>'
        )

    def test_md1_preserve_attrs(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1" id="parent">

                <div markdown="1" class="foo">
                <p markdown="1" class="bar baz">*foo*</p>
                </div>

                </div>
                """
            ),
            self.dedent(
                """
                <div id="parent">
                <div class="foo">
                <p class="bar baz"><em>foo</em></p>
                </div>
                </div>
                """
            )
        )

    def test_md1_unclosed_div(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">

                _foo_

                <div class="unclosed>

                _bar_

                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p><em>foo</em></p>
                <div class="unclosed">
                __bar__
                </div>
                </div>
                """
            )
        )

    def test_md1_orphan_endtag(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">

                _foo_

                </p>

                _bar_

                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p><em>foo</em></p>
                <p></p>
                <p><em>bar</em></p>
                </div>
                """
            )
        )

    def test_md1_unclosed_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p markdown="1">_foo_
                <p markdown="1">_bar_
                """
            ),
            self.dedent(
                """
                <p><em>foo</em>
                </p>
                <p><em>bar</em>
                </p>
                """
            )
        )

    def test_md1_nested_unclosed_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div markdown="1">
                <p markdown="1">_foo_
                <p markdown="1">_bar_
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p><em>foo</em>
                </p>
                <p><em>bar</em>
                </p>
                </div>
                """
            )
        )
