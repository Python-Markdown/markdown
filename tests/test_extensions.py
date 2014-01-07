"""
Python-Markdown Extension Regression Tests
==========================================

A collection of regression tests to confirm that the included extensions
continue to work as advertised. This used to be accomplished by doctests.

"""

from __future__ import unicode_literals
import unittest
import markdown

class TestAbbr(unittest.TestCase):
    """ Test abbr extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['abbr'])

    def testSimpleAbbr(self):
        """ Test Abbreviations. """
        text = 'Some text with an ABBR and a REF. Ignore REFERENCE and ref.' + \
               '\n\n*[ABBR]: Abbreviation\n' + \
               '*[REF]: Abbreviation Reference'
        self.assertEqual(self.md.convert(text),
            '<p>Some text with an <abbr title="Abbreviation">ABBR</abbr> '
            'and a <abbr title="Abbreviation Reference">REF</abbr>. Ignore '
            'REFERENCE and ref.</p>')

    def testNestedAbbr(self):
        """ Test Nested Abbreviations. """
        text = '[ABBR](/foo) and _ABBR_\n\n' + \
               '*[ABBR]: Abreviation'
        self.assertEqual(self.md.convert(text),
            '<p><a href="/foo"><abbr title="Abreviation">ABBR</abbr></a> '
            'and <em><abbr title="Abreviation">ABBR</abbr></em></p>')


class TestCodeHilite(unittest.TestCase):
    """ Test codehilite extension. """

    def setUp(self):
        self.has_pygments = True
        try:
            import pygments
        except ImportError:
            self.has_pygments = False

    def testBasicCodeHilite(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(extensions=['codehilite'])
        if self.has_pygments:
            self.assertEqual(md.convert(text),
                '<div class="codehilite">'
                '<pre><span class="c"># A Code Comment</span>\n'
                '</pre></div>')
        else:
            self.assertEqual(md.convert(text),
                '<pre class="codehilite"><code># A Code Comment'
                '</code></pre>')
    
    def testLinenumsTrue(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(extensions=['codehilite(linenums=True)'])
        if self.has_pygments:
            # Differant versions of pygments output slightly different markup.
            # So we use 'startwith' and test just enough to confirm that 
            # pygments received and processed linenums.
            self.assertTrue(md.convert(text).startswith(
                '<table class="codehilitetable"><tr><td class="linenos">'))
        else:
            self.assertEqual(md.convert(text),
                '<pre class="codehilite"><code class="linenums"># A Code Comment'
                '</code></pre>')

    def testLinenumsFalse(self):
        text = '\t#!Python\n\t# A Code Comment'
        md = markdown.Markdown(extensions=['codehilite(linenums=False)'])
        if self.has_pygments:
            self.assertEqual(md.convert(text),
                '<div class="codehilite">'
                '<pre><span class="c"># A Code Comment</span>\n'
                '</pre></div>')
        else:
            self.assertEqual(md.convert(text),
                '<pre class="codehilite"><code class="language-python"># A Code Comment'
                '</code></pre>')

    def testLinenumsNone(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(extensions=['codehilite(linenums=None)'])
        if self.has_pygments:
            self.assertEqual(md.convert(text),
                '<div class="codehilite">'
                '<pre><span class="c"># A Code Comment</span>\n'
                '</pre></div>')
        else:
            self.assertEqual(md.convert(text),
                '<pre class="codehilite"><code># A Code Comment'
                '</code></pre>')

    def testLinenumsNoneWithShebang(self):
        text = '\t#!Python\n\t# A Code Comment'
        md = markdown.Markdown(extensions=['codehilite(linenums=None)'])
        if self.has_pygments:
            # Differant versions of pygments output slightly different markup.
            # So we use 'startwith' and test just enough to confirm that 
            # pygments received and processed linenums.
            self.assertTrue(md.convert(text).startswith(
                '<table class="codehilitetable"><tr><td class="linenos">'))
        else:
            self.assertEqual(md.convert(text),
                '<pre class="codehilite"><code class="language-python linenums"># A Code Comment'
                '</code></pre>')

    def testLinenumsNoneWithColon(self):
        text = '\t:::Python\n\t# A Code Comment'
        md = markdown.Markdown(extensions=['codehilite(linenums=None)'])
        if self.has_pygments:
            self.assertEqual(md.convert(text),
                '<div class="codehilite">'
                '<pre><span class="c"># A Code Comment</span>\n'
                '</pre></div>')
        else:
            self.assertEqual(md.convert(text),
                '<pre class="codehilite"><code class="language-python"># A Code Comment'
                '</code></pre>')

    def testHighlightLinesWithColon(self):
        # Test with hl_lines delimited by single or double quotes.
        text0 = '\t:::Python hl_lines="2"\n\t#line 1\n\t#line 2\n\t#line 3'
        text1 = "\t:::Python hl_lines='2'\n\t#line 1\n\t#line 2\n\t#line 3"

        for text in (text0, text1):
            md = markdown.Markdown(extensions=['codehilite'])
            if self.has_pygments:
                self.assertEqual(md.convert(text),
                    '<div class="codehilite"><pre>'
                    '<span class="c">#line 1</span>\n'
                    '<span class="hll"><span class="c">#line 2</span>\n</span>'
                    '<span class="c">#line 3</span>\n'
                    '</pre></div>')
            else:
                self.assertEqual(md.convert(text),
                    '<pre class="codehilite">'
                    '<code class="language-python">#line 1\n'
                    '#line 2\n'
                    '#line 3</code></pre>')

class TestFencedCode(unittest.TestCase):
    """ Test fenced_code extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['fenced_code'])
        self.has_pygments = True
        try:
            import pygments
        except ImportError:
            self.has_pygments = False

    def testBasicFence(self):
        """ Test Fenced Code Blocks. """
        text = '''
A paragraph before a fenced code block:

~~~
Fenced code block
~~~'''
        self.assertEqual(self.md.convert(text),
            '<p>A paragraph before a fenced code block:</p>\n'
            '<pre><code>Fenced code block\n'
            '</code></pre>')

    def testSafeFence(self):
        """ Test Fenced Code with safe_mode. """
        text = '~~~\nCode\n~~~'
        self.md.safeMode = 'replace'
        self.assertEqual(self.md.convert(text),
            '<pre><code>Code\n'
            '</code></pre>')

    def testNestedFence(self):
        """ Test nested fence. """

        text = '''
~~~~~~~~

~~~~
~~~~~~~~'''
        self.assertEqual(self.md.convert(text),
            '<pre><code>\n'
            '~~~~\n'
            '</code></pre>')

    def testFencedLanguage(self):
        """ Test Language Tags. """

        text = '''
~~~~{.python}
# Some python code
~~~~'''
        self.assertEqual(self.md.convert(text),
            '<pre><code class="python"># Some python code\n'
            '</code></pre>')

    def testFencedBackticks(self):
        """ Test Code Fenced with Backticks. """

        text = '''
`````
# Arbitrary code
~~~~~ # these tildes will not close the block
`````'''
        self.assertEqual(self.md.convert(text),
        '<pre><code># Arbitrary code\n'
        '~~~~~ # these tildes will not close the block\n'
        '</code></pre>')

    def testFencedCodeWithHighlightLines(self):
        """ Test Fenced Code with Highlighted Lines. """

        text = '''
```hl_lines="1 3"
line 1
line 2
line 3
```'''
        md = markdown.Markdown(extensions=[
            'codehilite(linenums=None,guess_lang=False)',
            'fenced_code'])

        if self.has_pygments:
            self.assertEqual(md.convert(text),
                '<div class="codehilite"><pre>'
                '<span class="hll">line 1\n</span>'
                'line 2\n'
                '<span class="hll">line 3\n</span>'
                '</pre></div>')
        else:
            self.assertEqual(md.convert(text),
                '<pre class="codehilite"><code>line 1\n'
                'line 2\n'
                'line 3</code></pre>')

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
            md = markdown.Markdown(extensions=[
                'codehilite(linenums=None,guess_lang=False)',
                'fenced_code'])

            if self.has_pygments:
                self.assertEqual(md.convert(text),
                    '<div class="codehilite"><pre>'
                    '<span class="hll"><span class="c">#line 1</span>\n</span>'
                    '<span class="c">#line 2</span>\n'
                    '<span class="hll"><span class="c">#line 3</span>\n</span>'
                    '</pre></div>')
            else:
                self.assertEqual(md.convert(text),
                    '<pre class="codehilite"><code class="language-python">#line 1\n'
                    '#line 2\n'
                    '#line 3</code></pre>')

