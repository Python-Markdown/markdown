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

Python-Markdown Extension Regression Tests
==========================================

A collection of regression tests to confirm that the included extensions
continue to work as advertised. This used to be accomplished by `doctests`.
"""

import unittest
import markdown


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
        # `self.ext.setConfig('bad', 'baz)` => `KeyError`
        self.assertRaises(KeyError, self.ext.setConfig, 'bad', 'baz')

    def testConfigAsKwargsOnInit(self):
        ext = self.ExtKlass(foo='baz', bar='blah')
        self.assertEqual(ext.getConfigs(), {'foo': 'baz', 'bar': 'blah'})


class TestMetaData(unittest.TestCase):
    """ Test `MetaData` extension. """

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
        """ Test document with only metadata and no newline at end."""
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
    """ Test `Wikilinks` Extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['wikilinks'])
        self.text = "Some text with a [[WikiLink]]."

    def testBasicWikilinks(self):
        """ Test `[[wikilinks]]`. """

        self.assertEqual(
            self.md.convert(self.text),
            '<p>Some text with a '
            '<a class="wikilink" href="/WikiLink/">WikiLink</a>.</p>'
        )

    def testWikilinkWhitespace(self):
        """ Test whitespace in `wikilinks`. """
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
        """ test `MetaData` with `Wikilinks` Extension. """

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

        # `MetaData` should not carry over to next document:
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


