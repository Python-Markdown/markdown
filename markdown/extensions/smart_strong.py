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
from ..inlinepatterns import SimpleTagPattern, DoubleTagPattern
from ..inlinepatterns import UNDER_CONTENT, SMART_CONTENT, SMART_STRONG_EM_RE

SMART_STRONG_2_RE = r'(?<!\w)(_{2})(?![\s_])%s(?<!\s)\2(?!\w)' % SMART_CONTENT

# Smart rules for when "smart emphasis" is enabled
# ___strong,em_strong__
SMART_STRONG_EM_4_RE = \
r'(?<!\w)(_{3})(?!\s)(?![\s_])%s(?<!\s)_%s(?<!\s)_{2}(?!\w)' % (SMART_CONTENT, SMART_CONTENT)
# ___em,strong__em_
SMART_EM_STRONG_2_RE = \
r'(?<!\w)(_{3})(?!\s)(?![\s_])%s(?<!\s)_{2}(?![\s_])%s(?<!\s)_(?!\w)' % (SMART_CONTENT, SMART_CONTENT)

# Smart rules for when "smart emphasis" is disabled
# ___strong,em_strong__
STRONG_EM_4_RE = \
r'(?<!\w)(_{3})(?!\s)%s(?<!\s)_%s(?<!\s)_{2}(?!\w)' % (UNDER_CONTENT, SMART_CONTENT)
# ___em,strong__em_
EM_STRONG_2_RE = \
r'(?<!\w)(_{3})(?!\s)(?![\s_])%s(?<!\s)_{2}(?!\w)%s(?<!\s)_' % (SMART_CONTENT, UNDER_CONTENT)


class SmartEmphasisExtension(Extension):
    """ Add smart_emphasis extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """ Modify inline patterns. """

        md.inlinePatterns['strong2'] = SimpleTagPattern(SMART_STRONG_2_RE, 'strong')
        md.inlinePatterns['strong_em2'] = DoubleTagPattern(SMART_STRONG_EM_RE, 'strong,em')

        if not md.smart_emphasis:
            md.inlinePatterns['em_strong2'] = DoubleTagPattern(EM_STRONG_2_RE, 'em,strong')
            md.inlinePatterns['strong_em4'] = DoubleTagPattern(STRONG_EM_4_RE, 'strong,em')
        else:
            md.inlinePatterns['em_strong2'] = DoubleTagPattern(SMART_EM_STRONG_2_RE, 'em,strong')
            md.inlinePatterns['strong_em4'] = DoubleTagPattern(SMART_STRONG_EM_4_RE, 'strong,em')

def makeExtension(*args, **kwargs):
    return SmartEmphasisExtension(*args, **kwargs)
