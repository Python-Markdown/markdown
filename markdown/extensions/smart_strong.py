'''
Smart_Strong Extension for Python-Markdown
==========================================

This extention adds smarter handling of double underscores within words.

See <https://pythonhosted.org/Markdown/extensions/smart_strong.html> 
for documentation.

Original code Copyright 2011 [Waylan Limberg](http://achinghead.com)

All changes Copyright 2011-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php) 

'''

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..inlinepatterns import SimpleTagPattern

SMART_STRONG_RE = r'(?<!\w)(_{2})(?![_\s])(.+?_*?)(?<!\s)\2(?!\w)'
SMART_STRONG_EM_RE = r'(?<!\w)(_{3})(?![_\s])(.+?_*?)(?<!\s)\2(?!\w)'

class SmartEmphasisExtension(Extension):
    """ Add smart_emphasis extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """ Modify inline patterns. """
        md.inlinePatterns['strong2'] = SimpleTagPattern(SMART_STRONG_RE, 'strong')
        md.inlinePatterns['strong_em2'] = SimpleTagPattern(SMART_STRONG_EM_RE, 'strong')
        del md.inlinePatterns['strong_em4']
        del md.inlinePatterns['em_strong2']

def makeExtension(*args, **kwargs):
    return SmartEmphasisExtension(*args, **kwargs)
