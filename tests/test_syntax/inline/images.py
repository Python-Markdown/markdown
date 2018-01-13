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

    def test_single_quote(self):
        self.assertMarkdownRenders(
            """![test](link"notitle.png)""",
            """<p><img alt="test" src="link&quot;notitle.png" /></p>"""
        )

    def test_angle_with_mixed_title_quotes(self):
        self.assertMarkdownRenders(
            """![Text](<http://link.com/with spaces '"and quotes".png> 'and title') more text""",
            """<p><img alt="Text" src="http://link.com/with spaces '&quot;and quotes&quot;.png" title="and title" />"""
            """ more text</p>"""
        )

    def test_misc(self):
        self.assertMarkdownRenders(
            """![Poster](http://humane_man.jpg "The most humane man.")""",
           """<p><img alt="Poster" src="http://humane_man.jpg" title="The most humane man." /></p>"""
        )

    def test_misc_ref(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ![Poster][]

                [Poster]:http://humane_man.jpg "The most humane man."
                """
            ),
            self.dedent(
                """
                <p><img alt="Poster" src="http://humane_man.jpg" title="The most humane man." /></p>
                """
            )
        )

    def test_misc_blank(self):
        self.assertMarkdownRenders(
            """![Blank]()""",
            """<p><img alt="Blank" src="" /></p>"""
        )

    def test_misc_img_title(self):
        self.assertMarkdownRenders(
            """![Image](http://humane man.jpg "The most humane man.")""",
            """<p><img alt="Image" src="http://humane man.jpg" title="The most humane man." /></p>"""
        )

    def test_misc_img(self):
        self.assertMarkdownRenders(
            """![Image](http://humane man.jpg)""",
            """<p><img alt="Image" src="http://humane man.jpg" /></p>"""
        )
