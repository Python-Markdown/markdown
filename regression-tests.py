#!/usr/bin/python
"""
Python-Markdown Regression Tests
================================

Tests of the various APIs with the python markdown lib.

"""

import unittest
import markdown

class TestMarkdownParser(unittest.TestCase):
    """ Tests of the MarkdownParser class. """

    def setUp(self):
        """ Create instance of MarkdownParser. """
        self.parser = markdown.MarkdownParser()

    def testDetectTabbed(self):
        """ Test MarkdownParser.detectTabbed. """
        lines = ["\tfoo", "    bar", "baz"]
        tabbed, lines = self.parser.detectTabbed(lines)
        self.assertEqual(tabbed, ["foo", "bar"])
        self.assertEqual(lines, ["baz"])

    def testParseChunk(self):
        """ Test MarkdownParser.parseChunk. """
        root = markdown.etree.Element("div")
        lines = ['foo']
        self.parser.parseChunk(root, lines)
        self.assertEqual(markdown.etree.tostring(root), "<div><p>foo</p></div>")

    def testParseDocument(self):
        """ Test MarkdownParser.parseDocument. """
        lines = ['#foo', '', 'bar', '', '\tbaz']
        tree = self.parser.parseDocument(lines)
        self.assert_(isinstance(tree, markdown.etree.ElementTree))
        self.assert_(markdown.etree.iselement(tree.getroot()))
        self.assertEqual(markdown.etree.tostring(tree.getroot()),
            "<div><h1>foo</h1><p>bar</p><pre><code>baz\n</code></pre></div>")

class TestHtmlStash(unittest.TestCase):
    """ Test Markdown's HtmlStash. """
    
    def setUp(self):
        self.stash = markdown.HtmlStash()
        self.placeholder = self.stash.store('foo')

    def testSimpleStore(self):
        """ Test HtmlStash.store. """
        self.assertEqual(self.placeholder, markdown.HTML_PLACEHOLDER % 0)
        self.assertEqual(self.stash.html_counter, 1)
        self.assertEqual(self.stash.rawHtmlBlocks, [('foo', False)])

    def testStoreMore(self):
        """ Test HtmlStash.store with additional blocks. """
        placeholder = self.stash.store('bar')
        self.assertEqual(placeholder, markdown.HTML_PLACEHOLDER % 1)
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

class testTreap(unittest.TestCase):
    """ Test Treap storage class. """

    def setUp(self):
        self.treap = markdown.Treap()
        self.treap.add('first', 'This', '_begin')
        self.treap.add('second', 'is', '>first')
        self.treap.add('fourth', 'self', '>second')
        self.treap.add('fifth', 'test', '>fourth')
        self.treap.add('third', 'a', '>second')
        self.treap['seventh'] = '.'

    def testHeapsorted(self):
        """ Test output of Treap.heapsorted(). """
        self.assertEqual(self.treap.heapsorted(),
                    ['This', 'is', 'a', 'self', 'test','.'])
        self.assertEqual(self.treap.heapsorted(keys=1),
                    ['first', 'second', 'third', 'fourth', 'fifth','seventh'])
        self.assertEqual(self.treap.heapsorted(items=1),
                    [('first', 'This'), ('second', 'is'), ('third', 'a'), 
                    ('fourth', 'self'), ('fifth', 'test'), ('seventh','.')])

    def testDictStorage(self):
        """ Test Treap's Dict Storage. """
        self.treap._reset()
        self.assertEqual(self.treap.values(), self.treap._vals)
        self.assertEqual(self.treap.keys(), self.treap._keys)
        self.assertEqual(self.treap.items(), self.treap._items)

    def testDeleteNode(self):
        """ Test deletion of a Treap node. """
        del self.treap['second']
        self.assertEqual(self.treap.heapsorted(),
                    ['This', 'a', 'self', 'test','.'])
        self.assertEqual(self.treap.heapsorted(keys=1),
                    ['first', 'third', 'fourth', 'fifth','seventh'])
        self.assertEqual(self.treap.heapsorted(items=1),
                    [('first', 'This'), ('third', 'a'), ('fourth', 'self'), 
                    ('fifth', 'test'), ('seventh','.')])

    def testChangeValue(self):
        """ Test Treap change value. """
        self.treap['seventh'] = 'CRAZY'
        self.assertEqual(self.treap.heapsorted(),
                    ['This', 'is', 'a', 'self', 'test','CRAZY'])
        self.assertEqual(self.treap.heapsorted(keys=1),
                    ['first', 'second', 'third', 'fourth', 'fifth','seventh'])
        self.assertEqual(self.treap.heapsorted(items=1),
                    [('first', 'This'), ('second', 'is'), ('third', 'a'), 
                    ('fourth', 'self'), ('fifth', 'test'), ('seventh','CRAZY')])

    def testChangePriority(self):
        """ Test Treap change priority. """
        self.treap.link('seventh', '<third')
        self.assertEqual(self.treap.heapsorted(),
                    ['This', 'is', 'a', 'self', '.', 'test'])
        self.assertEqual(self.treap.heapsorted(keys=1),
                    ['first', 'second', 'third', 'fourth', 'seventh', 'fifth'])
        self.assertEqual(self.treap.heapsorted(items=1),
                    [('first', 'This'), ('second', 'is'), ('third', 'a'), 
                    ('fourth', 'self'), ('seventh','.'), ('fifth', 'test')])

if __name__ == '__main__':
    unittest.main()

