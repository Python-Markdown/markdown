#!/usr/bin/python
import markdown

# --------------- CONSTANTS YOU MIGHT WANT TO MODIFY -----------------

DEFAULT_HILITER = 'pygments' # one of 'enscript', 'dp', or 'pygments'
try:
    TAB_LENGTH = markdown.TAB_LENGTH
except AttributeError:
    TAB_LENGTH = 4

# --------------- THE CODE -------------------------------------------
# --------------- hiliter utility functions --------------------------
def escape(txt) :
    '''basic html escaping'''
    txt = txt.replace('&', '&amp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    return txt

def number(txt):
    '''use <ol> for line numbering'''
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

# ---------------- The hiliters ---------------------------------------
def enscript(src, lang=None, num=True):
    '''
Pass source code on to [enscript] (http://www.codento.com/people/mtr/genscript/)
command line utility for hiliting.

Usage:
    >>> enscript(src [, lang [, num ]] )

      @param src:  Can be a string or any object with a .readline attribute.

      @param lang: The language of code. Basic escaping only, if None.

      @param num: (Boolen) Turns line numbering 'on' or 'off' (on by default).
      
      @returns : A string of html.
    '''
    if lang:
        cmd = 'enscript --highlight=%s --color --language=html --tabsize=%d --output=-'% (lang, TAB_LENGTH)
        from os import popen3
        (i, out, err) = popen3(cmd)
        i.write(src)
        i.close()
        # check for errors
        e = err.read()
        if e != 'output left in -\n' :
            # error - just escape
            txt = escape(src)
        else :
            import re
            pattern = re.compile(r'<PRE>(?P<code>.*?)</PRE>', re.DOTALL)
            txt =  pattern.search(out.read()).group('code')
            # fix enscripts output
            txt = txt.replace('\n</FONT></I>', '</FONT></I>\n').strip()
            html_map = {'<I>' : '<em>',
                        '</I>' : '</em>',
                        '<B>' : '<strong>',
                        '</B>' : '</strong>',
                        '<FONT COLOR="#' : '<span style="color:#',
                        '</FONT>' : '</span>'
                        }
            for k, v in html_map.items() :
                txt = txt.replace(k, v)
    else:
        txt = escape(src)
    if num :
        txt = number(txt)
    else :
        txt = '<div class="codehilite"><pre>%s</pre></div>\n'% txt
    return txt


def dp(src, lang=None, num=True):
    '''
Pass source code to a textarea for the [dp.SyntaxHighlighter] (http://www.dreamprojections.com/syntaxhighlighter/Default.aspx)

Usage:
    >>> dp(src [, lang [, num ]] )

      @param src:  A string.

      @param lang: The language of code. Undefined if None.

      @param num: (Boolen) Turns line numbering 'on' or 'off' (on by default).
      
      @returns : A string of html.
    '''
    gutter = ''
    if not num: 
        gutter = ':nogutter'
    if not lang:
        lang = ''

    return '<div class="codehilite"><textarea name="code" class="%s%s" cols="60" rows="10">\n%s\n</textarea></div>\n'% (lang, gutter, src)
    
def pygment(src, lang = None, num = True):
    '''
Pass code to the [Pygments](http://pygments.pocoo.org/) highliter with 
optional line numbers. The output should then be styled with css to your liking.
No styles are applied by default - only styling hooks (i.e.: <span class="k">). 

Usage:
    >>> pygment(src [, lang [, num ]] )

      @param src:  Can be a string or any object with a .readline attribute.

      @param lang: The language of code. Pygments will try to guess language if None.

      @param num: (Boolen) Turns line numbering 'on' or 'off' (on by default).
      
      @returns : A string of html.
    '''
    try:
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
        from pygments.formatters import HtmlFormatter
    except ImportError:
        # just escape and pass through
        txt = escape(src)
        if num:
            txt = number(txt)
        else :
            txt = '<div class="codehilite"><pre>%s</pre></div>\n'% txt
        return txt
    else:
        try:
            lexer = get_lexer_by_name(lang)
        except ValueError:
            try:
                lexer = guess_lexer(src)
            except ValueError:
                lexer = TextLexer()
        formatter = HtmlFormatter(linenos=num, cssclass="codehilite")
        return highlight(src, lexer, formatter)


# ------------------ The Main CodeHilite Class ----------------------
class CodeHilite:
    '''
A wrapper class providing a single API for various hilighting engines. Takes source code, determines which language it containes (if not provided), and passes it into the hiliter specified.

Basic Usage:
    >>> code = CodeHilite(src = text)
    >>> html = code.hilite()
    
      @param  src:  Can be a string or any object with a .readline attribute.
      
      @param  lang: A string. Accepted values determined by hiliter used. Overrides _getLang()
      
      @param  linenos:  (Boolen) Turns line numbering 'on' or 'off' (off by default).
      
      @param  hiliter:  A string. One of 'enscript', 'dp', or 'pygments'.

Low Level Usage:
    >>> code = CodeHilite()
    >>> code.src = text                 # Can be a string or any object with a .readline attribute.
    >>> code.lang = 'python'            # Setting this will override _getLang()
    >>> code.linenos = True             # True or False; Turns line numbering on or off.
    >>> code.hiliter = MyCustomHiliter  # Where MyCustomHiliter is callable, takes three arguments (src, lang, linenos) and returns a string.
    >>> html = code.hilite()
    '''
    def __init__(self, src=None, lang=None, linenos = False, hiliter=DEFAULT_HILITER):
        self.src = src
        self.lang = lang
        self.linenos = linenos
        # map of highlighters
        hl_map = { 'enscript' : enscript, 'dp' : dp, 'pygments' : pygment }
        try :
            self.hiliter = hl_map[hiliter]
        except KeyError:
            raise "Please provide a valid hiliter as a string. One of 'enscript', 'dp', or 'pygments'"


    def _getLang(self):
        ''' 
Determines language of a code block from shebang lines and whether said line should be removed or left in place. If the sheband line contains a path (even a single /) then it is assumed to be a real shebang lines and left alone. However, if no path is given (e.i.: #!python or :::python) then it is assumed to be a mock shebang for language identifitation of a code fragment and removed from the code block prior to processing for code highlighting. When a mock shebang (e.i: #!python) is found, line numbering is turned on. When colons are found in place of a shebang (e.i.: :::python), line numbering is left in the current state - off by default.
        '''
        import re
    
        #split text into lines
        lines = self.src.split("\n")
        #pull first line to examine
        fl = lines.pop(0)
    
        c = re.compile(r'''
            (?:(?:::+)|(?P<shebang>[#]!))	#shebang or 2 or more colons
            (?P<path>(?:/\w+)*[/ ])? # zero or 1 path ending in either a / or a single space
            (?P<lang>\w*)	# the language (a single /  or space before lang is a path)
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

    def hilite(self):
        '''The wrapper function which brings it all togeather'''
        self.src = self.src.strip('\n')
        
        if not self.lang : self._getLang()
        
        return self.hiliter(self.src, self.lang, self.linenos)


# ------------------ The Markdown Extention -------------------------------
class CodeHiliteExtention (markdown.Extension) :
    def __init__(self, configs):
        # define default configs
        self.config = {'hiliter' : [DEFAULT_HILITER, "one of 'enscript', 'dp', or 'pygments'"],
                       'force_linenos' : [False, "Force line numbers - Default: False"] }
        
        # Override defaults with user settings
        for key, value in configs :
            # self.config[key][0] = value
            self.setConfig(key, value) 
            
    def extendMarkdown(self, md, md_globals) :
  
        def _hiliteCodeBlock(parent_elem, lines, inList):
            """Overrides function of same name in standard Markdown class and
               sends code blocks to a code highlighting proccessor. The result
               is then stored in the HtmlStash, a placeholder is inserted into
               the dom and the remainder of the text file is processed recursively.

               @param parent_elem: DOM element to which the content will be added
               @param lines: a list of lines
               @param inList: a level
               @returns: None"""
            detabbed, theRest = md.blockGuru.detectTabbed(lines)
            text = "\n".join(detabbed).rstrip()+"\n"
            code = CodeHilite(text, hiliter=self.config['hiliter'][0], linenos=self.config['force_linenos'][0]) 
            placeholder = md.htmlStash.store(code.hilite())
            parent_elem.appendChild(md.doc.createTextNode(placeholder))
            md._processSection(parent_elem, theRest, inList)
            
        md._processCodeBlock = _hiliteCodeBlock

def makeExtension(configs=None) :
  return CodeHiliteExtention(configs=configs)
