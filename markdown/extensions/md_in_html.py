"""
Python-Markdown Markdown in HTML Extension
===============================

An implementation of [PHP Markdown Extra](http://michelf.com/projects/php-markdown/extra/)'s
parsing of Markdown syntax in raw HTML.

See <https://Python-Markdown.github.io/extensions/raw_html>
for documentation.

Copyright The Python Markdown Project

License: [BSD](https://opensource.org/licenses/bsd-license.php)

"""

from . import Extension
from ..blockprocessors import BlockProcessor
from ..preprocessors import Preprocessor
from .. import util
from ..htmlparser import HTMLExtractor
import xml.etree.ElementTree as etree


# Block-level tags in which the content only gets span level parsing
span_tags = ['address', 'dd', 'dt', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'legend', 'li', 'p', 'td', 'th']

# Block-level tags in which the content gets parsed as blocks
block_tags = [
    'address', 'article', 'aside', 'blockquote', 'body', 'colgroup', 'details', 'div', 'dl', 'fieldset',
    'figcaption', 'figure', 'footer', 'form', 'iframe', 'header', 'hr', 'main', 'menu', 'nav',  'map',
    'noscript', 'object', 'ol', 'section', 'table', 'tbody', 'thead', 'tfoot', 'tr', 'ul'
]

# Block-level tags which never get their content parsed.
raw_tags = ['canvas', 'math', 'option', 'pre', 'script', 'style', 'textarea']

block_level_tags = span_tags + block_tags + raw_tags


class HTMLExtractorExtra(HTMLExtractor):
    """
    Override HTMLExtractor and create etree Elements for any elements which should have content parsed as Markdown.
    """

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.mdstack = []  # When markdown=1, stack contains a list of tags
        self.treebuilder = etree.TreeBuilder()
        self.mdstate = []  # one of 'block', 'span', 'off', or None
        super().reset()

    def close(self):
        """Handle any buffered data."""
        super().close()
        # Handle any unclosed tags.
        if self.mdstack:
            # Close the outermost parent. handle_endtag will close all unclosed children.
            self.handle_endtag(self.mdstack[0])

    def get_element(self):
        """ Return element from treebuilder and reset treebuilder for later use. """
        element = self.treebuilder.close()
        self.treebuilder = etree.TreeBuilder()
        return element

    def get_state(self, tag, attrs):
        """ Return state from tag and `markdown` attr. One of 'block', 'span', or 'off'. """
        md_attr = attrs.get('markdown', '0')
        if md_attr == 'markdown':
            # `<tag markdown>` is the same as `<tag markdown='1'>`.
            md_attr = '1'
        parent_state = self.mdstate[-1] if self.mdstate else None
        if parent_state == 'off' or (parent_state == 'span' and md_attr != '0'):
            # Only use the parent state if it is more restrictive than the markdown attribute.
            md_attr = parent_state
        if ((md_attr == '1' and tag in block_tags) or
                (md_attr == 'block' and tag in span_tags + block_tags)):
            return 'block'
        elif ((md_attr == '1' and tag in span_tags) or
              (md_attr == 'span' and tag in span_tags + block_tags)):
            return 'span'
        elif tag in block_level_tags:
            return 'off'
        else:  # pragma: no cover
            return None

    def handle_starttag(self, tag, attrs):
        if tag in block_level_tags:
            # Valueless attr (ex: `<tag checked>`) results in `[('checked', None)]`.
            # Convert to `{'checked': 'checked'}`.
            attrs = {key: value if value is not None else key for key, value in attrs}
            state = self.get_state(tag, attrs)

            if self.inraw or (state in [None, 'off'] and not self.mdstack):
                # fall back to default behavior
                attrs.pop('markdown', None)
                super().handle_starttag(tag, attrs)
            else:
                if 'p' in self.mdstack and tag in block_level_tags:
                    # Close unclosed 'p' tag
                    self.handle_endtag('p')
                self.mdstate.append(state)
                self.mdstack.append(tag)
                attrs['markdown'] = state
                self.treebuilder.start(tag, attrs)
        else:
            # Span level tag
            if self.inraw:
                super().handle_starttag(tag, attrs)
            else:
                text = self.get_starttag_text()
                self.handle_data(text)

    def handle_endtag(self, tag):
        if tag in block_level_tags:
            if self.inraw:
                super().handle_endtag(tag)
            elif tag in self.mdstack:
                # Close element and any unclosed children
                while self.mdstack:
                    item = self.mdstack.pop()
                    self.mdstate.pop()
                    self.treebuilder.end(item)
                    if item == tag:
                        break
                if not self.mdstack:
                    # Last item in stack is closed. Stash it
                    element = self.get_element()
                    self.cleandoc.append(self.md.htmlStash.store(element))
                    self.cleandoc.append('\n\n')
                    self.state = []
            else:
                # Treat orphan closing tag as a span level tag.
                text = self.get_endtag_text(tag)
                self.handle_data(text)
        else:
            # Span level tag
            if self.inraw:
                super().handle_endtag(tag)
            else:
                text = self.get_endtag_text(tag)
                self.handle_data(text)

    def handle_data(self, data):
        if self.inraw or not self.mdstack:
            super().handle_data(data)
        else:
            self.treebuilder.data(data)

    def handle_empty_tag(self, data, is_block):
        if self.inraw or not self.mdstack:
            super().handle_empty_tag(data, is_block)
        else:
            if self.at_line_start() and is_block:
                self.handle_data('\n' + self.md.htmlStash.store(data) + '\n\n')
            else:
                self.handle_data(data)


