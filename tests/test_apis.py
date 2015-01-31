#!/usr/bin/python
"""
Python-Markdown Regression Tests
================================

Tests of the various APIs with the python markdown lib.

"""

from __future__ import unicode_literals
import unittest
import sys
import os
import types
import markdown
import warnings
from markdown.__main__ import parse_options
from logging import DEBUG, WARNING, CRITICAL
import yaml
import tempfile

PY3 = sys.version_info[0] == 3


class TestMarkdownBasics(unittest.TestCase):
    """ Tests basics of the Markdown class. """

    def setUp(self):
        """ Create instance of Markdown. """
        self.md = markdown.Markdown()

    def testBlankInput(self):
        """ Test blank input. """
        self.assertEqual(self.md.convert(''), '')

    def testWhitespaceOnly(self):
        """ Test input of only whitespace. """
        self.assertEqual(self.md.convert(' '), '')

    def testSimpleInput(self):
        """ Test simple input. """
        self.assertEqual(self.md.convert('foo'), '<p>foo</p>')

    def testInstanceExtension(self):
        """ Test Extension loading with a class instance. """
        from markdown.extensions.footnotes import FootnoteExtension
        markdown.Markdown(extensions=[FootnoteExtension()])

    def testNamedExtension(self):
        """ Test Extension loading with Name (`path.to.module`). """
        markdown.Markdown(extensions=['markdown.extensions.footnotes'])

    def TestNamedExtensionWithClass(self):
        """ Test Extension loading with class name (`path.to.module:Class`). """
        markdown.Markdown(extensions=['markdown.extensions.footnotes:FootnoteExtension'])


class TestBlockParser(unittest.TestCase):
    """ Tests of the BlockParser class. """

    def setUp(self):
        """ Create instance of BlockParser. """
        self.parser = markdown.Markdown().parser

    def testParseChunk(self):
        """ Test BlockParser.parseChunk. """
        root = markdown.util.etree.Element("div")
        text = 'foo'
        self.parser.parseChunk(root, text)
        self.assertEqual(
            markdown.serializers.to_xhtml_string(root),
            "<div><p>foo</p></div>"
        )

    def testParseDocument(self):
        """ Test BlockParser.parseDocument. """
        lines = ['#foo', '', 'bar', '', '    baz']
        tree = self.parser.parseDocument(lines)
        self.assertTrue(isinstance(tree, markdown.util.etree.ElementTree))
        self.assertTrue(markdown.util.etree.iselement(tree.getroot()))
        self.assertEqual(
            markdown.serializers.to_xhtml_string(tree.getroot()),
            "<div><h1>foo</h1><p>bar</p><pre><code>baz\n</code></pre></div>"
        )


class TestBlockParserState(unittest.TestCase):
    """ Tests of the State class for BlockParser. """

    def setUp(self):
        self.state = markdown.blockparser.State()

    def testBlankState(self):
        """ Test State when empty. """
        self.assertEqual(self.state, [])

    def testSetSate(self):
        """ Test State.set(). """
        self.state.set('a_state')
        self.assertEqual(self.state, ['a_state'])
        self.state.set('state2')
        self.assertEqual(self.state, ['a_state', 'state2'])

    def testIsSate(self):
        """ Test State.isstate(). """
        self.assertEqual(self.state.isstate('anything'), False)
        self.state.set('a_state')
        self.assertEqual(self.state.isstate('a_state'), True)
        self.state.set('state2')
        self.assertEqual(self.state.isstate('state2'), True)
        self.assertEqual(self.state.isstate('a_state'), False)
        self.assertEqual(self.state.isstate('missing'), False)

    def testReset(self):
        """ Test State.reset(). """
        self.state.set('a_state')
        self.state.reset()
        self.assertEqual(self.state, [])
        self.state.set('state1')
        self.state.set('state2')
        self.state.reset()
        self.assertEqual(self.state, ['state1'])


