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
        """Test back-link configuration."""

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
        """Test back-link title configuration without placeholder."""

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

    def test_footnote_order(self):
        """Test that footnotes occur in order of reference appearance."""

        self.assertMarkdownRenders(
            'First footnote reference[^first]. Second footnote reference[^last].\n\n'
            '[^last]: Second footnote.\n[^first]: First footnote.',
            '<p>First footnote reference<sup id="fnref:first"><a class="footnote-ref" '
            'href="#fn:first">1</a></sup>. Second footnote reference<sup id="fnref:last">'
            '<a class="footnote-ref" href="#fn:last">2</a></sup>.</p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:first">\n'
            '<p>First footnote.&#160;<a class="footnote-backref" href="#fnref:first" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '<li id="fn:last">\n'
            '<p>Second footnote.&#160;<a class="footnote-backref" href="#fnref:last" '
            'title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_order_tricky(self):
        """Test that tricky sequence of footnote references."""

        self.assertMarkdownRenders(
            '`Footnote reference in code spans should be ignored[^tricky]`. '
            'A footnote reference[^ordinary]. '
            'Another footnote reference[^tricky].\n\n'
            '[^ordinary]: This should be the first footnote.\n'
            '[^tricky]: This should be the second footnote.',
            '<p><code>Footnote reference in code spans should be ignored[^tricky]</code>. '
            'A footnote reference<sup id="fnref:ordinary"><a class="footnote-ref" '
            'href="#fn:ordinary">1</a></sup>. Another footnote reference<sup id="fnref:tricky">'
            '<a class="footnote-ref" href="#fn:tricky">2</a></sup>.</p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:ordinary">\n'
            '<p>This should be the first footnote.&#160;<a class="footnote-backref" '
            'href="#fnref:ordinary" title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '<li id="fn:tricky">\n'
            '<p>This should be the second footnote.&#160;<a class="footnote-backref" '
            'href="#fnref:tricky" title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_reference_within_code_span(self):
        """Test footnote reference within a code span."""

        self.assertMarkdownRenders(
            'A `code span with a footnote[^1] reference`.',
            '<p>A <code>code span with a footnote[^1] reference</code>.</p>'
        )

    def test_footnote_reference_within_link(self):
        """Test footnote reference within a link."""

        self.assertMarkdownRenders(
            'A [link with a footnote[^1] reference](http://example.com).',
            '<p>A <a href="http://example.com">link with a footnote[^1] reference</a>.</p>'
        )

    def test_footnote_reference_within_footnote_definition(self):
        """Test footnote definition containing another footnote reference."""

        self.assertMarkdownRenders(
            'Main footnote[^main].\n\n'
            '[^main]: This footnote references another[^nested].\n'
            '[^nested]: Nested footnote.',
            '<p>Main footnote<sup id="fnref:main"><a class="footnote-ref" href="#fn:main">1</a></sup>.</p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:main">\n'
            '<p>This footnote references another<sup id="fnref:nested"><a class="footnote-ref" '
            'href="#fn:nested">2</a></sup>.&#160;<a class="footnote-backref" href="#fnref:main" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '<li id="fn:nested">\n'
            '<p>Nested footnote.&#160;<a class="footnote-backref" href="#fnref:nested" '
            'title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_reference_within_blockquote(self):
        """Test footnote reference within a blockquote."""

        self.assertMarkdownRenders(
            '> This is a quote with a footnote[^quote].\n\n[^quote]: Quote footnote.',
            '<blockquote>\n'
            '<p>This is a quote with a footnote<sup id="fnref:quote">'
            '<a class="footnote-ref" href="#fn:quote">1</a></sup>.</p>\n'
            '</blockquote>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:quote">\n'
            '<p>Quote footnote.&#160;<a class="footnote-backref" href="#fnref:quote" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_reference_within_list(self):
        """Test footnote reference within a list item."""

        self.assertMarkdownRenders(
            '1. First item with footnote[^note]\n1. Second item\n\n[^note]: List footnote.',
            '<ol>\n'
            '<li>First item with footnote<sup id="fnref:note">'
            '<a class="footnote-ref" href="#fn:note">1</a></sup></li>\n'
            '<li>Second item</li>\n'
            '</ol>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:note">\n'
            '<p>List footnote.&#160;<a class="footnote-backref" href="#fnref:note" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_references_within_loose_list(self):
        """Test footnote references within loose list items."""

        self.assertMarkdownRenders(
            self.dedent(
                '''
                * Reference to [^first]

                * Reference to [^second]

                [^first]: First footnote definition
                [^second]: Second footnote definition
                '''
            ),
            '<ul>\n'
            '<li>\n'
            '<p>Reference to <sup id="fnref:first"><a class="footnote-ref" href="#fn:first">1</a></sup></p>\n'
            '</li>\n'
            '<li>\n'
            '<p>Reference to <sup id="fnref:second"><a class="footnote-ref" href="#fn:second">2</a></sup></p>\n'
            '</li>\n'
            '</ul>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:first">\n'
            '<p>First footnote definition&#160;<a class="footnote-backref" href="#fnref:first" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '<li id="fn:second">\n'
            '<p>Second footnote definition&#160;<a class="footnote-backref" href="#fnref:second" '
            'title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_reference_within_html(self):
        """Test footnote reference within HTML tags."""

        self.assertMarkdownRenders(
            'A <span>footnote reference[^1] within a span element</span>.\n\n[^1]: The footnote.',
            '<p>A <span>footnote reference<sup id="fnref:1">'
            '<a class="footnote-ref" href="#fn:1">1</a>'
            '</sup> within a span element</span>.</p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>The footnote.&#160;<a class="footnote-backref" href="#fnref:1" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_duplicate_footnote_references(self):
        """Test multiple references to the same footnote."""

        self.assertMarkdownRenders(
            'First[^dup] and second[^dup] reference.\n\n[^dup]: Duplicate footnote.',
            '<p>First<sup id="fnref:dup">'
            '<a class="footnote-ref" href="#fn:dup">1</a></sup> and second<sup id="fnref2:dup">'
            '<a class="footnote-ref" href="#fn:dup">1</a></sup> reference.</p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:dup">\n'
            '<p>Duplicate footnote.&#160;'
            '<a class="footnote-backref" href="#fnref:dup" '
            'title="Jump back to footnote 1 in the text">&#8617;</a>'
            '<a class="footnote-backref" href="#fnref2:dup" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_reference_without_definition(self):
        """Test footnote reference without corresponding definition."""

        self.assertMarkdownRenders(
            'This has a missing footnote[^missing].',
            '<p>This has a missing footnote[^missing].</p>'
        )

    def test_footnote_definition_without_reference(self):
        """Test footnote definition without corresponding reference."""

        self.assertMarkdownRenders(
            'No reference here.\n\n[^orphan]: Orphaned footnote.',
            '<p>No reference here.</p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:orphan">\n'
            '<p>Orphaned footnote.&#160;<a class="footnote-backref" href="#fnref:orphan" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )

    def test_footnote_id_with_special_chars(self):
        """Test footnote id containing special and Unicode characters."""

        self.assertMarkdownRenders(
            'Special footnote id[^!#¤%/()=?+}{§øé].\n\n[^!#¤%/()=?+}{§øé]: The footnote.',
            '<p>Special footnote id<sup id="fnref:!#¤%/()=?+}{§øé">'
            '<a class="footnote-ref" href="#fn:!#¤%/()=?+}{§øé">1</a></sup>.</p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:!#¤%/()=?+}{§øé">\n'
            '<p>The footnote.&#160;<a class="footnote-backref" href="#fnref:!#¤%/()=?+}{§øé" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )
