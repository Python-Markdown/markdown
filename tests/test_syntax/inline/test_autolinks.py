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

Copyright 2007-2021 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from markdown.test_tools import TestCase


class TestAutomaticLinks(TestCase):

    def test_url_schemes(self):
        for url in (
            'http://example.org',
            'https://example.org',
            'ftp://example.org',
            'ftps://example.org',
            'HtTpS://example.org',
            'ssh://example.org',
            'git://example.org/repo',
            's3://bucket/key',
            'git+ssh://example.org/repo',
            'x.y-z://example.org',
        ):
            with self.subTest(url=url):
                self.assertMarkdownRenders(
                    f'<{url}>',
                    f'<p><a href="{url}">{url}</a></p>'
                )

    def test_url_scheme_with_query(self):
        self.assertMarkdownRenders(
            '<ssh://example.org/path?q=one&x=two>',
            '<p><a href="ssh://example.org/path?q=one&amp;x=two">'
            'ssh://example.org/path?q=one&amp;x=two</a></p>'
        )

    def test_adjacent_url_schemes(self):
        self.assertMarkdownRenders(
            'Before <ssh://one><git://two> after',
            '<p>Before <a href="ssh://one">ssh://one</a>'
            '<a href="git://two">git://two</a> after</p>'
        )

    def test_url_scheme_without_closing_bracket(self):
        self.assertMarkdownRenders(
            '<ssh://example.org',
            '<p>&lt;ssh://example.org</p>'
        )

    def test_url_scheme_in_code_span(self):
        self.assertMarkdownRenders(
            '`<ssh://example.org>`',
            '<p><code>&lt;ssh://example.org&gt;</code></p>'
        )

    def test_invalid_url_schemes(self):
        for source, expected in (
            ('<1http://example.org>', '<p>&lt;1http://example.org&gt;</p>'),
            ('<git_ssh://example.org>', '<p><git_ssh://example.org></p>'),
            ('<urn:foo>', '<p><urn:foo></p>'),
            ('<em>boo!</em>', '<p><em>boo!</em></p>'),
        ):
            with self.subTest(source=source):
                self.assertMarkdownRenders(source, expected)

    def test_email_address(self):
        self.assertMarkdownRenders(
            'asdfasdfadsfasd <yuri@freewisdom.org> or you can say ',
            '<p>asdfasdfadsfasd <a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#121;&#117;&#114;'
            '&#105;&#64;&#102;&#114;&#101;&#101;&#119;&#105;&#115;&#100;&#111;&#109;&#46;&#111;&#114;'
            '&#103;">&#121;&#117;&#114;&#105;&#64;&#102;&#114;&#101;&#101;&#119;&#105;&#115;&#100;'
            '&#111;&#109;&#46;&#111;&#114;&#103;</a> or you can say </p>'
        )

    def test_mailto_email_address(self):
        self.assertMarkdownRenders(
            'instead <mailto:yuri@freewisdom.org>',
            '<p>instead <a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#121;&#117;&#114;&#105;&#64;'
            '&#102;&#114;&#101;&#101;&#119;&#105;&#115;&#100;&#111;&#109;&#46;&#111;&#114;&#103;">'
            '&#121;&#117;&#114;&#105;&#64;&#102;&#114;&#101;&#101;&#119;&#105;&#115;&#100;&#111;&#109;'
            '&#46;&#111;&#114;&#103;</a></p>'
        )

    def test_email_address_with_ampersand(self):
        self.assertMarkdownRenders(
            '<bob&sue@example.com>',
            '<p><a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#98;&#111;&#98;&#38;&#115;&#117;&#101;'
            '&#64;&#101;&#120;&#97;&#109;&#112;&#108;&#101;&#46;&#99;&#111;&#109;">&#98;&#111;&#98;&amp;'
            '&#115;&#117;&#101;&#64;&#101;&#120;&#97;&#109;&#112;&#108;&#101;&#46;&#99;&#111;&#109;</a></p>'
        )

    def test_invalid_email_address_local_part(self):
        self.assertMarkdownRenders(
            'Missing local-part <@domain>',
            '<p>Missing local-part &lt;@domain&gt;</p>'
        )

    def test_invalid_email_address_domain(self):
        self.assertMarkdownRenders(
            'Missing domain <local-part@>',
            '<p>Missing domain &lt;local-part@&gt;</p>'
        )
