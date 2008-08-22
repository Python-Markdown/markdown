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
    u'<p>Some text with a <a href="/WikiLink/" class="wikilink">WikiLink</a>.\\n</p>'

To define custom settings the simple way:

    >>> md = markdown.markdown(text, 
    ...     ['wikilink(base_url=/wiki/,end_url=.html,html_class=foo)']
    ... )
    >>> md
    u'<p>Some text with a <a href="/wiki/WikiLink.html" class="foo">WikiLink</a>.\\n</p>'
    
Custom settings the complex way:

    >>> md = markdown.Markdown(
    ...     extensions = ['wikilink'], 
    ...     extension_configs = {'wikilink': [
    ...                                 ('base_url', 'http://example.com/'), 
    ...                                 ('end_url', '.html'),
    ...                                 ('html_class', '') ]},
    ...     safe_mode = True)
    >>> md.convert(text)
    u'<p>Some text with a <a href="http://example.com/WikiLink.html">WikiLink</a>.\\n</p>'

Use MetaData with mdx_meta.py (Note the blank html_class in MetaData):

    >>> text = """wiki_base_url: http://example.com/
    ... wiki_end_url:   .html
    ... wiki_html_class:
    ...
    ... Some text with a WikiLink."""
    >>> md = markdown.Markdown(extensions=['meta', 'wikilink'])
    >>> md.convert(text)
    u'<p>Some text with a <a href="http://example.com/WikiLink.html">WikiLink</a>.\\n</p>'

MetaData should not carry over to next document:

    >>> md.convert("No MetaData here.")
    u'<p>No <a href="/MetaData/" class="wikilink">MetaData</a> here.\\n</p>'

From the command line:

    python markdown.py -x wikilink(base_url=http://example.com/,end_url=.html,html_class=foo) src.txt

By [Waylan Limberg](http://achinghead.com/).

Project website: http://achinghead.com/markdown-wikilinks/
Contact: waylan [at] gmail [dot] com

License: [BSD](http://www.opensource.org/licenses/bsd-license.php) 

Version: 0.6 (May 2, 2008)

Dependencies:
* [Python 2.3+](http://python.org)
* [Markdown 1.6+](http://www.freewisdom.org/projects/python-markdown/)
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
            self.setConfig(key, value)
        
    def extendMarkdown(self, md, md_globals):
        self.md = md
    
        # append to end of inline patterns
        WIKILINK_RE = r'''(?P<escape>\\|\b)(?P<camelcase>([A-Z]+[a-z-_]+){2,})\b'''
        WIKILINK_PATTERN = WikiLinks(WIKILINK_RE, self.config)
        WIKILINK_PATTERN.md = md
        md.inlinePatterns.append(WIKILINK_PATTERN)  
        

class WikiLinks (markdown.BasePattern) :
    def __init__(self, pattern, config):
        markdown.BasePattern.__init__(self, pattern)
        self.config = config
  
    def handleMatch(self, m):
        if  m.group('escape') == '\\':
            a = m.group('camelcase')
        else:
            base_url, end_url, html_class = self._getMeta()
            url = '%s%s%s'% (base_url, m.group('camelcase'), end_url)
            label = m.group('camelcase').replace('_', ' ')
            a = markdown.etree.Element('a')
            a.text = markdown.AtomicString(label)
            a.set('href', url)
            if html_class:
                a.set('class', html_class)
        return a

    def _getMeta(self):
        """ Return meta data or config data. """
        base_url = self.config['base_url'][0]
        end_url = self.config['end_url'][0]
        html_class = self.config['html_class'][0]
        if hasattr(self.md, 'Meta'):
            if self.md.Meta.has_key('wiki_base_url'):
                base_url = self.md.Meta['wiki_base_url'][0]
            if self.md.Meta.has_key('wiki_end_url'):
                end_url = self.md.Meta['wiki_end_url'][0]
            if self.md.Meta.has_key('wiki_html_class'):
                html_class = self.md.Meta['wiki_html_class'][0]
        return base_url, end_url, html_class
    
    def type(self):
        return "WLink"


def makeExtension(configs=None) :
    return WikiLinkExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

