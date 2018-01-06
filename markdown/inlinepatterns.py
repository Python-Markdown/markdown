"""
INLINE PATTERNS
=============================================================================

Inline patterns such as *emphasis* are handled by means of auxiliary
objects, one per pattern.  Pattern objects must be instances of classes
that extend markdown.Pattern.  Each pattern object uses a single regular
expression and needs support the following methods:

    pattern.getCompiledRegExp() # returns a regular expression

    pattern.handleMatch(m) # takes a match object and returns
                           # an ElementTree element or just plain text

All of python markdown's built-in patterns subclass from Pattern,
but you can add additional patterns that don't.

Also note that all the regular expressions used by inline must
capture the whole block.  For this reason, they all start with
'^(.*)' and end with '(.*)!'.  In case with built-in expression
Pattern takes care of adding the "^(.*)" and "(.*)!".

Finally, the order in which regular expressions are applied is very
important - e.g. if we first replace http://.../ links with <a> tags
and _then_ try to replace inline html, we would end up with a mess.
So, we apply the expressions in the following order:

* escape and backticks have to go before everything else, so
  that we can preempt any markdown patterns by escaping them.

* then we handle auto-links (must be done before inline html)

* then we handle inline HTML.  At this point we will simply
  replace all inline HTML strings with a placeholder and add
  the actual HTML to a hash.

* then inline images (must be done before links)

* then bracketed links, first regular then reference-style

* finally we apply strong and emphasis
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import util
from . import odict
import re
try:  # pragma: no cover
    from urllib.parse import urlparse, urlunparse
except ImportError:  # pragma: no cover
    from urlparse import urlparse, urlunparse
try:  # pragma: no cover
    from html import entities
except ImportError:  # pragma: no cover
    import htmlentitydefs as entities


def build_inlinepatterns(md_instance, **kwargs):
    """ Build the default set of inline patterns for Markdown. """
    inlinePatterns = odict.OrderedDict()
    inlinePatterns["backtick"] = BacktickInlineProcessor(BACKTICK_RE)
    inlinePatterns["escape"] = EscapeInlineProcessor(ESCAPE_RE, md_instance)
    inlinePatterns["reference"] = ReferenceInlineProcessor(REFERENCE_RE, md_instance)
    inlinePatterns["link"] = LinkInlineProcessor(LINK_RE, md_instance)
    inlinePatterns["image_link"] = ImageInlineProcessor(IMAGE_LINK_RE, md_instance)
    inlinePatterns["image_reference"] = ImageReferenceInlineProcessor(
        IMAGE_REFERENCE_RE, md_instance
    )
    inlinePatterns["short_reference"] = ShortReferenceInlineProcessor(
        REFERENCE_RE, md_instance
    )
    inlinePatterns["autolink"] = AutolinkInlineProcessor(AUTOLINK_RE, md_instance)
    inlinePatterns["automail"] = AutomailInlineProcessor(AUTOMAIL_RE, md_instance)
    inlinePatterns["linebreak"] = SubstituteTagInlineProcessor(LINE_BREAK_RE, 'br')
    if md_instance.safeMode != 'escape':
        inlinePatterns["html"] = HtmlInlineProcessor(HTML_RE, md_instance)
    inlinePatterns["entity"] = HtmlInlineProcessor(ENTITY_RE, md_instance)
    inlinePatterns["not_strong"] = SimpleTextInlineProcessor(NOT_STRONG_RE)
    inlinePatterns["em_strong"] = DoubleTagInlineProcessor(EM_STRONG_RE, 'strong,em')
    inlinePatterns["strong_em"] = DoubleTagInlineProcessor(STRONG_EM_RE, 'em,strong')
    inlinePatterns["strong"] = SimpleTagInlineProcessor(STRONG_RE, 'strong')
    inlinePatterns["emphasis"] = SimpleTagInlineProcessor(EMPHASIS_RE, 'em')
    if md_instance.smart_emphasis:
        inlinePatterns["emphasis2"] = SimpleTagInlineProcessor(SMART_EMPHASIS_RE, 'em')
    else:
        inlinePatterns["emphasis2"] = SimpleTagInlineProcessor(EMPHASIS_2_RE, 'em')
    return inlinePatterns


"""
The actual regular expressions for patterns
-----------------------------------------------------------------------------
"""

NOBRACKET = r'[^\]\[]*'
BRK = (
    r'\[(' +
    (NOBRACKET + r'(\[')*6 +
    (NOBRACKET + r'\])*')*6 +
    NOBRACKET + r')\]'
)
NOIMG = r'(?<!\!)'

# `e=f()` or ``e=f("`")``
BACKTICK_RE = r'(?:(?<!\\)((?:\\{2})+)(?=`+)|(?<!\\)(`+)(.+?)(?<!`)\2(?!`))'

# \<
ESCAPE_RE = r'\\(.)'

# *emphasis*
EMPHASIS_RE = r'(\*)([^\*]+)\1'

# **strong**
STRONG_RE = r'(\*{2}|_{2})(.+?)\1'

# ***strongem*** or ***em*strong**
EM_STRONG_RE = r'(\*|_)\1{2}(.+?)\1(.*?)\1{2}'

# ***strong**em*
STRONG_EM_RE = r'(\*|_)\1{2}(.+?)\1{2}(.*?)\1'

# _smart_emphasis_
SMART_EMPHASIS_RE = r'(?<!\w)(_)(?!_)(.+?)(?<!_)\1(?!\w)'

# _emphasis_
EMPHASIS_2_RE = r'(_)(.+?)\1'

# [text](url) or [text](<url>) or [text](url "title")
LINK_RE = NOIMG + r'\['

# ![alttxt](http://x.com/) or ![alttxt](<http://x.com/>)
IMAGE_LINK_RE = r'\!\['

# [Google][3]
REFERENCE_RE = LINK_RE

# ![alt text][2]
IMAGE_REFERENCE_RE = IMAGE_LINK_RE

# stand-alone * or _
NOT_STRONG_RE = r'((^| )(\*|_)( |$))'

# <http://www.123.com>
AUTOLINK_RE = r'<((?:[Ff]|[Hh][Tt])[Tt][Pp][Ss]?://[^>]*)>'

# <me@example.com>
AUTOMAIL_RE = r'<([^> \!]*@[^> ]*)>'

# <...>
HTML_RE = r'(\<([a-zA-Z/][^\>]*?|\!--.*?--)\>)'

# &amp;
ENTITY_RE = r'(&[\#a-zA-Z0-9]*;)'

# two spaces at end of line
LINE_BREAK_RE = r'  \n'


def dequote(string):
    """Remove quotes from around a string."""
    if ((string.startswith('"') and string.endswith('"')) or
       (string.startswith("'") and string.endswith("'"))):
        return string[1:-1]
    else:
        return string


ATTR_RE = re.compile(r"\{@([^\}]*)=([^\}]*)}")  # {@id=123}


def handleAttributes(text, parent):
    """Set values of an element based on attribute definitions ({@id=123})."""
    def attributeCallback(match):
        parent.set(match.group(1), match.group(2).replace('\n', ' '))
        return ''
    return ATTR_RE.sub(attributeCallback, text)


"""
The pattern classes
-----------------------------------------------------------------------------
"""


class Pattern(object):
    """Base class that inline patterns subclass. """

    ANCESTOR_EXCLUDES = tuple()

    def __init__(self, pattern, markdown_instance=None):
        """
        Create an instant of an inline pattern.

        Keyword arguments:

        * pattern: A regular expression that matches a pattern

        """
        self.pattern = pattern
        self.compiled_re = re.compile(r"^(.*?)%s(.*)$" % pattern,
                                      re.DOTALL | re.UNICODE)

        # Api for Markdown to pass safe_mode into instance
        self.safe_mode = False
        if markdown_instance:
            self.markdown = markdown_instance

    def getCompiledRegExp(self):
        """ Return a compiled regular expression. """
        return self.compiled_re

    def handleMatch(self, m):
        """Return a ElementTree element from the given match.

        Subclasses should override this method.

        Keyword arguments:

        * m: A re match object containing a match of the pattern.

        """
        pass  # pragma: no cover

    def type(self):
        """ Return class name, to define pattern type """
        return self.__class__.__name__

    def unescape(self, text):
        """ Return unescaped text given text with an inline placeholder. """
        try:
            stash = self.markdown.treeprocessors['inline'].stashed_nodes
        except KeyError:  # pragma: no cover
            return text

        def itertext(el):  # pragma: no cover
            ' Reimplement Element.itertext for older python versions '
            tag = el.tag
            if not isinstance(tag, util.string_type) and tag is not None:
                return
            if el.text:
                yield el.text
            for e in el:
                for s in itertext(e):
                    yield s
                if e.tail:
                    yield e.tail

        def get_stash(m):
            id = m.group(1)
            if id in stash:
                value = stash.get(id)
                if isinstance(value, util.string_type):
                    return value
                else:
                    # An etree Element - return text content only
                    return ''.join(itertext(value))
        return util.INLINE_PLACEHOLDER_RE.sub(get_stash, text)


class InlineProcessor(Pattern):
    """
    Base class that inline patterns subclass.

    This is the newer style inline processor that uses a more
    efficient and flexible search approach.
    """

    def __init__(self, pattern, markdown_instance=None):
        """
        Create an instant of an inline pattern.

        Keyword arguments:

        * pattern: A regular expression that matches a pattern

        """
        self.pattern = pattern
        self.compiled_re = re.compile(pattern, re.DOTALL | re.UNICODE)

        # Api for Markdown to pass safe_mode into instance
        self.safe_mode = False
        if markdown_instance:
            self.markdown = markdown_instance

    def handleMatch(self, m, data):
        """Return a ElementTree element from the given match and the
        start and end index of the matched text.

        If `start` and/or `end` are returned as `None`, it will be
        assumed that the processor did not find a valid region of text.

        Subclasses should override this method.

        Keyword arguments:

        * m: A re match object containing a match of the pattern.
        * data: The buffer current under analysis

        Returns:

        * el: The ElementTree element, text or None.
        * start: The start of the region that has been matched or None.
        * end: The end of the region that has been matched or None.

        """
        pass  # pragma: no cover


class SimpleTextPattern(Pattern):
    """ Return a simple text of group(2) of a Pattern. """
    def handleMatch(self, m):
        return m.group(2)


class SimpleTextInlineProcessor(InlineProcessor):
    """ Return a simple text of group(1) of a Pattern. """
    def handleMatch(self, m, data):
        return m.group(1), m.start(0), m.end(0)


class EscapeInlineProcessor(InlineProcessor):
    """ Return an escaped character. """

    def handleMatch(self, m, data):
        char = m.group(1)
        if char in self.markdown.ESCAPED_CHARS:
            return '%s%s%s' % (util.STX, ord(char), util.ETX), m.start(0), m.end(0)
        else:
            return None, m.start(0), m.end(0)


class SimpleTagPattern(Pattern):
    """
    Return element of type `tag` with a text attribute of group(3)
    of a Pattern.

    """
    def __init__(self, pattern, tag):
        Pattern.__init__(self, pattern)
        self.tag = tag

    def handleMatch(self, m):
        el = util.etree.Element(self.tag)
        el.text = m.group(3)
        return el


class SimpleTagInlineProcessor(InlineProcessor):
    """
    Return element of type `tag` with a text attribute of group(2)
    of a Pattern.

    """
    def __init__(self, pattern, tag):
        InlineProcessor.__init__(self, pattern)
        self.tag = tag

    def handleMatch(self, m, data):
        el = util.etree.Element(self.tag)
        el.text = m.group(2)
        return el, m.start(0), m.end(0)


class SubstituteTagPattern(SimpleTagPattern):
    """ Return an element of type `tag` with no children. """
    def handleMatch(self, m):
        return util.etree.Element(self.tag)


class SubstituteTagInlineProcessor(SimpleTagInlineProcessor):
    """ Return an element of type `tag` with no children. """
    def handleMatch(self, m, data):
        return util.etree.Element(self.tag), m.start(0), m.end(0)


class BacktickInlineProcessor(InlineProcessor):
    """ Return a `<code>` element containing the matching text. """
    def __init__(self, pattern):
        InlineProcessor.__init__(self, pattern)
        self.ESCAPED_BSLASH = '%s%s%s' % (util.STX, ord('\\'), util.ETX)
        self.tag = 'code'

    def handleMatch(self, m, data):
        if m.group(3):
            el = util.etree.Element(self.tag)
            el.text = util.AtomicString(m.group(3).strip())
            return el, m.start(0), m.end(0)
        else:
            return m.group(1).replace('\\\\', self.ESCAPED_BSLASH), m.start(0), m.end(0)


class DoubleTagPattern(SimpleTagPattern):
    """Return a ElementTree element nested in tag2 nested in tag1.

    Useful for strong emphasis etc.

    """
    def handleMatch(self, m):
        tag1, tag2 = self.tag.split(",")
        el1 = util.etree.Element(tag1)
        el2 = util.etree.SubElement(el1, tag2)
        el2.text = m.group(3)
        if len(m.groups()) == 5:
            el2.tail = m.group(4)
        return el1


class DoubleTagInlineProcessor(SimpleTagInlineProcessor):
    """Return a ElementTree element nested in tag2 nested in tag1.

    Useful for strong emphasis etc.

    """
    def handleMatch(self, m, data):
        tag1, tag2 = self.tag.split(",")
        el1 = util.etree.Element(tag1)
        el2 = util.etree.SubElement(el1, tag2)
        el2.text = m.group(2)
        if len(m.groups()) == 3:
            el2.tail = m.group(3)
        return el1, m.start(0), m.end(0)


class HtmlInlineProcessor(InlineProcessor):
    """ Store raw inline html and return a placeholder. """
    def handleMatch(self, m, data):
        rawhtml = self.unescape(m.group(1))
        place_holder = self.markdown.htmlStash.store(rawhtml)
        return place_holder, m.start(0), m.end(0)

    def unescape(self, text):
        """ Return unescaped text given text with an inline placeholder. """
        try:
            stash = self.markdown.treeprocessors['inline'].stashed_nodes
        except KeyError:  # pragma: no cover
            return text

        def get_stash(m):
            id = m.group(1)
            value = stash.get(id)
            if value is not None:
                try:
                    return self.markdown.serializer(value)
                except Exception:
                    return r'\%s' % value

        return util.INLINE_PLACEHOLDER_RE.sub(get_stash, text)


class LinkInlineProcessor(InlineProcessor):
    """ Return a link element from the given match. """
    RE_LINK = re.compile(r'''\(\s*(?:(<.*?>)\s*(?:(['"])(.*?)\2\s*)?\))?''', re.DOTALL | re.UNICODE)
    RE_TITLE_CLEAN = re.compile(r'\s')

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))

        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = util.etree.Element("a")
        el.text = text

        el.set("href", self.sanitize_url(href))

        if title is not None:
            el.set("title", title)

        return el, m.start(0), index

    def getLink(self, data, index):
        """Parse data between `()` of `[Text]()` allowing recursive `()`. """

        href = ''
        title = None
        handled = False

        m = self.RE_LINK.match(data, pos=index)
        if m and m.group(1):
            # Matches [Text](<link> "title")
            href = m.group(1)[1:-1].strip()
            if m.group(3):
                title = m.group(3)
            index = m.end(0)
            handled = True
        elif m:
            # Track bracket nesting and index in string
            bracket_count = 1
            backtrack_count = 1
            start_index = m.end()
            index = start_index
            last_bracket = -1

            # Primary (first found) quote tracking
            # or spaced title (first quote preceeded by a space).
            quote = None
            start_quote = -1
            exit_quote = -1
            ignore_matches = False

            # Secondary (second found) quote tracking,
            # assuming no quote is preceeded by a space.
            alt_quote = None
            start_alt_quote = -1
            exit_alt_quote = -1

            # Track if previous char was a space and the last non-space value
            space = False
            last = ''

            for pos in util.iterrange(index, len(data)):
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
                        # We've found our backup end location if the title doesn't reslove.
                        if backtrack_count == 0:
                            last_bracket = index + 1

                elif c in ("'", '"'):
                    # Quote has started
                    if not quote:
                        # Quote preceeded by a space [text](link "title").
                        # We'll assume we are now in a title.
                        # Brackets are quoted, so no need to match them (except for the final one).
                        ignore_matches = True
                        backtrack_count = bracket_count
                        bracket_count = 1
                        start_quote = index + 1
                        quote = c
                    # Secondary quote (in case the first doesn't resolve): [text](link'"title")
                    # If we are in this situation: [text](link' "title"), we will assume the double quotes
                    # are the the ones we want as they are preceeded by a space.
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

            # We have a scenario: [test](link"notitle)
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

        href = self.sanitize_url(self.unescape(href).strip())

        return href, title, index, handled

    def getText(self, data, index):
        """Parse the content between `[]` of the start of an image or link
        resolving nested square brackets.

        """
        bracket_count = 1
        text = []
        for pos in util.iterrange(index, len(data)):
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

    def sanitize_url(self, url):
        """
        Sanitize a url against xss attacks in "safe_mode".

        Rather than specifically blacklisting `javascript:alert("XSS")` and all
        its aliases (see <http://ha.ckers.org/xss.html>), we whitelist known
        safe url formats. Most urls contain a network location, however some
        are known not to (i.e.: mailto links). Script urls do not contain a
        location. Additionally, for `javascript:...`, the scheme would be
        "javascript" but some aliases will appear to `urlparse()` to have no
        scheme. On top of that relative links (i.e.: "foo/bar.html") have no
        scheme. Therefore we must check "path", "parameters", "query" and
        "fragment" for any literal colons. We don't check "scheme" for colons
        because it *should* never have any and "netloc" must allow the form:
        `username:password@host:port`.

        """
        if not self.markdown.safeMode:
            # Return immediately bipassing parsing.
            return url

        try:
            scheme, netloc, path, params, query, fragment = url = urlparse(url)
        except ValueError:  # pragma: no cover
            # Bad url - so bad it couldn't be parsed.
            return ''

        locless_schemes = ['', 'mailto', 'news']
        allowed_schemes = locless_schemes + ['http', 'https', 'ftp', 'ftps']
        if scheme not in allowed_schemes:
            # Not a known (allowed) scheme. Not safe.
            return ''

        if netloc == '' and scheme not in locless_schemes:  # pragma: no cover
            # This should not happen. Treat as suspect.
            return ''

        for part in url[2:]:
            if ":" in part:
                # A colon in "path", "parameters", "query"
                # or "fragment" is suspect.
                return ''

        # Url passes all tests. Return url as-is.
        return urlunparse(url)


class ImageInlineProcessor(LinkInlineProcessor):
    """ Return a img element from the given match. """

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = util.etree.Element("img")

        el.set("src", self.sanitize_url(src))

        if title is not None:
            el.set("title", title)

        if self.markdown.enable_attributes:
            truealt = handleAttributes(text, el)
        else:
            truealt = text

        el.set('alt', self.unescape(truealt))
        return el, m.start(0), index


class ReferenceInlineProcessor(LinkInlineProcessor):
    """ Match to a stored reference and return link element. """
    NEWLINE_CLEANUP_RE = re.compile(r'[ ]?\n', re.MULTILINE)

    RE_LINK = re.compile(r'\s?\[([^\]]*)\]', re.DOTALL | re.UNICODE)

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        id, end, handled = self.evalId(data, index, text)
        if not handled:
            return None, None, None

        # Clean up linebreaks in id
        id = self.NEWLINE_CLEANUP_RE.sub(' ', id)
        if id not in self.markdown.references:  # ignore undefined refs
            return None, m.start(0), end

        href, title = self.markdown.references[id]

        return self.makeTag(href, title, text), m.start(0), end

    def evalId(self, data, index, text):
        """
        Evaluate the id portion of [ref][id].

        If [ref][] use [ref].
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

    def makeTag(self, href, title, text):
        el = util.etree.Element('a')

        el.set('href', self.sanitize_url(href))
        if title:
            el.set('title', title)

        el.text = text
        return el


class ShortReferenceInlineProcessor(ReferenceInlineProcessor):
    """Shorte form of reference: [google]. """
    def evalId(self, data, index, text):
        """Evaluate the id from of [ref]  """

        return text.lower(), index, True


class ImageReferenceInlineProcessor(ReferenceInlineProcessor):
    """ Match to a stored reference and return img element. """
    def makeTag(self, href, title, text):
        el = util.etree.Element("img")
        el.set("src", self.sanitize_url(href))
        if title:
            el.set("title", title)

        if self.markdown.enable_attributes:
            text = handleAttributes(text, el)

        el.set("alt", self.unescape(text))
        return el


class AutolinkInlineProcessor(InlineProcessor):
    """ Return a link Element given an autolink (`<http://example/com>`). """
    def handleMatch(self, m, data):
        el = util.etree.Element("a")
        el.set('href', self.unescape(m.group(1)))
        el.text = util.AtomicString(m.group(1))
        return el, m.start(0), m.end(0)


class AutomailInlineProcessor(InlineProcessor):
    """
    Return a mailto link Element given an automail link (`<foo@example.com>`).
    """
    def handleMatch(self, m, data):
        el = util.etree.Element('a')
        email = self.unescape(m.group(1))
        if email.startswith("mailto:"):
            email = email[len("mailto:"):]

        def codepoint2name(code):
            """Return entity definition by code, or the code if not defined."""
            entity = entities.codepoint2name.get(code)
            if entity:
                return "%s%s;" % (util.AMP_SUBSTITUTE, entity)
            else:
                return "%s#%d;" % (util.AMP_SUBSTITUTE, code)

        letters = [codepoint2name(ord(letter)) for letter in email]
        el.text = util.AtomicString(''.join(letters))

        mailto = "mailto:" + email
        mailto = "".join([util.AMP_SUBSTITUTE + '#%d;' %
                          ord(letter) for letter in mailto])
        el.set('href', mailto)
        return el, m.start(0), m.end(0)