class TestSmarty(unittest.TestCase):
    def setUp(self):
        config = {
            'smarty': [
                ('smart_angled_quotes', True),
                ('substitutions', {
                    'ndash': '\u2013',
                    'mdash': '\u2014',
                    'ellipsis': '\u2026',
                    'left-single-quote': '&sbquo;',  # `sb` is not a typo!
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


class TestFootnotes(unittest.TestCase):
    """Test Footnotes Extension."""

    def setUp(self):
        self.md = markdown.Markdown(extensions=["footnotes"])

    def testBasicFootnote(self):
        """ Test basic footnote syntax. """
        text = "This is a footnote reference[^1].\n\n[^1]: This is the footnote."

        expected = (
            '<p>This is a footnote reference<sup id="fnref:1">'
            '<a class="footnote-ref" href="#fn:1">1</a></sup>.</p>\n'
            '<div class="footnote">\n'
            "<hr />\n"
            "<ol>\n"
            '<li id="fn:1">\n'
            "<p>This is the footnote.&#160;"
            '<a class="footnote-backref" href="#fnref:1" title="Jump back to '
            'footnote 1 in the text">&#8617;</a></p>\n'
            "</li>\n"
            "</ol>\n"
            "</div>"
        )

        self.assertEqual(self.md.convert(text), expected)

    def testFootnoteOrder(self):
        """ Test that footnotes are ordered correctly. """
        text = (
            "First footnote reference[^first]. Second footnote reference[^last].\n\n"
            "[^last]: Second footnote.\n[^first]: First footnote."
        )

        expected = (
            '<p>First footnote reference<sup id="fnref:first"><a class="footnote-ref" '
            'href="#fn:first">1</a></sup>. Second footnote reference<sup id="fnref:last">'
            '<a class="footnote-ref" href="#fn:last">2</a></sup>.</p>\n'
            '<div class="footnote">\n'
            "<hr />\n"
            "<ol>\n"
            '<li id="fn:first">\n'
            '<p>First footnote.&#160;<a class="footnote-backref" href="#fnref:first" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            "</li>\n"
            '<li id="fn:last">\n'
            '<p>Second footnote.&#160;<a class="footnote-backref" href="#fnref:last" '
            'title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            "</li>\n"
            "</ol>\n"
            "</div>"
        )

        self.assertEqual(self.md.convert(text), expected)

    def testFootnoteReferenceWithinCodeSpan(self):
        """ Test footnote reference within a code span. """

        text = "A `code span with a footnote[^1] reference`."
        expected = "<p>A <code>code span with a footnote[^1] reference</code>.</p>"

        self.assertEqual(self.md.convert(text), expected)

    def testFootnoteReferenceInLink(self):
        """ Test footnote reference within a link. """

        text = "A [link with a footnote[^1] reference](http://example.com)."
        expected = '<p>A <a href="http://example.com">link with a footnote[^1] reference</a>.</p>'

        self.assertEqual(self.md.convert(text), expected)

    def testDuplicateFootnoteReferences(self):
        """ Test multiple references to the same footnote. """
        text = "First[^dup] and second[^dup] reference.\n\n[^dup]: Duplicate footnote."

        expected = (
            '<p>First<sup id="fnref:dup">'
            '<a class="footnote-ref" href="#fn:dup">1</a></sup> and second<sup id="fnref2:dup">'
            '<a class="footnote-ref" href="#fn:dup">1</a></sup> reference.</p>\n'
            '<div class="footnote">\n'
            "<hr />\n"
            "<ol>\n"
            '<li id="fn:dup">\n'
            "<p>Duplicate footnote.&#160;"
            '<a class="footnote-backref" href="#fnref:dup" '
            'title="Jump back to footnote 1 in the text">&#8617;</a>'
            '<a class="footnote-backref" href="#fnref2:dup" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            "</li>\n"
            "</ol>\n"
            "</div>"
        )

        self.assertEqual(self.md.convert(text), expected)

    def testFootnoteReferenceWithoutDefinition(self):
        """ Test footnote reference without corresponding definition. """
        text = "This has a missing footnote[^missing]."
        expected = "<p>This has a missing footnote[^missing].</p>"

        self.assertEqual(self.md.convert(text), expected)

    def testFootnoteDefinitionWithoutReference(self):
        """ Test footnote definition without corresponding reference. """
        text = "No reference here.\n\n[^orphan]: Orphaned footnote."

        self.assertIn("fn:orphan", self.md.convert(text))

        # For the opposite behavior:
        # self.assertNotIn("fn:orphan", self.md.convert(text))

    def testMultilineFootnote(self):
        """ Test footnote definition spanning multiple lines. """

        text = (
            "Multi-line footnote[^multi].\n\n"
            "[^multi]: This is a footnote\n"
            "    that spans multiple lines\n"
            "    with proper indentation."
        )

        expected = (
            '<p>Multi-line footnote<sup id="fnref:multi"><a class="footnote-ref" href="#fn:multi">1</a></sup>.</p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:multi">\n'
            '<p>This is a footnote\n'
            'that spans multiple lines\n'
            'with proper indentation.&#160;<a class="footnote-backref" href="#fnref:multi" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>'
        )
        self.assertEqual(self.md.convert(text), expected)

    def testFootnoteInBlockquote(self):
        """ Test footnote reference within a blockquote. """
        text = "> This is a quote with a footnote[^quote].\n\n[^quote]: Quote footnote."

        result = self.md.convert(text)
        self.assertIn("<blockquote>", result)
        self.assertIn("fnref:quote", result)

    def testFootnoteInList(self):
        """ Test footnote reference within a list item. """
        text = "1. First item with footnote[^note]\n1. Second item\n\n[^note]: List footnote."

        result = self.md.convert(text)
        self.assertIn("<ol>", result)
        self.assertIn("fnref:note", result)

    def testNestedFootnotes(self):
        """ Test footnote definition containing another footnote reference. """
        text = (
            "Main footnote[^main].\n\n"
            "[^main]: This footnote references another[^nested].\n"
            "[^nested]: Nested footnote."
        )
        result = self.md.convert(text)

        self.assertIn("fnref:main", result)
        self.assertIn("fnref:nested", result)
        self.assertIn("fn:main", result)
        self.assertIn("fn:nested", result)

    def testFootnoteReset(self):
        """ Test that footnotes are properly reset between documents. """
        text1 = "First doc[^1].\n\n[^1]: First footnote."
        text2 = "Second doc[^1].\n\n[^1]: Different footnote."

        result1 = self.md.convert(text1)
        self.md.reset()
        result2 = self.md.convert(text2)

        self.assertIn("First footnote", result1)
        self.assertIn("Different footnote", result2)
        self.assertNotIn("Different footnote", result1)

    def testFootnoteIdWithSpecialChars(self):
        """ Test footnote id containing special and unicode characters. """
        text = "Unicode footnote id[^!#¤%/()=?+}{§øé].\n\n[^!#¤%/()=?+}{§øé]: Footnote with unicode id."

        self.assertIn("fnref:!#¤%/()=?+}{§øé", self.md.convert(text))

    def testFootnoteRefInHtml(self):
        """ Test footnote reference within HTML tags. """
        text = "A <span>footnote reference[^1] in an HTML</span>.\n\n[^1]: The footnote."

        self.assertIn("fnref:1", self.md.convert(text))

    def testFootnoteWithHtmlAndMarkdown(self):
        """ Test footnote containing HTML and markdown elements. """
        text = "A footnote with style[^html].\n\n[^html]: Has *emphasis* and <strong>bold</strong>."

        result = self.md.convert(text)
        self.assertIn("<em>emphasis</em>", result)
        self.assertIn("<strong>bold</strong>", result)