class TestHtmlStash(unittest.TestCase):
    """ Test Markdown's HtmlStash. """

    def setUp(self):
        self.stash = markdown.util.HtmlStash()
        self.placeholder = self.stash.store('foo')

    def testSimpleStore(self):
        """ Test HtmlStash.store. """
        self.assertEqual(self.placeholder, self.stash.get_placeholder(0))
        self.assertEqual(self.stash.html_counter, 1)
        self.assertEqual(self.stash.rawHtmlBlocks, [('foo', False)])

    def testStoreMore(self):
        """ Test HtmlStash.store with additional blocks. """
        placeholder = self.stash.store('bar')
        self.assertEqual(placeholder, self.stash.get_placeholder(1))
        self.assertEqual(self.stash.html_counter, 2)
        self.assertEqual(
            self.stash.rawHtmlBlocks,
            [('foo', False), ('bar', False)]
        )

    def testSafeStore(self):
        """ Test HtmlStash.store with 'safe' html. """
        self.stash.store('bar', True)
        self.assertEqual(
            self.stash.rawHtmlBlocks,
            [('foo', False), ('bar', True)]
        )

    def testReset(self):
        """ Test HtmlStash.reset. """
        self.stash.reset()
        self.assertEqual(self.stash.html_counter, 0)
        self.assertEqual(self.stash.rawHtmlBlocks, [])

    def testUnsafeHtmlInSafeMode(self):
        """ Test that unsafe HTML gets escaped in safe_mode. """
        output = markdown.markdown('foo', extensions=[self.build_extension()], safe_mode='escape')
        self.assertEqual(output, '<p>&lt;script&gt;print(&quot;evil&quot;)&lt;/script&gt;</p>')

    def build_extension(self):
        """ Build an extention that addes unsafe html to Stash in same_mode. """
        class Unsafe(markdown.treeprocessors.Treeprocessor):
            def run(self, root):
                el = root.find('p')
                el.text = self.markdown.htmlStash.store('<script>print("evil")</script>', safe=False)
                return root

        class StoreUnsafeHtml(markdown.extensions.Extension):
            def extendMarkdown(self, md, md_globals):
                md.treeprocessors.add('unsafe', Unsafe(md), '_end')

        return StoreUnsafeHtml()


class TestOrderedDict(unittest.TestCase):
    """ Test OrderedDict storage class. """

    def setUp(self):
        self.odict = markdown.odict.OrderedDict()
        self.odict['first'] = 'This'
        self.odict['third'] = 'a'
        self.odict['fourth'] = 'self'
        self.odict['fifth'] = 'test'

    def testValues(self):
        """ Test output of OrderedDict.values(). """
        self.assertEqual(list(self.odict.values()), ['This', 'a', 'self', 'test'])

    def testKeys(self):
        """ Test output of OrderedDict.keys(). """
        self.assertEqual(
            list(self.odict.keys()),
            ['first', 'third', 'fourth', 'fifth']
        )

    def testItems(self):
        """ Test output of OrderedDict.items(). """
        self.assertEqual(
            list(self.odict.items()), [
                ('first', 'This'),
                ('third', 'a'),
                ('fourth', 'self'),
                ('fifth', 'test')
            ]
        )

    def testAddBefore(self):
        """ Test adding an OrderedDict item before a given key. """
        self.odict.add('second', 'is', '<third')
        self.assertEqual(
            list(self.odict.items()), [
                ('first', 'This'),
                ('second', 'is'),
                ('third', 'a'),
                ('fourth', 'self'),
                ('fifth', 'test')
            ]
        )

    def testAddAfter(self):
        """ Test adding an OrderDict item after a given key. """
        self.odict.add('second', 'is', '>first')
        self.assertEqual(
            list(self.odict.items()), [
                ('first', 'This'),
                ('second', 'is'),
                ('third', 'a'),
                ('fourth', 'self'),
                ('fifth', 'test')
            ]
        )

    def testAddAfterEnd(self):
        """ Test adding an OrderedDict item after the last key. """
        self.odict.add('sixth', '.', '>fifth')
        self.assertEqual(
            list(self.odict.items()), [
                ('first', 'This'),
                ('third', 'a'),
                ('fourth', 'self'),
                ('fifth', 'test'),
                ('sixth', '.')
            ]
        )

    def testAdd_begin(self):
        """ Test adding an OrderedDict item using "_begin". """
        self.odict.add('zero', 'CRAZY', '_begin')
        self.assertEqual(
            list(self.odict.items()), [
                ('zero', 'CRAZY'),
                ('first', 'This'),
                ('third', 'a'),
                ('fourth', 'self'),
                ('fifth', 'test')
            ]
        )

    def testAdd_end(self):
        """ Test adding an OrderedDict item using "_end". """
        self.odict.add('sixth', '.', '_end')
        self.assertEqual(
            list(self.odict.items()), [
                ('first', 'This'),
                ('third', 'a'),
                ('fourth', 'self'),
                ('fifth', 'test'),
                ('sixth', '.')
            ]
        )

    def testAddBadLocation(self):
        """ Test Error on bad location in OrderedDict.add(). """
        self.assertRaises(ValueError, self.odict.add, 'sixth', '.', '<seventh')
        self.assertRaises(ValueError, self.odict.add, 'second', 'is', 'third')

    def testDeleteItem(self):
        """ Test deletion of an OrderedDict item. """
        del self.odict['fourth']
        self.assertEqual(
            list(self.odict.items()),
            [('first', 'This'), ('third', 'a'), ('fifth', 'test')]
        )

    def testChangeValue(self):
        """ Test OrderedDict change value. """
        self.odict['fourth'] = 'CRAZY'
        self.assertEqual(
            list(self.odict.items()), [
                ('first', 'This'),
                ('third', 'a'),
                ('fourth', 'CRAZY'),
                ('fifth', 'test')
            ]
        )

    def testChangeOrder(self):
        """ Test OrderedDict change order. """
        self.odict.link('fourth', '<third')
        self.assertEqual(
            list(self.odict.items()), [
                ('first', 'This'),
                ('fourth', 'self'),
                ('third', 'a'),
                ('fifth', 'test')
            ]
        )

    def textBadLink(self):
        """ Test OrderedDict change order with bad location. """
        self.assertRaises(ValueError, self.odict.link('fourth', '<bad'))
        # Check for data integrity ("fourth" wasn't deleted).'
        self.assertEqual(
            list(self.odict.items()), [
                ('first', 'This'),
                ('third', 'a'),
                ('fourth', 'self'),
                ('fifth', 'test')
            ]
        )


