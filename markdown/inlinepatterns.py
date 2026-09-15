# Python Markdown

# A Python implementation of John Gruber's Markdown.

# Documentation: https://python-markdown.github.io/
# GitHub: https://github.com/Python-Markdown/markdown/
# PyPI: https://pypi.org/project/Markdown/

# Started by Manfred Stienstra (http://www.dwerg.net/).
# Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
# Currently maintained by Waylan Limberg (https://github.com/waylan),
# Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

# Copyright 2007-2023 The Python Markdown Project (v. 1.7 and later)
# Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
# Copyright 2004 Manfred Stienstra (the original version)

# License: BSD (see LICENSE.md for details).

"""
In version 3.0, a new, more flexible inline processor was added, [`markdown.inlinepatterns.InlineProcessor`][].   The
original inline patterns, which inherit from [`markdown.inlinepatterns.Pattern`][] or one of its children are still
supported, though users are encouraged to migrate.

The new `InlineProcessor` provides two major enhancements to `Patterns`:

1. Inline Processors no longer need to match the entire block, so regular expressions no longer need to start with
  `r'^(.*?)'` and end with `r'(.*?)%'`. This runs faster. The returned [`Match`][re.Match] object will only contain
   what is explicitly matched in the pattern, and extension pattern groups now start with `m.group(1)`.

2.  The `handleMatch` method now takes an additional input called `data`, which is the entire block under analysis,
    not just what is matched with the specified pattern. The method now returns the element *and* the indexes relative
    to `data` that the return element is replacing (usually `m.start(0)` and `m.end(0)`).  If the boundaries are
    returned as `None`, it is assumed that the match did not take place, and nothing will be altered in `data`.

    This allows handling of more complex constructs than regular expressions can handle, e.g., matching nested
    brackets, and explicit control of the span "consumed" by the processor.

"""

from __future__ import annotations

from . import util
from typing import TYPE_CHECKING, Any, Collection, NamedTuple, cast
from collections import deque
import re
import xml.etree.ElementTree as etree
from html import entities

if TYPE_CHECKING:  # pragma: no cover
    from markdown import Markdown


def build_inlinepatterns(md: Markdown, **kwargs: Any) -> util.Registry[InlineProcessor]:
    """
    Build the default set of inline patterns for Markdown.

    The order in which processors and/or patterns are applied is very important - e.g. if we first replace
    `http://.../` links with `<a>` tags and _then_ try to replace inline HTML, we would end up with a mess. So, we
    apply the expressions in the following order:

    * backticks and escaped characters have to be handled before everything else so that we can preempt any markdown
      patterns by escaping them;

    * then we handle the various types of links (auto-links must be handled before inline HTML);

    * then we handle inline HTML.  At this point we will simply replace all inline HTML strings with a placeholder
      and add the actual HTML to a stash;

    * finally we apply strong, emphasis, etc.

    """
    inlinePatterns = util.Registry()
    inlinePatterns.register(BacktickInlineProcessor(BACKTICK_RE), 'backtick', 190)
    inlinePatterns.register(EscapeInlineProcessor(ESCAPE_RE, md), 'escape', 180)
    inlinePatterns.register(ReferenceInlineProcessor(REFERENCE_RE, md), 'reference', 170)
    inlinePatterns.register(LinkInlineProcessor(LINK_RE, md), 'link', 160)
    inlinePatterns.register(ImageInlineProcessor(IMAGE_LINK_RE, md), 'image_link', 150)
    inlinePatterns.register(
        ImageReferenceInlineProcessor(IMAGE_REFERENCE_RE, md), 'image_reference', 140
    )
    inlinePatterns.register(
        ShortReferenceInlineProcessor(REFERENCE_RE, md), 'short_reference', 130
    )
    inlinePatterns.register(
        ShortImageReferenceInlineProcessor(IMAGE_REFERENCE_RE, md), 'short_image_ref', 125
    )
    inlinePatterns.register(AutolinkInlineProcessor(AUTOLINK_RE, md), 'autolink', 120)
    inlinePatterns.register(AutomailInlineProcessor(AUTOMAIL_RE, md), 'automail', 110)
    inlinePatterns.register(SubstituteTagInlineProcessor(LINE_BREAK_RE, 'br'), 'linebreak', 100)
    inlinePatterns.register(HtmlInlineProcessor(HTML_RE, md), 'html', 90)
    inlinePatterns.register(HtmlInlineProcessor(ENTITY_RE, md), 'entity', 80)
    inlinePatterns.register(DelimiterProcessor('*', 'strong,em', md), 'em_strong', 60)
    md.delimiters.add('_', 'strong,em', smart=True)
    return inlinePatterns


# The actual regular expressions for patterns
# -----------------------------------------------------------------------------

NOIMG = r'(?<!\!)'
""" Match not an image. Partial regular expression which matches if not preceded by `!`. """

BACKTICK_RE = r'(?:(?<!\\)((?:\\{2})+)(?=`+)|(?<!\\)`)'
""" Match backtick quoted string (`` `e=f()` `` or ``` ``e=f("`")`` ```). """

ESCAPE_RE = r'\\(.)'
""" Match a backslash escaped character (`\\<` or `\\*`). """

LINK_RE = NOIMG + r'\['
""" Match start of in-line link (`[text](url)` or `[text](<url>)` or `[text](url "title")`). """

IMAGE_LINK_RE = r'\!\['
""" Match start of in-line image link (`![alttxt](url)` or `![alttxt](<url>)`). """

REFERENCE_RE = LINK_RE
""" Match start of reference link (`[Label][3]`). """

IMAGE_REFERENCE_RE = IMAGE_LINK_RE
""" Match start of image reference (`![alt text][2]`). """

AUTOLINK_RE = r'<((?:[Ff]|[Hh][Tt])[Tt][Pp][Ss]?://[^<>]*)>'
""" Match an automatic link (`<http://www.example.com>`). """

AUTOMAIL_RE = r'<([^<> !]+@[^@<> ]+)>'
""" Match an automatic email link (`<me@example.com>`). """

HTML_RE = (
    r'(<(\/?[a-zA-Z][^<>@ ]*( [^<>]*)?|'          # Tag
    r'!--(?:(?!<!--|-->).)*--|'                   # Comment
    r'[?](?:(?!<[?]|[?]>).)*[?]|'                 # Processing instruction
    r'!\[CDATA\[(?:(?!<!\[CDATA\[|\]\]>).)*\]\]'  # `CDATA`
    ')>)'
)
""" Match an HTML tag (`<...>`). """

ENTITY_RE = r'(&(?:\#[0-9]+|\#x[0-9a-fA-F]+|[a-zA-Z0-9]+);)'
""" Match an HTML entity (`&#38;` (decimal) or `&#x26;` (hex) or `&amp;` (named)). """

LINE_BREAK_RE = r'  \n'
""" Match two spaces at end of line. """


def dequote(string: str) -> str:
    """Remove quotes from around a string."""
    if ((string.startswith('"') and string.endswith('"')) or
       (string.startswith("'") and string.endswith("'"))):
        return string[1:-1]
    else:
        return string


class EmStrongItem(NamedTuple):
    """Emphasis/strong pattern item."""
    pattern: re.Pattern[str]
    builder: str
    tags: str


# The pattern classes
# -----------------------------------------------------------------------------