class TestHeaderId(unittest.TestCase):
    """ Test HeaderId Extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['headerid'])

    def testBasicHeaderId(self):
        """ Test Basic HeaderID """

        text = "# Some Header #"
        self.assertEqual(self.md.convert(text),
            '<h1 id="some-header">Some Header</h1>')

    def testUniqueFunc(self):
        """ Test 'unique' function. """
        from markdown.extensions.headerid import unique
        ids = set(['foo'])
        self.assertEqual(unique('foo', ids), 'foo_1')
        self.assertEqual(ids, set(['foo', 'foo_1']))

    def testUniqueIds(self):
        """ Test Unique IDs. """

        text = '#Header\n#Header\n#Header'
        self.assertEqual(self.md.convert(text),
            '<h1 id="header">Header</h1>\n'
            '<h1 id="header_1">Header</h1>\n'
            '<h1 id="header_2">Header</h1>')

    def testBaseLevel(self):
        """ Test Header Base Level. """

        text = '#Some Header\n## Next Level'
        self.assertEqual(markdown.markdown(text, ['headerid(level=3)']),
            '<h3 id="some-header">Some Header</h3>\n'
            '<h4 id="next-level">Next Level</h4>')

    def testHeaderInlineMarkup(self):
        """ Test Header IDs with inline markup. """

        text = '#Some *Header* with [markup](http://example.com).'
        self.assertEqual(self.md.convert(text),
            '<h1 id="some-header-with-markup">Some <em>Header</em> with '
            '<a href="http://example.com">markup</a>.</h1>')

    def testHtmlEntities(self):
        """ Test HeaderIDs with HTML Entities. """
        text = '# Foo &amp; bar'
        self.assertEqual(self.md.convert(text),
            '<h1 id="foo-bar">Foo &amp; bar</h1>')

    def testRawHtml(self):
        """ Test HeaderIDs with raw HTML. """
        text = '# Foo <b>Bar</b> Baz.'
        self.assertEqual(self.md.convert(text),
            '<h1 id="foo-bar-baz">Foo <b>Bar</b> Baz.</h1>')

    def testNoAutoIds(self):
        """ Test HeaderIDs with no auto generated IDs. """

        text = '# Some Header\n# Another Header'
        self.assertEqual(markdown.markdown(text, ['headerid(forceid=False)']),
            '<h1>Some Header</h1>\n'
            '<h1>Another Header</h1>')

    def testHeaderIdWithMetaData(self):
        """ Test Header IDs with MetaData extension. """

        text = '''header_level: 2
header_forceid: Off

# A Header'''
        self.assertEqual(markdown.markdown(text, ['headerid', 'meta']),
            '<h2>A Header</h2>')

    def testHeaderIdWithAttr_List(self):
        """ Test HeaderIDs with Attr_List extension. """
        
        text = '# Header1 {: #foo }\n# Header2 {: .bar }'
        self.assertEqual(markdown.markdown(text, ['headerid', 'attr_list']),
            '<h1 id="foo">Header1</h1>\n'
            '<h1 class="bar" id="header2">Header2</h1>')
        # Switch order extensions are loaded - should be no change in behavior.
        self.assertEqual(markdown.markdown(text, ['attr_list', 'headerid']),
            '<h1 id="foo">Header1</h1>\n'
            '<h1 class="bar" id="header2">Header2</h1>')

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
        self.assertEqual(self.md.convert(text),
            '<p>The body. This is paragraph one.</p>')
        self.assertEqual(self.md.Meta,
            {'author': ['Waylan Limberg', 'John Doe'],
             'blank_data': [''],
             'title': ['A Test Doc.']})

    def testMissingMetaData(self):
        """ Test document without Meta Data. """

        text = '    Some Code - not extra lines of meta data.'
        self.assertEqual(self.md.convert(text),
            '<pre><code>Some Code - not extra lines of meta data.\n'
            '</code></pre>')
        self.assertEqual(self.md.Meta, {})

    def testMetaDataWithoutNewline(self):
        """ Test doocument with only metadata and no newline at end."""
        text = 'title: No newline'
        self.assertEqual(self.md.convert(text), '')
        self.assertEqual(self.md.Meta, {'title': ['No newline']})


class TestWikiLinks(unittest.TestCase):
    """ Test Wikilinks Extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['wikilinks'])
        self.text = "Some text with a [[WikiLink]]."

    def testBasicWikilinks(self):
        """ Test [[wikilinks]]. """

        self.assertEqual(self.md.convert(self.text),
            '<p>Some text with a '
            '<a class="wikilink" href="/WikiLink/">WikiLink</a>.</p>')

    def testWikilinkWhitespace(self):
        """ Test whitespace in wikilinks. """
        self.assertEqual(self.md.convert('[[ foo bar_baz ]]'),
            '<p><a class="wikilink" href="/foo_bar_baz/">foo bar_baz</a></p>')
        self.assertEqual(self.md.convert('foo [[ ]] bar'),
            '<p>foo  bar</p>')

    def testSimpleSettings(self):
        """ Test Simple Settings. """

        self.assertEqual(markdown.markdown(self.text,
            ['wikilinks(base_url=/wiki/,end_url=.html,html_class=foo)']),
            '<p>Some text with a '
            '<a class="foo" href="/wiki/WikiLink.html">WikiLink</a>.</p>')

    def testComplexSettings(self):
        """ Test Complex Settings. """

        md = markdown.Markdown(
            extensions = ['wikilinks'],
            extension_configs = {'wikilinks': [
                                        ('base_url', 'http://example.com/'),
                                        ('end_url', '.html'),
                                        ('html_class', '') ]},
            safe_mode = True)
        self.assertEqual(md.convert(self.text),
            '<p>Some text with a '
            '<a href="http://example.com/WikiLink.html">WikiLink</a>.</p>')

    def testWikilinksMetaData(self):
        """ test MetaData with Wikilinks Extension. """

        text = """wiki_base_url: http://example.com/
wiki_end_url:   .html
wiki_html_class:

Some text with a [[WikiLink]]."""
        md = markdown.Markdown(extensions=['meta', 'wikilinks'])
        self.assertEqual(md.convert(text),
            '<p>Some text with a '
            '<a href="http://example.com/WikiLink.html">WikiLink</a>.</p>')

        # MetaData should not carry over to next document:
        self.assertEqual(md.convert("No [[MetaData]] here."),
            '<p>No <a class="wikilink" href="/MetaData/">MetaData</a> '
            'here.</p>')

    def testURLCallback(self):
        """ Test used of a custom URL builder. """

        def my_url_builder(label, base, end):
            return '/bar/'
        md = markdown.Markdown(extensions=['wikilinks'],
            extension_configs={'wikilinks' : [('build_url', my_url_builder)]})
        self.assertEqual(md.convert('[[foo]]'),
            '<p><a class="wikilink" href="/bar/">foo</a></p>')

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

