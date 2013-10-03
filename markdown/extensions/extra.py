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
            start_spanmode_placeholder = "xx7882146723658911jj"
            end_spanmode_placeholder = "jj3912235655514745xx"
            md.preprocessors['html_block'].start_spanmode_placeholder = \
                start_spanmode_placeholder
            md.preprocessors['html_block'].end_spanmode_placeholder = \
                end_spanmode_placeholder
            md.parser.blockprocessors.add('html_block',
                                          HtmlBlockProcessor(md.parser),
                                          '_begin')
            md.parser.blockprocessors.start_spanmode_placeholder = \
                start_spanmode_placeholder
            md.parser.blockprocessors.end_spanmode_placeholder = \
                end_spanmode_placeholder


class HtmlBlockProcessor(BlockProcessor):
    """ Process Markdown Inside HTML Blocks. """

    def test(self, parent, block):
        return block == self.parser.blockprocessors.start_spanmode_placeholder

    def run(self, parent, blocks):
        del blocks[0]
        line = blocks.pop(0)
        block = ""
        while line != self.parser.blockprocessors.end_spanmode_placeholder:
            block += line
            line = blocks.pop(0)
        parent.append(util.etree.fromstring(block))


def makeExtension(configs={}):
    return ExtraExtension(configs=dict(configs))