class Pattern:  # pragma: no cover
    """
    Base class that inline patterns subclass.

    Inline patterns are handled by means of `Pattern` subclasses, one per regular expression.
    Each pattern object uses a single regular expression and must support the following methods:
    [`getCompiledRegExp`][markdown.inlinepatterns.Pattern.getCompiledRegExp] and
    [`handleMatch`][markdown.inlinepatterns.Pattern.handleMatch].

    All the regular expressions used by `Pattern` subclasses must capture the whole block.  For this
    reason, they all start with `^(.*)` and end with `(.*)!`.  When passing a regular expression on
    class initialization, the `^(.*)` and `(.*)!` are added automatically and the regular expression
    is pre-compiled.

    It is strongly suggested that the newer style [`markdown.inlinepatterns.InlineProcessor`][] that
    use a more efficient and flexible search approach be used instead. However, the older style
    `Pattern` remains for backward compatibility with many existing third-party extensions.

    """

    ANCESTOR_EXCLUDES: Collection[str] = tuple()
    """
    A collection of elements which are undesirable ancestors. The processor will be skipped if it
    would cause the content to be a descendant of one of the listed tag names.
    """

    compiled_re: re.Pattern[str]
    md: Markdown | None

    def __init__(self, pattern: str, md: Markdown | None = None):
        """
        Create an instant of an inline pattern.

        Arguments:
            pattern: A regular expression that matches a pattern.
            md: An optional pointer to the instance of `markdown.Markdown` and is available as
                `self.md` on the class instance.


        """
        self.pattern = pattern
        self.compiled_re = re.compile(r"^(.*?)%s(.*)$" % pattern,
                                      re.DOTALL | re.UNICODE)

        self.md = md

    def getCompiledRegExp(self) -> re.Pattern:
        """ Return a compiled regular expression. """
        return self.compiled_re

    def handleMatch(self, m: re.Match[str]) -> etree.Element | str:
        """Return a ElementTree element from the given match.

        Subclasses should override this method.

        Arguments:
            m: A match object containing a match of the pattern.

        Returns: An ElementTree Element object.

        """
        pass  # pragma: no cover

    def type(self) -> str:
        """ Return class name, to define pattern type """
        return self.__class__.__name__

    def unescape(self, text: str) -> str:
        """ Return unescaped text given text with an inline placeholder. """
        try:
            stash = self.md.treeprocessors['inline'].stashed_nodes
        except KeyError:  # pragma: no cover
            return text

        def get_stash(m):
            id = m.group(1)
            if id in stash:
                value = stash.get(id)
                if isinstance(value, str):
                    return value
                else:
                    # An `etree` Element - return text content only
                    return ''.join(value.itertext())
        return util.INLINE_PLACEHOLDER_RE.sub(get_stash, text)


class InlineProcessor(Pattern):
    """
    Base class that inline processors subclass.

    This is the newer style inline processor that uses a more
    efficient and flexible search approach.

    """

    def __init__(self, pattern: str, md: Markdown | None = None):
        """
        Create an instant of an inline processor.

        Arguments:
            pattern: A regular expression that matches a pattern.
            md: An optional pointer to the instance of `markdown.Markdown` and is available as
                `self.md` on the class instance.

        """
        self.pattern = pattern
        self.compiled_re = re.compile(pattern, re.DOTALL | re.UNICODE)

        # API for Markdown to pass `safe_mode` into instance
        self.safe_mode = False
        self.md = md

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | str | None, int | None, int | None]:
        """Return a ElementTree element from the given match and the
        start and end index of the matched text.

        If `start` and/or `end` are returned as `None`, it will be
        assumed that the processor did not find a valid region of text.

        Subclasses should override this method.

        Arguments:
            m: A re match object containing a match of the pattern.
            data: The buffer currently under analysis.

        Returns:
            el: The ElementTree element, text or None.
            start: The start of the region that has been matched or None.
            end: The end of the region that has been matched or None.

        """
        pass  # pragma: no cover


class SimpleTextPattern(Pattern):  # pragma: no cover
    """ Return a simple text of `group(2)` of a Pattern. """
    def handleMatch(self, m: re.Match[str]) -> str:
        """ Return string content of `group(2)` of a matching pattern. """
        return m.group(2)


class SimpleTextInlineProcessor(InlineProcessor):
    """ Return a simple text of `group(1)` of a Pattern. """
    def handleMatch(self, m: re.Match[str], data: str) -> tuple[str, int, int]:
        """ Return string content of `group(1)` of a matching pattern. """
        return m.group(1), m.start(0), m.end(0)


class EscapeInlineProcessor(InlineProcessor):
    """ Return an escaped character. """

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[str | None, int, int]:
        """
        If the character matched by `group(1)` of a pattern is in [`ESCAPED_CHARS`][markdown.Markdown.ESCAPED_CHARS]
        then return the integer representing the character's Unicode code point (as returned by [`ord`][]) wrapped
        in [`util.STX`][markdown.util.STX] and [`util.ETX`][markdown.util.ETX].

        If the matched character is not in [`ESCAPED_CHARS`][markdown.Markdown.ESCAPED_CHARS], then return `None`.
        """

        char = m.group(1)
        if char in self.md.ESCAPED_CHARS:
            return '{}{}{}'.format(util.STX, ord(char), util.ETX), m.start(0), m.end(0)
        else:
            return None, m.start(0), m.end(0)


class SimpleTagPattern(Pattern):  # pragma: no cover
    """
    Return element of type `tag` with a text attribute of `group(3)`
    of a Pattern.

    """
    def __init__(self, pattern: str, tag: str):
        """
        Create an instant of an simple tag pattern.

        Arguments:
            pattern: A regular expression that matches a pattern.
            tag: Tag of element.

        """
        Pattern.__init__(self, pattern)
        self.tag = tag
        """ The tag of the rendered element. """

    def handleMatch(self, m: re.Match[str]) -> etree.Element:
        """
        Return [`Element`][xml.etree.ElementTree.Element] of type `tag` with the string in `group(3)` of a
        matching pattern as the Element's text.
        """
        el = etree.Element(self.tag)
        el.text = m.group(3)
        return el


class SimpleTagInlineProcessor(InlineProcessor):
    """
    Return element of type `tag` with a text attribute of `group(2)`
    of a Pattern.

    """
    def __init__(self, pattern: str, tag: str):
        """
        Create an instant of an simple tag processor.

        Arguments:
            pattern: A regular expression that matches a pattern.
            tag: Tag of element.

        """
        InlineProcessor.__init__(self, pattern)
        self.tag = tag
        """ The tag of the rendered element. """

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:  # pragma: no cover
        """
        Return [`Element`][xml.etree.ElementTree.Element] of type `tag` with the string in `group(2)` of a
        matching pattern as the Element's text.
        """
        el = etree.Element(self.tag)
        el.text = m.group(2)
        return el, m.start(0), m.end(0)


class SubstituteTagPattern(SimpleTagPattern):  # pragma: no cover
    """ Return an element of type `tag` with no children. """
    def handleMatch(self, m: re.Match[str]) -> etree.Element:
        """ Return empty [`Element`][xml.etree.ElementTree.Element] of type `tag`. """
        return etree.Element(self.tag)


class SubstituteTagInlineProcessor(SimpleTagInlineProcessor):
    """ Return an element of type `tag` with no children. """
    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:
        """ Return empty [`Element`][xml.etree.ElementTree.Element] of type `tag`. """
        return etree.Element(self.tag), m.start(0), m.end(0)


