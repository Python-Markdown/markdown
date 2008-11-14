"""
Legacy Extension for Python-Markdown
====================================

Replaces the core parser with the old one.

"""

import markdown, re
from markdown import etree

"""Basic and reusable regular expressions."""

def wrapRe(raw_re) : return re.compile("^%s$" % raw_re, re.DOTALL)
CORE_RE = {
    'header':          wrapRe(r'(#{1,6})[ \t]*(.*?)[ \t]*(#*)'), # # A title
    'reference-def':   wrapRe(r'(\ ?\ ?\ ?)\[([^\]]*)\]:\s*([^ ]*)(.*)'),
                               # [Google]: http://www.google.com/
    'containsline':    wrapRe(r'([-]*)$|^([=]*)'), # -----, =====, etc.
    'ol':              wrapRe(r'[ ]{0,3}[\d]*\.\s+(.*)'), # 1. text
    'ul':              wrapRe(r'[ ]{0,3}[*+-]\s+(.*)'), # "* text"
    'isline1':         wrapRe(r'(\**)'), # ***
    'isline2':         wrapRe(r'(\-*)'), # ---
    'isline3':         wrapRe(r'(\_*)'), # ___
    'tabbed':          wrapRe(r'((\t)|(    ))(.*)'), # an indented line
    'quoted':          wrapRe(r'[ ]{0,2}> ?(.*)'), # a quoted block ("> ...")
    'containsline':    re.compile(r'^([-]*)$|^([=]*)$', re.M),
    'attr':            re.compile("\{@([^\}]*)=([^\}]*)}") # {@id=123}
}

