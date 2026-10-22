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

from markdown.test_tools import TestCase


class TestSaneLists(TestCase):

    default_kwargs = {'extensions': ['sane_lists']}

    # A marker of the other list type does not start an item, so it does not end the
    # indented block before it (#845).
    def test_other_list_type_after_indented_paragraph(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                1. item one

                    second paragraph of item 1
                - not an item
                """
            ),
            self.dedent(
                """
                <ol>
                <li>
                <p>item one</p>
                <p>second paragraph of item 1
                - not an item</p>
                </li>
                </ol>
                """
            )
        )