class BacktickInlineProcessor(InlineProcessor):
    """ Return a `<code>` element containing the escaped matching text. """

    def __init__(self, pattern: str):
        InlineProcessor.__init__(self, pattern)
        self.ESCAPED_BSLASH = '{}{}{}'.format(util.STX, ord('\\'), util.ETX)
        self.tag = 'code'
        """ The tag of the rendered element. """

    def find_code_spans(self, start: int, text: str) -> tuple[int, int] | None:
        """Find code spans."""

        last = len(text)

        # Get the maximum starting ticks
        max_ticks = 0
        while start < last and text[start] == '`':
            max_ticks += 1
            start += 1

        if not max_ticks:  # pragma: no cover
            # This is not ever expected to happen.
            return None

        longest_span = 0
        end = 0

        # Find an ending span of backticks that matches our opening
        i = start
        while i < last:
            span_length = 0
            while i < last and text[i] == '`':
                span_length += 1
                i += 1
            if not span_length:
                i += 1
                continue

            # Did we find the end?
            if max_ticks == span_length:
                return start, i - span_length

            # Track the longest span of backticks we find as a fallback.
            if span_length > longest_span:
                longest_span = span_length
                end = i

        # Since we didn't find an exact matching start and end,
        # adjust start to match the largest end we could calculate.
        if longest_span:
            return start - (max_ticks - longest_span), end - longest_span

        # We could not find a suitable pairing
        return None

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | str | None, int | None, int | None]:
        """
        If the match contains `group(3)` of a pattern, then return a `code`
        [`Element`][xml.etree.ElementTree.Element] which contains HTML escaped text (with
        [`code_escape`][markdown.util.code_escape]) as an [`AtomicString`][markdown.util.AtomicString].

        If the match contains `group(1)` then return the text of `group(1)` as backslash escaped.

        """
        if m.group(1):
            return m.group(1).replace('\\\\', self.ESCAPED_BSLASH), m.start(0), m.end(0)

        begin = m.start(0)
        result = self.find_code_spans(begin, data)
        if result is not None:
            start, end = result
            el = etree.Element(self.tag)
            el.text = util.AtomicString(util.code_escape(data[start:end].strip()))
            return el, begin, result[1] + (start - begin)
        return None, None, None


class DoubleTagPattern(SimpleTagPattern):  # pragma: no cover
    """Return a ElementTree element nested in tag2 nested in tag1.

    Useful for strong emphasis etc.

    """
    def handleMatch(self, m: re.Match[str]) -> etree.Element:
        """
        Return [`Element`][xml.etree.ElementTree.Element] in following format:
        `<tag1><tag2>group(3)</tag2>group(4)</tag2>` where `group(4)` is optional.

        """
        tag1, tag2 = self.tag.split(",")
        el1 = etree.Element(tag1)
        el2 = etree.SubElement(el1, tag2)
        el2.text = m.group(3)
        if len(m.groups()) == 5:
            el2.tail = m.group(4)
        return el1


class DoubleTagInlineProcessor(SimpleTagInlineProcessor):
    """Return a ElementTree element nested in tag2 nested in tag1.

    Useful for strong emphasis etc.

    """
    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:  # pragma: no cover
        """
        Return [`Element`][xml.etree.ElementTree.Element] in following format:
        `<tag1><tag2>group(2)</tag2>group(3)</tag2>` where `group(3)` is optional.

        """
        tag1, tag2 = self.tag.split(",")
        el1 = etree.Element(tag1)
        el2 = etree.SubElement(el1, tag2)
        el2.text = m.group(2)
        if len(m.groups()) == 3:
            el2.tail = m.group(3)
        return el1, m.start(0), m.end(0)


class HtmlInlineProcessor(InlineProcessor):
    """ Store raw inline html and return a placeholder. """
    def handleMatch(self, m: re.Match[str], data: str) -> tuple[str, int, int]:
        """ Store the text of `group(1)` of a pattern and return a placeholder string. """
        rawhtml = self.backslash_unescape(self.unescape(m.group(1)))
        place_holder = self.md.htmlStash.store(rawhtml)
        return place_holder, m.start(0), m.end(0)

    def unescape(self, text: str) -> str:
        """ Return unescaped text given text with an inline placeholder. """
        try:
            stash = self.md.treeprocessors['inline'].stashed_nodes
        except KeyError:  # pragma: no cover
            return text

        def get_stash(m: re.Match[str]) -> str:
            id = m.group(1)
            value = stash.get(id)
            if value is not None:
                try:
                    # Ensure we don't have a placeholder inside a placeholder
                    return self.unescape(self.md.serializer(value))
                except Exception:
                    return r'\%s' % value

        return util.INLINE_PLACEHOLDER_RE.sub(get_stash, text)

    def backslash_unescape(self, text: str) -> str:
        """ Return text with backslash escapes undone (backslashes are restored). """
        try:
            RE = self.md.treeprocessors['unescape'].RE
        except KeyError:  # pragma: no cover
            return text

        def _unescape(m: re.Match[str]) -> str:
            return chr(int(m.group(1)))

        return RE.sub(_unescape, text)