class TestErrors(unittest.TestCase):
    """ Test Error Reporting. """

    def setUp(self):
        # Set warnings to be raised as errors
        warnings.simplefilter('error')

    def tearDown(self):
        # Reset warning behavior back to default
        warnings.simplefilter('default')

    def testNonUnicodeSource(self):
        """ Test falure on non-unicode source text. """
        if sys.version_info < (3, 0):
            source = "foo".encode('utf-16')
            self.assertRaises(UnicodeDecodeError, markdown.markdown, source)

    def testBadOutputFormat(self):
        """ Test failure on bad output_format. """
        self.assertRaises(KeyError, markdown.Markdown, output_format='invalid')

    def testLoadExtensionFailure(self):
        """ Test failure of an extension to load. """
        self.assertRaises(
            ImportError,
            markdown.Markdown, extensions=['non_existant_ext']
        )

    def testLoadBadExtension(self):
        """ Test loading of an Extension with no makeExtension function. """
        self.assertRaises(AttributeError, markdown.Markdown, extensions=['markdown.util'])

    def testNonExtension(self):
        """ Test loading a non Extension object as an extension. """
        self.assertRaises(TypeError, markdown.Markdown, extensions=[object])

    def testBaseExtention(self):
        """ Test that the base Extension class will raise NotImplemented. """
        self.assertRaises(
            NotImplementedError,
            markdown.Markdown, extensions=[markdown.extensions.Extension()]
        )

    def testMdxExtention(self):
        """ Test that prepending mdx_ raises a DeprecationWarning. """
        _create_fake_extension(name='fake', use_old_style=True)
        self.assertRaises(
            DeprecationWarning,
            markdown.Markdown, extensions=['fake']
        )

    def testShortNameExtention(self):
        """ Test that using a short name raises a DeprecationWarning. """
        self.assertRaises(
            DeprecationWarning,
            markdown.Markdown, extensions=['footnotes']
        )

    def testStringConfigExtention(self):
        """ Test that passing configs to an Extension in the name raises a DeprecationWarning. """
        self.assertRaises(
            DeprecationWarning,
            markdown.Markdown, extensions=['markdown.extension.footnotes(PLACE_MARKER=FOO)']
        )


