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

Copyright 2007-2020 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from markdown.test_tools import TestCase


class TestAttrList(TestCase):

    maxDiff = None

    # TODO: Move the rest of the attr_list tests here.

    def test_empty_list(self):
        self.assertMarkdownRenders(
            '*foo*{ }',
            '<p><em>foo</em>{ }</p>',
            extensions=['attr_list']
        )

    def test_table_td(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                | A { .foo }  | *B*{ .foo } | C { } | D{ .foo }     | E { .foo } F |
                |-------------|-------------|-------|---------------|--------------|
                | a { .foo }  | *b*{ .foo } | c { } | d{ .foo }     | e { .foo } f |
                | valid on td | inline      | empty | missing space | not at end   |
                """
            ),
            self.dedent(
                """
                <table>
                <thead>
                <tr>
                <th class="foo">A</th>
                <th><em class="foo">B</em></th>
                <th>C { }</th>
                <th>D{ .foo }</th>
                <th>E { .foo } F</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                <td class="foo">a</td>
                <td><em class="foo">b</em></td>
                <td>c { }</td>
                <td>d{ .foo }</td>
                <td>e { .foo } f</td>
                </tr>
                <tr>
                <td>valid on td</td>
                <td>inline</td>
                <td>empty</td>
                <td>missing space</td>
                <td>not at end</td>
                </tr>
                </tbody>
                </table>
                """
            ),
            extensions=['attr_list', 'tables']
        )