PUNCT = (
    b'!-/:-@\\[-`{-\\~\xc2\xa1-\xc2\xa9\xc2\xab-\xc2\xac\xc2\xae-\xc2\xb1\xc2\xb4\xc2\xb6-\xc2\xb8\xc2\xbb\xc2\xbf\xc3'
    b'\x97\xc3\xb7\xcb\x82-\xcb\x85\xcb\x92-\xcb\x9f\xcb\xa5-\xcb\xab\xcb\xad\xcb\xaf-\xcb\xbf\xcd\xb5\xcd\xbe\xce\x84'
    b'-\xce\x85\xce\x87\xcf\xb6\xd2\x82\xd5\x9a-\xd5\x9f\xd6\x89-\xd6\x8a\xd6\x8d-\xd6\x8f\xd6\xbe\xd7\x80\xd7\x83\xd7'
    b'\x86\xd7\xb3-\xd7\xb4\xd8\x86-\xd8\x8f\xd8\x9b\xd8\x9d-\xd8\x9f\xd9\xaa-\xd9\xad\xdb\x94\xdb\x9e\xdb\xa9\xdb\xbd'
    b'-\xdb\xbe\xdc\x80-\xdc\x8d\xdf\xb6-\xdf\xb9\xdf\xbe-\xdf\xbf\xe0\xa0\xb0-\xe0\xa0\xbe\xe0\xa1\x9e\xe0\xa2\x88'
    b'\xe0\xa5\xa4-\xe0\xa5\xa5\xe0\xa5\xb0\xe0\xa7\xb2-\xe0\xa7\xb3\xe0\xa7\xba-\xe0\xa7\xbb\xe0\xa7\xbd\xe0\xa9\xb6'
    b'\xe0\xab\xb0-\xe0\xab\xb1\xe0\xad\xb0\xe0\xaf\xb3-\xe0\xaf\xba\xe0\xb1\xb7\xe0\xb1\xbf\xe0\xb2\x84\xe0\xb5\x8f'
    b'\xe0\xb5\xb9\xe0\xb7\xb4\xe0\xb8\xbf\xe0\xb9\x8f\xe0\xb9\x9a-\xe0\xb9\x9b\xe0\xbc\x81-\xe0\xbc\x97\xe0\xbc\x9a-'
    b'\xe0\xbc\x9f\xe0\xbc\xb4\xe0\xbc\xb6\xe0\xbc\xb8\xe0\xbc\xba-\xe0\xbc\xbd\xe0\xbe\x85\xe0\xbe\xbe-\xe0\xbf\x85'
    b'\xe0\xbf\x87-\xe0\xbf\x8c\xe0\xbf\x8e-\xe0\xbf\x9a\xe1\x81\x8a-\xe1\x81\x8f\xe1\x82\x9e-\xe1\x82\x9f\xe1\x83\xbb'
    b'\xe1\x8d\xa0-\xe1\x8d\xa8\xe1\x8e\x90-\xe1\x8e\x99\xe1\x90\x80\xe1\x99\xad-\xe1\x99\xae\xe1\x9a\x9b-\xe1\x9a\x9c'
    b'\xe1\x9b\xab-\xe1\x9b\xad\xe1\x9c\xb5-\xe1\x9c\xb6\xe1\x9f\x94-\xe1\x9f\x96\xe1\x9f\x98-\xe1\x9f\x9b\xe1\xa0\x80'
    b'-\xe1\xa0\x8a\xe1\xa5\x80\xe1\xa5\x84-\xe1\xa5\x85\xe1\xa7\x9e-\xe1\xa7\xbf\xe1\xa8\x9e-\xe1\xa8\x9f\xe1\xaa\xa0'
    b'-\xe1\xaa\xa6\xe1\xaa\xa8-\xe1\xaa\xad\xe1\xad\x8e-\xe1\xad\x8f\xe1\xad\x9a-\xe1\xad\xaa\xe1\xad\xb4-\xe1\xad'
    b'\xbf\xe1\xaf\xbc-\xe1\xaf\xbf\xe1\xb0\xbb-\xe1\xb0\xbf\xe1\xb1\xbe-\xe1\xb1\xbf\xe1\xb3\x80-\xe1\xb3\x87\xe1\xb3'
    b'\x93\xe1\xbe\xbd\xe1\xbe\xbf-\xe1\xbf\x81\xe1\xbf\x8d-\xe1\xbf\x8f\xe1\xbf\x9d-\xe1\xbf\x9f\xe1\xbf\xad-\xe1\xbf'
    b'\xaf\xe1\xbf\xbd-\xe1\xbf\xbe\xe2\x80\x90-\xe2\x80\xa7\xe2\x80\xb0-\xe2\x81\x9e\xe2\x81\xba-\xe2\x81\xbe\xe2\x82'
    b'\x8a-\xe2\x82\x8e\xe2\x82\xa0-\xe2\x83\x80\xe2\x84\x80-\xe2\x84\x81\xe2\x84\x83-\xe2\x84\x86\xe2\x84\x88-\xe2'
    b'\x84\x89\xe2\x84\x94\xe2\x84\x96-\xe2\x84\x98\xe2\x84\x9e-\xe2\x84\xa3\xe2\x84\xa5\xe2\x84\xa7\xe2\x84\xa9\xe2'
    b'\x84\xae\xe2\x84\xba-\xe2\x84\xbb\xe2\x85\x80-\xe2\x85\x84\xe2\x85\x8a-\xe2\x85\x8d\xe2\x85\x8f\xe2\x86\x8a-\xe2'
    b'\x86\x8b\xe2\x86\x90-\xe2\x90\xa9\xe2\x91\x80-\xe2\x91\x8a\xe2\x92\x9c-\xe2\x93\xa9\xe2\x94\x80-\xe2\x9d\xb5\xe2'
    b'\x9e\x94-\xe2\xad\xb3\xe2\xad\xb6-\xe2\xae\x95\xe2\xae\x97-\xe2\xaf\xbf\xe2\xb3\xa5-\xe2\xb3\xaa\xe2\xb3\xb9-'
    b'\xe2\xb3\xbc\xe2\xb3\xbe-\xe2\xb3\xbf\xe2\xb5\xb0\xe2\xb8\x80-\xe2\xb8\xae\xe2\xb8\xb0-\xe2\xb9\x9d\xe2\xba\x80-'
    b'\xe2\xba\x99\xe2\xba\x9b-\xe2\xbb\xb3\xe2\xbc\x80-\xe2\xbf\x95\xe2\xbf\xb0-\xe2\xbf\xbf\xe3\x80\x81-\xe3\x80\x84'
    b'\xe3\x80\x88-\xe3\x80\xa0\xe3\x80\xb0\xe3\x80\xb6-\xe3\x80\xb7\xe3\x80\xbd-\xe3\x80\xbf\xe3\x82\x9b-\xe3\x82\x9c'
    b'\xe3\x82\xa0\xe3\x83\xbb\xe3\x86\x90-\xe3\x86\x91\xe3\x86\x96-\xe3\x86\x9f\xe3\x87\x80-\xe3\x87\xa5\xe3\x87\xaf'
    b'\xe3\x88\x80-\xe3\x88\x9e\xe3\x88\xaa-\xe3\x89\x87\xe3\x89\x90\xe3\x89\xa0-\xe3\x89\xbf\xe3\x8a\x8a-\xe3\x8a\xb0'
    b'\xe3\x8b\x80-\xe3\x8f\xbf\xe4\xb7\x80-\xe4\xb7\xbf\xea\x92\x90-\xea\x93\x86\xea\x93\xbe-\xea\x93\xbf\xea\x98\x8d'
    b'-\xea\x98\x8f\xea\x99\xb3\xea\x99\xbe\xea\x9b\xb2-\xea\x9b\xb7\xea\x9c\x80-\xea\x9c\x96\xea\x9c\xa0-\xea\x9c\xa1'
    b'\xea\x9e\x89-\xea\x9e\x8a\xea\xa0\xa8-\xea\xa0\xab\xea\xa0\xb6-\xea\xa0\xb9\xea\xa1\xb4-\xea\xa1\xb7\xea\xa3\x8e'
    b'-\xea\xa3\x8f\xea\xa3\xb8-\xea\xa3\xba\xea\xa3\xbc\xea\xa4\xae-\xea\xa4\xaf\xea\xa5\x9f\xea\xa7\x81-\xea\xa7\x8d'
    b'\xea\xa7\x9e-\xea\xa7\x9f\xea\xa9\x9c-\xea\xa9\x9f\xea\xa9\xb7-\xea\xa9\xb9\xea\xab\x9e-\xea\xab\x9f\xea\xab\xb0'
    b'-\xea\xab\xb1\xea\xad\x9b\xea\xad\xaa-\xea\xad\xab\xea\xaf\xab\xef\xac\xa9\xef\xae\xb2-\xef\xaf\x82\xef\xb4\xbe-'
    b'\xef\xb5\x8f\xef\xb7\x8f\xef\xb7\xbc-\xef\xb7\xbf\xef\xb8\x90-\xef\xb8\x99\xef\xb8\xb0-\xef\xb9\x92\xef\xb9\x94-'
    b'\xef\xb9\xa6\xef\xb9\xa8-\xef\xb9\xab\xef\xbc\x81-\xef\xbc\x8f\xef\xbc\x9a-\xef\xbc\xa0\xef\xbc\xbb-\xef\xbd\x80'
    b'\xef\xbd\x9b-\xef\xbd\xa5\xef\xbf\xa0-\xef\xbf\xa6\xef\xbf\xa8-\xef\xbf\xae\xef\xbf\xbc-\xef\xbf\xbd\xf0\x90\x84'
    b'\x80-\xf0\x90\x84\x82\xf0\x90\x84\xb7-\xf0\x90\x84\xbf\xf0\x90\x85\xb9-\xf0\x90\x86\x89\xf0\x90\x86\x8c-\xf0\x90'
    b'\x86\x8e\xf0\x90\x86\x90-\xf0\x90\x86\x9c\xf0\x90\x86\xa0\xf0\x90\x87\x90-\xf0\x90\x87\xbc\xf0\x90\x8e\x9f\xf0'
    b'\x90\x8f\x90\xf0\x90\x95\xaf\xf0\x90\xa1\x97\xf0\x90\xa1\xb7-\xf0\x90\xa1\xb8\xf0\x90\xa4\x9f\xf0\x90\xa4\xbf'
    b'\xf0\x90\xa9\x90-\xf0\x90\xa9\x98\xf0\x90\xa9\xbf\xf0\x90\xab\x88\xf0\x90\xab\xb0-\xf0\x90\xab\xb6\xf0\x90\xac'
    b'\xb9-\xf0\x90\xac\xbf\xf0\x90\xae\x99-\xf0\x90\xae\x9c\xf0\x90\xb5\xae\xf0\x90\xb6\x8e-\xf0\x90\xb6\x8f\xf0\x90'
    b'\xba\xad\xf0\x90\xbd\x95-\xf0\x90\xbd\x99\xf0\x90\xbe\x86-\xf0\x90\xbe\x89\xf0\x91\x81\x87-\xf0\x91\x81\x8d\xf0'
    b'\x91\x82\xbb-\xf0\x91\x82\xbc\xf0\x91\x82\xbe-\xf0\x91\x83\x81\xf0\x91\x85\x80-\xf0\x91\x85\x83\xf0\x91\x85\xb4-'
    b'\xf0\x91\x85\xb5\xf0\x91\x87\x85-\xf0\x91\x87\x88\xf0\x91\x87\x8d\xf0\x91\x87\x9b\xf0\x91\x87\x9d-\xf0\x91\x87'
    b'\x9f\xf0\x91\x88\xb8-\xf0\x91\x88\xbd\xf0\x91\x8a\xa9\xf0\x91\x8f\x94-\xf0\x91\x8f\x95\xf0\x91\x8f\x97-\xf0\x91'
    b'\x8f\x98\xf0\x91\x91\x8b-\xf0\x91\x91\x8f\xf0\x91\x91\x9a-\xf0\x91\x91\x9b\xf0\x91\x91\x9d\xf0\x91\x93\x86\xf0'
    b'\x91\x97\x81-\xf0\x91\x97\x97\xf0\x91\x99\x81-\xf0\x91\x99\x83\xf0\x91\x99\xa0-\xf0\x91\x99\xac\xf0\x91\x9a\xb9'
    b'\xf0\x91\x9c\xbc-\xf0\x91\x9c\xbf\xf0\x91\xa0\xbb\xf0\x91\xa5\x84-\xf0\x91\xa5\x86\xf0\x91\xa7\xa2\xf0\x91\xa8'
    b'\xbf-\xf0\x91\xa9\x86\xf0\x91\xaa\x9a-\xf0\x91\xaa\x9c\xf0\x91\xaa\x9e-\xf0\x91\xaa\xa2\xf0\x91\xac\x80-\xf0\x91'
    b'\xac\x89\xf0\x91\xaf\xa1\xf0\x91\xb1\x81-\xf0\x91\xb1\x85\xf0\x91\xb1\xb0-\xf0\x91\xb1\xb1\xf0\x91\xbb\xb7-\xf0'
    b'\x91\xbb\xb8\xf0\x91\xbd\x83-\xf0\x91\xbd\x8f\xf0\x91\xbf\x95-\xf0\x91\xbf\xb1\xf0\x91\xbf\xbf\xf0\x92\x91\xb0-'
    b'\xf0\x92\x91\xb4\xf0\x92\xbf\xb1-\xf0\x92\xbf\xb2\xf0\x96\xa9\xae-\xf0\x96\xa9\xaf\xf0\x96\xab\xb5\xf0\x96\xac'
    b'\xb7-\xf0\x96\xac\xbf\xf0\x96\xad\x84-\xf0\x96\xad\x85\xf0\x96\xb5\xad-\xf0\x96\xb5\xaf\xf0\x96\xba\x97-\xf0\x96'
    b'\xba\x9a\xf0\x96\xbf\xa2\xf0\x9b\xb2\x9c\xf0\x9b\xb2\x9f\xf0\x9c\xb0\x80-\xf0\x9c\xb3\xaf\xf0\x9c\xb4\x80-\xf0'
    b'\x9c\xba\xb3\xf0\x9c\xbd\x90-\xf0\x9c\xbf\x83\xf0\x9d\x80\x80-\xf0\x9d\x83\xb5\xf0\x9d\x84\x80-\xf0\x9d\x84\xa6'
    b'\xf0\x9d\x84\xa9-\xf0\x9d\x85\xa4\xf0\x9d\x85\xaa-\xf0\x9d\x85\xac\xf0\x9d\x86\x83-\xf0\x9d\x86\x84\xf0\x9d\x86'
    b'\x8c-\xf0\x9d\x86\xa9\xf0\x9d\x86\xae-\xf0\x9d\x87\xaa\xf0\x9d\x88\x80-\xf0\x9d\x89\x81\xf0\x9d\x89\x85\xf0\x9d'
    b'\x8c\x80-\xf0\x9d\x8d\x96\xf0\x9d\x9b\x81\xf0\x9d\x9b\x9b\xf0\x9d\x9b\xbb\xf0\x9d\x9c\x95\xf0\x9d\x9c\xb5\xf0'
    b'\x9d\x9d\x8f\xf0\x9d\x9d\xaf\xf0\x9d\x9e\x89\xf0\x9d\x9e\xa9\xf0\x9d\x9f\x83\xf0\x9d\xa0\x80-\xf0\x9d\xa7\xbf'
    b'\xf0\x9d\xa8\xb7-\xf0\x9d\xa8\xba\xf0\x9d\xa9\xad-\xf0\x9d\xa9\xb4\xf0\x9d\xa9\xb6-\xf0\x9d\xaa\x83\xf0\x9d\xaa'
    b'\x85-\xf0\x9d\xaa\x8b\xf0\x9e\x85\x8f\xf0\x9e\x8b\xbf\xf0\x9e\x97\xbf\xf0\x9e\xa5\x9e-\xf0\x9e\xa5\x9f\xf0\x9e'
    b'\xb2\xac\xf0\x9e\xb2\xb0\xf0\x9e\xb4\xae\xf0\x9e\xbb\xb0-\xf0\x9e\xbb\xb1\xf0\x9f\x80\x80-\xf0\x9f\x80\xab\xf0'
    b'\x9f\x80\xb0-\xf0\x9f\x82\x93\xf0\x9f\x82\xa0-\xf0\x9f\x82\xae\xf0\x9f\x82\xb1-\xf0\x9f\x82\xbf\xf0\x9f\x83\x81-'
    b'\xf0\x9f\x83\x8f\xf0\x9f\x83\x91-\xf0\x9f\x83\xb5\xf0\x9f\x84\x8d-\xf0\x9f\x86\xad\xf0\x9f\x87\xa6-\xf0\x9f\x88'
    b'\x82\xf0\x9f\x88\x90-\xf0\x9f\x88\xbb\xf0\x9f\x89\x80-\xf0\x9f\x89\x88\xf0\x9f\x89\x90-\xf0\x9f\x89\x91\xf0\x9f'
    b'\x89\xa0-\xf0\x9f\x89\xa5\xf0\x9f\x8c\x80-\xf0\x9f\x9b\x97\xf0\x9f\x9b\x9c-\xf0\x9f\x9b\xac\xf0\x9f\x9b\xb0-\xf0'
    b'\x9f\x9b\xbc\xf0\x9f\x9c\x80-\xf0\x9f\x9d\xb6\xf0\x9f\x9d\xbb-\xf0\x9f\x9f\x99\xf0\x9f\x9f\xa0-\xf0\x9f\x9f\xab'
    b'\xf0\x9f\x9f\xb0\xf0\x9f\xa0\x80-\xf0\x9f\xa0\x8b\xf0\x9f\xa0\x90-\xf0\x9f\xa1\x87\xf0\x9f\xa1\x90-\xf0\x9f\xa1'
    b'\x99\xf0\x9f\xa1\xa0-\xf0\x9f\xa2\x87\xf0\x9f\xa2\x90-\xf0\x9f\xa2\xad\xf0\x9f\xa2\xb0-\xf0\x9f\xa2\xbb\xf0\x9f'
    b'\xa3\x80-\xf0\x9f\xa3\x81\xf0\x9f\xa4\x80-\xf0\x9f\xa9\x93\xf0\x9f\xa9\xa0-\xf0\x9f\xa9\xad\xf0\x9f\xa9\xb0-\xf0'
    b'\x9f\xa9\xbc\xf0\x9f\xaa\x80-\xf0\x9f\xaa\x89\xf0\x9f\xaa\x8f-\xf0\x9f\xab\x86\xf0\x9f\xab\x8e-\xf0\x9f\xab\x9c'
    b'\xf0\x9f\xab\x9f-\xf0\x9f\xab\xa9\xf0\x9f\xab\xb0-\xf0\x9f\xab\xb8\xf0\x9f\xac\x80-\xf0\x9f\xae\x92\xf0\x9f\xae'
    b'\x94-\xf0\x9f\xaf\xaf'
).decode('utf-8')


