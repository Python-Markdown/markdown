#!/usr/bin/env python

"""
Fenced Code Extension for Python Markdown
=========================================

This extension adds Fenced Code Blocks to Python-Markdown.

    >>> import markdown
    >>> text = '''
    ... A paragraph before a fenced code block:
    ... 
    ... ~~~
    ... Fenced code block
    ... ~~~
    ... '''
    >>> html = markdown.markdown(text, extensions=['fenced_code'])
    >>> html
    u'<p>A paragraph before a fenced code block:\\n</p>\\n<pre><code>Fenced code block\\n<code><pre>'

Works with safe_mode also (we check this because we are using the HtmlStash):

    >>> markdown.markdown(text, extensions=['fenced_code'], safe_mode='replace')
    u'<p>A paragraph before a fenced code block:\\n</p>\\n<pre><code>Fenced code block\\n<code><pre>'
    
Include tilde's in a code block and wrap with blank lines:

    >>> text = '''
    ... ~~~~~~~~
    ... 
    ... ~~~~
    ... 
    ... ~~~~~~~~'''
    >>> markdown.markdown(text, extensions=['fenced_code'])
    u'<pre><code>\\n~~~~\\n\\n<code><pre>'

Multiple blocks and language tags:

    >>> text = '''
    ... ~~~~
    ... block one
    ... ~~~~{.python}
    ... 
    ... ~~~~
    ... <p>block two</p>
    ... ~~~~{.html}'''
    >>> markdown.markdown(text, extensions=['fenced_code'])
    u'<pre><code class="python">block one\\n<code><pre>\\n\\n<pre><code class="html">&lt;p&gt;block two&lt;/p&gt;\\n<code><pre>'

"""

import markdown, re

# Global vars
FENCED_BLOCK_RE = re.compile( \
    r'(?P<fence>^~{3,})[ ]*\n(?P<code>.*?)(?P=fence)[ ]*(\{\.(?P<lang>[a-zA-Z0-9_-]*)\})?[ ]*$', 
    re.MULTILINE|re.DOTALL
    )
CODE_WRAP = '<pre><code%s>%s<code><pre>'
LANG_TAG = ' class="%s"'


class FencedCodeExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add FencedBlockPreprocessor to the Markdown instance. """

        FENCED_BLOCK_PREPROCESSOR = FencedBlockPreprocessor()
        FENCED_BLOCK_PREPROCESSOR.md = md
        md.textPreprocessors.insert(0, FENCED_BLOCK_PREPROCESSOR)


class FencedBlockPreprocessor(markdown.TextPreprocessor):
    
    def run(self, text):
        """ Match and store Fenced Code Blocks in the HtmlStash. """
        while 1:
            m = FENCED_BLOCK_RE.search(text)
            if m:
                lang = ''
                if m.group('lang'):
                    lang = LANG_TAG % m.group('lang')
                code = CODE_WRAP % (lang, self._escape(m.group('code')))
                placeholder = self.md.htmlStash.store(code, safe=True)
                text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
            else:
                break
        return text

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


def makeExtension(configs=None):
    return FencedCodeExtension()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
