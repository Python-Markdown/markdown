#!/usr/bin/env python

"""
Passthrough extension for Python Markdown
=========================================

This extension adds passthrough Blocks to Python-Markdown. Passthrough blocks
are not transformed by the markdown processor at all.

    >>> import markdown
    >>> text = '''
    ... A paragraph before a *passthrough* block:
    ...
    ... +++++
    ... *passed through*
    ... +++++
    ... '''
    >>> html = markdown.markdown(text, extensions=['passthrough'])
    >>> html
    u'<p>A paragraph before a <em>passthrough</em> block:</p>\\n*passed through*'

Works with safe_mode also (we check this because we are using the HtmlStash):

    >>> markdown.markdown(text, extensions=['passthrough'], safe_mode='replace')
    u'<p>A paragraph before a <em>passthrough</em> block:</p>\\n*passed through*'

Author:
Lakshmi Vyasarajan for the Hyde project(http://github.com/hyde)     2011-05-02

License: BSD (see ../docs/LICENSE for details)

Dependencies:
* [Python 2.4+](http://python.org)
* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)

"""

import re
import markdown

# Global vars
PASSTHROUGH_BLOCK_RE = re.compile( \
    r'(?P<passthrough>^\+{5,})[ ]*\n(?P<content>.*?)(?P=passthrough)[ ]*$',
    re.MULTILINE|re.DOTALL
    )

class PassthroughExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add PassthroughBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('passthrough_block',
                                 PassthroughBlockPreprocessor(md),
                                 "_begin")


class PassthroughBlockPreprocessor(markdown.preprocessors.Preprocessor):

    def __init__(self, md):
        markdown.preprocessors.Preprocessor.__init__(self, md)

    def getConfig(self, key):
        if key in self.config:
            return self.config[key][0]
        else:
            return None

    def run(self, lines):
        """ Match and store passthrough blocks in the HtmlStash. """

        text = "\n".join(lines)
        while 1:
            m = PASSTHROUGH_BLOCK_RE.search(text)
            if m:
                content = m.group('content')
                placeholder = self.markdown.htmlStash.store(content, safe=True)
                text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
            else:
                break
        return text.split("\n")

def makeExtension(configs=None):
    return PassthroughExtension(configs=configs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
