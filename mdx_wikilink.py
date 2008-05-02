#!/usr/bin/env python

'''
WikiLink Extention for Python-Markdown
======================================

Converts CamelCase words to relative links.  Requires Python-Markdown 1.6+

Basic usage:

    >>> import markdown
    >>> text = "Some text with a WikiLink."
    >>> md = markdown.markdown(text, ['wikilink'])
    >>> md
    '\\n<p>Some text with a <a href="/WikiLink/" class="wikilink">WikiLink</a>.\\n</p>\\n\\n\\n'

To define custom settings the simple way:

    >>> md = markdown.markdown(text, 
    ...     ['wikilink(base_url=/wiki/,end_url=.html,html_class=foo)']
    ... )
    >>> md
    '\\n<p>Some text with a <a href="/wiki/WikiLink.html" class="foo">WikiLink</a>.\\n</p>\\n\\n\\n'
    
Custom settings the complex way:

    >>> md = markdown.Markdown(text, 
    ...     extensions = ['wikilink'], 
    ...     extension_configs = {'wikilink': [
    ...                                 ('base_url', 'http://example.com/'), 
    ...                                 ('end_url', '.html'),
    ...                                 ('html_class', '') ]},
    ...     encoding='utf8',
    ...     safe_mode = True)
    >>> str(md)
    '\\n<p>Some text with a <a href="http://example.com/WikiLink.html">WikiLink</a>.\\n</p>\\n\\n\\n'

From the command line:

    python markdown.py -x wikilink(base_url=http://example.com/,end_url=.html,html_class=foo) src.txt

By [Waylan Limberg](http://achinghead.com/).

Project website: http://achinghead.com/markdown-wikilinks/
Contact: waylan [at] gmail [dot] com

License: [BSD](http://www.opensource.org/licenses/bsd-license.php) 

Version: 0.4 (Oct 14, 2006)

Dependencies:
* [Python 2.3+](http://python.org)
* [Markdown 1.6+](http://www.freewisdom.org/projects/python-markdown/)
* For older dependencies use [WikiLink Version 0.3]
(http://code.limberg.name/svn/projects/py-markdown-ext/wikilinks/tags/release-0.3/)
'''

import markdown

class WikiLinkExtension (markdown.Extension) :
    def __init__(self, configs):
        # set extension defaults
        self.config = {
                        'base_url' : ['/', 'String to append to beginning or URL.'],
                        'end_url' : ['/', 'String to append to end of URL.'],
                        'html_class' : ['wikilink', 'CSS hook. Leave blank for none.']
        }
        
        # Override defaults with user settings
        for key, value in configs :
            # self.config[key][0] = value
            self.setConfig(key, value)
        
    def extendMarkdown(self, md, md_globals):
        self.md = md
        #md.registerExtension(self) #???
    
        # append to end of inline patterns
        WIKILINK_RE = r'''(?P<escape>\\|\b)(?P<camelcase>([A-Z]+[a-z-_]+){2,})\b'''
        md.inlinePatterns.append(WikiLinks(WIKILINK_RE, self.config))  

class WikiLinks (markdown.BasePattern) :
    def __init__(self, pattern, config):
        markdown.BasePattern.__init__(self, pattern)
        self.config = config
  
    def handleMatch(self, m, doc) :
        if  m.group('escape') == '\\':
            a = doc.createTextNode(m.group('camelcase'))
        else :
            url = '%s%s%s'% (self.config['base_url'][0], m.group('camelcase'), self.config['end_url'][0])
            label = m.group('camelcase').replace('_', ' ')
            a = doc.createElement('a')
            a.appendChild(doc.createTextNode(label))
            a.setAttribute('href', url)
            if self.config['html_class'][0] :
                a.setAttribute('class', self.config['html_class'][0])
        return a
    
def makeExtension(configs=None) :
    return WikiLinkExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()