#!/usr/bin/env python
"""
Python-Markdown Extra Extension
===============================

A compilation of various Python-Markdown extensions that imitates
[PHP Markdown Extra](http://michelf.com/projects/php-markdown/extra/).

As no-one has yet written a Definition List extension for Python-
Markdown, definition lists are not yet supported by Extra.

Note that each of the individual extensions still need to be available
on your PYTHONPATH. This extension simply wraps them all up as a 
convenience so that only one extension needs to be listed when
initiating Markdown. See the documentation for each individual
extension for specifics about that extension.

In the event that one or more of the supported extensions are not 
available for import, Markdown will simply continue without that 
extension. If you would like to be notified of such failures,
you may set Python-Markdown's logger level to "WARN".

There may be additional extensions that are distributed with 
Python-Markdown that are not included here in Extra. Those extensions
are not part of PHP Markdown Extra, and therefore, not part of
Python-Markdown Extra. If you really would like Extra to include
additional extensions, we suggest creating your own clone of Extra
under a differant name. You could also edit the `extensions` global 
variable defined below, but be aware that such changes may be lost 
when you upgrade to any future version of Python-Markdown.

"""

import markdown

extensions = ['fenced_code',
              'footnotes',
              'headerid',
              'tables',
              'abbr',
              ]
              

class ExtraExtension(markdown.Extension):
    """ Add various extensions to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """ Register extension instances. """
        md.registerExtensions(extensions, self.config)

def makeExtension(configs={}):
    return ExtraExtension(configs=dict(configs))