class MarkdownParser:
    """Parser Markdown into a ElementTree."""

    def __init__(self):
        pass

    def parseDocument(self, lines):
        """Parse a markdown string into an ElementTree."""
        # Create a ElementTree from the lines
        root = etree.Element("div")
        buffer = []
        for line in lines:
            if line.startswith("#"):
                self.parseChunk(root, buffer)
                buffer = [line]
            else:
                buffer.append(line)

        self.parseChunk(root, buffer)

        return etree.ElementTree(root)

    def parseChunk(self, parent_elem, lines, inList=0, looseList=0):
        """Process a chunk of markdown-formatted text and attach the parse to
        an ElementTree node.

        Process a section of a source document, looking for high
        level structural elements like lists, block quotes, code
        segments, html blocks, etc.  Some those then get stripped
        of their high level markup (e.g. get unindented) and the
        lower-level markup is processed recursively.

        Keyword arguments:

        * parent_elem: The ElementTree element to which the content will be
                       added.
        * lines: a list of lines
        * inList: a level

        Returns: None

        """
        # Loop through lines until none left.
        while lines:
            # Skipping empty line
            if not lines[0]:
                lines = lines[1:]
                continue

            # Check if this section starts with a list, a blockquote or
            # a code block.  If so, process them.
            processFn = { 'ul':     self.__processUList,
                          'ol':     self.__processOList,
                          'quoted': self.__processQuote,
                          'tabbed': self.__processCodeBlock}
            for regexp in ['ul', 'ol', 'quoted', 'tabbed']:
                m = CORE_RE[regexp].match(lines[0])
                if m:
                    processFn[regexp](parent_elem, lines, inList)
                    return

            # We are NOT looking at one of the high-level structures like
            # lists or blockquotes.  So, it's just a regular paragraph
            # (though perhaps nested inside a list or something else).  If
            # we are NOT inside a list, we just need to look for a blank
            # line to find the end of the block.  If we ARE inside a
            # list, however, we need to consider that a sublist does not
            # need to be separated by a blank line.  Rather, the following
            # markup is legal:
            #
            # * The top level list item
            #
            #     Another paragraph of the list.  This is where we are now.
            #     * Underneath we might have a sublist.
            #

            if inList:
                start, lines  = self.__linesUntil(lines, (lambda line:
                                 CORE_RE['ul'].match(line)
                                 or CORE_RE['ol'].match(line)
                                                  or not line.strip()))
                self.parseChunk(parent_elem, start, inList-1,
                                looseList=looseList)
                inList = inList-1

            else: # Ok, so it's just a simple block
                test = lambda line: not line.strip() or line[0] == '>'
                paragraph, lines = self.__linesUntil(lines, test)
                if len(paragraph) and paragraph[0].startswith('#'):
                    self.__processHeader(parent_elem, paragraph)
                elif len(paragraph) and CORE_RE["isline3"].match(paragraph[0]):
                    self.__processHR(parent_elem)
                    lines = paragraph[1:] + lines
                elif paragraph:
                    self.__processParagraph(parent_elem, paragraph,
                                          inList, looseList)

            if lines and not lines[0].strip():
                lines = lines[1:]  # skip the first (blank) line

    def __processHR(self, parentElem):
        hr = etree.SubElement(parentElem, "hr")

    def __processHeader(self, parentElem, paragraph):
        m = CORE_RE['header'].match(paragraph[0])
        if m:
            level = len(m.group(1))
            h = etree.SubElement(parentElem, "h%d" % level)
            h.text = m.group(2).strip()
        else:
            message(CRITICAL, "We've got a problem header!")

    def __processParagraph(self, parentElem, paragraph, inList, looseList):

        if ( parentElem.tag == 'li'
                and not (looseList or parentElem.getchildren())):

            # If this is the first paragraph inside "li", don't
            # put <p> around it - append the paragraph bits directly
            # onto parentElem
            el = parentElem
        else:
            # Otherwise make a "p" element
            el = etree.SubElement(parentElem, "p")

        dump = []

        # Searching for hr or header
        for line in paragraph:
            # it's hr
            if CORE_RE["isline3"].match(line):
                el.text = "\n".join(dump)
                self.__processHR(el)
                dump = []
            # it's header
            elif line.startswith("#"):
                el.text = "\n".join(dump)
                self.__processHeader(parentElem, [line])
                dump = []
            else:
                dump.append(line)
        if dump:
            text = "\n".join(dump)
            el.text = text

    def __processUList(self, parentElem, lines, inList):
        self.__processList(parentElem, lines, inList, listexpr='ul', tag='ul')

    def __processOList(self, parentElem, lines, inList):
        self.__processList(parentElem, lines, inList, listexpr='ol', tag='ol')

    def __processList(self, parentElem, lines, inList, listexpr, tag):
        """
        Given a list of document lines starting with a list item,
        finds the end of the list, breaks it up, and recursively
        processes each list item and the remainder of the text file.

        Keyword arguments:

        * parentElem: A ElementTree element to which the content will be added
        * lines: a list of lines
        * inList: a level

        Returns: None

        """
        ul = etree.SubElement(parentElem, tag) # ul might actually be '<ol>'

        looseList = 0

        # Make a list of list items
        items = []
        item = -1

        i = 0  # a counter to keep track of where we are
        for line in lines:
            loose = 0
            if not line.strip():
                # If we see a blank line, this _might_ be the end of the list
                i += 1
                loose = 1

                # Find the next non-blank line
                for j in range(i, len(lines)):
                    if lines[j].strip():
                        next = lines[j]
                        break
                else:
                    # There is no more text => end of the list
                    break

                # Check if the next non-blank line is still a part of the list

                if ( CORE_RE[listexpr].match(next) or
                     CORE_RE['tabbed'].match(next) ):
                    # get rid of any white space in the line
                    items[item].append(line.strip())
                    looseList = loose or looseList
                    continue
                else:
                    break # found end of the list

            # Now we need to detect list items (at the current level)
            # while also detabing child elements if necessary

            for expr in ['ul', 'ol', 'tabbed']:
                m = CORE_RE[expr].match(line)
                if m:
                    if expr in ['ul', 'ol']:  # We are looking at a new item
                        #if m.group(1) :
                        # Removed the check to allow for a blank line
                        # at the beginning of the list item
                        items.append([m.group(1)])
                        item += 1
                    elif expr == 'tabbed':  # This line needs to be detabbed
                        items[item].append(m.group(4)) #after the 'tab'
                    i += 1
                    break
            else:
                items[item].append(line)  # Just regular continuation
                i += 1 # added on 2006.02.25
        else:
            i += 1

        # Add the ElementTree elements
        for item in items:
            li = etree.SubElement(ul, "li")
            self.parseChunk(li, item, inList + 1, looseList = looseList)

        # Process the remaining part of the section
        self.parseChunk(parentElem, lines[i:], inList)

    def __linesUntil(self, lines, condition):
        """
        A utility function to break a list of lines upon the
        first line that satisfied a condition.  The condition
        argument should be a predicate function.

        """
        i = -1
        for line in lines:
            i += 1
            if condition(line):
                break
        else:
            i += 1
        return lines[:i], lines[i:]

    def __processQuote(self, parentElem, lines, inList):
        """
        Given a list of document lines starting with a quote finds
        the end of the quote, unindents it and recursively
        processes the body of the quote and the remainder of the
        text file.

        Keyword arguments:

        * parentElem: ElementTree element to which the content will be added
        * lines: a list of lines
        * inList: a level

        Returns: None

        """
        dequoted = []
        i = 0
        blank_line = False # allow one blank line between paragraphs
        for line in lines:
            m = CORE_RE['quoted'].match(line)
            if m:
                dequoted.append(m.group(1))
                i += 1
                blank_line = False
            elif not blank_line and line.strip() != '':
                dequoted.append(line)
                i += 1
            elif not blank_line and line.strip() == '':
                dequoted.append(line)
                i += 1
                blank_line = True
            else:
                break

        blockquote = etree.SubElement(parentElem, "blockquote")

        self.parseChunk(blockquote, dequoted, inList)
        self.parseChunk(parentElem, lines[i:], inList)

    def __processCodeBlock(self, parentElem, lines, inList):
        """
        Given a list of document lines starting with a code block
        finds the end of the block, puts it into the ElementTree verbatim
        wrapped in ("<pre><code>") and recursively processes the
        the remainder of the text file.

        Keyword arguments:

        * parentElem: ElementTree element to which the content will be added
        * lines: a list of lines
        * inList: a level

        Returns: None

        """
        detabbed, theRest = self.detectTabbed(lines)
        pre = etree.SubElement(parentElem, "pre")
        code = etree.SubElement(pre, "code")
        text = "\n".join(detabbed).rstrip()+"\n"
        code.text = markdown.AtomicString(text)
        self.parseChunk(parentElem, theRest, inList)

    def detectTabbed(self, lines):
        """ Find indented text and remove indent before further proccesing.

        Keyword arguments:

        * lines: an array of strings

        Returns: a list of post processed items and the unused
        remainder of the original list

        """
        items = []
        item = -1
        i = 0 # to keep track of where we are

        def detab(line):
            match = CORE_RE['tabbed'].match(line)
            if match:
               return match.group(4)

        for line in lines:
            if line.strip(): # Non-blank line
                line = detab(line)
                if line:
                    items.append(line)
                    i += 1
                    continue
                else:
                    return items, lines[i:]

            else: # Blank line: _maybe_ we are done.
                i += 1 # advance

                # Find the next non-blank line
                for j in range(i, len(lines)):
                    if lines[j].strip():
                        next_line = lines[j]; break
                else:
                    break # There is no more text; we are done.

                # Check if the next non-blank line is tabbed
                if detab(next_line): # Yes, more work to do.
                    items.append("")
                    continue
                else:
                    break # No, we are done.
        else:
            i += 1

        return items, lines[i:]

