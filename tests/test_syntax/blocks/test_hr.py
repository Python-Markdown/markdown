from markdown.test_tools import TestCase


class TestHorizontalRules(TestCase):

    def test_hr_asterisks(self):
        self.assertMarkdownRenders(
            '***',

            '<hr />'
        )

    def test_hr_asterisks_spaces(self):
        self.assertMarkdownRenders(
            '* * *',

            '<hr />'
        )

    def test_hr_asterisks_long(self):
        self.assertMarkdownRenders(
            '*******',

            '<hr />'
        )

    def test_hr_asterisks_spaces_long(self):
        self.assertMarkdownRenders(
            '* * * * * * *',

            '<hr />'
        )

    def test_hr_asterisks_1_indent(self):
        self.assertMarkdownRenders(
            ' ***',

            '<hr />'
        )

    def test_hr_asterisks_spaces_1_indent(self):
        self.assertMarkdownRenders(
            ' * * *',

            '<hr />'
        )

    def test_hr_asterisks_2_indent(self):
        self.assertMarkdownRenders(
            '  ***',

            '<hr />'
        )

    def test_hr_asterisks_spaces_2_indent(self):
        self.assertMarkdownRenders(
            '  * * *',

            '<hr />'
        )

    def test_hr_asterisks_3_indent(self):
        self.assertMarkdownRenders(
            '   ***',

            '<hr />'
        )

    def test_hr_asterisks_spaces_3_indent(self):
        self.assertMarkdownRenders(
            '   * * *',

            '<hr />'
        )

    def test_hr_asterisks_trailing_space(self):
        self.assertMarkdownRenders(
            '*** ',

            '<hr />'
        )

    def test_hr_asterisks_spaces_trailing_space(self):
        self.assertMarkdownRenders(
            '* * * ',

            '<hr />'
        )

    def test_hr_hyphens(self):
        self.assertMarkdownRenders(
            '---',

            '<hr />'
        )

    def test_hr_hyphens_spaces(self):
        self.assertMarkdownRenders(
            '- - -',

            '<hr />'
        )

    def test_hr_hyphens_long(self):
        self.assertMarkdownRenders(
            '-------',

            '<hr />'
        )

    def test_hr_hyphens_spaces_long(self):
        self.assertMarkdownRenders(
            '- - - - - - -',

            '<hr />'
        )

    def test_hr_hyphens_1_indent(self):
        self.assertMarkdownRenders(
            ' ---',

            '<hr />'
        )

    def test_hr_hyphens_spaces_1_indent(self):
        self.assertMarkdownRenders(
            ' - - -',

            '<hr />'
        )

    def test_hr_hyphens_2_indent(self):
        self.assertMarkdownRenders(
            '  ---',

            '<hr />'
        )

    def test_hr_hyphens_spaces_2_indent(self):
        self.assertMarkdownRenders(
            '  - - -',

            '<hr />'
        )

    def test_hr_hyphens_3_indent(self):
        self.assertMarkdownRenders(
            '   ---',

            '<hr />'
        )

    def test_hr_hyphens_spaces_3_indent(self):
        self.assertMarkdownRenders(
            '   - - -',

            '<hr />'
        )

    def test_hr_hyphens_trailing_space(self):
        self.assertMarkdownRenders(
            '--- ',

            '<hr />'
        )

    def test_hr_hyphens_spaces_trailing_space(self):
        self.assertMarkdownRenders(
            '- - - ',

            '<hr />'
        )

    def test_hr_underscores(self):
        self.assertMarkdownRenders(
            '___',

            '<hr />'
        )

    def test_hr_underscores_spaces(self):
        self.assertMarkdownRenders(
            '_ _ _',

            '<hr />'
        )

    def test_hr_underscores_long(self):
        self.assertMarkdownRenders(
            '_______',

            '<hr />'
        )

    def test_hr_underscores_spaces_long(self):
        self.assertMarkdownRenders(
            '_ _ _ _ _ _ _',

            '<hr />'
        )

    def test_hr_underscores_1_indent(self):
        self.assertMarkdownRenders(
            ' ___',

            '<hr />'
        )

    def test_hr_underscores_spaces_1_indent(self):
        self.assertMarkdownRenders(
            ' _ _ _',

            '<hr />'
        )

    def test_hr_underscores_2_indent(self):
        self.assertMarkdownRenders(
            '  ___',

            '<hr />'
        )

    def test_hr_underscores_spaces_2_indent(self):
        self.assertMarkdownRenders(
            '  _ _ _',

            '<hr />'
        )

    def test_hr_underscores_3_indent(self):
        self.assertMarkdownRenders(
            '   ___',

            '<hr />'
        )

    def test_hr_underscores_spaces_3_indent(self):
        self.assertMarkdownRenders(
            '   _ _ _',

            '<hr />'
        )

    def test_hr_underscores_trailing_space(self):
        self.assertMarkdownRenders(
            '___ ',

            '<hr />'
        )

    def test_hr_underscores_spaces_trailing_space(self):
        self.assertMarkdownRenders(
            '_ _ _ ',

            '<hr />'
        )

    def test_hr_before_paragraph(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ***
                An HR followed by a paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <hr />
                <p>An HR followed by a paragraph with no blank line.</p>
                """
            )
        )

    def test_hr_after_paragraph(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                A paragraph followed by an HR with no blank line.
                ***
                """
            ),
            self.dedent(
                """
                <p>A paragraph followed by an HR with no blank line.</p>
                <hr />
                """
            )
        )

    def test_not_hr_2_asterisks(self):
        self.assertMarkdownRenders(
            '**',

            '<p>**</p>'
        )

    def test_not_hr_2_asterisks_spaces(self):
        self.assertMarkdownRenders(
            '* *',

            self.dedent(
                """
                <ul>
                <li>*</li>
                </ul>
                """
            )
        )

    def test_not_hr_2_hyphens(self):
        self.assertMarkdownRenders(
            '--',

            '<p>--</p>'
        )

    def test_not_hr_2_hyphens_spaces(self):
        self.assertMarkdownRenders(
            '- -',

            self.dedent(
                """
                <ul>
                <li>-</li>
                </ul>
                """
            )
        )

    def test_not_hr_2_underscores(self):
        self.assertMarkdownRenders(
            '__',

            '<p>__</p>'
        )

    def test_not_hr_2_underscores_spaces(self):
        self.assertMarkdownRenders(
            '_ _',

            '<p>_ _</p>'
        )
