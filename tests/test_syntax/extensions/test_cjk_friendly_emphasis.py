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

Copyright 2007-2023 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from markdown.test_tools import TestCase


class TestCJKFriendlyEmphasis(TestCase):
    # -- Japanese: underscore strong --

    def test_underscore_strong_with_cjk(self):
        self.assertMarkdownRenders(
            'これは__重要__です',
            '<p>これは<strong>重要</strong>です</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    def test_underscore_em_with_cjk(self):
        self.assertMarkdownRenders(
            'これは_重要_です',
            '<p>これは<em>重要</em>です</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    def test_underscore_strong_with_cjk_quotes(self):
        self.assertMarkdownRenders(
            '彼は__「異常」__と言った',
            '<p>彼は<strong>「異常」</strong>と言った</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    def test_underscore_strong_with_cjk_parens(self):
        self.assertMarkdownRenders(
            '私は__（仮説）__だと思う',
            '<p>私は<strong>（仮説）</strong>だと思う</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    def test_underscore_strong_with_cjk_period(self):
        self.assertMarkdownRenders(
            'これは__重要。__だから',
            '<p>これは<strong>重要。</strong>だから</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    def test_underscore_strong_at_start(self):
        self.assertMarkdownRenders(
            '__「注意」__してください',
            '<p><strong>「注意」</strong>してください</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    # -- Chinese --

    def test_underscore_strong_chinese(self):
        self.assertMarkdownRenders(
            '这是__强调__文本',
            '<p>这是<strong>强调</strong>文本</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    # -- Korean --

    def test_underscore_strong_korean(self):
        self.assertMarkdownRenders(
            '__강조__합니다',
            '<p><strong>강조</strong>합니다</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    # -- Mixed CJK and Latin --

    def test_underscore_strong_mixed(self):
        self.assertMarkdownRenders(
            '日本語__English__混在',
            '<p>日本語<strong>English</strong>混在</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    # -- ASCII intraword protection preserved --

    def test_ascii_intraword_underscore_protected(self):
        self.assertMarkdownRenders(
            'foo_bar_baz',
            '<p>foo_bar_baz</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    def test_ascii_intraword_double_underscore_protected(self):
        self.assertMarkdownRenders(
            'foo__bar__baz',
            '<p>foo__bar__baz</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    # -- Asterisk emphasis unchanged --

    def test_asterisk_strong_cjk(self):
        self.assertMarkdownRenders(
            'これは**「重要」**です',
            '<p>これは<strong>「重要」</strong>です</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    def test_asterisk_em_cjk(self):
        self.assertMarkdownRenders(
            'これは*重要*です',
            '<p>これは<em>重要</em>です</p>',
            extensions=['markdown.extensions.cjk_friendly_emphasis']
        )

    # -- Without extension, underscore CJK should NOT work --

    def test_without_extension_underscore_cjk_fails(self):
        self.assertMarkdownRenders(
            'これは__重要__です',
            '<p>これは__重要__です</p>',
        )
