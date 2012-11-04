"""
Python-Markdown Extension Regression Tests
==========================================

A collection of regression tests to confirm that the included extensions 
continue to work as advertised. This used to be accomplished by doctests.

"""

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

class TestCodeHilite(unittest.TestCase):
    """ Test codehilite extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['codehilite'])

        self.has_pygments = True
        try:
            import pygments
        except ImportError:
            self.has_pygments = False

    def testBasicCodeHilite(self):
        text = '\t# A Code Comment'
        if self.has_pygments:
            self.assertEqual(self.md.convert(text),
                '<div class="codehilite">'
                '<pre><span class="c"># A Code Comment</span>\n'
                '</pre></div>')
        else:
            self.assertEqual(self.md.convert(text),
                '<pre class="codehilite"><code># A Code Comment'
                '</code></pre>')


class TestFencedCode(unittest.TestCase):
    """ Test fenced_code extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['fenced_code'])

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

class TestHeaderId(unittest.TestCase):
    """ Test HeaderId Extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['headerid'])

    def testBasicHeaderId(self):
        """ Test Basic HeaderID """
    
        text = "# Some Header #"
        self.assertEqual(self.md.convert(text),
            '<h1 id="some-header">Some Header</h1>')

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