class HtmlBlockPreprocessor(Preprocessor):
    """Remove html blocks from the text and store them for later retrieval."""

    def run(self, lines):
        source = '\n'.join(lines)
        parser = HTMLExtractorExtra(self.md)
        parser.feed(source)
        parser.close()
        return ''.join(parser.cleandoc).split('\n')


class MarkdownInHtmlProcessor(BlockProcessor):
    """Process Markdown Inside HTML Blocks which have been stored in the HtmlStash."""

    def test(self, parent, block):
        # ALways return True. `run` will return `False` it not a valid match.
        return True

    def parse_element_content(self, element):
        """
        Resursively parse the text content of an etree Element as Markdown.

        Any block level elements generated from the Markdown will be inserted as children of the element in place
        of the text content. All `markdown` attributes are removed. For any elements in which Markdown parsing has
        been dissabled, the text content of it and its chidlren are wrapped in an `AtomicString`.
        """

        md_attr = element.attrib.pop('markdown', 'off')

        if md_attr == 'block':
            # Parse content as block level
            # The order in which the different parts are parsed (text, children, tails) is important here as the
            # order of elements needs to be preserved. We can't be inserting items at a later point in the current
            # iteration as we don't want to do raw processing on elements created from parsing Markdown text (for
            # example). Therefore, the order of operations is children, tails, text.

            # Recursively parse existing children from raw HTML
            for child in list(element):
                self.parse_element_content(child)

            # Parse Markdown text in tail of children. Do this seperate to avoid raw HTML parsing.
            # Save the position of each item to be inserted later in reverse.
            tails = []
            for pos, child in enumerate(element):
                if child.tail:
                    block = child.tail.rstrip('\n')
                    child.tail = ''
                    # Use a dummy placeholder element.
                    dummy = etree.Element('div')
                    self.parser.parseBlocks(dummy, block.split('\n\n'))
                    children = list(dummy)
                    children.reverse()
                    tails.append((pos + 1, children))

            # Insert the elements created from the tails in reverse.
            tails.reverse()
            for pos, tail in tails:
                for item in tail:
                    element.insert(pos, item)

            # Parse Markdown text content. Do this last to avoid raw HTML parsing.
            if element.text:
                block = element.text.rstrip('\n')
                element.text = ''
                # Use a dummy placeholder element as the content needs to get inserted before existing children.
                dummy = etree.Element('div')
                self.parser.parseBlocks(dummy, block.split('\n\n'))
                children = list(dummy)
                children.reverse()
                for child in children:
                    element.insert(0, child)

        elif md_attr == 'span':
            # Span level parsing will be handled by inlineprocessors.
            # Walk children here to remove any `markdown` attributes.
            for child in list(element):
                self.parse_element_content(child)

        else:
            # Disable inline parsing for everything else
            element.text = util.AtomicString(element.text)
            for child in list(element):
                self.parse_element_content(child)
                if child.tail:
                    child.tail = util.AtomicString(child.tail)

    def run(self, parent, blocks):
        m = util.HTML_PLACEHOLDER_RE.match(blocks[0])
        if m:
            index = int(m.group(1))
            element = self.parser.md.htmlStash.rawHtmlBlocks[index]
            if isinstance(element, etree.Element):
                # We have a matched element. Process it.
                blocks.pop(0)
                self.parse_element_content(element)
                parent.append(element)
                # Cleanup stash. Replace element with empty string to avoid confusing postprocessor.
                self.parser.md.htmlStash.rawHtmlBlocks.pop(index)
                self.parser.md.htmlStash.rawHtmlBlocks.insert(index, '')
                # Comfirm the match to the blockparser.
                return True
        # No match found.
        return False


class MarkdownInHtmlExtension(Extension):
    """Add Markdown parsing in HTML to Markdown class."""

    def extendMarkdown(self, md):
        """ Register extension instances. """

        # Replace raw HTML preprocessor
        md.preprocessors.register(HtmlBlockPreprocessor(md), 'html_block', 20)
        # Add blockprocessor which handles the placeholders for etree elements
        md.parser.blockprocessors.register(
            MarkdownInHtmlProcessor(md.parser), 'markdown_block', 105
        )


def makeExtension(**kwargs):  # pragma: no cover
    return MarkdownInHtmlExtension(**kwargs)
