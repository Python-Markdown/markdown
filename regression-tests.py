#!/usr/bin/python
"""
Python-Markdown Regression Tests
================================

Tests of the various APIs with the python markdown lib.

"""

import unittest
from doctest import DocTestSuite
import os
import markdown

class TestMarkdown(unittest.TestCase):
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
        root = markdown.etree.Element("div")
        text = 'foo'
        self.parser.parseChunk(root, text)
        self.assertEqual(markdown.etree.tostring(root), "<div><p>foo</p></div>")

    def testParseDocument(self):
        """ Test BlockParser.parseDocument. """
        lines = ['#foo', '', 'bar', '', '    baz']
        tree = self.parser.parseDocument(lines)
        self.assert_(isinstance(tree, markdown.etree.ElementTree))
        self.assert_(markdown.etree.iselement(tree.getroot()))
        self.assertEqual(markdown.etree.tostring(tree.getroot()),
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
        self.stash = markdown.preprocessors.HtmlStash()
        self.placeholder = self.stash.store('foo')

    def testSimpleStore(self):
        """ Test HtmlStash.store. """
        self.assertEqual(self.placeholder, 
                         markdown.preprocessors.HTML_PLACEHOLDER % 0)
        self.assertEqual(self.stash.html_counter, 1)
        self.assertEqual(self.stash.rawHtmlBlocks, [('foo', False)])

    def testStoreMore(self):
        """ Test HtmlStash.store with additional blocks. """
        placeholder = self.stash.store('bar')
        self.assertEqual(placeholder, 
                         markdown.preprocessors.HTML_PLACEHOLDER % 1)
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

def suite():
    """ Build a test suite of the above tests and extension doctests. """
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMarkdown))
    suite.addTest(unittest.makeSuite(TestBlockParser))
    suite.addTest(unittest.makeSuite(TestBlockParserState))
    suite.addTest(unittest.makeSuite(TestHtmlStash))
    suite.addTest(unittest.makeSuite(TestOrderedDict))

    for filename in os.listdir('markdown/extensions'):
        if filename.endswith('.py'):
            module = 'markdown.extensions.%s' % filename[:-3]
            try:
                suite.addTest(DocTestSuite(module))
            except: ValueError
                # No tests
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
