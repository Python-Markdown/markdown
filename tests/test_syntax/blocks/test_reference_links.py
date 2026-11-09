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

    def test_malformed_reference_with_long_run_of_spaces(self):
        """
        A reference definition whose URL is missing (only trailing spaces
        after the colon) should still be treated as plain text, no matter
        how many trailing spaces there are.

        See https://github.com/Python-Markdown/markdown/issues/798
        """
        text = '[id]:' + (' ' * 50000)
        self.assertMarkdownRenders(
            text, f'<p>{text}</p>', expected_attrs={'references': {}}
        )

    def test_reference_definitions_before_setext_underline(self):
        """
        A setext underline after consecutive reference definitions is a paragraph,
        and does not turn the last definition into a header.
        """
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]: http://example.com/b\n===',
            '<p>===</p>',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_reference_definitions_before_split_definition(self):
        """
        A definition split across lines after other definitions is left for the
        next pass, so a horizontal rule on its second line is not taken as the link.
        """
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]:\n***',
            '<p>[b]:</p>\n<hr />',
            expected_attrs={'references': {'a': ('http://example.com/a', None)}}
        )

    def test_reference_definitions_before_definition_split_across_lines(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]:\nhttp://example.com/b',
            '',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_reference_definitions_title_on_own_line(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]: http://example.com/b\n"Title"',
            '',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', 'Title')}
            }
        )

    def test_reference_definitions_before_paragraph(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]: http://example.com/b\nSome text',
            '<p>Some text</p>',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_paragraph_before_reference_definitions(self):
        self.assertMarkdownRenders(
            'Some text\n[a]: http://example.com/a\n[b]: http://example.com/b',
            '<p>Some text</p>',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_reference_definitions_separated_by_paragraph(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\nSome text\n[b]: http://example.com/b',
            '<p>Some text</p>',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_indented_reference_definitions(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n   [b]: http://example.com/b',
            '',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_indented_reference_definitions_short_tab_length(self):
        """
        A definition indented by `tab_length` spaces directly after another
        definition is a definition, not an indented code block.
        """
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n  [b]: http://example.com/b',
            '',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            },
            tab_length=2
        )

    def test_duplicate_reference_definitions(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[a]: http://example.com/b',
            '',
            expected_attrs={'references': {'a': ('http://example.com/b', None)}}
        )

    def test_reference_definitions_before_hash_header(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]: http://example.com/b\n# Header',
            '<h1>Header</h1>',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_reference_definitions_before_hr(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]: http://example.com/b\n***',
            '<hr />',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_reference_definitions_before_blockquote(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]: http://example.com/b\n> quote',
            '<blockquote>\n<p>quote</p>\n</blockquote>',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_reference_definitions_before_code_block(self):
        self.assertMarkdownRenders(
            '[a]: http://example.com/a\n[b]: http://example.com/b\n    code',
            '<pre><code>code\n</code></pre>',
            expected_attrs={
                'references': {'a': ('http://example.com/a', None), 'b': ('http://example.com/b', None)}
            }
        )

    def test_many_reference_definitions(self):
        """
        Consecutive reference definitions should be consumed together rather
        than returning the remainder of the block to be parsed once per
        definition.
        """
        count = 10000
        text = ''.join(f'[id{i}]: http://example.com/{i}\n' for i in range(count))
        self.assertMarkdownRenders(
            text,
            '',
            expected_attrs={
                'references': {f'id{i}': (f'http://example.com/{i}', None) for i in range(count)}
            }
        )
