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

EMPHASIS_RE = r'(\*|_)(.+?)\1'
STRONG_RE = r'(\*{2}|_{2})(.+?)\1'


class LegacyEmExtension(Extension):
    """ Add legacy_em extension to Markdown class."""

    def extendMarkdown(self, md):
        """ Modify inline patterns. """
        md.inlinePatterns['strong'] = SimpleTagPattern(STRONG_RE, 'strong')
        md.inlinePatterns['emphasis'] = SimpleTagPattern(EMPHASIS_RE, 'em')
        del md.inlinePatterns['strong2']
        del md.inlinePatterns['emphasis2']