def _create_fake_extension(name, has_factory_func=True, is_wrong_type=False, use_old_style=False):
    """ Create a fake extension module for testing. """
    if use_old_style:
        mod_name = '_'.join(['mdx', name])
    else:
        mod_name = name
    if not PY3:
        # mod_name must be bytes in Python 2.x
        mod_name = bytes(mod_name)
    ext_mod = types.ModuleType(mod_name)

    def makeExtension(*args, **kwargs):
        if is_wrong_type:
            return object
        else:
            return markdown.extensions.Extension(*args, **kwargs)

    if has_factory_func:
        ext_mod.makeExtension = makeExtension
    # Warning: this brute forces the extenson module onto the system. Either
    # this needs to be specificly overriden or a new python session needs to
    # be started to get rid of this. This should be ok in a testing context.
    sys.modules[mod_name] = ext_mod


class testETreeComments(unittest.TestCase):
    """
    Test that ElementTree Comments work.

    These tests should only be a concern when using cElementTree with third
    party serializers (including markdown's (x)html serializer). While markdown
    doesn't use ElementTree.Comment itself, we should certainly support any
    third party extensions which may. Therefore, these tests are included to
    ensure such support is maintained.
    """

    def setUp(self):
        # Create comment node
        self.comment = markdown.util.etree.Comment('foo')
        if hasattr(markdown.util.etree, 'test_comment'):
            self.test_comment = markdown.util.etree.test_comment
        else:
            self.test_comment = markdown.util.etree.Comment

    def testCommentIsComment(self):
        """ Test that an ElementTree Comment passes the `is Comment` test. """
        self.assertTrue(self.comment.tag is markdown.util.etree.test_comment)

    def testCommentIsBlockLevel(self):
        """ Test that an ElementTree Comment is recognized as BlockLevel. """
        self.assertFalse(markdown.util.isBlockLevel(self.comment.tag))

    def testCommentSerialization(self):
        """ Test that an ElementTree Comment serializes properly. """
        self.assertEqual(
            markdown.serializers.to_html_string(self.comment),
            '<!--foo-->'
        )

    def testCommentPrettify(self):
        """ Test that an ElementTree Comment is prettified properly. """
        pretty = markdown.treeprocessors.PrettifyTreeprocessor()
        pretty.run(self.comment)
        self.assertEqual(
            markdown.serializers.to_html_string(self.comment),
            '<!--foo-->\n'
        )


class testElementTailTests(unittest.TestCase):
    """ Element Tail Tests """
    def setUp(self):
        self.pretty = markdown.treeprocessors.PrettifyTreeprocessor()

    def testBrTailNoNewline(self):
        """ Test that last <br> in tree has a new line tail """
        root = markdown.util.etree.Element('root')
        br = markdown.util.etree.SubElement(root, 'br')
        self.assertEqual(br.tail, None)
        self.pretty.run(root)
        self.assertEqual(br.tail, "\n")


class testSerializers(unittest.TestCase):
    """ Test the html and xhtml serializers. """

    def testHtml(self):
        """ Test HTML serialization. """
        el = markdown.util.etree.Element('div')
        p = markdown.util.etree.SubElement(el, 'p')
        p.text = 'foo'
        markdown.util.etree.SubElement(el, 'hr')
        self.assertEqual(
            markdown.serializers.to_html_string(el),
            '<div><p>foo</p><hr></div>'
        )

    def testXhtml(self):
        """" Test XHTML serialization. """
        el = markdown.util.etree.Element('div')
        p = markdown.util.etree.SubElement(el, 'p')
        p.text = 'foo'
        markdown.util.etree.SubElement(el, 'hr')
        self.assertEqual(
            markdown.serializers.to_xhtml_string(el),
            '<div><p>foo</p><hr /></div>'
        )

    def testMixedCaseTags(self):
        """" Test preservation of tag case. """
        el = markdown.util.etree.Element('MixedCase')
        el.text = 'not valid '
        em = markdown.util.etree.SubElement(el, 'EMPHASIS')
        em.text = 'html'
        markdown.util.etree.SubElement(el, 'HR')
        self.assertEqual(
            markdown.serializers.to_xhtml_string(el),
            '<MixedCase>not valid <EMPHASIS>html</EMPHASIS><HR /></MixedCase>'
        )

    def buildExtension(self):
        """ Build an extension which registers fakeSerializer. """
        def fakeSerializer(elem):
            # Ignore input and return hardcoded output
            return '<div><p>foo</p></div>'

        class registerFakeSerializer(markdown.extensions.Extension):
            def extendMarkdown(self, md, md_globals):
                md.output_formats['fake'] = fakeSerializer

        return registerFakeSerializer()

    def testRegisterSerializer(self):
        self.assertEqual(
            markdown.markdown(
                'baz', extensions=[self.buildExtension()], output_format='fake'
            ),
            '<p>foo</p>'
        )