class Delimiter:
    """Delimiter."""

    def __init__(self, token: str, tags: str, smart: bool, double: bool):
        """Initialize."""

        self.stack: deque[tuple[int, int, bool, int]] = deque()
        temp = tags.split(',')
        self.tag_count = len(temp)
        self.tags: tuple[str, str] = (temp[0], temp[1]) if self.tag_count == 2 else (temp[0], temp[0])
        self.double = len(temp) != 2 and double
        self.single = len(temp) != 2 and not double
        self.smart = smart
        self._build_patterns(token)

    def _build_patterns(self, token: str) -> str:
        """Build regular expression patterns."""

        # Build up patterns
        self.token = token
        etoken = re.escape(token)
        # Avoid at start and end
        xstart = fr'(?:(?<=_)|(?<![\w{etoken}]))' if token != '_' else fr'(?<![\w{etoken}])'
        xend = fr'(?:(?=_)|(?![\w{etoken}]))' if token != '_' else fr'(?![\w{etoken}])'
        self.max_size = 2
        if self.tag_count != 2 and not self.double:
            self.max_size = 1

        # Python Markdown uses `STX` and `ETX` for placeholders.
        # Include handling for these characters in addition to CommonMark rules.
        stx, etx = '\x02', '\x03'

        # Patterns for "smart" cases.
        if self.smart:
            self.boundary = re.compile(
                fr'''(?x)
                (?P<ambiguous>
                    (?<!^)(?<![\s{etoken}{PUNCT}]){xstart}{etoken}{{1,}}{xend}(?![\s{etoken}{PUNCT}])(?!$)|
                    (?<!^)(?<=[{PUNCT}{etx}])(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[{PUNCT}{stx}])(?!$)
                )|
                (?P<end>
                    (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{1,}}{xend}|
                    (?<=[{PUNCT}])(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[\s{stx}{PUNCT}]|$)
                )|
                (?P<start>
                    {xstart}{etoken}{{1,}}(?![\s{etoken}{PUNCT}])(?!$)|
                    (?:(?<=[\s{etx}{PUNCT}])|^)(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[{PUNCT}])
                )
                ''',
                flags=re.UNICODE
            )
        # Patterns for "dumb" cases.
        else:
            self.boundary = re.compile(
                fr'''(?x)
                (?P<ambiguous>
                    (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{1,}}(?![\s{etoken}{PUNCT}])(?!$)|
                    (?<!^)(?<=[{PUNCT}{etx}])(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[{PUNCT}{stx}])(?!$)
                )|
                (?P<end>
                    (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{1,}}|
                    (?<=[{PUNCT}])(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[\s{stx}{PUNCT}]|$)
                )|
                (?P<start>
                    {etoken}{{1,}}(?![\s{etoken}{PUNCT}])(?!$)|
                    (?:(?<=[\s{etx}{PUNCT}])|^)(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[{PUNCT}])
                )
                ''',
                flags=re.UNICODE
            )

        return fr'{etoken}'

    def reset(self) -> None:
        """Reset."""

        # Cache info
        self.stack.clear()


