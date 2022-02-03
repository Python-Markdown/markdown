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


class TestFootnotes(TestCase):

    default_kwargs = {'extensions': ['footnotes']}
    maxDiff = None

    def test_basic_footnote(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                paragraph[^1]

                [^1]: A Footnote
                """
            ),
            '<p>paragraph<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_multiple_footnotes(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                foo[^1]

                bar[^2]

                [^1]: Footnote 1
                [^2]: Footnote 2
                """
            ),
            '<p>foo<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<p>bar<sup id="fnref:2"><a class="footnote-ref" href="#fn:2">2</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>Footnote 1&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '<li id="fn:2">\n'
            '<p>Footnote 2&#160;<a class="footnote-backref" href="#fnref:2"'
            ' title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_multiple_footnotes_multiline(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                foo[^1]

                bar[^2]

                [^1]: Footnote 1
                    line 2
                [^2]: Footnote 2
                """
            ),
            '<p>foo<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<p>bar<sup id="fnref:2"><a class="footnote-ref" href="#fn:2">2</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>Footnote 1\nline 2&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '<li id="fn:2">\n'
            '<p>Footnote 2&#160;<a class="footnote-backref" href="#fnref:2"'
            ' title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_multi_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                paragraph[^1]
                [^1]: A Footnote
                    line 2
                """
            ),
            '<p>paragraph<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote\nline 2&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_multi_line_lazy_indent(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                paragraph[^1]
                [^1]: A Footnote
                line 2
                """
            ),
            '<p>paragraph<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote\nline 2&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_multi_line_complex(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                paragraph[^1]

                [^1]:

                    A Footnote
                    line 2

                    * list item

                    > blockquote
                """
            ),
            '<p>paragraph<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote\nline 2</p>\n'
            '<ul>\n<li>list item</li>\n</ul>\n'
            '<blockquote>\n<p>blockquote</p>\n</blockquote>\n'
            '<p><a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_multple_complex(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                foo[^1]

                bar[^2]

                [^1]:

                    A Footnote
                    line 2

                    * list item

                    > blockquote

                [^2]: Second footnote

                    paragraph 2
                """
            ),
            '<p>foo<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<p>bar<sup id="fnref:2"><a class="footnote-ref" href="#fn:2">2</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote\nline 2</p>\n'
            '<ul>\n<li>list item</li>\n</ul>\n'
            '<blockquote>\n<p>blockquote</p>\n</blockquote>\n'
            '<p><a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '<li id="fn:2">\n'
            '<p>Second footnote</p>\n'
            '<p>paragraph 2&#160;<a class="footnote-backref" href="#fnref:2"'
            ' title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_multple_complex_no_blank_line_between(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                foo[^1]

                bar[^2]

                [^1]:

                    A Footnote
                    line 2

                    * list item

                    > blockquote
                [^2]: Second footnote

                    paragraph 2
                """
            ),
            '<p>foo<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<p>bar<sup id="fnref:2"><a class="footnote-ref" href="#fn:2">2</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote\nline 2</p>\n'
            '<ul>\n<li>list item</li>\n</ul>\n'
            '<blockquote>\n<p>blockquote</p>\n</blockquote>\n'
            '<p><a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '<li id="fn:2">\n'
            '<p>Second footnote</p>\n'
            '<p>paragraph 2&#160;<a class="footnote-backref" href="#fnref:2"'
            ' title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

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
            extension_configs={'footnotes': {'SEPARATOR': '-'}}
        )

    def test_backlink_title(self):
        """Test backlink title configuration without placeholder."""

        self.assertMarkdownRenders(
            'paragraph[^1]\n\n[^1]: A Footnote',
            '<p>paragraph<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extension_configs={'footnotes': {'BACKLINK_TITLE': 'Jump back to footnote'}}
        )

    def test_superscript_text(self):
        """Test superscript text configuration."""

        self.assertMarkdownRenders(
            'paragraph[^1]\n\n[^1]: A Footnote',
            '<p>paragraph<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">[1]</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>A Footnote&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extension_configs={'footnotes': {'SUPERSCRIPT_TEXT': '[{}]'}}
        )
