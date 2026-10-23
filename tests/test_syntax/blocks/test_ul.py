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

Copyright 2007-2024 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

import unittest
from markdown.test_tools import TestCase


class TestUnorderedLists(TestCase):

    # TODO: Move legacy tests here

    def test_header_and_paragraph_no_blank_line_loose_list(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - ### List 1
                    Entry 1.1

                - ### List 2
                    Entry 2.1
                """
            ),
            self.dedent(
                """
                <ul>
                <li>
                <h3>List 1</h3>
                <p>Entry 1.1</p>
                </li>
                <li>
                <h3>List 2</h3>
                <p>Entry 2.1</p>
                </li>
                </ul>
                """
            )
        )

    # Note: This is strange. Any other element on first line of list item would get very
    # different behavior. However, as a heading can only ever be one line, this is the
    # correct behavior. In fact, `markdown.pl` behaves this way with no indentation.
    def test_header_and_paragraph_no_blank_line_loose_list_no_indent(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - ### List 1
                Entry 1.1

                - ### List 2
                Entry 2.1
                """
            ),
            self.dedent(
                """
                <ul>
                <li>
                <h3>List 1</h3>
                <p>Entry 1.1</p>
                </li>
                <li>
                <h3>List 2</h3>
                <p>Entry 2.1</p>
                </li>
                </ul>
                """
            )
        )

    # TODO: Possibly change this behavior. While this test follows the behavior
    # of `markdown.pl`, it is likely surprising to most users. In fact, actual
    # behavior is to return the same results as for a loose list.
    @unittest.skip('This behaves as a loose list in Python-Markdown')
    def test_header_and_paragraph_no_blank_line_tight_list(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - ### List 1
                    Entry 1.1
                - ### List 2
                    Entry 2.1
                """
            ),
            self.dedent(
                """
                <ul>
                <li>### List 1
                Entry 1.1</li>
                <li>### List 2
                Entry 2.1</li>
                </ul>
                """
            )
        )

    # TODO: Possibly change this behavior. While this test follows the behavior
    # of `markdown.pl`, it is likely surprising to most users. In fact, actual
    # behavior is to return the same results as for a loose list.
    @unittest.skip('This behaves as a loose list in Python-Markdown')
    def test_header_and_paragraph_no_blank_line_tight_list_no_indent(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - ### List 1
                Entry 1.1
                - ### List 2
                Entry 2.1
                """
            ),
            self.dedent(
                """
                <ul>
                <li>### List 1
                Entry 1.1</li>
                <li>### List 2
                Entry 2.1</li>
                </ul>
                """
            )
        )

    # An unindented list item ends the indented block before it, even without a blank
    # line. As no blank line comes before the new item, it is not a loose item (#845).
    def test_item_after_indented_paragraph_no_blank_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - item one

                    second paragraph of item 1
                - item two
                - item three
                """
            ),
            self.dedent(
                """
                <ul>
                <li>
                <p>item one</p>
                <p>second paragraph of item 1</p>
                </li>
                <li>item two</li>
                <li>item three</li>
                </ul>
                """
            )
        )

    def test_ordered_item_after_indented_paragraph_no_blank_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                1. item one

                    second paragraph of item 1
                2. item two
                """
            ),
            self.dedent(
                """
                <ol>
                <li>
                <p>item one</p>
                <p>second paragraph of item 1</p>
                </li>
                <li>item two</li>
                </ol>
                """
            )
        )

    def test_item_after_nested_list_and_paragraph_no_blank_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                * First item:

                    * First sub-item
                    * Second sub-item

                    Additional paragraph in first item
                * Second item
                """
            ),
            self.dedent(
                """
                <ul>
                <li>
                <p>First item:</p>
                <ul>
                <li>First sub-item</li>
                <li>Second sub-item</li>
                </ul>
                <p>Additional paragraph in first item</p>
                </li>
                <li>Second item</li>
                </ul>
                """
            )
        )

    # An unindented line which does not start a list item is still a lazy
    # continuation of the paragraph.
    def test_lazy_paragraph_continuation_after_indented_paragraph(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - item one

                    second paragraph of item 1
                line two of second paragraph of item 1
                """
            ),
            self.dedent(
                """
                <ul>
                <li>
                <p>item one</p>
                <p>second paragraph of item 1
                line two of second paragraph of item 1</p>
                </li>
                </ul>
                """
            )
        )

    def test_item_after_indented_paragraph_in_blockquote(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                > - item one
                >
                >     second paragraph of item 1
                > - item two
                """
            ),
            self.dedent(
                """
                <blockquote>
                <ul>
                <li>
                <p>item one</p>
                <p>second paragraph of item 1</p>
                </li>
                <li>item two</li>
                </ul>
                </blockquote>
                """
            )
        )

    # As with a list at the top level, a horizontal rule ends the list.
    def test_hr_after_indented_paragraph(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - item one

                    second paragraph of item 1
                * * *
                """
            ),
            self.dedent(
                """
                <ul>
                <li>
                <p>item one</p>
                <p>second paragraph of item 1</p>
                </li>
                </ul>
                <hr />
                """
            )
        )

    # The same applies to a nested list item after an indented paragraph of the previous
    # nested item. The items after it, at any level, are tight.
    def test_nested_item_after_indented_paragraph_no_blank_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - item one
                    - sub-item one

                        second paragraph of sub-item 1
                    - sub-item two
                - item two
                """
            ),
            self.dedent(
                """
                <ul>
                <li>
                <p>item one</p>
                <ul>
                <li>
                <p>sub-item one</p>
                <p>second paragraph of sub-item 1</p>
                </li>
                <li>sub-item two</li>
                </ul>
                </li>
                <li>item two</li>
                </ul>
                """
            )
        )
