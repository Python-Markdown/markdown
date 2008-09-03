#!/usr/bin/python

"""
CodeHilite Extension for Python-Markdown
=======================================

Adds code/syntax highlighting to standard Python-Markdown code blocks.

By [Waylan Limberg](http://achinghead.com/).

Project website: http://achinghead.com/markdown-wikilinks/
Contact: waylan [at] gmail [dot] com
 
License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
 
Version: 0.2 (April 30, 2008)
  
Dependencies:
* [Python 2.3+](http://python.org/)
* [Markdown 1.7+](http://www.freewisdom.org/projects/python-markdown/)
* [Pygments](http://pygments.org/)

"""

import markdown

# --------------- CONSTANTS YOU MIGHT WANT TO MODIFY -----------------

try:
    TAB_LENGTH = markdown.TAB_LENGTH
except AttributeError:
    TAB_LENGTH = 4


# ------------------ The Main CodeHilite Class ----------------------
class CodeHilite:
    """
    Determine language of source code, and pass it into the pygments hilighter.

    Basic Usage:
        >>> code = CodeHilite(src = text)
        >>> html = code.hilite()
    
    * src: Source string or any object with a .readline attribute.
      
    * linenos: (Boolen) Turn line numbering 'on' or 'off' (off by default).

    * css_class: Set class name of wrapper div ('codehilite' by default).
      
    Low Level Usage:
        >>> code = CodeHilite()
        >>> code.src = text      # String or anything with a .readline attribute
        >>> code.linenos = True  # True or False; Turns line numbering on or of.
        >>> html = code.hilite()
    
    """

    def __init__(self, src=None, linenos=False, css_class="codehilite"):
        self.src = src
        self.lang = None
        self.linenos = linenos
        self.css_class = css_class

    def hilite(self):
        """
        Pass code to the [Pygments](http://pygments.pocoo.org/) highliter with 
        optional line numbers. The output should then be styled with css to 
        your liking. No styles are applied by default - only styling hooks 
        (i.e.: <span class="k">). 

        returns : A string of html.
    
        """

        self.src = self.src.strip('\n')
        
        self._getLang()

        try:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name, guess_lexer, \
                                        TextLexer
            from pygments.formatters import HtmlFormatter
        except ImportError:
            # just escape and pass through
            txt = self._escape(self.src)
            if self.linenos:
                txt = self._number(txt)
            else :
                txt = '<div class="%s"><pre>%s</pre></div>\n'% \
                        (txt, self.css_class)
            return txt
        else:
            try:
                lexer = get_lexer_by_name(self.lang)
            except ValueError:
                try:
                    lexer = guess_lexer(self.src)
                except ValueError:
                    lexer = TextLexer()
            formatter = HtmlFormatter(linenos=self.linenos, 
                                      cssclass=self.css_class)
            return highlight(self.src, lexer, formatter)

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt

    def _number(self, txt):
        """ Use <ol> for line numbering """
        # Fix Whitespace
        txt = txt.replace('\t', ' '*TAB_LENGTH)
        txt = txt.replace(" "*4, "&nbsp; &nbsp; ")
        txt = txt.replace(" "*3, "&nbsp; &nbsp;")
        txt = txt.replace(" "*2, "&nbsp; ")        
        
        # Add line numbers
        lines = txt.splitlines()
        txt = '<div class="codehilite"><pre><ol>\n'
        for line in lines:
            txt += '\t<li>%s</li>\n'% line
        txt += '</ol></pre></div>\n'
        return txt


    def _getLang(self):
        """ 
        Determines language of a code block from shebang lines and whether said
        line should be removed or left in place. If the sheband line contains a
        path (even a single /) then it is assumed to be a real shebang lines and
        left alone. However, if no path is given (e.i.: #!python or :::python) 
        then it is assumed to be a mock shebang for language identifitation of a
        code fragment and removed from the code block prior to processing for 
        code highlighting. When a mock shebang (e.i: #!python) is found, line 
        numbering is turned on. When colons are found in place of a shebang 
        (e.i.: :::python), line numbering is left in the current state - off 
        by default.
        
        """

        import re
    
        #split text into lines
        lines = self.src.split("\n")
        #pull first line to examine
        fl = lines.pop(0)
    
        c = re.compile(r'''
            (?:(?:::+)|(?P<shebang>[#]!))	# Shebang or 2 or more colons.
            (?P<path>(?:/\w+)*[/ ])?        # Zero or 1 path ending in either 
                                            #   a / or a single space.
            (?P<lang>\w*)	                # The language (a single /  or 
                                            #   space before lang is a path).
            ''',  re.VERBOSE)
        # search first line for shebang
        m = c.search(fl)
        if m:
            # we have a match
            try:
                self.lang = m.group('lang').lower()
            except IndexError:
                self.lang = None
            if m.group('path'):
                # path exists - restore first line
                lines.insert(0, fl)
            if m.group('shebang'):
                # shebang exists - use line numbers
                self.linenos = True
        else:
            # No match
            lines.insert(0, fl)
        
        self.src = "\n".join(lines).strip("\n")



# ------------------ The Markdown Extension -------------------------------
class CodeHiliteExtention(markdown.Extension):
    def __init__(self, configs):
        # define default configs
        self.config = {
            'force_linenos' : [False, "Force line numbers - Default: False"],
            'css_class' : ["codehilite", 
                           "Set class name for wrapper <div> - Default: codehilite"],
            }
        
        # Override defaults with user settings
        for key, value in configs:
            # self.config[key][0] = value
            self.setConfig(key, value) 
            
    def extendMarkdown(self, md, md_globals):
  
        def _hiliteCodeBlock(parent_elem, lines, inList):
            """
            Overrides `_processCodeBlock` method in standard Markdown class 
            and sends code blocks to a code highlighting proccessor. The result
            is then stored in the HtmlStash, a placeholder is inserted into
            the dom and the remainder of the text file is processed recursively.

            * parent_elem: DOM element to which the content will be added
            * lines: a list of lines
            * inList: a level
            
            returns: None

            """

            detabbed, theRest = md.blockGuru.detectTabbed(lines)
            text = "\n".join(detabbed).rstrip()+"\n"
            code = CodeHilite(text, linenos=self.config['force_linenos'][0],
                              css_class=self.config['css_class'][0]) 
            placeholder = md.htmlStash.store(code.hilite(), safe=True)
            # This wrapping p element will be removed when inserting raw html
            p = markdown.etree.SubElement(parent_elem, 'p')
            p.text = placeholder
            md._processSection(parent_elem, theRest, inList)
            
        md._processCodeBlock = _hiliteCodeBlock

def makeExtension(configs={}):
  return CodeHiliteExtention(configs=configs)

