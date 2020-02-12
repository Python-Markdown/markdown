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

Copyright 2007-2018 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).

Python-Markdown Extension Regression Tests
==========================================

A collection of regression tests to confirm that the included extensions
continue to work as advertised. This used to be accomplished by doctests.
"""

import unittest
import markdown


class TestCaseWithAssertStartsWith(unittest.TestCase):

    def assertStartsWith(self, expectedPrefix, text, msg=None):
        if not text.startswith(expectedPrefix):
            if len(expectedPrefix) + 5 < len(text):
                text = text[:len(expectedPrefix) + 5] + '...'
            standardMsg = '{} not found at the start of {}'.format(repr(expectedPrefix),
                                                                   repr(text))
            self.fail(self._formatMessage(msg, standardMsg))


class TestExtensionClass(unittest.TestCase):
    """ Test markdown.extensions.Extension. """

    def setUp(self):
        class TestExtension(markdown.extensions.Extension):
            config = {
                'foo': ['bar', 'Description of foo'],
                'bar': ['baz', 'Description of bar']
            }

        self.ext = TestExtension()
        self.ExtKlass = TestExtension

    def testGetConfig(self):
        self.assertEqual(self.ext.getConfig('foo'), 'bar')

    def testGetConfigDefault(self):
        self.assertEqual(self.ext.getConfig('baz'), '')
        self.assertEqual(self.ext.getConfig('baz', default='missing'), 'missing')

    def testGetConfigs(self):
        self.assertEqual(self.ext.getConfigs(), {'foo': 'bar', 'bar': 'baz'})

    def testGetConfigInfo(self):
        self.assertEqual(
            dict(self.ext.getConfigInfo()),
            dict([
                ('foo', 'Description of foo'),
                ('bar', 'Description of bar')
            ])
        )

    def testSetConfig(self):
        self.ext.setConfig('foo', 'baz')
        self.assertEqual(self.ext.getConfigs(), {'foo': 'baz', 'bar': 'baz'})

    def testSetConfigWithBadKey(self):
        # self.ext.setConfig('bad', 'baz) ==> KeyError
        self.assertRaises(KeyError, self.ext.setConfig, 'bad', 'baz')

    def testConfigAsKwargsOnInit(self):
        ext = self.ExtKlass(foo='baz', bar='blah')
        self.assertEqual(ext.getConfigs(), {'foo': 'baz', 'bar': 'blah'})


class TestAbbr(unittest.TestCase):
    """ Test abbr extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['abbr'])

    def testSimpleAbbr(self):
        """ Test Abbreviations. """
        text = 'Some text with an ABBR and a REF. Ignore REFERENCE and ref.' + \
               '\n\n*[ABBR]: Abbreviation\n' + \
               '*[REF]: Abbreviation Reference'
        self.assertEqual(
            self.md.convert(text),
            '<p>Some text with an <abbr title="Abbreviation">ABBR</abbr> '
            'and a <abbr title="Abbreviation Reference">REF</abbr>. Ignore '
            'REFERENCE and ref.</p>'
        )

    def testNestedAbbr(self):
        """ Test Nested Abbreviations. """
        text = '[ABBR](/foo) and _ABBR_\n\n' + \
               '*[ABBR]: Abreviation'
        self.assertEqual(
            self.md.convert(text),
            '<p><a href="/foo"><abbr title="Abreviation">ABBR</abbr></a> '
            'and <em><abbr title="Abreviation">ABBR</abbr></em></p>'
        )


