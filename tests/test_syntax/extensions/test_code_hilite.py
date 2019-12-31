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

Copyright 2007-2019 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from markdown.test_tools import TestCase
from markdown.extensions.codehilite import CodeHiliteExtension


class TestCodeHilite(TestCase):
    """ Test codehilite extension. """

    def setUp(self):
        self.has_pygments = True
        try:
            import pygments  # noqa
        except ImportError:
            self.has_pygments = False

    def testBasicCodeHilite(self):
        if self.has_pygments:
            # Odd result as no lang given and a single comment is not enough for guessing.
            expected = (
                '<div class="codehilite"><pre><span></span><code><span class="err"># A Code Comment</span>\n'
                '</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code># A Code Comment\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            '\t# A Code Comment',
            expected,
            extensions=['codehilite']
        )

    def testLinenumsTrue(self):
        if self.has_pygments:
            expected = (
                '<table class="codehilitetable"><tr>'
                '<td class="linenos"><div class="linenodiv"><pre>1</pre></div></td>'
                '<td class="code"><div class="codehilite"><pre><span></span>'
                '<code><span class="err"># A Code Comment</span>\n'
                '</code></pre></div>\n'
                '</td></tr></table>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code class="linenums"># A Code Comment\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            '\t# A Code Comment',
            expected,
            extensions=[CodeHiliteExtension(linenums=True)]
        )

    def testLinenumsFalse(self):
        if self.has_pygments:
            expected = (
                '<div class="codehilite"><pre><span></span><code><span class="c1"># A Code Comment</span>\n'
                '</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code class="language-python"># A Code Comment\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            (
                '\t#!Python\n'
                '\t# A Code Comment'
            ),
            expected,
            extensions=[CodeHiliteExtension(linenums=False)]
        )

    def testLinenumsNone(self):
        if self.has_pygments:
            expected = (
                '<div class="codehilite"><pre><span></span><code><span class="err"># A Code Comment</span>\n'
                '</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code># A Code Comment\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            '\t# A Code Comment',
            expected,
            extensions=[CodeHiliteExtension(linenums=None)]
        )

    def testLinenumsNoneWithShebang(self):
        if self.has_pygments:
            expected = (
                '<table class="codehilitetable"><tr>'
                '<td class="linenos"><div class="linenodiv"><pre>1</pre></div></td>'
                '<td class="code"><div class="codehilite"><pre><span></span>'
                '<code><span class="c1"># A Code Comment</span>\n'
                '</code></pre></div>\n'
                '</td></tr></table>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code class="language-python linenums"># A Code Comment\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            (
                '\t#!Python\n'
                '\t# A Code Comment'
            ),
            expected,
            extensions=[CodeHiliteExtension(linenums=None)]
        )

    def testLinenumsNoneWithColon(self):
        if self.has_pygments:
            expected = (
                '<div class="codehilite"><pre><span></span><code><span class="c1"># A Code Comment</span>\n'
                '</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code class="language-python"># A Code Comment\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            (
                '\t:::Python\n'
                '\t# A Code Comment'
            ),
            expected,
            extensions=[CodeHiliteExtension(linenums=None)]
        )

    def testHighlightLinesWithColon(self):
        if self.has_pygments:
            expected = (
                '<div class="codehilite"><pre><span></span><code><span class="hll"><span class="c1">#line 1</span>\n'
                '</span><span class="c1">#line 2</span>\n'
                '<span class="c1">#line 3</span>\n'
                '</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code class="language-python">#line 1\n'
                '#line 2\n'
                '#line 3\n'
                '</code></pre>'
            )
        # Double quotes
        self.assertMarkdownRenders(
            (
                '\t:::Python hl_lines="1"\n'
                '\t#line 1\n'
                '\t#line 2\n'
                '\t#line 3'
            ),
            expected,
            extensions=['codehilite']
        )
        # Single quotes
        self.assertMarkdownRenders(
            (
                "\t:::Python hl_lines='1'\n"
                '\t#line 1\n'
                '\t#line 2\n'
                '\t#line 3'
            ),
            expected,
            extensions=['codehilite']
        )

    def testUsePygmentsFalse(self):
        self.assertMarkdownRenders(
            (
                '\t:::Python\n'
                '\t# A Code Comment'
            ),
            (
                '<pre class="codehilite"><code class="language-python"># A Code Comment\n'
                '</code></pre>'
            ),
            extensions=[CodeHiliteExtension(use_pygments=False)]
        )

    def testDoubleEscape(self):
        if self.has_pygments:
            expected = (
                '<div class="codehilite"><pre>'
                '<span></span>'
                '<code><span class="p">&lt;</span><span class="nt">span</span><span class="p">&gt;</span>'
                'This<span class="ni">&amp;amp;</span>That'
                '<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>'
                '\n</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code class="language-html">'
                '&lt;span&gt;This&amp;amp;That&lt;/span&gt;\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            (
                '\t:::html\n'
                '\t<span>This&amp;That</span>'
            ),
            expected,
            extensions=['codehilite']
        )

    def testHighlightAmps(self):
        if self.has_pygments:
            expected = (
                '<div class="codehilite"><pre><span></span><code>&amp;\n'
                '&amp;amp;\n'
                '&amp;amp;amp;\n'
                '</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="codehilite"><code class="language-text">&amp;\n'
                '&amp;amp;\n'
                '&amp;amp;amp;\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            (
                '\t:::text\n'
                '\t&\n'
                '\t&amp;\n'
                '\t&amp;amp;'
            ),
            expected,
            extensions=['codehilite']
        )
