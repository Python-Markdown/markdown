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
import markdown


class TestFencedCode(TestCase):

    def setUp(self):
        self.has_pygments = True
        try:
            import pygments  # noqa
        except ImportError:
            self.has_pygments = False

    def testBasicFence(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                A paragraph before a fenced code block:

                ```
                Fenced code block
                ```
                '''
            ),
            self.dedent(
                '''
                <p>A paragraph before a fenced code block:</p>
                <pre><code>Fenced code block
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testNestedFence(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ````

                ```
                ````
                '''
            ),
            self.dedent(
                '''
                <pre><code>
                ```
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedTildes(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ~~~
                # Arbitrary code
                ``` # these backticks will not close the block
                ~~~
                '''
            ),
            self.dedent(
                '''
                <pre><code># Arbitrary code
                ``` # these backticks will not close the block
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedLanguageNoDot(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` python
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedLanguageWithDot(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` .python
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedCodeWithHighlightLines(self):
        if self.has_pygments:
            expected = self.dedent(
                '''
                <div class="codehilite"><pre><span></span><code><span class="hll">line 1
                </span>line 2
                <span class="hll">line 3
                </span></code></pre></div>
                '''
            )
        else:
            expected = self.dedent(
                    '''
                    <pre class="codehilite"><code>line 1
                    line 2
                    line 3
                    </code></pre>
                    '''
                )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ```hl_lines="1 3"
                line 1
                line 2
                line 3
                ```
                '''
            ),
            expected,
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),
                'fenced_code'
            ]
        )

    def testFencedLanguageAndHighlightLines(self):
        if self.has_pygments:
            expected = (
                '<div class="python codehilite"><pre><span></span><code>'
                '<span class="hll"><span class="n">line</span> <span class="mi">1</span>\n'
                '</span><span class="n">line</span> <span class="mi">2</span>\n'
                '<span class="hll"><span class="n">line</span> <span class="mi">3</span>\n'
                '</span></code></pre></div>'
            )
        else:
            expected = self.dedent(
                    '''
                    <pre class="python codehilite"><code class="language-python">line 1
                    line 2
                    line 3
                    </code></pre>
                    '''
                )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` .python hl_lines="1 3"
                line 1
                line 2
                line 3
                ```
                '''
            ),
            expected,
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),
                'fenced_code'
            ]
        )

    def testFencedLanguageAndPygmentsDisabled(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` .python
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(use_pygments=False),
                'fenced_code'
            ]
        )

    def testFencedLanguageDoubleEscape(self):
        if self.has_pygments:
            expected = (
                '<div class="html codehilite"><pre><span></span><code>'
                '<span class="p">&lt;</span><span class="nt">span</span>'
                '<span class="p">&gt;</span>This<span class="ni">&amp;amp;</span>'
                'That<span class="p">&lt;/</span><span class="nt">span</span>'
                '<span class="p">&gt;</span>\n'
                '</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="html codehilite"><code class="language-html">'
                '&lt;span&gt;This&amp;amp;That&lt;/span&gt;\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ```html
                <span>This&amp;That</span>
                ```
                '''
            ),
            expected,
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(),
                'fenced_code'
            ]
        )

    def testFencedAmps(self):
        if self.has_pygments:
            expected = self.dedent(
                '''
                <div class="text codehilite"><pre><span></span><code>&amp;
                &amp;amp;
                &amp;amp;amp;
                </code></pre></div>
                '''
            )
        else:
            expected = self.dedent(
                '''
                <pre class="text codehilite"><code class="language-text">&amp;
                &amp;amp;
                &amp;amp;amp;
                </code></pre>
                '''
            )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ```text
                &
                &amp;
                &amp;amp;
                ```
                '''
            ),
            expected,
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(),
                'fenced_code'
            ]
        )

    def test_fenced_code_in_raw_html(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <details>
                ```
                Begone placeholders!
                ```
                </details>
                """
            ),
            self.dedent(
                """
                <details>

                <pre><code>Begone placeholders!
                </code></pre>

                </details>
                """
            ),
            extensions=['fenced_code']
        )

    def testFencedLanguageInAttr(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` {.python}
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedMultipleClassesInAttr(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` {.python .foo .bar}
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python foo bar"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedIdInAttr(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { #foo }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre id="foo"><code># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedIdAndLangInAttr(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python #foo }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre id="foo"><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedIdAndLangAndClassInAttr(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python #foo .bar }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre id="foo"><code class="language-python bar"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedCodeWithHighlightLinesInAttr(self):
        if self.has_pygments:
            expected = self.dedent(
                '''
                <div class="codehilite"><pre><span></span><code><span class="hll">line 1
                </span>line 2
                <span class="hll">line 3
                </span></code></pre></div>
                '''
            )
        else:
            expected = self.dedent(
                    '''
                    <pre class="codehilite"><code>line 1
                    line 2
                    line 3
                    </code></pre>
                    '''
                )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ```{ hl_lines="1 3" }
                line 1
                line 2
                line 3
                ```
                '''
            ),
            expected,
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),
                'fenced_code'
            ]
        )

    def testFencedLanguageAndHighlightLinesInAttr(self):
        if self.has_pygments:
            expected = (
                '<div class="python codehilite"><pre><span></span><code>'
                '<span class="hll"><span class="n">line</span> <span class="mi">1</span>\n'
                '</span><span class="n">line</span> <span class="mi">2</span>\n'
                '<span class="hll"><span class="n">line</span> <span class="mi">3</span>\n'
                '</span></code></pre></div>'
            )
        else:
            expected = self.dedent(
                    '''
                    <pre class="python codehilite"><code class="language-python">line 1
                    line 2
                    line 3
                    </code></pre>
                    '''
                )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python hl_lines="1 3" }
                line 1
                line 2
                line 3
                ```
                '''
            ),
            expected,
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),
                'fenced_code'
            ]
        )

    def testFencedLanguageIdInAttrAndPygmentsDisabled(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python #foo }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre id="foo"><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(use_pygments=False),
                'fenced_code'
            ]
        )

    def testFencedLanguageIdAndPygmentsDisabledInAttr(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python #foo use_pygments=False }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre id="foo"><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=['codehilite', 'fenced_code']
        )

    def testFencedLanguageIdAndPygmentsDisabledInAttrNoCodehilite(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python #foo use_pygments=False }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre id="foo"><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedLanguageIdAndPygmentsEnabledInAttrNoCodehilite(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python #foo use_pygments=True }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre id="foo"><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code']
        )

    def testFencedLanguageAttrCssclass(self):
        if self.has_pygments:
            expected = self.dedent(
                '''
                <div class="python pygments"><pre><span></span><code><span class="c1"># Some python code</span>
                </code></pre></div>
                '''
            )
        else:
            expected = (
                '<pre class="python pygments"><code class="language-python"># Some python code\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python css_class='pygments' }
                # Some python code
                ```
                '''
            ),
            expected,
            extensions=['codehilite', 'fenced_code']
        )

    def testFencedLanguageAttrLinenums(self):
        if self.has_pygments:
            expected = (
                '<table class="python codehilitetable"><tr>'
                '<td class="linenos"><div class="linenodiv"><pre>1</pre></div></td>'
                '<td class="code"><div class="python codehilite"><pre><span></span>'
                '<code><span class="c1"># Some python code</span>\n'
                '</code></pre></div>\n'
                '</td></tr></table>'
            )
        else:
            expected = (
                '<pre class="python codehilite"><code class="language-python linenums"># Some python code\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python linenums=True }
                # Some python code
                ```
                '''
            ),
            expected,
            extensions=['codehilite', 'fenced_code']
        )

    def testFencedLanguageAttrGuesslang(self):
        if self.has_pygments:
            expected = self.dedent(
                '''
                <div class="codehilite"><pre><span></span><code># Some python code
                </code></pre></div>
                '''
            )
        else:
            expected = (
                '<pre class="codehilite"><code># Some python code\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { guess_lang=False }
                # Some python code
                ```
                '''
            ),
            expected,
            extensions=['codehilite', 'fenced_code']
        )

    def testFencedLanguageAttrNoclasses(self):
        if self.has_pygments:
            expected = (
                '<div class="python codehilite" style="background: #f8f8f8">'
                '<pre style="line-height: 125%"><span></span><code>'
                '<span style="color: #408080; font-style: italic"># Some python code</span>\n'
                '</code></pre></div>'
            )
        else:
            expected = (
                '<pre class="python codehilite"><code class="language-python"># Some python code\n'
                '</code></pre>'
            )
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python noclasses=True }
                # Some python code
                ```
                '''
            ),
            expected,
            extensions=['codehilite', 'fenced_code']
        )

    def testFencedLanguageNoCodehiliteWithAttrList(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python foo=bar }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python" foo="bar"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code', 'attr_list']
        )

    def testFencedLanguagePygmentsDisabledInAttrNoCodehiliteWithAttrList(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python foo=bar use_pygments=False }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python" foo="bar"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code', 'attr_list']
        )

    def testFencedLanguagePygmentsEnabledInAttrNoCodehiliteWithAttrList(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` { .python foo=bar use_pygments=True }
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="language-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=['fenced_code', 'attr_list']
        )

    def testFencedLanguageNoPrefix(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` python
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="python"># Some python code
                </code></pre>
                '''
            ),
            extensions=[markdown.extensions.fenced_code.FencedCodeExtension(lang_prefix='')]
        )

    def testFencedLanguageAltPrefix(self):
        self.assertMarkdownRenders(
            self.dedent(
                '''
                ``` python
                # Some python code
                ```
                '''
            ),
            self.dedent(
                '''
                <pre><code class="lang-python"># Some python code
                </code></pre>
                '''
            ),
            extensions=[markdown.extensions.fenced_code.FencedCodeExtension(lang_prefix='lang-')]
        )