class TestCodeHilite(TestCaseWithAssertStartsWith):
    """ Test codehilite extension. """

    def setUp(self):
        self.has_pygments = True
        try:
            import pygments  # noqa
        except ImportError:
            self.has_pygments = False

    def testBasicCodeHilite(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(extensions=['codehilite'])
        if self.has_pygments:
            # Pygments can use random lexer here as we did not specify the language
            self.assertStartsWith('<div class="codehilite"><pre>', md.convert(text))
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsTrue(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=True)])
        if self.has_pygments:
            # Different versions of pygments output slightly different markup.
            # So we use 'startwith' and test just enough to confirm that
            # pygments received and processed linenums.
            self.assertStartsWith(
                '<table class="codehilitetable"><tr><td class="linenos">',
                md.convert(text)
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="linenums"># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsFalse(self):
        text = '\t#!Python\n\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=False)])
        if self.has_pygments:
            self.assertStartsWith('<div class="codehilite"><pre><span', md.convert(text))
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-python"># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsNone(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=None)])
        if self.has_pygments:
            # Pygments can use random lexer here as we did not specify the language
            self.assertStartsWith('<div class="codehilite"><pre>', md.convert(text))
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsNoneWithShebang(self):
        text = '\t#!Python\n\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=None)])
        if self.has_pygments:
            # Differant versions of pygments output slightly different markup.
            # So we use 'startwith' and test just enough to confirm that
            # pygments received and processed linenums.
            self.assertStartsWith(
                '<table class="codehilitetable"><tr><td class="linenos">',
                md.convert(text)
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-python linenums"># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsNoneWithColon(self):
        text = '\t:::Python\n\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=None)]
        )
        if self.has_pygments:
            self.assertStartsWith('<div class="codehilite"><pre><span', md.convert(text))
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-python"># A Code Comment'
                '</code></pre>'
            )

    def testHighlightLinesWithColon(self):
        # Test with hl_lines delimited by single or double quotes.
        text0 = '\t:::Python hl_lines="1"\n\t#line 1\n\t#line 2\n\t#line 3'
        text1 = "\t:::Python hl_lines='1'\n\t#line 1\n\t#line 2\n\t#line 3"

        for text in (text0, text1):
            md = markdown.Markdown(extensions=['codehilite'])
            if self.has_pygments:
                self.assertStartsWith(
                    '<div class="codehilite"><pre><code><span class="hll"',
                    md.convert(text).replace('<span></span>', '')
                )
            else:
                self.assertEqual(
                    md.convert(text),
                    '<pre class="codehilite">'
                    '<code class="language-python">#line 1\n'
                    '#line 2\n'
                    '#line 3</code></pre>'
                )

    def testUsePygmentsFalse(self):
        text = '\t:::Python\n\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(use_pygments=False)]
        )
        self.assertEqual(
            md.convert(text),
            '<pre class="codehilite"><code class="language-python"># A Code Comment'
            '</code></pre>'
        )

    def testDoubleEscape(self):
        """ Test entity escape logic in indented code blocks. """

        text = '\t:::html\n\t<span>This&amp;That</span>'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension()]
        )
        if self.has_pygments:
            self.assertEqual(
                md.convert(text),
                '<div class="codehilite"><pre>'
                '<span></span>'
                '<code><span class="p">&lt;</span><span class="nt">span</span><span class="p">&gt;</span>'
                'This<span class="ni">&amp;amp;</span>That'
                '<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>'
                '\n</code></pre></div>'
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-html">'
                '&lt;span&gt;This&amp;amp;That&lt;/span&gt;'
                '</code></pre>'
            )

    def testHighlightAmps(self):
        """ Test amp conversion logic. """

        text = '\t:::text\n\t&\n\t&amp;\n\t&amp;amp;'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension()]
        )
        if self.has_pygments:
            self.assertEqual(
                md.convert(text),
                '<div class="codehilite"><pre><span></span><code>&amp;\n&amp;amp;\n&amp;amp;amp;\n</code></pre></div>'
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-text">&amp;\n&amp;amp;\n&amp;amp;amp;</code></pre>'
            )


