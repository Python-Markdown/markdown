from markdown.test_tools import TestCase


class TestAdvancedImages(TestCase):

    def test_nested_square_brackets(self):
        self.assertMarkdownRenders(
            """![Text[[[[[[[]]]]]]][]](http://link.com/image.png) more text""",
            """<p><img alt="Text[[[[[[[]]]]]]][]" src="http://link.com/image.png" /> more text</p>"""
        )

    def test_nested_round_brackets(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/(((((((()))))))()).png) more text""",
            """<p><img alt="Text" src="http://link.com/(((((((()))))))()).png" /> more text</p>"""
        )

    def test_uneven_brackets_with_titles1(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/(.png"title") more text""",
            """<p><img alt="Text" src="http://link.com/(.png" title="title" /> more text</p>"""
        )

    def test_uneven_brackets_with_titles2(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/('.png"title") more text""",
            """<p><img alt="Text" src="http://link.com/('.png" title="title" /> more text</p>"""
        )

    def test_uneven_brackets_with_titles3(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/(.png"title)") more text""",
            """<p><img alt="Text" src="http://link.com/(.png" title="title)" /> more text</p>"""
        )

    def test_uneven_brackets_with_titles4(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/(.png "title") more text""",
            """<p><img alt="Text" src="http://link.com/(.png" title="title" /> more text</p>"""
        )

    def test_uneven_brackets_with_titles5(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/(.png "title)") more text""",
            """<p><img alt="Text" src="http://link.com/(.png" title="title)" /> more text</p>"""
        )

    def test_mixed_title_quotes1(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/'.png"title") more text""",
            """<p><img alt="Text" src="http://link.com/'.png" title="title" /> more text</p>"""
        )

    def test_mixed_title_quotes2(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/".png'title') more text""",
            """<p><img alt="Text" src="http://link.com/&quot;.png" title="title" /> more text</p>"""
        )

    def test_mixed_title_quotes3(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/with spaces.png'"and quotes" 'and title') more text""",
            """<p><img alt="Text" src="http://link.com/with spaces.png" title="&quot;and quotes&quot; 'and title" />"""
            """ more text</p>"""
        )

    def test_mixed_title_quotes4(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/with spaces'.png"and quotes" 'and title") more text""",
            """<p><img alt="Text" src="http://link.com/with spaces'.png" title="and quotes&quot; 'and title" />"""
            """ more text</p>"""
        )

    def test_mixed_title_quotes5(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/with spaces .png'"and quotes" 'and title') more text""",
            """<p><img alt="Text" src="http://link.com/with spaces .png" title="&quot;and quotes&quot;"""
            """ 'and title" /> more text</p>"""
        )

    def test_mixed_title_quotes6(self):
        self.assertMarkdownRenders(
            """![Text](http://link.com/with spaces "and quotes".png 'and title') more text""",
            """<p><img alt="Text" src="http://link.com/with spaces &quot;and quotes&quot;.png" title="and title" />"""
            """ more text</p>"""
        )

    def test_angle_with_mixed_title_quotes(self):
        self.assertMarkdownRenders(
            """![Text](<http://link.com/with spaces '"and quotes".png> 'and title') more text""",
            """<p><img alt="Text" src="http://link.com/with spaces '&quot;and quotes&quot;.png" title="and title" />"""
            """ more text</p>"""
        )
