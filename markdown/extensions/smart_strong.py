'''
Smart_Strong Extension for Python-Markdown
==========================================

This extention adds smarter handling of double underscores within words.

See <https://Python-Markdown.github.io/extensions/smart_strong>
for documentation.

Original code Copyright 2011 [Waylan Limberg](http://achinghead.com)

All changes Copyright 2011-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

'''

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..inlinepatterns import SimpleTagInlineProcessor

SMART_STRONG_RE = r'(?<!\w)(_{2})(?!_)(.+?)(?<!_)\1(?!\w)'
STRONG_RE = r'(\*{2})(.+?)\1'


class SmartEmphasisExtension(Extension):
    """ Add smart_emphasis extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """ Modify inline patterns. """
        md.inlinePatterns['strong'] = SimpleTagInlineProcessor(STRONG_RE, 'strong')
        md.inlinePatterns.add(
            'strong2',
            SimpleTagInlineProcessor(SMART_STRONG_RE, 'strong'),
            '>emphasis2'
        )


def makeExtension(*args, **kwargs):
    return SmartEmphasisExtension(*args, **kwargs)