class TestFencedCode(TestCaseWithAssertStartsWith):
    """ Test fenced_code extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['fenced_code'])
        self.has_pygments = True
        try:
            import pygments  # noqa
        except ImportError:
            self.has_pygments = False

    def testBasicFence(self):
        """ Test Fenced Code Blocks. """
        text = '''
A paragraph before a fenced code block:

~~~
Fenced code block
~~~'''
        self.assertEqual(
            self.md.convert(text),
            '<p>A paragraph before a fenced code block:</p>\n'
            '<pre><code>Fenced code block\n'
            '</code></pre>'
        )

    def testSafeFence(self):
        """ Test Fenced Code with safe_mode. """
        text = '~~~\nCode\n~~~'
        self.md.safeMode = 'replace'
        self.assertEqual(
            self.md.convert(text),
            '<pre><code>Code\n'
            '</code></pre>'
        )

    def testNestedFence(self):
        """ Test nested fence. """

        text = '''
~~~~~~~~

~~~~
~~~~~~~~'''
        self.assertEqual(
            self.md.convert(text),
            '<pre><code>\n'
            '~~~~\n'
            '</code></pre>'
        )

    def testFencedLanguage(self):
        """ Test Language Tags. """

        text = '''
~~~~{.python}
# Some python code
~~~~'''
        self.assertEqual(
            self.md.convert(text),
            '<pre><code class="python"># Some python code\n'
            '</code></pre>'
        )

    def testFencedBackticks(self):
        """ Test Code Fenced with Backticks. """

        text = '''
`````
# Arbitrary code
~~~~~ # these tildes will not close the block
`````'''
        self.assertEqual(
            self.md.convert(text),
            '<pre><code># Arbitrary code\n'
            '~~~~~ # these tildes will not close the block\n'
            '</code></pre>'
        )

    def testFencedCodeWithHighlightLines(self):
        """ Test Fenced Code with Highlighted Lines. """

        text = '''
```hl_lines="1 3"
line 1
line 2
line 3
```'''
        md = markdown.Markdown(
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),
                'fenced_code'
            ]
        )

        if self.has_pygments:
            self.assertStartsWith(
                '<div class="codehilite"><pre><code><span class="hll"',
                md.convert(text).replace('<span></span>', '')
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code>line 1\n'
                'line 2\n'
                'line 3</code></pre>'
            )

    def testFencedLanguageAndHighlightLines(self):
        """ Test Fenced Code with Highlighted Lines. """

        text0 = '''
```.python hl_lines="1 3"
#line 1
#line 2
#line 3
```'''
        text1 = '''
~~~{.python hl_lines='1 3'}
#line 1
#line 2
#line 3
~~~'''
        for text in (text0, text1):
            md = markdown.Markdown(
                extensions=[
                    markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),
                    'fenced_code'
                ]
            )
            if self.has_pygments:
                self.assertStartsWith(
                    '<div class="codehilite"><pre><code><span class="hll"',
                    md.convert(text).replace('<span></span>', '')
                )
            else:
                self.assertEqual(
                    md.convert(text),
                    '<pre class="codehilite"><code class="language-python">#line 1\n'
                    '#line 2\n'
                    '#line 3</code></pre>'
                )

    def testFencedLanguageAndPygmentsDisabled(self):
        """ Test if fenced_code honors CodeHilite option use_pygments=False. """

        text = '```python\nfrom __future__ import braces\n```'
        md = markdown.Markdown(
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(use_pygments=False),
                'fenced_code'
            ]
        )
        self.assertIn('<code class="language-python">', md.convert(text))

    def testFencedLanguageDoubleEscape(self):
        """ Test entity escape logic in fences. """

        text = '```html\n<span>This&amp;That</span>\n```'
        md = markdown.Markdown(
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(),
                'fenced_code'
            ]
        )
        if self.has_pygments:
            self.assertEqual(
                md.convert(text),
                '<div class="codehilite"><pre>'
                '<span></span><code>'
                '<span class="p">&lt;</span><span class="nt">span</span><span class="p">&gt;</span>'
                'This<span class="ni">&amp;amp;</span>That'
                '<span class="p">&lt;/</span><span class="nt">span</span><span class="p">&gt;</span>'
                '\n</code></pre></div>'
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-html">'
                '&lt;span&gt;This&amp;amp;That&lt;/span&gt;'
                '</code></pre>'
            )

    def testFencedAmps(self):
        """ Test amp conversion. """

        text = '```text\n&\n&amp;\n&amp;amp;\n```'
        md = markdown.Markdown(
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(),
                'fenced_code'
            ]
        )
        if self.has_pygments:
            self.assertEqual(
                md.convert(text),
                '<div class="codehilite"><pre><span></span><code>&amp;\n&amp;amp;\n&amp;amp;amp;\n</code></pre></div>'
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-text">&amp;\n&amp;amp;\n&amp;amp;amp;</code></pre>'
            )


class TestMetaData(unittest.TestCase):
    """ Test MetaData extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['meta'])

    def testBasicMetaData(self):
        """ Test basic metadata. """

        text = '''Title: A Test Doc.
Author: Waylan Limberg
        John Doe
Blank_Data:

The body. This is paragraph one.'''
        self.assertEqual(
            self.md.convert(text),
            '<p>The body. This is paragraph one.</p>'
        )
        self.assertEqual(
            self.md.Meta, {
                'author': ['Waylan Limberg', 'John Doe'],
                'blank_data': [''],
                'title': ['A Test Doc.']
            }
        )

    def testYamlMetaData(self):
        """ Test metadata specified as simple YAML. """

        text = '''---
Title: A Test Doc.
Author: [Waylan Limberg, John Doe]
Blank_Data:
---

The body. This is paragraph one.'''
        self.assertEqual(
            self.md.convert(text),
            '<p>The body. This is paragraph one.</p>'
        )
        self.assertEqual(
            self.md.Meta, {
                'author': ['[Waylan Limberg, John Doe]'],
                'blank_data': [''],
                'title': ['A Test Doc.']
            }
        )

    def testMissingMetaData(self):
        """ Test document without Meta Data. """

        text = '    Some Code - not extra lines of meta data.'
        self.assertEqual(
            self.md.convert(text),
            '<pre><code>Some Code - not extra lines of meta data.\n'
            '</code></pre>'
        )
        self.assertEqual(self.md.Meta, {})

    def testMetaDataWithoutNewline(self):
        """ Test doocument with only metadata and no newline at end."""
        text = 'title: No newline'
        self.assertEqual(self.md.convert(text), '')
        self.assertEqual(self.md.Meta, {'title': ['No newline']})

    def testMetaDataReset(self):
        """ Test that reset call remove Meta entirely """

        text = '''Title: A Test Doc.
Author: Waylan Limberg
        John Doe
Blank_Data:

The body. This is paragraph one.'''
        self.md.convert(text)

        self.md.reset()
        self.assertEqual(self.md.Meta, {})


