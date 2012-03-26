#!usr/bin/python

'''
Image width and height attributes
=================================

This extension adds the capability to set image size attrivutes in markdown
when using reference style images.

Currently it supports single or double quoted titles, just like regular
reference style images. Unlike standard markdown, it does not support
parenthesized titles.

Basic usage:

    >>> import markdown
    >>> text = """
    ... ![image][]
    ... [image]: http://example.net/image.jpg height=800 width=600
    ... """
    >>> html = markdown.markdown(text, ['image_attr'])
    >>> print html
    <p><img alt="image" height="800" src="http://example.net/image.jpg" width="600" /></p>

Single quoted title:
    >>> import markdown
    >>> text = """
    ... ![image][]
    ... [image]: http://example.net/image.jpg 'title' height=800 width=600
    ... """
    >>> html = markdown.markdown(text, ['image_attr'])
    >>> print html
    <p><img alt="image" height="800" src="http://example.net/image.jpg" title="title" width="600" /></p>

Double quoted title:
    >>> import markdown
    >>> text = """
    ... ![image][]
    ... [image]: http://example.net/image.jpg "title" height=800 width=600
    ... """
    >>> html = markdown.markdown(text, ['image_attr'])
    >>> print html
    <p><img alt="image" height="800" src="http://example.net/image.jpg" title="title" width="600" /></p>

Double Quoted title which includes single quotes:
    >>> import markdown
    >>> text = """
    ... ![image][]
    ... [image]: http://example.net/image.jpg "title: 'Title'" height=800 width=600
    ... """
    >>> html = markdown.markdown(text, ['image_attr'])
    >>> print html
    <p><img alt="image" height="800" src="http://example.net/image.jpg" title="title: 'Title'" width="600" /></p>

Single Quoted title which includes double quotes:
    >>> import markdown
    >>> text = """
    ... ![image][]
    ... [image]: http://example.net/image.jpg 'title: "Title"' height=800 width=600
    ... """
    >>> html = markdown.markdown(text, ['image_attr'])
    >>> print html
    <p><img alt="image" height="800" src="http://example.net/image.jpg" title="title: &quot;Title&quot;" width="600" /></p>
'''

import re

import markdown
from markdown.util import etree
from markdown.inlinepatterns import IMAGE_REFERENCE_RE

ID_RE = re.compile(r'^[ ]{0,3}\[([^]]+)\]:\s*(\S+)\s+(.*)', re.DOTALL)
TITLE_RE = re.compile(r'(["\'])((?:(?!\1)[^\\]|\\.)*)\1\s*(.*)$', re.DOTALL)
TUPLE_RE = re.compile(r'(\S+)=(\S+)', re.DOTALL)
WHITELISTED_ATTRIBUTES = ['width', 'height']

class ImageAttrExtension(markdown.Extension):
    """Image Attributes extension for Python-Markdown."""
    references = dict()
    def __init__(self, configs={}):
        self.safeMode = True
        markdown.Extension.__init__(self, configs)
    def extendMarkdown(self, md, md_globals):
        """Add ImageAttrPreprocessor and ImageAttrPattern to Markdown
        instance."""
        md.preprocessors.add("image_attr", ImageAttrPreprocessor(md), "<reference")
        md.inlinePatterns.add("image_attr", ImageAttrPattern(IMAGE_REFERENCE_RE,
                                                             self), "<reference")


class ImageAttrPreprocessor(markdown.preprocessors.Preprocessor):
    """Extract Images with Attributes."""
    def run(self, lines):
        remaining_lines = []
        for line in lines:
            id = None
            link = None
            title = None
            attributes = []

            # Extract the id & link & "rest"
            m0 = ID_RE.match(line)
            if m0:
                id = m0.group(1).strip().lower()
                link = m0.group(2).lstrip('<').rstrip('>')

                # Attempt to extract a quotedtitle from "rest"
                m1 = TITLE_RE.match(m0.group(3).strip())
                if m1:
                    title = m1.group(2).strip()
                    # scan for key=value pairs as attributes
                    attributes = TUPLE_RE.findall(m1.group(3).strip())
                else:
                    # if there was no quoted string, scan for key=value pairs
                    # as attributes anyway
                    attributes = TUPLE_RE.findall(m0.group(3).strip())

            # Only allow whitelisted attributes to be set in this manner
            for attr in attributes:
                if attr[0] not in WHITELISTED_ATTRIBUTES:
                    attributes = []

            # Only handle the case where we found attributes in this
            # preprocessor. The standard reference preprocessor will catch
            # everything else
            if len(attributes) > 0:
                ImageAttrExtension.references[id] = (link, title, attributes)
            else:
                remaining_lines.append(line)

        return remaining_lines

class ImageAttrPattern(markdown.inlinepatterns.ImageReferencePattern):
    """Convert anything that matches the standard image reference pattern
    whose reference includes attrivutes to the proper image markup, including
    the attributes."""
    def handleMatch(self, m):
        """Handle the same situation as the standard ImageReferencePattern, but
        extract the reference information from the extension, and extract the
        attributes as well."""
        try:
            id = m.group(9).lower()
        except IndexError:
            id = None
        if not id:
            # if we got something like "[Google][]" or "[Goggle]"
            # we'll use "google" as the id
            id = m.group(2).lower()

        # Clean up linebreaks in id
        id = self.NEWLINE_CLEANUP_RE.sub(' ', id)
        if not id in self.markdown.references: # ignore undefined refs
            return None
        href, title, attributes = self.markdown.references[id]

        text = m.group(2)
        return self.makeTag(href, title, text, attributes)

    def makeTag(self, href, title, text, attributes):
        """Create the img element, add attributes"""
        el = etree.Element("img")
        el.set("src", self.sanitize_url(href))
        if title:
            el.set("title", title)
        el.set("alt", text)
        for attr in attributes:
            el.set(attr[0], attr[1])
        return el

def makeExtension(configs={}):
    return ImageAttrExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
