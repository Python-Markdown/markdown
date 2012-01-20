#!/usr/bin/python
"""
Python-Markdown Regression Tests
================================

Tests of the various APIs with the python markdown lib.

"""

import unittest
from doctest import DocTestSuite
import os
import sys
import types
import markdown
import warnings

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
        self.assertEqual(markdown.serializers.to_xhtml_string(root), 
                         "<div><p>foo</p></div>")

    def testParseDocument(self):
        """ Test BlockParser.parseDocument. """
        lines = ['#foo', '', 'bar', '', '    baz']
        tree = self.parser.parseDocument(lines)
        self.assertTrue(isinstance(tree, markdown.util.etree.ElementTree))
        self.assertTrue(markdown.util.etree.iselement(tree.getroot()))
        self.assertEqual(markdown.serializers.to_xhtml_string(tree.getroot()),
            "<div><h1>foo</h1><p>bar</p><pre><code>baz\n</code></pre></div>")


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
        self.assertEqual(self.stash.rawHtmlBlocks, 
                        [('foo', False), ('bar', False)])

    def testSafeStore(self):
        """ Test HtmlStash.store with 'safe' html. """
        self.stash.store('bar', True)
        self.assertEqual(self.stash.rawHtmlBlocks, 
                        [('foo', False), ('bar', True)])

    def testReset(self):
        """ Test HtmlStash.reset. """
        self.stash.reset()
        self.assertEqual(self.stash.html_counter, 0)
        self.assertEqual(self.stash.rawHtmlBlocks, [])

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
        self.assertEqual(self.odict.values(), ['This', 'a', 'self', 'test'])

    def testKeys(self):
        """ Test output of OrderedDict.keys(). """
        self.assertEqual(self.odict.keys(),
                    ['first', 'third', 'fourth', 'fifth'])

    def testItems(self):
        """ Test output of OrderedDict.items(). """
        self.assertEqual(self.odict.items(),
                    [('first', 'This'), ('third', 'a'), 
                    ('fourth', 'self'), ('fifth', 'test')])

    def testAddBefore(self):
        """ Test adding an OrderedDict item before a given key. """
        self.odict.add('second', 'is', '<third')
        self.assertEqual(self.odict.items(),
                    [('first', 'This'), ('second', 'is'), ('third', 'a'), 
                    ('fourth', 'self'), ('fifth', 'test')])

    def testAddAfter(self):
        """ Test adding an OrderDict item after a given key. """
        self.odict.add('second', 'is', '>first')
        self.assertEqual(self.odict.items(),
                    [('first', 'This'), ('second', 'is'), ('third', 'a'), 
                    ('fourth', 'self'), ('fifth', 'test')])

    def testAddAfterEnd(self):
        """ Test adding an OrderedDict item after the last key. """
        self.odict.add('sixth', '.', '>fifth')
        self.assertEqual(self.odict.items(),
                    [('first', 'This'), ('third', 'a'), 
                    ('fourth', 'self'), ('fifth', 'test'), ('sixth', '.')])

    def testAdd_begin(self):
        """ Test adding an OrderedDict item using "_begin". """
        self.odict.add('zero', 'CRAZY', '_begin')
        self.assertEqual(self.odict.items(),
                    [('zero', 'CRAZY'), ('first', 'This'), ('third', 'a'), 
                    ('fourth', 'self'), ('fifth', 'test')])

    def testAdd_end(self):
        """ Test adding an OrderedDict item using "_end". """
        self.odict.add('sixth', '.', '_end')
        self.assertEqual(self.odict.items(),
                    [('first', 'This'), ('third', 'a'), 
                    ('fourth', 'self'), ('fifth', 'test'), ('sixth', '.')])

    def testAddBadLocation(self):
        """ Test Error on bad location in OrderedDict.add(). """
        self.assertRaises(ValueError, self.odict.add, 'sixth', '.', '<seventh')
        self.assertRaises(ValueError, self.odict.add, 'second', 'is', 'third')

    def testDeleteItem(self):
        """ Test deletion of an OrderedDict item. """
        del self.odict['fourth']
        self.assertEqual(self.odict.items(),
                    [('first', 'This'), ('third', 'a'), ('fifth', 'test')])

    def testChangeValue(self):
        """ Test OrderedDict change value. """
        self.odict['fourth'] = 'CRAZY'
        self.assertEqual(self.odict.items(),
                    [('first', 'This'), ('third', 'a'), 
                    ('fourth', 'CRAZY'), ('fifth', 'test')])

    def testChangeOrder(self):
        """ Test OrderedDict change order. """
        self.odict.link('fourth', '<third')
        self.assertEqual(self.odict.items(),
                    [('first', 'This'), ('fourth', 'self'),
                    ('third', 'a'), ('fifth', 'test')])

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
        self.assertRaises(ValueError, 
                        markdown.Markdown, extensions=['non_existant_ext']) 

    def testLoadBadExtension(self):
        """ Test loading of an Extension with no makeExtension function. """
        _create_fake_extension(name='fake', has_factory_func=False)
        self.assertRaises(ValueError, markdown.Markdown, extensions=['fake'])

    def testNonExtension(self):
        """ Test loading a non Extension object as an extension. """
        _create_fake_extension(name='fake', is_wrong_type=True)
        self.assertRaises(ValueError, markdown.Markdown, extensions=['fake'])

    def testBaseExtention(self):
        """ Test that the base Extension class will raise NotImplemented. """
        _create_fake_extension(name='fake')
        self.assertRaises(NotImplementedError, 
                        markdown.Markdown, extensions=['fake'])


