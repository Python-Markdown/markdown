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

import markdown
from markdown.test_tools import TestCase, recursionlimit


class TestListNestingLimit(TestCase):

    # A list recurses through `parseBlocks` once per level of nesting, so the nesting
    # has to stop short of the interpreter's limit. The remaining markers are kept as
    # text, the same way a blockquote keeps its markers (see `TestBlockquoteBlocks`).

    def test_nesting_stops_short_of_the_recursion_limit(self):
        # Ten levels of markers is more than the limit below allows to nest.
        with recursionlimit(120):
            result = markdown.markdown('- ' * 10 + 'x')

        self.assertLess(result.count('<ul>'), 10)
        self.assertIn('- ', result)

    def test_deeply_nested_list_does_not_raise(self):
        # Around 1 KB of input, which raised `RecursionError` before the limit was applied.
        result = markdown.markdown('- ' * 500 + 'x')

        self.assertLess(result.count('<ul>'), 500)
        self.assertIn('x', result)

    def test_deeply_nested_ordered_list_does_not_raise(self):
        result = markdown.markdown('1. ' * 500 + 'x')

        self.assertLess(result.count('<ol>'), 500)
        self.assertIn('x', result)

    def test_deeply_indented_list_does_not_raise(self):
        source = ''.join('  ' * i + '- x\n' for i in range(600))
        result = markdown.markdown(source)

        self.assertLess(result.count('<ul>'), 600)
        self.assertEqual(result.count('x'), 600)

    def test_nesting_below_the_limit_is_unchanged(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                - x
                    - y
                        - z
                """
            ),
            self.dedent(
                """
                <ul>
                <li>x<ul>
                <li>y<ul>
                <li>z</li>
                </ul>
                </li>
                </ul>
                </li>
                </ul>
                """
            )
        )
