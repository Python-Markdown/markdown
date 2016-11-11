'''
Legacy Em Extension for Python-Markdown
=======================================

This extention provided legacy behavior for _connected_words_.

Copyright 2015 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

'''

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..inlinepatterns import SimpleTagPattern

EMPHASIS_RE = r'(\*|_)(.+?)\2'
STRONG_RE = r'(\*{2}|_{2})(.+?)\2'


class LegacyEmExtension(Extension):
    """ Add legacy_em extension to Markdown class."""

    def extendMarkdown(self, md):
        """ Modify inline patterns. """
        md.inlinePatterns.register(SimpleTagPattern(STRONG_RE, 'strong'), 'strong', 40)
        md.inlinePatterns.register(SimpleTagPattern(EMPHASIS_RE, 'em'), 'emphasis', 30)
        md.inlinePatterns.deregister('strong2', strict=False)
        md.inlinePatterns.deregister('emphasis2', strict=False)