class HeaderPreprocessor(markdown.Preprocessor):

    """Replace underlined headers with hashed headers.

    (To avoid the need for lookahead later.)

    """

    def run (self, lines):
        i = -1
        while i+1 < len(lines):
            i = i+1
            if not lines[i].strip():
                continue

            if lines[i].startswith("#"):
                lines.insert(i+1, "\n")

            if (i+1 <= len(lines)
                  and lines[i+1]
                  and lines[i+1][0] in ['-', '=']):

                underline = lines[i+1].strip()

                if underline == "="*len(underline):
                    lines[i] = "# " + lines[i].strip()
                    lines[i+1] = ""
                elif underline == "-"*len(underline):
                    lines[i] = "## " + lines[i].strip()
                    lines[i+1] = ""

        return lines


class LinePreprocessor(markdown.Preprocessor):
    """Convert HR lines to "___" format."""
    blockquote_re = re.compile(r'^(> )+')

    def run (self, lines):
        for i in range(len(lines)):
            prefix = ''
            m = self.blockquote_re.search(lines[i])
            if m:
                prefix = m.group(0)
            if self._isLine(lines[i][len(prefix):]):
                lines[i] = prefix + "___"
        return lines

    def _isLine(self, block):
        """Determine if a block should be replaced with an <HR>"""
        if block.startswith("    "):
            return False  # a code block
        text = "".join([x for x in block if not x.isspace()])
        if len(text) <= 2:
            return False
        for pattern in ['isline1', 'isline2', 'isline3']:
            m = CORE_RE[pattern].match(text)
            if (m and m.group(1)):
                return True
        else:
            return False


class LegacyExtension(markdown.Extension):
    """ Replace Markdown's core parser. """

    def extendMarkdown(self, md, md_globals):
        """ Set the core parser to an instance of MarkdownParser. """
        md.parser = MarkdownParser()
        md.preprocessors.add ("header", HeaderPreprocessor(self), "<reference")
        md.preprocessors.add("line",  LinePreprocessor(self), "<reference")
 

def makeExtension(configs={}):
    return LegacyExtension(configs=configs)

