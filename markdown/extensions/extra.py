"""
Python-Markdown Extra Extension
===============================

A compilation of various Python-Markdown extensions that imitates
[PHP Markdown Extra](http://michelf.com/projects/php-markdown/extra/).

Note that each of the individual extensions still need to be available
on your PYTHONPATH. This extension simply wraps them all up as a
convenience so that only one extension needs to be listed when
initiating Markdown. See the documentation for each individual
extension for specifics about that extension.

In the event that one or more of the supported extensions are not
available for import, Markdown will issue a warning and simply continue
without that extension.

There may be additional extensions that are distributed with
Python-Markdown that are not included here in Extra. Those extensions
are not part of PHP Markdown Extra, and therefore, not part of
Python-Markdown Extra. If you really would like Extra to include
additional extensions, we suggest creating your own clone of Extra
under a differant name. You could also edit the `extensions` global
variable defined below, but be aware that such changes may be lost
when you upgrade to any future version of Python-Markdown.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..blockprocessors import BlockProcessor
from .. import util
import re

extensions = ['smart_strong',
              'fenced_code',
              'footnotes',
              'attr_list',
              'def_list',
              'tables',
              'abbr',
              ]


class ExtraExtension(Extension):
    """ Add various extensions to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """ Register extension instances. """
        md.registerExtensions(extensions, self.config)
        if not md.safeMode:
            # Turn on processing of markdown text within raw html
            md.preprocessors['html_block'].markdown_in_raw = True
            md.parser.blockprocessors.add('markdown_block',
                                          MarkdownInHtmlProcessor(md.parser),
                                          '_begin')
            md.parser.blockprocessors.tag_counter = -1
            md.parser.blockprocessors.contain_span_tags = re.compile(
                r'^(p|h[1-6]|li|dd|dt|td|th|legend|address)$', re.IGNORECASE)
            md.parser.blockprocessors.left_tag = re.compile(
                r'^<\S*\s(\S*=".*"\s)*markdown=".*"(\s\S*=".*")*>')
            md.parser.blockprocessors.right_tag = re.compile(r'.*<\/\S*>$')


class MarkdownInHtmlProcessor(BlockProcessor):
    """ Process Markdown Inside HTML Blocks. """

    def test(self, parent, block):
        return block == util.TAG_PLACEHOLDER % \
            str(self.parser.blockprocessors.tag_counter + 1)

    def _recursive(self, element, block, right_tag_index):
        nest_index = []
        i = self.parser.blockprocessors.tag_counter + 1
        while len(self.parser.markdown.htmlStash.tag_data) > i and self.\
                parser.markdown.htmlStash.tag_data[i]['left_tag_index']:
            left_tag_index = \
                self.parser.markdown.htmlStash.tag_data[i]['left_tag_index']
            right_tag_index = \
                self.parser.markdown.htmlStash.tag_data[i]['right_tag_index']
            nest_index.append((left_tag_index - 1, right_tag_index))
            i += 1

        if len(nest_index) == 0:
            self.parser.parseBlocks(element, block)
        else:
            for n in reversed(nest_index):
                nest = block[n[0]:n[1]]
                self.run(element, nest, block[n[1]:], True)
                del block[n[0]:]

    def run(self, parent, blocks, tail=None, nested=False):
        self.parser.blockprocessors.tag_counter += 1
        tag_data = self.parser.markdown.htmlStash.tag_data[
            self.parser.blockprocessors.tag_counter]

        # Create Element
        markdown_value = tag_data['attrs'].pop('markdown')
        element = util.etree.SubElement(parent, tag_data['tag'],
                                        tag_data['attrs'])

        # Process Tail
        if nested:  # tail always block mode because no span nested in span
            self.parser.parseBlocks(parent, tail)
            block = blocks[1:]
        else:
            block = blocks[tag_data['left_tag_index'] + 1:
                           tag_data['right_tag_index']]
            del blocks[:tag_data['right_tag_index']]

        # Process Text
        if (self.parser.blockprocessors.contain_span_tags.match(  # span mode
                tag_data['tag']) and markdown_value != 'block') or \
                markdown_value == 'span':
            element.text = '\n'.join(block)
        else:                                                     # block mode
            i = self.parser.blockprocessors.tag_counter + 1
            if len(self.parser.markdown.htmlStash.tag_data) > i and self.\
                    parser.markdown.htmlStash.tag_data[i]['left_tag_index']:
                first_subelement_index = self.parser.markdown.htmlStash.\
                    tag_data[i]['left_tag_index'] - 1
                self.parser.parseBlocks(
                    element, block[:first_subelement_index])
                block = self._recursive(element, block,
                                        tag_data['right_tag_index'])
            else:
                self.parser.parseBlocks(element, block)


def makeExtension(configs={}):
    return ExtraExtension(configs=dict(configs))
