from markdown.test_tools import TestCase


class TestAdvancedLinks(TestCase):

    def test_nested_square_brackets(self):
        self.assertMarkdownRenders(
            """[Text[[[[[[[]]]]]]][]](http://link.com) more text""",
            """<p><a href="http://link.com">Text[[[[[[[]]]]]]][]</a> more text</p>"""
        )

    def test_nested_round_brackets(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/(((((((()))))))())) more text""",
            """<p><a href="http://link.com/(((((((()))))))())">Text</a> more text</p>"""
        )

    def test_uneven_brackets_with_titles1(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/("title") more text""",
            """<p><a href="http://link.com/(" title="title">Text</a> more text</p>"""
        )

    def test_uneven_brackets_with_titles2(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/('"title") more text""",
            """<p><a href="http://link.com/('" title="title">Text</a> more text</p>"""
        )

    def test_uneven_brackets_with_titles3(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/("title)") more text""",
            """<p><a href="http://link.com/(" title="title)">Text</a> more text</p>"""
        )

    def test_uneven_brackets_with_titles4(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/( "title") more text""",
            """<p><a href="http://link.com/(" title="title">Text</a> more text</p>"""
        )

    def test_uneven_brackets_with_titles5(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/( "title)") more text""",
            """<p><a href="http://link.com/(" title="title)">Text</a> more text</p>"""
        )

    def test_mixed_title_quotes1(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/'"title") more text""",
            """<p><a href="http://link.com/'" title="title">Text</a> more text</p>"""
        )

    def test_mixed_title_quotes2(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/"'title') more text""",
            """<p><a href="http://link.com/&quot;" title="title">Text</a> more text</p>"""
        )

    def test_mixed_title_quotes3(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/with spaces'"and quotes" 'and title') more text""",
            """<p><a href="http://link.com/with spaces" title="&quot;and quotes&quot; 'and title">"""
            """Text</a> more text</p>"""
        )

    def test_mixed_title_quotes4(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/with spaces'"and quotes" 'and title") more text""",
            """<p><a href="http://link.com/with spaces'" title="and quotes&quot; 'and title">Text</a> more text</p>"""
        )

    def test_mixed_title_quotes5(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/with spaces '"and quotes" 'and title') more text""",
            """<p><a href="http://link.com/with spaces" title="&quot;and quotes&quot; 'and title">"""
            """Text</a> more text</p>"""
        )

    def test_mixed_title_quotes6(self):
        self.assertMarkdownRenders(
            """[Text](http://link.com/with spaces "and quotes" 'and title') more text""",
            """<p><a href="http://link.com/with spaces &quot;and quotes&quot;" title="and title">"""
            """Text</a> more text</p>"""
        )

    def test_single_quote(self):
        self.assertMarkdownRenders(
            """[test](link"notitle)""",
            """<p><a href="link&quot;notitle">test</a></p>"""
        )

    def test_angle_with_mixed_title_quotes(self):
        self.assertMarkdownRenders(
            """[Text](<http://link.com/with spaces '"and quotes"> 'and title') more text""",
            """<p><a href="http://link.com/with spaces '&quot;and quotes&quot;" title="and title">"""
            """Text</a> more text</p>"""
        )

    def test_amp_in_url(self):
        """Test amp in URLs."""

        self.assertMarkdownRenders(
            '[link](http://www.freewisdom.org/this&that)',
            '<p><a href="http://www.freewisdom.org/this&amp;that">link</a></p>'
        )
        self.assertMarkdownRenders(
            '[title](http://example.com/?a=1&amp;b=2)',
            '<p><a href="http://example.com/?a=1&amp;b=2">title</a></p>'
        )
