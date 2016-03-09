import unittest
from markdown.test_tools import TestCase


class TestSetextHeaders(TestCase):

    def test_setext_h1(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H1
                =============
                """
            ),
            
            '<h1>This is an H1</h1>'
        )

    def test_setext_h2(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H2
                -------------
                """
            ),
            
            '<h2>This is an H2</h2>'
        )

    def test_setext_h1_mismatched_length(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H1
                ===
                """
            ),
            
            '<h1>This is an H1</h1>'
        )
    
    def test_setext_h2_mismatched_length(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H2
                ---
                """
            ),
            
            '<h2>This is an H2</h2>'
        )

    def test_setext_h1_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H1
                =============
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h1>This is an H1</h1>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )
    
    def test_setext_h2_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H2
                -------------
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h2>This is an H2</h2>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )

    # TODO: fix this
    # see http://johnmacfarlane.net/babelmark2/?normalize=1&text=Paragraph%0AAn+H1%0A%3D%3D%3D%3D%3D
    @unittest.skip('This is broken in Python-Markdown')
    def test_p_followed_by_setext_h1(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is a Paragraph.
                Followed by an H1 with no blank line.
                =====================================
                """
            ),
            self.dedent(
                """
                <p>This is a Paragraph.</p>
                <h1>Followed by an H1 with no blank line.</h1>
                """
            )
        )

    # TODO: fix this
    # see http://johnmacfarlane.net/babelmark2/?normalize=1&text=Paragraph%0AAn+H2%0A-----
    @unittest.skip('This is broken in Python-Markdown')
    def test_p_followed_by_setext_h2(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is a Paragraph.
                Followed by an H2 with no blank line.
                -------------------------------------
                """
            ),
            self.dedent(
                """
                <p>This is a Paragraph.</p>
                <h2>Followed by an H2 with no blank line.</h2>
                """
            )
        )
