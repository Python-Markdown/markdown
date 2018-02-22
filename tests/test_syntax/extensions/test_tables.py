# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