class DelimiterProcessor(InlineProcessor):
    """Processor for handling complex nested patterns such as strong and em matches."""

    SPACE = re.compile(r'\s')

    def __init__(
        self,
        token: str,
        tags: str,
        md: Markdown,
        smart: bool = False,
        double: bool = False
    ) -> None:
        """Initialize."""

        md.delimiters = self
        self.regions: list[tuple[int, int, int, int, tuple[str, str], int]] = []
        self.stack: list[tuple[int, int, bool, int]] = []
        self.tokens: list[str] = []
        self.delimiters: dict[str, Delimiter] = {}
        self.cache_index = 0
        self.cache_pos = 0
        self.md = md
        # API for Markdown to pass `safe_mode` into instance
        self.safe_mode = False
        self.add(token, tags, smart, double)

    def add(
        self,
        token: str,
        tags: str,
        smart: bool = False,
        double: bool = False
    ) -> None:
        """Add a delimiter."""

        if token not in self.tokens:
            self.tokens.append(token)
        self.delimiters[token] = Delimiter(token, tags, smart, double)
        self.pattern = '|'.join([re.escape(t) for t in self.tokens])
        self.compiled_re = re.compile(self.pattern, re.DOTALL | re.UNICODE)

    def remove(self, token: str) -> None:
        """Remove a token."""

        try:
            i = self.tokens.index(token)
            del self.tokens[i]
            del self.delimiters[token]
        except Exception:
            pass
        self.pattern = '|'.join([re.escape(t) for t in self.tokens])
        self.compiled_re = re.compile(self.pattern, re.DOTALL | re.UNICODE) if self.pattern else re.compile(r'(?!)')

    def reset(self) -> None:
        """Reset."""

        # Cache info
        for v in self.delimiters.values():
            v.reset()
        self.regions.clear()
        self.stack.clear()
        self.cache_index = 0
        self.cache_pos = 0

    def _build_element(
        self,
        data: str,
        start: int = 0,
        offset: int = 0
    ) -> tuple[etree.Element, int]:
        """Element builder."""

        regions = self.regions
        el: etree.Element | None = None
        last: Any = None
        previous: Any = None

        outer: list[etree.Element] = []
        outer_r: list[tuple[int, int, int, int, tuple[str, str], int]] = []

        # Iterate regions creating the elements they represent
        end = len(regions)
        idx = 0
        for idx, i in enumerate(range(start, end), 1):
            r = regions[i]
            # Not contained within region
            if idx and r[0] >= regions[start][3]:
                idx -= 1
                break

            # Get the appropriate element(s)
            if r[-1] == 2:
                el1 = etree.Element(r[4][0])
            else:
                el1 = etree.Element(r[4][1])

            # Populate the elements with their text
            if idx > 1:
                if last.text is None:
                    if previous[2] < r[0]:
                        last.text = data[previous[1]+offset:previous[2]+offset]
                    else:
                        last.text = data[previous[1]+offset:r[0]+offset]
                if last is not outer[-1] and last.tail is None:
                    if r[0] < outer_r[-1][3]:
                        last.tail = data[previous[3]+offset:r[0]+offset]
                    else:
                        last.tail = data[previous[3]+offset:outer_r[-1][2]+offset]
                        outer[-1].tail = data[outer_r[-1][3]+offset:r[0]+offset]

            # First element
            if el is None:
                el = el1
                last = el
                outer.append(el)
                outer_r.append(r)

            # Subsequent elements
            else:
                # Is the current outer element no longer wrapping this one?
                while len(outer_r) > 1 and r[3] > outer_r[-1][3]:
                    outer.pop()
                    outer_r.pop()

                # Non-nested
                else:
                    outer[-1].append(el1)

                # Is this element wrapping the next?
                if i + 1 < end:
                    if r[3] > regions[i + 1][3]:
                        outer.append(el1)
                        outer_r.append(r)

                # Track the last element we parsed.
                last = el1

            # Track the previous region.
            previous = r

        # Populate remaining elements with their text
        while outer:
            if last.text is None:
                last.text = data[previous[1]+offset:previous[2]+offset]
            if last.tail is None and last is not outer[-1]:
                last.tail = data[previous[3]+offset:outer_r[-1][2]+offset]
            last = outer.pop()
            previous = outer_r.pop()

        return cast('etree.Element', el), idx

    def increment_next_position(self, start: int, count: int) -> None:
        """
        Increment cache position to the next location that we can initiate an insertion.

        Cache position should be the first match after our current replacement.
        This gives us an anchor to calculate the new offset after insertion.
        """

        # Determine next offset
        self.cache_index += count
        if self.cache_index < len(self.regions):
            self.cache_pos = self.regions[self.cache_index][0]
            while self.stack:
                entry = self.stack.pop(0)
                if start < entry[0] <= self.cache_pos:
                    self.cache_pos = entry[0]
                    break

        # Nothing left to process
        else:
            self.reset()

    def get_cached_result(self, pos: int, data: str) -> tuple[etree.Element, int, int]:
        """Get a cached result."""

        # Process the next region(s) in the cache
        regions = self.regions
        offset = pos - self.cache_pos if pos != self.cache_pos else pos - regions[self.cache_index][0]
        start, end = regions[self.cache_index][0], regions[self.cache_index][3]
        el, count = self._build_element(data, self.cache_index, offset)
        self.increment_next_position(start, count)
        return el, start + offset, end + offset

    def get_match(self, data: str, start: int) -> re.Match[str] | None:
        """Get match."""

        for d in self.delimiters.values():
            m = d.boundary.match(data, start)
            if m is not None:
                return m
        return None

    def search(self, data: str, start: int) -> re.Match[str] | None:
        """Search."""

        for i in range(start, len(data)):
            if data[i] in self.delimiters:
                d = self.delimiters[data[i]]
                m = d.boundary.match(data, i)
                if m is not None:
                    if not d.stack and m.lastgroup[0] == 'e':  # type: ignore[index]
                        continue
                    return m
        return None

    def add_region(self, delim: Delimiter, a: int, b: int, c: int, d: int, size: int) -> None:
        """Add region."""

        self.regions.append((a, b, c, d, delim.tags, size))
        for delim in self.delimiters.values():
            while delim.stack:
                p = delim.stack[-1][0]
                if max(p, a) <= min(p, d - 1):
                    delim.stack.pop()
                    continue
                break

    def handleMatch(  # type: ignore[override]
        self,
        m: re.Match[str],
        data: str
    ) -> tuple[etree.Element | None, int | None, int | None]:
        """Parse delimiter pattern."""

        # Do we have entries we haven't returned yet?
        if self.regions:
            return self.get_cached_result(m.start(0), data)

        # If token is not an opening, quit
        m2 = self.get_match(data, m.start(0))
        if m2 is None or m2.lastgroup[0] == 'e':  # type: ignore[index]
            if m2 is not None:
                m = m2
            # Advance past the full length of the delimiter found
            return None, m.start(0), m.end(0)

        # Get the stack and regions
        token = data[m.start(0)]
        delim = self.delimiters[token]
        stack = delim.stack

        start = m2.start(0)
        end = m2.end(0)
        length = end - start

        # Double needs at least a size of 2
        if delim.double and length < 2:
            return None, m.start(0), m.end(0)

        is_ambiguous = m2.lastgroup[0] != 's'  # type: ignore[index]
        stack.append((start, start + length, is_ambiguous, length))

        # Pair tokens until the stack is empty or we can no longer find tokens.
        while any(d.stack for d in self.delimiters.values()):
            m2 = self.search(data, end)
            if m2 is None:
                break

            token = data[m2.start(0)]
            delim = self.delimiters[token]
            stack = delim.stack

            start = m2.start(0)
            end = m2.end(0)

            # Get current and last delimiter size
            current = len(m2.group(0))

            # Some delimiters may be ambiguous and look like both a start or an end
            is_start = m2.lastgroup[0] != 'e'  # type: ignore[index]
            is_end = not is_start or m2.lastgroup[0] != 's'  # type: ignore[index]
            is_ambiguous = is_start and is_end

            last = stack[-1][-1] if stack else 0

            # Find closing tokens
            # Looking for:
            # - `*em*`
            # - `**strong**`
            # - `***strong,em***`
            # - `*em**`
            # - `*em***`
            # - `**strong***`
            #
            # Avoid ambiguous tokens that could be a start or an end.
            # Consume starts until the end token is fully consumed.
            # If we don't consume the entire end, see if next rule consumes it.
            if stack and is_end and ((not is_ambiguous and current > last) or current == last or current >= 3):
                is_start = False

                # Consume previous points until the delimiter is consumed
                original = current
                while stack and current and last <= current:
                    delimiter = stack.pop()

                    # Build up region for pair and adjust accounting.
                    size = min(delimiter[-1], 1 if delim.tag_count == 2 and delimiter[-1] == 3 else delim.max_size)
                    self.add_region(delim, delimiter[1] - size, delimiter[1], start, start + size, size)
                    start += size
                    current -= size
                    new = 0
                    if size < delimiter[-1] and (not delim.double or (delimiter[-1] - size) != 1):
                        new = delimiter[-1] - size
                        stack.append((delimiter[0], delimiter[1] - size, delimiter[2], new))

                    if not stack:
                        if any(d.stack for d in self.delimiters.values() if d is not delim):
                            delim.reset()
                            continue
                        is_end = False
                        break

                    last = stack[-1][-1]

                # Should remainder be treated as a new start?
                if original >= 3 and current and is_ambiguous:
                    delim.stack.append((m2.start(0) + (original - current), end, False, current))
                    is_end = False

                # Do we still have more to consume?
                else:
                    is_end = current and stack and last > current

            # Looking for:
            # - `***em*`
            # - `***strong**`
            # - `**em*`
            if stack and is_end and (last >= 3 or not is_ambiguous) and last > current:
                delimiter = stack.pop()

                # Don't pair with an ambiguous opening
                while stack and delimiter[-1] != 3 and delimiter[2]:
                    delimiter = stack.pop()
                    last = delimiter[-1]

                if delimiter[2] and delimiter[-1] != 3:
                    if any(d.stack for d in self.delimiters.values() if d is not delim):
                        delim.reset()
                        continue
                    break

                ignore = False
                # Create new region if end is valid.
                # If not valid, ignore the end but continue parsing.
                if not ignore:
                    is_start = False
                    ds, de = delimiter[:2]
                    while current and (not delim.double or current != 1):
                        size = min(current, 1 if delim.tag_count == 2 and current == 3 else delim.max_size)
                        new = last - size
                        self.add_region(delim, ds + new, de, start, start + size, size)
                        start += size
                        current -= size
                        last -= size
                        de -= size
                    if not delim.double or last > 1:
                        stack.append((ds, de, False, last))

            # Find opening tokens
            # Looking for:
            # - `*em ...*`
            # - `**strong ...*`
            # - `***em ...*`
            if is_start and (not delim.double or current != 1):
                stack.append((start, end, is_ambiguous, current))

        # Combine the stacks and order them
        for delim in self.delimiters.values():
            self.stack.extend(delim.stack)
        self.stack.sort(key=lambda x: x[0])

        # Build the HTML elements
        if self.regions:
            # Regions may be out of order.
            self.regions.sort(key=lambda x: x[0])
            start, end = self.regions[0][0], self.regions[0][3]
            el, count = self._build_element(data)
            self.increment_next_position(start, count)
            return el, start, end

        # We failed to pair any valid start/end delimiters, avoid the parsed range next pass.
        start = m.start(0)
        end = self.stack[-1][1] if self.stack else m.end(0)
        self.reset()
        return None, start, end


