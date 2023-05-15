"""
Badge extension for Python-Markdown
========================================

Adds support for badges to Python-Markdown.

See <https://Python-Markdown.github.io/extensions/badge>
for documentation.

Original code Copyright [Tiago Serafim](https://www.tiagoserafim.com/).

All changes Copyright The Python Markdown Project

License: [BSD](https://opensource.org/licenses/bsd-license.php)

"""

from . import Extension
from ..inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
import re

BADGE_RE = r'\{\{ ?([\w\-]+(?: +[\w\-]+)*)(?: +"(.*?)")? *\}\}'

class BadgeExtension(Extension):
    """ Badge extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Add Badge to Markdown instance. """
        md.registerExtension(self)

        md.inlinePatterns.register(BadgeInlineProcessor(BADGE_RE, md), 'badge', 215)


class BadgeInlineProcessor(InlineProcessor):
    """ Badge inline pattern. """
    CLASSNAME = 'badge'
    CLASSNAME_TITLE = 'badge-title'
    RE_SPACES = re.compile('  +')

    def __init__(self, pattern, title):
        super().__init__(pattern)
        self.tag = "span"

    def handleMatch(self, m, data):
        klass, title = self.get_class_and_title(m)
        el = etree.Element(self.tag)
        el.set('class', '{} {}'.format(self.CLASSNAME, klass))
        if title:
            badge = etree.SubElement(el, self.tag)
            badge.text = title
            badge.set('class', self.CLASSNAME_TITLE)

        return el, m.start(0), m.end(0)

    def get_class_and_title(self, match):
        klass, title = match.group(1).lower(), match.group(2)
        klass = self.RE_SPACES.sub(' ', klass)
        if title is None:
            # no title was provided, use the capitalized class name as title
            # e.g.: `{{ note }}` will render
            # `<span class="badge-title">Note</span>`
            title = klass.split(' ', 1)[0].capitalize()
        elif title == '':
            # an explicit blank title should not be rendered
            # e.g.: `{{ warning "" }}` will *not* render `span` with a title
            title = None
        return klass, title

def makeExtension(**kwargs):  # pragma: no cover
    return BadgeExtension(**kwargs)