class TestWikiLinks(unittest.TestCase):
    """ Test Wikilinks Extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['wikilinks'])
        self.text = "Some text with a [[WikiLink]]."

    def testBasicWikilinks(self):
        """ Test [[wikilinks]]. """

        self.assertEqual(
            self.md.convert(self.text),
            '<p>Some text with a '
            '<a class="wikilink" href="/WikiLink/">WikiLink</a>.</p>'
        )

    def testWikilinkWhitespace(self):
        """ Test whitespace in wikilinks. """
        self.assertEqual(
            self.md.convert('[[ foo bar_baz ]]'),
            '<p><a class="wikilink" href="/foo_bar_baz/">foo bar_baz</a></p>'
        )
        self.assertEqual(
            self.md.convert('foo [[ ]] bar'),
            '<p>foo  bar</p>'
        )

    def testSimpleSettings(self):
        """ Test Simple Settings. """

        self.assertEqual(markdown.markdown(
            self.text, extensions=[
                markdown.extensions.wikilinks.WikiLinkExtension(
                    base_url='/wiki/',
                    end_url='.html',
                    html_class='foo')
                ]
            ),
            '<p>Some text with a '
            '<a class="foo" href="/wiki/WikiLink.html">WikiLink</a>.</p>')

    def testComplexSettings(self):
        """ Test Complex Settings. """

        md = markdown.Markdown(
            extensions=['wikilinks'],
            extension_configs={
                'wikilinks': [
                    ('base_url', 'http://example.com/'),
                    ('end_url', '.html'),
                    ('html_class', '')
                ]
            },
            safe_mode=True
        )
        self.assertEqual(
            md.convert(self.text),
            '<p>Some text with a '
            '<a href="http://example.com/WikiLink.html">WikiLink</a>.</p>'
        )

    def testWikilinksMetaData(self):
        """ test MetaData with Wikilinks Extension. """

        text = """wiki_base_url: http://example.com/
wiki_end_url:   .html
wiki_html_class:

Some text with a [[WikiLink]]."""
        md = markdown.Markdown(extensions=['meta', 'wikilinks'])
        self.assertEqual(
            md.convert(text),
            '<p>Some text with a '
            '<a href="http://example.com/WikiLink.html">WikiLink</a>.</p>'
        )

        # MetaData should not carry over to next document:
        self.assertEqual(
            md.convert("No [[MetaData]] here."),
            '<p>No <a class="wikilink" href="/MetaData/">MetaData</a> '
            'here.</p>'
        )

    def testURLCallback(self):
        """ Test used of a custom URL builder. """

        from markdown.extensions.wikilinks import WikiLinkExtension

        def my_url_builder(label, base, end):
            return '/bar/'

        md = markdown.Markdown(extensions=[WikiLinkExtension(build_url=my_url_builder)])
        self.assertEqual(
            md.convert('[[foo]]'),
            '<p><a class="wikilink" href="/bar/">foo</a></p>'
        )


class TestAdmonition(unittest.TestCase):
    """ Test Admonition Extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['admonition'])

    def testRE(self):
        RE = self.md.parser.blockprocessors['admonition'].RE
        tests = [
            ('!!! note', ('note', None)),
            ('!!! note "Please Note"', ('note', 'Please Note')),
            ('!!! note ""', ('note', '')),
        ]
        for test, expected in tests:
            self.assertEqual(RE.match(test).groups(), expected)