class LinkInlineProcessor(InlineProcessor):
    """ Return a link element from the given match. """
    RE_LINK = re.compile(r'''\(\s*(?:(<[^<>]*>)\s*(?:('[^']*'|"[^"]*")\s*)?\))?''', re.DOTALL | re.UNICODE)
    RE_TITLE_CLEAN = re.compile(r'\s')

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | None, int | None, int | None]:
        """ Return an `a` [`Element`][xml.etree.ElementTree.Element] or `(None, None, None)`. """
        text, index, handled = self.getText(data, m.end(0))

        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = etree.Element("a")
        el.text = text

        el.set("href", href)

        if title is not None:
            el.set("title", title)

        return el, m.start(0), index

    def getLink(self, data: str, index: int) -> tuple[str, str | None, int, bool]:
        """Parse data between `()` of `[Text]()` allowing recursive `()`. """

        href = ''
        title: str | None = None
        handled = False

        m = self.RE_LINK.match(data, pos=index)
        if m and m.group(1):
            # Matches [Text](<link> "title")
            href = m.group(1)[1:-1].strip()
            if m.group(2):
                title = m.group(2)[1:-1]
            index = m.end(0)
            handled = True
        elif m:
            # Track bracket nesting and index in string
            bracket_count = 1
            backtrack_count = 1
            start_index = m.end()
            index = start_index
            last_bracket = -1

            # Primary (first found) quote tracking.
            quote: str | None = None
            start_quote = -1
            exit_quote = -1
            ignore_matches = False

            # Secondary (second found) quote tracking.
            alt_quote = None
            start_alt_quote = -1
            exit_alt_quote = -1

            # Track last character
            last = ''

            for pos in range(index, len(data)):
                c = data[pos]
                if c == '(':
                    # Count nested (
                    # Don't increment the bracket count if we are sure we're in a title.
                    if not ignore_matches:
                        bracket_count += 1
                    elif backtrack_count > 0:
                        backtrack_count -= 1
                elif c == ')':
                    # Match nested ) to (
                    # Don't decrement if we are sure we are in a title that is unclosed.
                    if ((exit_quote != -1 and quote == last) or (exit_alt_quote != -1 and alt_quote == last)):
                        bracket_count = 0
                    elif not ignore_matches:
                        bracket_count -= 1
                    elif backtrack_count > 0:
                        backtrack_count -= 1
                        # We've found our backup end location if the title doesn't resolve.
                        if backtrack_count == 0:
                            last_bracket = index + 1

                elif c in ("'", '"'):
                    # Quote has started
                    if not quote:
                        # We'll assume we are now in a title.
                        # Brackets are quoted, so no need to match them (except for the final one).
                        ignore_matches = True
                        backtrack_count = bracket_count
                        bracket_count = 1
                        start_quote = index + 1
                        quote = c
                    # Secondary quote (in case the first doesn't resolve): [text](link'"title")
                    elif c != quote and not alt_quote:
                        start_alt_quote = index + 1
                        alt_quote = c
                    # Update primary quote match
                    elif c == quote:
                        exit_quote = index + 1
                    # Update secondary quote match
                    elif alt_quote and c == alt_quote:
                        exit_alt_quote = index + 1

                index += 1

                # Link is closed, so let's break out of the loop
                if bracket_count == 0:
                    # Get the title if we closed a title string right before link closed
                    if exit_quote >= 0 and quote == last:
                        href = data[start_index:start_quote - 1]
                        title = ''.join(data[start_quote:exit_quote - 1])
                    elif exit_alt_quote >= 0 and alt_quote == last:
                        href = data[start_index:start_alt_quote - 1]
                        title = ''.join(data[start_alt_quote:exit_alt_quote - 1])
                    else:
                        href = data[start_index:index - 1]
                    break

                if c != ' ':
                    last = c

            # We have a scenario: `[test](link"notitle)`
            # When we enter a string, we stop tracking bracket resolution in the main counter,
            # but we do keep a backup counter up until we discover where we might resolve all brackets
            # if the title string fails to resolve.
            if bracket_count != 0 and backtrack_count == 0:
                href = data[start_index:last_bracket - 1]
                index = last_bracket
                bracket_count = 0

            handled = bracket_count == 0

        if title is not None:
            title = self.RE_TITLE_CLEAN.sub(' ', dequote(self.unescape(title.strip())))

        href = self.unescape(href).strip()

        return href, title, index, handled

    def getText(self, data: str, index: int) -> tuple[str, int, bool]:
        """Parse the content between `[]` of the start of an image or link
        resolving nested square brackets.

        """
        bracket_count = 1
        text = []
        for pos in range(index, len(data)):
            c = data[pos]
            if c == ']':
                bracket_count -= 1
            elif c == '[':
                bracket_count += 1
            index += 1
            if bracket_count == 0:
                break
            text.append(c)
        return ''.join(text), index, bracket_count == 0


