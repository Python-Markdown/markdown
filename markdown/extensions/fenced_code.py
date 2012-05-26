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
    >>> print html
    <p>A paragraph before a fenced code block:</p>
    <pre>Fenced code block
    </pre>

Backticks, as in Github Flavored Markdown, are also supported:

    >>> text = '''
    ... `````
    ... # Arbitrary code
    ... ~~~~~ # these tildes will not close the block
    ... `````'''
    >>> print markdown.markdown(text, extensions=['fenced_code'])
    <pre># Arbitrary code
    ~~~~~ # these tildes will not close the block
    </pre>

Works with safe_mode also (we check this because we are using the HtmlStash):

    >>> print markdown.markdown(text, extensions=['fenced_code'], safe_mode='replace')
    <p>A paragraph before a fenced code block:</p>
    <pre>Fenced code block
    </pre>

Include tildes in a code block and wrap with blank lines:

    >>> text = '''
    ... ~~~~~~~~
    ...
    ... ~~~~
    ... ~~~~~~~~'''
    >>> print markdown.markdown(text, extensions=['fenced_code'])
    <pre>
    ~~~~
    </pre>

Language tags:

    >>> text = '''
    ... ~~~~{.python}
    ... # Some python code
    ... ~~~~'''
    >>> print markdown.markdown(text, extensions=['fenced_code'])
    <pre class="python"># Some python code
    </pre>

Number lines:

    >>> text = '''
    ... ~~~~{.python;number}
    ... # Some lines
    ...   # of python
    ...
    ...   # code
    ... ~~~~'''
    >>> print markdown.markdown(text, extensions=['fenced_code'])
    <pre class="python">1  # Some lines
    2    # of python
    3  
    4    # code
    </pre>

Number lines, except blank ones:

    >>> text = '''
    ... ~~~~{;number;skip}
    ... # Some lines
    ... #  of python
    ... 
    ... #  code
    ... ~~~~'''
    >>> print markdown.markdown(text, extensions=['fenced_code'])
    <pre>1  # Some lines
    2    # of python
      
    3    # code
    </pre>

Number lines, but don't start at "1":

    >>> text = '''
    ... ~~~~{.python;number;98}
    ... # Some lines
    ...   # of python
    ...
    ...   # code
    ... ~~~~'''
    >>> print markdown.markdown(text, extensions=['fenced_code'])
    <pre class="python">098  # Some lines
    099    # of python
    100  
    101    # code
    </pre>

If 'number', 'skip', and the start-from number are all used, they must
be specified in that order.

Copyright 2007-2008 [Waylan Limberg](http://achinghead.com/).

Project website: <http://www.freewisdom.org/project/python-markdown/Fenced__Code__Blocks>
Contact: markdown@freewisdom.org

License: BSD (see ../docs/LICENSE for details)

Dependencies:
* [Python 2.4+](http://python.org)
* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)
* [Pygments (optional)](http://pygments.org)

"""

import re
import markdown
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension

# Global vars
FENCED_BLOCK_RE = re.compile( \
    r'(?P<fence>^(?:~{3,}|`{3,}))[ ]*(\{\.?(?P<lang>[a-zA-Z0-9_-]+)?(?P<number>;number)?(?P<nological>;nological)?(?P<skip>;skip)?;?(?P<start>\d+)?\})?[ ]*\n(?P<code>.*?)(?<=\n)(?P=fence)[ ]*$',
    re.MULTILINE|re.DOTALL
    )
LINECONT_RE = re.compile(r'[\\,]\s*$')
CODE_WRAP = '<pre%s>%s</pre>'
LANG_TAG = ' class="%s"'

class FencedCodeExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add FencedBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('fenced_code_block',
                                 FencedBlockPreprocessor(md),
                                 "_begin")


class FencedBlockPreprocessor(markdown.preprocessors.Preprocessor):

    def __init__(self, md):
        markdown.preprocessors.Preprocessor.__init__(self, md)

        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        """ Match and store Fenced Code Blocks in the HtmlStash. """

        # Check for code hilite extension
        if not self.checked_for_codehilite:
            for ext in self.markdown.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.config
                    break

            self.checked_for_codehilite = True

        text = "\n".join(lines)
        while 1:
            m = FENCED_BLOCK_RE.search(text)
            if m:
                lang = ''

                if m.group('number'):
                    # prep the fence for next pass
                    if m.group('lang'):
                        fence = "```{." + "{}".format(m.group('lang')) + "}"
                    else:
                        fence = "```"
                    # set flag for line continuation
                    linecont = True
                    if m.group('nological'): linecont = False

                    # split code; pad with numbers
                    i = 1
                    if m.group('start'): i = int(m.group('start'))
                    code = m.group('code').split("\n")
                    code.pop() # yank trailing newline; add it back after processing
                    zpad = len(str(len(code) + i))
                    linecont_on = False
                    for j in range(len(code)):
                        # don't number blank lines if skip is on
                        if m.group('skip') and code[j] == "": continue
                        if linecont:
                            if LINECONT_RE.search(code[j]):
                                if linecont_on:
                                    # linecont and matched and continuation active: no number; space pad; continue
                                    code[j] = "{0: >{pad}}".format('', pad=(zpad+2)) + code[j]
                                    continue
                                else:
                                    # linecont and matched: number, engage continuation
                                    linecont_on = True
                                    code[j] = "{:0{pad}}  {}".format(i, code[j], pad=zpad)
                            elif linecont_on:
                                # linecont and no match and continuation: end continuation; number; continue
                                linecont_on = False
                                code[j] = "{0: >{pad}}".format('', pad=(zpad+2)) + code[j]
                                continue
                            else:
                                # linecont and no match: number
                                code[j] = "{:0{pad}}  {}".format(i, code[j], pad=zpad)
                        else:
                            # logical mode is off: number
                            code[j] = "{:0{pad}}  {}".format(i, code[j], pad=zpad)
                        i = i + 1

                    # put it all back together with fences; reprocess this block
                    text = '%s\n%s\n%s\n```\n%s'% (text[:m.start()], fence, "\n".join(code), text[m.end():])
                    continue

                if m.group('lang'):
                    lang = LANG_TAG % m.group('lang')

                # If config is not empty, then the codehighlite extension
                # is enabled, so we call it to highlite the code
                if self.codehilite_conf:
                    highliter = CodeHilite(m.group('code'),
                            linenos=self.codehilite_conf['force_linenos'][0],
                            guess_lang=self.codehilite_conf['guess_lang'][0],
                            css_class=self.codehilite_conf['css_class'][0],
                            style=self.codehilite_conf['pygments_style'][0],
                            lang=(m.group('lang') or None),
                            noclasses=self.codehilite_conf['noclasses'][0])

                    code = highliter.hilite()
                else:
                    code = CODE_WRAP % (lang, self._escape(m.group('code')))

                placeholder = self.markdown.htmlStash.store(code, safe=True)
                text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
            else:
                break
        return text.split("\n")

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


def makeExtension(configs=None):
    return FencedCodeExtension(configs=configs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
