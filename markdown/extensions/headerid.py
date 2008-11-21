#!/usr/bin/python

"""
HeaderID Extension for Python-Markdown
======================================

Adds ability to set HTML IDs for headers.

Basic usage:

    >>> import markdown
    >>> text = "# Some Header # {#some_id}"
    >>> md = markdown.markdown(text, ['headerid'])
    >>> md
    u'<h1 id="some_id">Some Header</h1>'

All header IDs are unique:

    >>> text = '''
    ... #Header
    ... #Another Header {#header}
    ... #Third Header {#header}'''
    >>> md = markdown.markdown(text, ['headerid'])
    >>> md
    u'<h1 id="header">Header</h1>\\n<h1 id="header_1">Another Header</h1>\\n<h1 id="header_2">Third Header</h1>'

To fit within a html template's hierarchy, set the header base level:

    >>> text = '''
    ... #Some Header
    ... ## Next Level'''
    >>> md = markdown.markdown(text, ['headerid(level=3)'])
    >>> md
    u'<h3 id="some_header">Some Header</h3>\\n<h4 id="next_level">Next Level</h4>'

Turn off auto generated IDs:

    >>> text = '''
    ... # Some Header
    ... # Header with ID # { #foo }'''
    >>> md = markdown.markdown(text, ['headerid(forceid=False)'])
    >>> md
    u'<h1>Some Header</h1>\\n<h1 id="foo">Header with ID</h1>'

Use with MetaData extension:

    >>> text = '''header_level: 2
    ... header_forceid: Off
    ...
    ... # A Header'''
    >>> md = markdown.markdown(text, ['headerid', 'meta'])
    >>> md
    u'<h2>A Header</h2>'

Copyright 2007-2008 [Waylan Limberg](http://achinghead.com/).

Project website: <http://www.freewisdom.org/project/python-markdown/HeaderId>
Contact: markdown@freewisdom.org

License: BSD (see ../docs/LICENSE for details) 

Dependencies:
* [Python 2.3+](http://python.org)
* [Markdown 2.0+](http://www.freewisdom.org/projects/python-markdown/)

"""

import markdown
from markdown import etree
import re
from string import ascii_lowercase, digits, punctuation

ID_CHARS = ascii_lowercase + digits + '-_'

HEADER_RE = re.compile(r'''^(\#{1,6})		# group(1) = string of hashes
                           ( [^{^#]*)		# group(2) = Header text
                           [\#]*		    # optional closing hashes 
                           (?:[ \t]*\{[ \t]*\#([-_:a-zA-Z0-9]+)[ \t]*\})?	# group(3) = id attr''',
                           re.VERBOSE)

IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')

class HeaderIdExtension (markdown.Extension) :
    def __init__(self, configs):
        # set defaults
        self.config = {
                'level' : ['1', 'Base level for headers.'],
                'forceid' : ['True', 'Force all headers to have an id.']
            }

        for key, value in configs:
            self.setConfig(key, value)


    def extendMarkdown(self, md, md_globals) :

        md.IDs = []
        
        def _processHeaderId(parent_elem, paragraph) :
            ''' 
            Overrides __processHeader of MarkdownParser() and 
            adds an 'id' to the header. 
            '''
            m = HEADER_RE.match(paragraph[0])
            if m :
                start_level, force_id = _get_meta()
                level = len(m.group(1)) + start_level
                if level > 6: 
                    level = 6
                h = etree.Element("h%d" % level)
                parent_elem.append(h)
                h.text = m.group(2).strip()
                if m.group(3) :
                    h.set('id', _unique_id(m.group(3)))
                elif force_id:
                    h.set('id', _create_id(m.group(2).strip()))
            else :
                message(CRITICAL, "We've got a problem header!")
        
        md.parser._MarkdownParser__processHeader = _processHeaderId

        def _get_meta():
            ''' Return meta data suported by this ext as a tuple '''
            level = int(self.config['level'][0]) - 1
            force = _str2bool(self.config['forceid'][0])
            if hasattr(md, 'Meta'):
                if md.Meta.has_key('header_level'):
                    level = int(md.Meta['header_level'][0]) - 1
                if md.Meta.has_key('header_forceid'): 
                    force = _str2bool(md.Meta['header_forceid'][0])
            return level, force

        def _str2bool(s, default=False):
            ''' Convert a string to a booleen value. '''
            s = str(s)
            if s.lower() in ['0', 'f', 'false', 'off', 'no', 'n']:
                return False
            elif s.lower() in ['1', 't', 'true', 'on', 'yes', 'y']:
                    return True
            return default

        def _unique_id(id):
            ''' Ensure ID is unique. Append '_1', '_2'... if not '''
            while id in md.IDs:
                m = IDCOUNT_RE.match(id)
                if m:
                    id = '%s_%d'% (m.group(1), int(m.group(2))+1)
                else:
                    id = '%s_%d'% (id, 1)
            md.IDs.append(id)
            return id


        def _create_id(header):
            ''' Return ID from Header text. '''
            h = ''
            for c in header.lower().replace(' ', '_'):
                if c in ID_CHARS:
                    h += c
                elif c not in punctuation:
                    h += '+'
            return _unique_id(h)

            

def makeExtension(configs=None) :
    return HeaderIdExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

