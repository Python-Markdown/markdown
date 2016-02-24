from .. import MdTestCase

class TestParagraphBlocks(MdTestCase):

    def test_simple_paragraph(self):
        self.assertMarkdownRenders(
            'A paragraph.',

            '<p>A paragraph.</p>'
        )

    def test_blank_line_before_paragraph(self):
        self.assertMarkdownRenders(
            '\nA paragraph.',

            '<p>A paragraph.</p>'
        )

    def test_multiline_paragraph(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                line 1
                line 2
                """
            ),
            self.dedent(
                """
                <p>line 1
                line 2</p>
                """
            )
        )

    def test_consecutive_paragraphs(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Paragraph 1.

                Paragraph 2.
                """
            ),
            self.dedent(
                """
                <p>Paragraph 1.</p>
                <p>Paragraph 2.</p>
                """
            )
        )