class ImageInlineProcessor(LinkInlineProcessor):
    """ Return a `img` element from the given match. """

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | None, int | None, int | None]:
        """ Return an `img` [`Element`][xml.etree.ElementTree.Element] or `(None, None, None)`. """
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = etree.Element("img")

        el.set("src", src)

        if title is not None:
            el.set("title", title)

        el.set('alt', self.unescape(text))
        return el, m.start(0), index


class ReferenceInlineProcessor(LinkInlineProcessor):
    """ Match to a stored reference and return link element. """
    NEWLINE_CLEANUP_RE = re.compile(r'\s+', re.MULTILINE)

    RE_LINK = re.compile(r'\s?\[([^\]]*)\]', re.DOTALL | re.UNICODE)

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | None, int | None, int | None]:
        """
        Return [`Element`][xml.etree.ElementTree.Element] returned by `makeTag` method or `(None, None, None)`.

        """
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        id, end, handled = self.evalId(data, index, text)
        if not handled:
            return None, None, None

        # Clean up line breaks in id
        id = self.NEWLINE_CLEANUP_RE.sub(' ', id)
        if id not in self.md.references:  # ignore undefined refs
            return None, m.start(0), end

        href, title = self.md.references[id]

        return self.makeTag(href, title, text), m.start(0), end

    def evalId(self, data: str, index: int, text: str) -> tuple[str | None, int, bool]:
        """
        Evaluate the id portion of `[ref][id]`.

        If `[ref][]` use `[ref]`.
        """
        m = self.RE_LINK.match(data, pos=index)
        if not m:
            return None, index, False
        else:
            id = m.group(1).lower()
            end = m.end(0)
            if not id:
                id = text.lower()
        return id, end, True

    def makeTag(self, href: str, title: str, text: str) -> etree.Element:
        """ Return an `a` [`Element`][xml.etree.ElementTree.Element]. """
        el = etree.Element('a')

        el.set('href', href)
        if title:
            el.set('title', title)

        el.text = text
        return el


class ShortReferenceInlineProcessor(ReferenceInlineProcessor):
    """Short form of reference: `[google]`. """
    def evalId(self, data: str, index: int, text: str) -> tuple[str, int, bool]:
        """Evaluate the id of `[ref]`.  """

        return text.lower(), index, True


class ImageReferenceInlineProcessor(ReferenceInlineProcessor):
    """ Match to a stored reference and return `img` element. """
    def makeTag(self, href: str, title: str, text: str) -> etree.Element:
        """ Return an `img` [`Element`][xml.etree.ElementTree.Element]. """
        el = etree.Element("img")
        el.set("src", href)
        if title:
            el.set("title", title)
        el.set("alt", self.unescape(text))
        return el


class ShortImageReferenceInlineProcessor(ImageReferenceInlineProcessor):
    """ Short form of image reference: `![ref]`. """
    def evalId(self, data: str, index: int, text: str) -> tuple[str, int, bool]:
        """Evaluate the id of `[ref]`.  """

        return text.lower(), index, True


class AutolinkInlineProcessor(InlineProcessor):
    """ Return a link Element given an auto-link (`<http://example/com>`). """
    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:
        """ Return an `a` [`Element`][xml.etree.ElementTree.Element] of `group(1)`. """
        el = etree.Element("a")
        el.set('href', self.unescape(m.group(1)))
        el.text = util.AtomicString(m.group(1))
        return el, m.start(0), m.end(0)


class AutomailInlineProcessor(InlineProcessor):
    """
    Return a `mailto` link Element given an auto-mail link (`<foo@example.com>`).
    """
    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element, int, int]:
        """ Return an [`Element`][xml.etree.ElementTree.Element] containing a `mailto` link  of `group(1)`. """
        el = etree.Element('a')
        email = self.unescape(m.group(1))
        if email.startswith("mailto:"):
            email = email[len("mailto:"):]

        def codepoint2name(code: int) -> str:
            """Return entity definition by code, or the code if not defined."""
            entity = entities.codepoint2name.get(code)
            if entity:
                return "{}{};".format(util.AMP_SUBSTITUTE, entity)
            else:
                return "%s#%d;" % (util.AMP_SUBSTITUTE, code)

        letters = [codepoint2name(ord(letter)) for letter in email]
        el.text = util.AtomicString(''.join(letters))

        mailto = "mailto:" + email
        mailto = "".join([util.AMP_SUBSTITUTE + '#%d;' %
                          ord(letter) for letter in mailto])
        el.set('href', mailto)
        return el, m.start(0), m.end(0)