class TestTOC(TestCaseWithAssertStartsWith):
    """ Test TOC Extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['toc'])

    def testMarker(self):
        """ Test TOC with a Marker. """
        text = '[TOC]\n\n# Header 1\n\n## Header 2'
        self.assertEqual(
            self.md.convert(text),
            '<div class="toc">\n'
              '<ul>\n'                                             # noqa
                '<li><a href="#header-1">Header 1</a>'             # noqa
                  '<ul>\n'                                         # noqa
                    '<li><a href="#header-2">Header 2</a></li>\n'  # noqa
                  '</ul>\n'                                        # noqa
                '</li>\n'                                          # noqa
              '</ul>\n'                                            # noqa
            '</div>\n'
            '<h1 id="header-1">Header 1</h1>\n'
            '<h2 id="header-2">Header 2</h2>'
        )

    def testNoMarker(self):
        """ Test TOC without a Marker. """
        text = '# Header 1\n\n## Header 2'
        self.assertEqual(
            self.md.convert(text),
            '<h1 id="header-1">Header 1</h1>\n'
            '<h2 id="header-2">Header 2</h2>'
        )
        self.assertEqual(
            self.md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                             # noqa
                '<li><a href="#header-1">Header 1</a>'             # noqa
                  '<ul>\n'                                         # noqa
                    '<li><a href="#header-2">Header 2</a></li>\n'  # noqa
                  '</ul>\n'                                        # noqa
                '</li>\n'                                          # noqa
              '</ul>\n'                                            # noqa
            '</div>\n'
        )

    def testAlternateMarker(self):
        """ Test TOC with user defined marker. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(marker='{{marker}}')]
        )
        text = '{{marker}}\n\n# Header 1\n\n## Header 2'
        self.assertEqual(
            md.convert(text),
            '<div class="toc">\n'
              '<ul>\n'                                             # noqa
                '<li><a href="#header-1">Header 1</a>'             # noqa
                  '<ul>\n'                                         # noqa
                    '<li><a href="#header-2">Header 2</a></li>\n'  # noqa
                  '</ul>\n'                                        # noqa
                '</li>\n'                                          # noqa
              '</ul>\n'                                            # noqa
            '</div>\n'
            '<h1 id="header-1">Header 1</h1>\n'
            '<h2 id="header-2">Header 2</h2>'
        )

    def testDisabledMarker(self):
        """ Test TOC with disabled marker. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(marker='')]
        )
        text = '[TOC]\n\n# Header 1\n\n## Header 2'
        self.assertEqual(
            md.convert(text),
            '<p>[TOC]</p>\n'
            '<h1 id="header-1">Header 1</h1>\n'
            '<h2 id="header-2">Header 2</h2>'
        )
        self.assertStartsWith('<div class="toc">', md.toc)

    def testReset(self):
        """ Test TOC Reset. """
        self.assertEqual(self.md.toc, '')
        self.md.convert('# Header 1\n\n## Header 2')
        self.assertStartsWith('<div class="toc">', self.md.toc)
        self.md.reset()
        self.assertEqual(self.md.toc, '')
        self.assertEqual(self.md.toc_tokens, [])

    def testUniqueIds(self):
        """ Test Unique IDs. """

        text = '#Header\n#Header\n#Header'
        self.assertEqual(
            self.md.convert(text),
            '<h1 id="header">Header</h1>\n'
            '<h1 id="header_1">Header</h1>\n'
            '<h1 id="header_2">Header</h1>'
        )
        self.assertEqual(
            self.md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                       # noqa
                '<li><a href="#header">Header</a></li>\n'    # noqa
                '<li><a href="#header_1">Header</a></li>\n'  # noqa
                '<li><a href="#header_2">Header</a></li>\n'  # noqa
              '</ul>\n'                                      # noqa
            '</div>\n'
        )
        self.assertEqual(self.md.toc_tokens, [
            {'level': 1, 'id': 'header', 'name': 'Header', 'children': []},
            {'level': 1, 'id': 'header_1', 'name': 'Header', 'children': []},
            {'level': 1, 'id': 'header_2', 'name': 'Header', 'children': []},
        ])

    def testHtmlEntities(self):
        """ Test Headers with HTML Entities. """
        text = '# Foo &amp; bar'
        self.assertEqual(
            self.md.convert(text),
            '<h1 id="foo-bar">Foo &amp; bar</h1>'
        )
        self.assertEqual(
            self.md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                             # noqa
                '<li><a href="#foo-bar">Foo &amp; bar</a></li>\n'  # noqa
              '</ul>\n'                                            # noqa
            '</div>\n'
        )
        self.assertEqual(self.md.toc_tokens, [
            {'level': 1, 'id': 'foo-bar', 'name': 'Foo &amp; bar', 'children': []},
        ])

    def testHtmlSpecialChars(self):
        """ Test Headers with HTML special characters. """
        text = '# Foo > & bar'
        self.assertEqual(
            self.md.convert(text),
            '<h1 id="foo-bar">Foo &gt; &amp; bar</h1>'
        )
        self.assertEqual(
            self.md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                                  # noqa
                '<li><a href="#foo-bar">Foo &gt; &amp; bar</a></li>\n'  # noqa
              '</ul>\n'                                                 # noqa
            '</div>\n'
        )
        self.assertEqual(self.md.toc_tokens, [
            {'level': 1, 'id': 'foo-bar', 'name': 'Foo &gt; &amp; bar', 'children': []},
        ])

    def testRawHtml(self):
        """ Test Headers with raw HTML. """
        text = '# Foo <b>Bar</b> Baz.'
        self.assertEqual(
            self.md.convert(text),
            '<h1 id="foo-bar-baz">Foo <b>Bar</b> Baz.</h1>'
        )
        self.assertEqual(
            self.md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                                # noqa
                '<li><a href="#foo-bar-baz">Foo Bar Baz.</a></li>\n'  # noqa
              '</ul>\n'                                               # noqa
            '</div>\n'
        )
        self.assertEqual(self.md.toc_tokens, [
            {'level': 1, 'id': 'foo-bar-baz', 'name': 'Foo Bar Baz.', 'children': []},
        ])

    def testBaseLevel(self):
        """ Test Header Base Level. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(baselevel=5)]
        )
        text = '# Some Header\n\n## Next Level\n\n### Too High'
        self.assertEqual(
            md.convert(text),
            '<h5 id="some-header">Some Header</h5>\n'
            '<h6 id="next-level">Next Level</h6>\n'
            '<h6 id="too-high">Too High</h6>'
        )
        self.assertEqual(
            md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                                 # noqa
                '<li><a href="#some-header">Some Header</a>'           # noqa
                  '<ul>\n'                                             # noqa
                    '<li><a href="#next-level">Next Level</a></li>\n'  # noqa
                    '<li><a href="#too-high">Too High</a></li>\n'      # noqa
                  '</ul>\n'                                            # noqa
                '</li>\n'                                              # noqa
              '</ul>\n'                                                # noqa
            '</div>\n'
        )
        self.assertEqual(md.toc_tokens, [
            {'level': 5, 'id': 'some-header', 'name': 'Some Header', 'children': [
                {'level': 6, 'id': 'next-level', 'name': 'Next Level', 'children': []},
                {'level': 6, 'id': 'too-high', 'name': 'Too High', 'children': []},
            ]},
        ])

    def testHeaderInlineMarkup(self):
        """ Test Headers with inline markup. """

        text = '#Some *Header* with [markup](http://example.com).'
        self.assertEqual(
            self.md.convert(text),
            '<h1 id="some-header-with-markup">Some <em>Header</em> with '
            '<a href="http://example.com">markup</a>.</h1>'
        )
        self.assertEqual(
            self.md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                     # noqa
                '<li><a href="#some-header-with-markup">'  # noqa
                  'Some Header with markup.</a></li>\n'    # noqa
              '</ul>\n'                                    # noqa
            '</div>\n'
        )
        self.assertEqual(self.md.toc_tokens, [
            {'level': 1, 'id': 'some-header-with-markup', 'name': 'Some Header with markup.', 'children': []},
        ])

    def testAnchorLink(self):
        """ Test TOC Anchorlink. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(anchorlink=True)]
        )
        text = '# Header 1\n\n## Header *2*'
        self.assertEqual(
            md.convert(text),
            '<h1 id="header-1"><a class="toclink" href="#header-1">Header 1</a></h1>\n'
            '<h2 id="header-2"><a class="toclink" href="#header-2">Header <em>2</em></a></h2>'
        )

    def testAnchorLinkWithSingleInlineCode(self):
        """ Test TOC Anchorlink with single inline code. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(anchorlink=True)]
        )
        text = '# This is `code`.'
        self.assertEqual(
            md.convert(text),
            '<h1 id="this-is-code">'                        # noqa
                '<a class="toclink" href="#this-is-code">'  # noqa
                    'This is <code>code</code>.'            # noqa
                '</a>'                                      # noqa
            '</h1>'                                         # noqa
        )

    def testAnchorLinkWithDoubleInlineCode(self):
        """ Test TOC Anchorlink with double inline code. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(anchorlink=True)]
        )
        text = '# This is `code` and `this` too.'
        self.assertEqual(
            md.convert(text),
            '<h1 id="this-is-code-and-this-too">'                           # noqa
                '<a class="toclink" href="#this-is-code-and-this-too">'     # noqa
                    'This is <code>code</code> and <code>this</code> too.'  # noqa
                '</a>'                                                      # noqa
            '</h1>'                                                         # noqa
        )

    def testPermalink(self):
        """ Test TOC Permalink. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(permalink=True)]
        )
        text = '# Header'
        self.assertEqual(
            md.convert(text),
            '<h1 id="header">'                                                            # noqa
                'Header'                                                                  # noqa
                '<a class="headerlink" href="#header" title="Permanent link">&para;</a>'  # noqa
            '</h1>'                                                                       # noqa
        )

    def testPermalinkWithSingleInlineCode(self):
        """ Test TOC Permalink with single inline code. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(permalink=True)]
        )
        text = '# This is `code`.'
        self.assertEqual(
            md.convert(text),
            '<h1 id="this-is-code">'                                                            # noqa
                'This is <code>code</code>.'                                                    # noqa
                '<a class="headerlink" href="#this-is-code" title="Permanent link">&para;</a>'  # noqa
            '</h1>'                                                                             # noqa
        )

    def testPermalinkWithDoubleInlineCode(self):
        """ Test TOC Permalink with double inline code. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(permalink=True)]
        )
        text = '# This is `code` and `this` too.'
        self.assertEqual(
            md.convert(text),
            '<h1 id="this-is-code-and-this-too">'                                                            # noqa
                'This is <code>code</code> and <code>this</code> too.'                                       # noqa
                '<a class="headerlink" href="#this-is-code-and-this-too" title="Permanent link">&para;</a>'  # noqa
            '</h1>'                                                                                          # noqa
        )

    def testTitle(self):
        """ Test TOC Title. """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(title='Table of Contents')]
        )
        md.convert('# Header 1\n\n## Header 2')
        self.assertStartsWith(
            '<div class="toc"><span class="toctitle">Table of Contents</span><ul>',
            md.toc
        )

    def testWithAttrList(self):
        """ Test TOC with attr_list Extension. """
        md = markdown.Markdown(extensions=['toc', 'attr_list'])
        text = ('# Header 1\n\n'
                '## Header 2 { #foo }\n\n'
                '## Header 3 { data-toc-label="Foo Bar" }\n\n'
                '# Header 4 { data-toc-label="Foo > Baz" }\n\n'
                '# Header 5 { data-toc-label="Foo <b>Quux</b>" }')

        self.assertEqual(
            md.convert(text),
            '<h1 id="header-1">Header 1</h1>\n'
            '<h2 id="foo">Header 2</h2>\n'
            '<h2 id="header-3">Header 3</h2>\n'
            '<h1 id="header-4">Header 4</h1>\n'
            '<h1 id="header-5">Header 5</h1>'
        )
        self.assertEqual(
            md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                             # noqa
                '<li><a href="#header-1">Header 1</a>'             # noqa
                  '<ul>\n'                                         # noqa
                    '<li><a href="#foo">Header 2</a></li>\n'       # noqa
                    '<li><a href="#header-3">Foo Bar</a></li>\n'   # noqa
                  '</ul>\n'                                        # noqa
                '</li>\n'                                          # noqa
                '<li><a href="#header-4">Foo &gt; Baz</a></li>\n'  # noqa
                '<li><a href="#header-5">Foo Quux</a></li>\n'      # noqa
              '</ul>\n'                                            # noqa
            '</div>\n'
        )
        self.assertEqual(md.toc_tokens, [
            {'level': 1, 'id': 'header-1', 'name': 'Header 1', 'children': [
                {'level': 2, 'id': 'foo', 'name': 'Header 2', 'children': []},
                {'level': 2, 'id': 'header-3', 'name': 'Foo Bar', 'children': []}
            ]},
            {'level': 1, 'id': 'header-4', 'name': 'Foo &gt; Baz', 'children': []},
            {'level': 1, 'id': 'header-5', 'name': 'Foo Quux', 'children': []},
        ])

    def testUniqueFunc(self):
        """ Test 'unique' function. """
        from markdown.extensions.toc import unique
        ids = {'foo'}
        self.assertEqual(unique('foo', ids), 'foo_1')
        self.assertEqual(ids, {'foo', 'foo_1'})

    def testTocInHeaders(self):

        text = '[TOC]\n#[TOC]'
        self.assertEqual(
            self.md.convert(text),
            '<div class="toc">\n'                       # noqa
              '<ul>\n'                                  # noqa
                '<li><a href="#toc">[TOC]</a></li>\n'   # noqa
              '</ul>\n'                                 # noqa
            '</div>\n'                                  # noqa
            '<h1 id="toc">[TOC]</h1>'                   # noqa
        )

        text = '#[TOC]\n[TOC]'
        self.assertEqual(
            self.md.convert(text),
            '<h1 id="toc">[TOC]</h1>\n'                 # noqa
            '<div class="toc">\n'                       # noqa
              '<ul>\n'                                  # noqa
                '<li><a href="#toc">[TOC]</a></li>\n'   # noqa
              '</ul>\n'                                 # noqa
            '</div>'                                    # noqa
        )

        text = '[TOC]\n# *[TOC]*'
        self.assertEqual(
            self.md.convert(text),
            '<div class="toc">\n'                       # noqa
              '<ul>\n'                                  # noqa
                '<li><a href="#toc">[TOC]</a></li>\n'   # noqa
              '</ul>\n'                                 # noqa
            '</div>\n'                                  # noqa
            '<h1 id="toc"><em>[TOC]</em></h1>'          # noqa
        )

    def testMinMaxLevel(self):
        """ Test toc_height setting """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(toc_depth='3-4')]
        )
        text = '# Header 1 not in TOC\n\n## Header 2 not in TOC\n\n### Header 3\n\n####Header 4'
        self.assertEqual(
            md.convert(text),
            '<h1>Header 1 not in TOC</h1>\n'
            '<h2>Header 2 not in TOC</h2>\n'
            '<h3 id="header-3">Header 3</h3>\n'
            '<h4 id="header-4">Header 4</h4>'
        )
        self.assertEqual(
            md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                             # noqa
                '<li><a href="#header-3">Header 3</a>'             # noqa
                  '<ul>\n'                                         # noqa
                    '<li><a href="#header-4">Header 4</a></li>\n'  # noqa
                  '</ul>\n'                                        # noqa
                '</li>\n'                                          # noqa
              '</ul>\n'                                            # noqa
            '</div>\n'
        )

        self.assertNotIn("Header 1", md.toc)

    def testMaxLevel(self):
        """ Test toc_depth setting """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(toc_depth=2)]
        )
        text = '# Header 1\n\n## Header 2\n\n###Header 3 not in TOC'
        self.assertEqual(
            md.convert(text),
            '<h1 id="header-1">Header 1</h1>\n'
            '<h2 id="header-2">Header 2</h2>\n'
            '<h3>Header 3 not in TOC</h3>'
        )
        self.assertEqual(
            md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                             # noqa
                '<li><a href="#header-1">Header 1</a>'             # noqa
                  '<ul>\n'                                         # noqa
                    '<li><a href="#header-2">Header 2</a></li>\n'  # noqa
                  '</ul>\n'                                        # noqa
                '</li>\n'                                          # noqa
              '</ul>\n'                                            # noqa
            '</div>\n'
        )

        self.assertNotIn("Header 3", md.toc)

    def testMinMaxLevelwithBaseLevel(self):
        """ Test toc_height setting together with baselevel """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(toc_depth='4-6',
                                                             baselevel=3)]
        )
        text = '# First Header\n\n## Second Level\n\n### Third Level'
        self.assertEqual(
            md.convert(text),
            '<h3>First Header</h3>\n'
            '<h4 id="second-level">Second Level</h4>\n'
            '<h5 id="third-level">Third Level</h5>'
        )
        self.assertEqual(
            md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                                  # noqa
                '<li><a href="#second-level">Second Level</a>'          # noqa
                  '<ul>\n'                                              # noqa
                    '<li><a href="#third-level">Third Level</a></li>\n' # noqa
                  '</ul>\n'                                             # noqa
                '</li>\n'                                               # noqa
              '</ul>\n'                                                 # noqa
            '</div>\n'
        )
        self.assertNotIn("First Header", md.toc)

    def testMaxLevelwithBaseLevel(self):
        """ Test toc_depth setting together with baselevel """
        md = markdown.Markdown(
            extensions=[markdown.extensions.toc.TocExtension(toc_depth=3,
                                                             baselevel=2)]
        )
        text = '# Some Header\n\n## Next Level\n\n### Too High'
        self.assertEqual(
            md.convert(text),
            '<h2 id="some-header">Some Header</h2>\n'
            '<h3 id="next-level">Next Level</h3>\n'
            '<h4>Too High</h4>'
        )
        self.assertEqual(
            md.toc,
            '<div class="toc">\n'
              '<ul>\n'                                                 # noqa
                '<li><a href="#some-header">Some Header</a>'           # noqa
                  '<ul>\n'                                             # noqa
                    '<li><a href="#next-level">Next Level</a></li>\n'  # noqa
                  '</ul>\n'                                            # noqa
                '</li>\n'                                              # noqa
              '</ul>\n'                                                # noqa
            '</div>\n'
        )
        self.assertNotIn("Too High", md.toc)


class TestSmarty(unittest.TestCase):
    def setUp(self):
        config = {
            'smarty': [
                ('smart_angled_quotes', True),
                ('substitutions', {
                    'ndash': '\u2013',
                    'mdash': '\u2014',
                    'ellipsis': '\u2026',
                    'left-single-quote': '&sbquo;',  # sb is not a typo!
                    'right-single-quote': '&lsquo;',
                    'left-double-quote': '&bdquo;',
                    'right-double-quote': '&ldquo;',
                    'left-angle-quote': '[',
                    'right-angle-quote': ']',
                }),
            ]
        }
        self.md = markdown.Markdown(
            extensions=['smarty'],
            extension_configs=config
        )

    def testCustomSubstitutions(self):
        text = """<< The "Unicode char of the year 2014"
is the 'mdash': ---
Must not be confused with 'ndash'  (--) ... >>
"""
        correct = """<p>[ The &bdquo;Unicode char of the year 2014&ldquo;
is the &sbquo;mdash&lsquo;: \u2014
Must not be confused with &sbquo;ndash&lsquo;  (\u2013) \u2026 ]</p>"""
        self.assertEqual(self.md.convert(text), correct)
