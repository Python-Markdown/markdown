"""
example:

```python
md_text = "How ~~is a~~ nice weather!"
md = markdown.Markdown(['extra', 'smart_del'])
html = md.convert(text)
print(html)
# <p>How <del>is a</del> nice weather!</p>
```

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import SimpleTagPattern

DEL_RE = r'(\~{2})(.+?)\2'


class SmartEmphasisExtension(Extension):
    """ Add smart_emphasis extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """ Modify inline patterns. """
        md.inlinePatterns['del'] = SimpleTagPattern(DEL_RE, 'del')


def makeExtension(*args, **kwargs):
    return SmartEmphasisExtension(*args, **kwargs)