class testAtomicString(unittest.TestCase):
    """ Test that AtomicStrings are honored (not parsed). """

    def setUp(self):
        md = markdown.Markdown()
        self.inlineprocessor = md.treeprocessors['inline']

    def testString(self):
        """ Test that a regular string is parsed. """
        tree = markdown.util.etree.Element('div')
        p = markdown.util.etree.SubElement(tree, 'p')
        p.text = 'some *text*'
        new = self.inlineprocessor.run(tree)
        self.assertEqual(
            markdown.serializers.to_html_string(new),
            '<div><p>some <em>text</em></p></div>'
        )

    def testSimpleAtomicString(self):
        """ Test that a simple AtomicString is not parsed. """
        tree = markdown.util.etree.Element('div')
        p = markdown.util.etree.SubElement(tree, 'p')
        p.text = markdown.util.AtomicString('some *text*')
        new = self.inlineprocessor.run(tree)
        self.assertEqual(
            markdown.serializers.to_html_string(new),
            '<div><p>some *text*</p></div>'
        )

    def testNestedAtomicString(self):
        """ Test that a nested AtomicString is not parsed. """
        tree = markdown.util.etree.Element('div')
        p = markdown.util.etree.SubElement(tree, 'p')
        p.text = markdown.util.AtomicString('*some* ')
        span1 = markdown.util.etree.SubElement(p, 'span')
        span1.text = markdown.util.AtomicString('*more* ')
        span2 = markdown.util.etree.SubElement(span1, 'span')
        span2.text = markdown.util.AtomicString('*text* ')
        span3 = markdown.util.etree.SubElement(span2, 'span')
        span3.text = markdown.util.AtomicString('*here*')
        span3.tail = markdown.util.AtomicString(' *to*')
        span2.tail = markdown.util.AtomicString(' *test*')
        span1.tail = markdown.util.AtomicString(' *with*')
        new = self.inlineprocessor.run(tree)
        self.assertEqual(
            markdown.serializers.to_html_string(new),
            '<div><p>*some* <span>*more* <span>*text* <span>*here*</span> '
            '*to*</span> *test*</span> *with*</p></div>'
        )


class TestConfigParsing(unittest.TestCase):
    def assertParses(self, value, result):
        self.assertTrue(markdown.util.parseBoolValue(value, False) is result)

    def testBooleansParsing(self):
        self.assertParses(True, True)
        self.assertParses('novalue', None)
        self.assertParses('yES', True)
        self.assertParses('FALSE', False)
        self.assertParses(0., False)
        self.assertParses('none', False)

    def testPreserveNone(self):
        self.assertTrue(markdown.util.parseBoolValue('None', preserve_none=True) is None)
        self.assertTrue(markdown.util.parseBoolValue(None, preserve_none=True) is None)

    def testInvalidBooleansParsing(self):
        self.assertRaises(ValueError, markdown.util.parseBoolValue, 'novalue')


