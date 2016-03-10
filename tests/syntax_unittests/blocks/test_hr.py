from markdown.test_tools import TestCase


class TestHorizontalRules(TestCase):

    def test_hr_asterisk(self):
        self.assertMarkdownRenders(
            '***',

            '<hr />'
        )

    def test_hr_asterisk_spaces(self):
        self.assertMarkdownRenders(
            '* * *',

            '<hr />'
        )

    def test_hr_asterisk_long(self):
        self.assertMarkdownRenders(
            '*******',

            '<hr />'
        )

    def test_hr_asterisk_spaces_long(self):
        self.assertMarkdownRenders(
            '* * * * * * *',

            '<hr />'
        )

    def test_hr_asterisk_1_indent(self):
        self.assertMarkdownRenders(
            ' ***',

            '<hr />'
        )

    def test_hr_asterisk_spaces_1_indent(self):
        self.assertMarkdownRenders(
            ' * * *',

            '<hr />'
        )
    
    def test_hr_asterisk_2_indent(self):
        self.assertMarkdownRenders(
            '  ***',

            '<hr />'
        )

    def test_hr_asterisk_spaces_2_indent(self):
        self.assertMarkdownRenders(
            '  * * *',

            '<hr />'
        )
    
    def test_hr_asterisk_3_indent(self):
        self.assertMarkdownRenders(
            '   ***',

            '<hr />'
        )

    def test_hr_asterisk_spaces_3_indent(self):
        self.assertMarkdownRenders(
            '   * * *',

            '<hr />'
        )
    
    def test_hr_asterisk_trailing_space(self):
        self.assertMarkdownRenders(
            '*** ',

            '<hr />'
        )

    def test_hr_asterisk_spaces_trailing_space(self):
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

    def test_not_hr_2_asterisk(self):
        self.assertMarkdownRenders(
            '**',

            '<p>**</p>'
        )

    def test_not_hr_2_asterisk_spaces(self):
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