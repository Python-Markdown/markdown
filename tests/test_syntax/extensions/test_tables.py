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


class TestTableBlocks(TestCase):

    def test_empty_cells(self):
        """Empty cells (nbsp)."""

        text = """
   | Second Header
------------- | -------------
   | Content Cell
Content Cell  |  
"""

        self.assertMarkdownRenders(
            text,
            self.dedent(
                """
                <table>
                <thead>
                <tr>
                <th> </th>
                <th>Second Header</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                <td> </td>
                <td>Content Cell</td>
                </tr>
                <tr>
                <td>Content Cell</td>
                <td> </td>
                </tr>
                </tbody>
                </table>
                """
            ),
            extensions=['tables']
        )