class TestTOC(unittest.TestCase):
    """ Test TOC Extension. """
    
    def setUp(self):
        self.md = markdown.Markdown(extensions=['toc'])

    def testMarker(self):
        """ Test TOC with a Marker. """
        text = '[TOC]\n\n# Header 1\n\n## Header 2'
        self.assertEqual(self.md.convert(text),
            '<div class="toc">\n'
              '<ul>\n'
                '<li><a href="#header-1">Header 1</a>'
                  '<ul>\n'
                    '<li><a href="#header-2">Header 2</a></li>\n'
                  '</ul>\n'
                '</li>\n'
              '</ul>\n'
            '</div>\n'
            '<h1 id="header-1">Header 1</h1>\n'
            '<h2 id="header-2">Header 2</h2>')
    
    def testNoMarker(self):
        """ Test TOC without a Marker. """
        text = '# Header 1\n\n## Header 2'
        self.assertEqual(self.md.convert(text),
            '<h1 id="header-1">Header 1</h1>\n'
            '<h2 id="header-2">Header 2</h2>')
        self.assertEqual(self.md.toc,
            '<div class="toc">\n'
              '<ul>\n'
                '<li><a href="#header-1">Header 1</a>'
                  '<ul>\n'
                    '<li><a href="#header-2">Header 2</a></li>\n'
                  '</ul>\n'
                '</li>\n'
              '</ul>\n'
            '</div>\n')
