from markdown.test_tools import TestCase


class TestParagraphBlocks(TestCase):

    def test_simple_paragraph(self):
        self.assertMarkdownRenders(
            'A simple paragraph.',

            '<p>A simple paragraph.</p>'
        )

    def test_blank_line_before_paragraph(self):
        self.assertMarkdownRenders(
            '\nA paragraph preceded by a blank line.',

            '<p>A paragraph preceded by a blank line.</p>'
        )

    def test_multiline_paragraph(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is a paragraph
                on multiple lines
                with hard returns.
                """
            ),
            self.dedent(
                """
                <p>This is a paragraph
                on multiple lines
                with hard returns.</p>
                """
            )
        )

    def test_paragraph_long_line(self):
        self.assertMarkdownRenders(
            'A very long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long paragraph on 1 line.',

            '<p>A very long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long paragraph on 1 line.</p>'
        )

    def test_2_paragraphs_long_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                A very long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long paragraph on 1 line.

                A new long long long long long long long long long long long long long long long long paragraph on 1 line.
                """
            ),
            self.dedent(
                """
                <p>A very long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long long paragraph on 1 line.</p>
                <p>A new long long long long long long long long long long long long long long long long paragraph on 1 line.</p>
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

    def test_consecutive_paragraphs_tab(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Paragraph followed by a line with a tab only.
                \t
                Paragraph after a line with a tab only.
                """
            ),
            self.dedent(
                """
                <p>Paragraph followed by a line with a tab only.</p>
                <p>Paragraph after a line with a tab only.</p>
                """
            )
        )

    def test_consecutive_paragraphs_space(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Paragraph followed by a line with a space only.

                Paragraph after a line with a space only.
                """
            ),
            self.dedent(
                """
                <p>Paragraph followed by a line with a space only.</p>
                <p>Paragraph after a line with a space only.</p>
                """
            )
        )

    def test_consecutive_multiline_paragraphs(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Paragraph 1, line 1.
                Paragraph 1, line 2.

                Paragraph 2, line 1.
                Paragraph 2, line 2.
                """
            ),
            self.dedent(
                """
                <p>Paragraph 1, line 1.
                Paragraph 1, line 2.</p>
                <p>Paragraph 2, line 1.
                Paragraph 2, line 2.</p>
                """
            )
        )

    def test_paragraph_leading_space(self):
        self.assertMarkdownRenders(
            ' A paragraph with 1 leading space.',

            '<p>A paragraph with 1 leading space.</p>'
        )

    def test_paragraph_2_leading_spaces(self):
        self.assertMarkdownRenders(
            '  A paragraph with 2 leading spaces.',

            '<p>A paragraph with 2 leading spaces.</p>'
        )

    def test_paragraph_3_leading_spaces(self):
        self.assertMarkdownRenders(
            '   A paragraph with 3 leading spaces.',

            '<p>A paragraph with 3 leading spaces.</p>'
        )

    def test_paragraph_trailing_leading_space(self):
        self.assertMarkdownRenders(
            ' A paragraph with 1 trailing and 1 leading space. ',

            '<p>A paragraph with 1 trailing and 1 leading space. </p>'
        )

    def test_paragraph_trailing_tab(self):
        self.assertMarkdownRenders(
            'A paragraph with 1 trailing tab.\t',

            '<p>A paragraph with 1 trailing tab.    </p>'
        )

    def test_paragraphs_CR(self):
        self.assertMarkdownRenders(
            'Paragraph 1, line 1.\rParagraph 1, line 2.\r\rParagraph 2, line 1.\rParagraph 2, line 2.\r',

            self.dedent(
                """
                <p>Paragraph 1, line 1.
                Paragraph 1, line 2.</p>
                <p>Paragraph 2, line 1.
                Paragraph 2, line 2.</p>
                """
            )
        )

    def test_paragraphs_LF(self):
        self.assertMarkdownRenders(
            'Paragraph 1, line 1.\nParagraph 1, line 2.\n\nParagraph 2, line 1.\nParagraph 2, line 2.\n',

            self.dedent(
                """
                <p>Paragraph 1, line 1.
                Paragraph 1, line 2.</p>
                <p>Paragraph 2, line 1.
                Paragraph 2, line 2.</p>
                """
            )
        )

    def test_paragraphs_CR_LF(self):
        self.assertMarkdownRenders(
            'Paragraph 1, line 1.\r\nParagraph 1, line 2.\r\n\r\nParagraph 2, line 1.\r\nParagraph 2, line 2.\r\n',

            self.dedent(
                """
                <p>Paragraph 1, line 1.
                Paragraph 1, line 2.</p>
                <p>Paragraph 2, line 1.
                Paragraph 2, line 2.</p>
                """
            )
        )