def _create_fake_extension(name, has_factory_func=True, is_wrong_type=False):
    """ Create a fake extension module for testing. """
    mod_name = '_'.join(['mdx', name])
    ext_mod = types.ModuleType(mod_name)
    def makeExtension(configs=None):
        if is_wrong_type:
            return object
        else:
            return markdown.extensions.Extension(configs=configs)
    if has_factory_func:
        ext_mod.makeExtension = makeExtension
    # Warning: this brute forces the extenson module onto the system. Either 
    # this needs to be specificly overriden or a new python session needs to 
    # be started to get rid of this. This should be ok in a testing context.
    sys.modules[mod_name] =  ext_mod


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
        self.assertEqual(markdown.serializers.to_html_string(self.comment),
                    '<!--foo-->')

    def testCommentPrettify(self):
        """ Test that an ElementTree Comment is prettified properly. """
        pretty = markdown.treeprocessors.PrettifyTreeprocessor()
        pretty.run(self.comment)
        self.assertEqual(markdown.serializers.to_html_string(self.comment),
                    '<!--foo-->\n')


class testAtomicString(unittest.TestCase):
    """ Test that AtomicStrings are honored (not parsed). """

    def setUp(self):
        md = markdown.Markdown()
        self.inlineprocessor = md.treeprocessors['inline']

    def testString(self):
        """ Test that a regular string is parsed. """
        tree = markdown.util.etree.Element('div')
        p = markdown.util.etree.SubElement(tree, 'p')
        p.text = u'some *text*'
        new = self.inlineprocessor.run(tree)
        self.assertEqual(markdown.serializers.to_html_string(new), 
                    '<div><p>some <em>text</em></p></div>')

    def testSimpleAtomicString(self):
        """ Test that a simple AtomicString is not parsed. """
        tree = markdown.util.etree.Element('div')
        p = markdown.util.etree.SubElement(tree, 'p')
        p.text = markdown.util.AtomicString(u'some *text*')
        new = self.inlineprocessor.run(tree)
        self.assertEqual(markdown.serializers.to_html_string(new), 
                    '<div><p>some *text*</p></div>')

    def testNestedAtomicString(self):
        """ Test that a nested AtomicString is not parsed. """
        tree = markdown.util.etree.Element('div')
        p = markdown.util.etree.SubElement(tree, 'p')
        p.text = markdown.util.AtomicString(u'*some* ')
        span1 = markdown.util.etree.SubElement(p, 'span')
        span1.text = markdown.util.AtomicString(u'*more* ')
        span2 = markdown.util.etree.SubElement(span1, 'span')
        span2.text = markdown.util.AtomicString(u'*text* ')
        span3 = markdown.util.etree.SubElement(span2, 'span')
        span3.text = markdown.util.AtomicString(u'*here*')
        span3.tail = markdown.util.AtomicString(u' *to*')
        span2.tail = markdown.util.AtomicString(u' *test*')
        span1.tail = markdown.util.AtomicString(u' *with*')
        new = self.inlineprocessor.run(tree)
        self.assertEqual(markdown.serializers.to_html_string(new), 
            '<div><p>*some* <span>*more* <span>*text* <span>*here*</span> '
            '*to*</span> *test*</span> *with*</p></div>')

