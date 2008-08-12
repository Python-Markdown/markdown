#!usr/bin/python

'''
Meta Data Extension for Python-Markdown
==========================================

This extension adds Meta Data handling to markdown.

    >>> import markdown
    >>> text = """Title: A Test Doc.
    ... Author: Waylan Limberg
    ...         John Doe
    ... Blank_Data:
    ...
    ... The body. This is paragraph one.
    ... """
    >>> md = markdown.Markdown(text, ['meta'])
    >>> md.convert()
    u'<p>The body. This is paragraph one.\\n</p>'
    >>> md.Meta
    {u'blank_data': [u''], u'author': [u'Waylan Limberg', u'John Doe'], u'title': [u'A Test Doc.']}

Make sure text without Meta Data still works (markdown < 1.6b returns a <p>).

    >>> text = '    Some Code - not extra lines of meta data.'
    >>> md = markdown.Markdown(text, ['meta'])
    >>> md.convert()
    u'<pre><code>Some Code - not extra lines of meta data.\\n</code></pre>'
    >>> md.Meta
    {}

'''

import markdown, re

# Global Vars
META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')
META_MORE_RE = re.compile(r'^[ ]{4,}(?P<value>.*)')

class MetaExtension (markdown.Extension) :
    def __init__(self, configs):
        pass

    def extendMarkdown(self, md, md_globals) :
        self.md = md

        # Insert meta preprocessor first
        META_PREPROCESSOR = MetaPreprocessor()
        META_PREPROCESSOR.md = md
        md.preprocessors.insert(0, META_PREPROCESSOR)
        
class MetaPreprocessor(markdown.Preprocessor) :
    def run(self, lines) :
        meta = {}
        key = None
        while 1:
            line = lines.pop(0)
            if line.strip() == '':
                break # blank line - done
            m1 = META_RE.match(line)
            if m1:
                key = m1.group('key').lower().strip()
                meta[key] = [m1.group('value').strip()]
            else:
                m2 = META_MORE_RE.match(line)
                if m2 and key:
                    # Add another line to existing key
                    meta[key].append(m2.group('value').strip())
                else:
                    lines.insert(0, line)
                    break # no meta data - done
        self.md.Meta = meta
        return lines
        

def makeExtension(configs=None) :
    return MetaExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
