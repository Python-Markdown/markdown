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
    r'(?P<fence>^(?:~{3,}|`{3,}))[ ]*(\{\.?(?P<lang>[a-zA-Z0-9_-]+)?(;(?P<mode>(?:lines|skipblanks|statements)))?(;(?P<offset>\d+))?\})?[ ]*\n(?P<code>.*?)(?<=\n)(?P=fence)[ ]*$',
    re.MULTILINE|re.DOTALL
    )
STMTCONT_RE = re.compile(r'[\\,]\s*$')
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

                if m.group('mode'):
                    mode = m.group('mode')
                    # prep the fence for next pass
                    if m.group('lang'):
                        fence = "```{." + "{}".format(m.group('lang')) + "}"
                    else:
                        fence = "```"
                    # set starting line number
                    i = 1
                    if m.group('offset'): i = int(m.group('offset'))
                    # split code text into array
                    code = m.group('code').split("\n")
                    # yank trailing newline; we'll add it back last thing
                    code.pop()
                    # pad the number of digits in the largest line number
                    zpad = len(str(len(code) + i))
                    in_statement = False

                    for j in range(len(code)):
                        if mode == "statements" and STMTCONT_RE.search(code[j]):
                            stmt_continuation = True
                        else:
                            stmt_continuation = False

                        # ignore blank lines where appropriate
                        if (mode == "skipblanks" or mode == "statements") and code[j] == "":
                            continue

                        if stmt_continuation is False and in_statement is False:
                            code[j] = "{:0{pad}}  {}".format(i, code[j], pad=zpad)
                            i = i + 1
                        else:
                            if stmt_continuation:
                                if in_statement is False:
                                    # begin statment
                                    in_statement = True
                                    code[j] = "{:0{pad}}  {}".format(i, code[j], pad=zpad)
                                    i = i + 1
                                else:
                                    # in statement: space pad
                                    code[j] = "{0: >{pad}}".format('', pad=(zpad+2)) + code[j]
                            else:
                                # not continuation but in statment: end statment
                                in_statement = False
                                code[j] = "{0: >{pad}}".format('', pad=(zpad+2)) + code[j]

                    # put it all back together with fences; restart loop to reprocess this block
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