class TestCliOptionParsing(unittest.TestCase):
    """ Test parsing of Command Line Interface Options. """

    def setUp(self):
        self.default_options = {
            'input': None,
            'output': None,
            'encoding': None,
            'output_format': 'xhtml1',
            'lazy_ol': True,
            'extensions': [],
            'extension_configs': {},
        }
        self.tempfile = ''

    def tearDown(self):
        if os.path.isfile(self.tempfile):
            os.remove(self.tempfile)

    def testNoOptions(self):
        options, logging_level = parse_options([])
        self.assertEqual(options, self.default_options)
        self.assertEqual(logging_level, CRITICAL)

    def testQuietOption(self):
        options, logging_level = parse_options(['-q'])
        self.assertTrue(logging_level > CRITICAL)

    def testVerboseOption(self):
        options, logging_level = parse_options(['-v'])
        self.assertEqual(logging_level, WARNING)

    def testNoisyOption(self):
        options, logging_level = parse_options(['--noisy'])
        self.assertEqual(logging_level, DEBUG)

    def testInputFileOption(self):
        options, logging_level = parse_options(['foo.txt'])
        self.default_options['input'] = 'foo.txt'
        self.assertEqual(options, self.default_options)

    def testOutputFileOption(self):
        options, logging_level = parse_options(['-f', 'foo.html'])
        self.default_options['output'] = 'foo.html'
        self.assertEqual(options, self.default_options)

    def testInputAndOutputFileOptions(self):
        options, logging_level = parse_options(['-f', 'foo.html', 'foo.txt'])
        self.default_options['output'] = 'foo.html'
        self.default_options['input'] = 'foo.txt'
        self.assertEqual(options, self.default_options)

    def testEncodingOption(self):
        options, logging_level = parse_options(['-e', 'utf-8'])
        self.default_options['encoding'] = 'utf-8'
        self.assertEqual(options, self.default_options)

    def testSafeModeOption(self):
        options, logging_level = parse_options(['-s', 'escape'])
        self.default_options['safe_mode'] = 'escape'
        self.assertEqual(options, self.default_options)

    def testOutputFormatOption(self):
        options, logging_level = parse_options(['-o', 'html5'])
        self.default_options['output_format'] = 'html5'
        self.assertEqual(options, self.default_options)

    def testNoLazyOlOption(self):
        options, logging_level = parse_options(['-n'])
        self.default_options['lazy_ol'] = False
        self.assertEqual(options, self.default_options)

    def testExtensionOption(self):
        options, logging_level = parse_options(['-x', 'markdown.extensions.footnotes'])
        self.default_options['extensions'] = ['markdown.extensions.footnotes']
        self.assertEqual(options, self.default_options)

    def testMultipleExtensionOptions(self):
        options, logging_level = parse_options([
            '-x', 'markdown.extensions.footnotes',
            '-x', 'markdown.extensions.smarty'
        ])
        self.default_options['extensions'] = [
            'markdown.extensions.footnotes',
            'markdown.extensions.smarty'
        ]
        self.assertEqual(options, self.default_options)

    def create_config_file(self, config):
        """ Helper to create temp config files. """
        if not isinstance(config, markdown.util.string_type):
            # convert to string
            config = yaml.dump(config)
        fd, self.tempfile = tempfile.mkstemp('.yml')
        with os.fdopen(fd, 'w') as fp:
            fp.write(config)

    def testExtensionConfigOption(self):
        config = {
            'markdown.extensions.wikilinks': {
                'base_url': 'http://example.com/',
                'end_url': '.html',
                'html_class': 'test',
            },
            'markdown.extensions.footnotes:FootnotesExtension': {
                'PLACE_MARKER': '~~~footnotes~~~'
            }
        }
        self.create_config_file(config)
        options, logging_level = parse_options(['-c', self.tempfile])
        self.default_options['extension_configs'] = config
        self.assertEqual(options, self.default_options)

    def textBoolExtensionConfigOption(self):
        config = {
            'markdown.extensions.toc': {
                'title': 'Some Title',
                'anchorlink': True,
                'permalink': True
            }
        }
        self.create_config_file(config)
        options, logging_level = parse_options(['-c', self.tempfile])
        self.default_options['extension_configs'] = config
        self.assertEqual(options, self.default_options)

    def testExtensonConfigOptionAsJSON(self):
        config = {
            'markdown.extensions.wikilinks': {
                'base_url': 'http://example.com/',
                'end_url': '.html',
                'html_class': 'test',
            },
            'markdown.extensions.footnotes:FootnotesExtension': {
                'PLACE_MARKER': '~~~footnotes~~~'
            }
        }
        import json
        self.create_config_file(json.dumps(config))
        options, logging_level = parse_options(['-c', self.tempfile])
        self.default_options['extension_configs'] = config
        self.assertEqual(options, self.default_options)

    def testExtensonConfigOptionMissingFile(self):
        self.assertRaises(IOError, parse_options, ['-c', 'missing_file.yaml'])

    def testExtensonConfigOptionBadFormat(self):
        config = """
[footnotes]
PLACE_MARKER= ~~~footnotes~~~
"""
        self.create_config_file(config)
        self.assertRaises(yaml.YAMLError, parse_options, ['-c', self.tempfile])
