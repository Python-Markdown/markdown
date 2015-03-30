"""
Legacy Attributes Extension
===========================

An extension to Python Markdown which implements legacy attributes.

Prior to Python-Markdown version 3.0, the Markdown class had an `enable_attributes`
keyword which was on by default and provided for attributes to be defined for elements
using the format `{@key=value}`. This extension is provided as a replacement for
backward compatability. New documents should be authored using attr_lists. However,
numerious documents exist which have been using the old attribute format for many
years. This extension can be used to continue to render those documents correctly.
"""

import re
from markdown.treeprocessors import Treeprocessor, isString
from markdown.extensions import Extension


ATTR_RE = re.compile("\{@([^\}]*)=([^\}]*)}")  # {@id=123}


class LegacyAttrs(Treeprocessor):
    def run(self, doc):
        """Find and set values of attributes ({@key=value}). """
        for el in doc.iter():
            alt = el.get('alt', None)
            if alt is not None:
                el.set('alt', self.handleAttributes(el, alt))
            if el.text and isString(el.text):
                el.text = self.handleAttributes(el, el.text)
            if el.tail and isString(el.tail):
                el.tail = self.handleAttributes(el, el.tail)

    def handleAttributes(self, el, txt):
        """ Set attributes and return text without definitions. """
        def attributeCallback(match):
            el.set(match.group(1), match.group(2).replace('\n', ' '))
        return ATTR_RE.sub(attributeCallback, txt)


class LegacyAttrExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        la = LegacyAttrs(md)
        md.treeprocessors.add('legacyattrs', la, '>inline')


def makeExtension(**kwargs):  # pragma: no cover
    return LegacyAttrExtension(**kwargs)
