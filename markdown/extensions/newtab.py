"""
New Tab Extension for Python-Markdown
=====================================

Modify the behavior of Links in Python-Markdown to open a in a new
window. This changes the HTML output to add target="_blank" to all
generated links.
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..inlinepatterns import \
    LinkPattern, ReferencePattern, AutolinkPattern, AutomailPattern, \
    LINK_RE, SHORT_REF_RE, AUTOLINK_RE, AUTOMAIL_RE

def openNewTab(el):
    el.set("target", "_blank")
    return el

class NewTabLinkPattern(LinkPattern):
    def handleMatch(self, m):
        return openNewTab(super().handleMatch(m))

class NewTabReferencePattern(ReferencePattern):
    def handleMatch(self, m):
        return openNewTab(super().handleMatch(m))

class NewTabAutolinkPattern(AutolinkPattern):
    def handleMatch(self, m):
        return openNewTab(super().handleMatch(m))

class NewTabAutomailPattern(AutomailPattern):
    def handleMatch(self, m):
        return openNewTab(super().handleMatch(m))

class NewTabExtension(Extension):
    """Modifies HTML output to open links in a new tab."""
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns["link"] = \
            NewTabLinkPattern(LINK_RE, md)
        md.inlinePatterns["short_reference"] = \
            NewTabReferencePattern(SHORT_REF_RE, md)
        md.inlinePatterns["autolink"] = \
            NewTabAutolinkPattern(AUTOLINK_RE, md)
        md.inlinePatterns["automail"] = \
            NewTabAutomailPattern(AUTOMAIL_RE, md)

def makeExtension(configs = {}):
    return NewTabExtension(configs = configs)

