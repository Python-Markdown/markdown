#!/usr/bin/env Python
"""
Definition List Extension for Python-Markdown
=============================================

Added parsing of Definition Lists to Python-Markdown.

A simple example:

    Apple
    :   Pomaceous fruit of plants of the genus Malus in 
        the family Rosaceae.
    :   An american computer company.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.

Copyright 2008 - [Waylan Limberg](http://achinghead.com)

"""

import markdown
from markdown import etree, CORE_RE

class DefListParser(markdown.MarkdownParser):
    """ Subclass of MarkdownParser which adds definition list parsing. """

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
            processFn = { 'ul':     self._MarkdownParser__processUList,
                          'ol':     self._MarkdownParser__processOList,
                          'quoted': self._MarkdownParser__processQuote,
                          'tabbed': self._MarkdownParser__processCodeBlock}
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
                start, lines  = self._MarkdownParser__linesUntil(lines, (lambda line:
                                 CORE_RE['ul'].match(line)
                                 or CORE_RE['ol'].match(line)
                                                  or not line.strip()))
                self.parseChunk(parent_elem, start, inList-1,
                                looseList=looseList)
                inList = inList-1

            else: # Ok, so it's just a simple block
                test = lambda line: not line.strip() or line[0] == '>'
                paragraph, lines = self._MarkdownParser__linesUntil(lines, test)
                if len(paragraph) and paragraph[0].startswith('#'):
                    self._MarkdownParser__processHeader(parent_elem, paragraph)
                elif len(paragraph) and CORE_RE["isline3"].match(paragraph[0]):
                    self._MarkdownParser__processHR(parent_elem)
                    lines = paragraph[1:] + lines
                elif paragraph:
                    terms, defs, paragraph = self._getDefs(paragraph)
                    if defs:
                        # check for extra paragraphs of a def
                        extradef, lines = self.detectTabbed(lines)
                        defs[-1].extend(extradef)
                        self._processDef(parent_elem, terms, defs)
                    if len(paragraph):
                        self._MarkdownParser__processParagraph(parent_elem, 
                                                               paragraph,
                                                               inList, 
                                                               looseList)

            if lines and not lines[0].strip():
                lines = lines[1:]  # skip the first (blank) line


    def _getDefs(self, lines):
        terms = []
        defs = []
        i = 0
        while i < len(lines):
            if lines[i].startswith(':   '):
                d  = self._getDef(lines[i:])
                if d:
                    defs.append(d)
                    i += len(d)
            else:
                terms.append(lines[i])
                i += 1
        if defs:
            return terms, defs, []
        else:
            return None, None, terms

    def _getDef(self, lines):
        if lines[0].startswith(':   '):
            Def, theRest  = self.detectTabbed(lines[1:])
            Def.insert(0, lines[0][4:])
            return Def
        return []

    def _processDef(self, parentElem, terms, defs):
        children = parentElem.getchildren()
        if children and children[-1].tag == "dl":
            dl = children[-1]
        else:
            dl = etree.SubElement(parentElem, "dl")
        for term in terms:
            dt = etree.SubElement(dl, "dt")
            dt.text = term
        for d in defs:
            dd = etree.SubElement(dl, "dd")
            self.parseChunk(dd, d)

    def _MarkdownParser__processParagraph(self, parentElem, paragraph, inList, looseList):

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


class DefListExtension(markdown.Extension):
    """ Add definition lists to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Set the core parser to an instance of DefListParser. """
        md.parser = DefListParser()


def makeExtension(configs={}):
    return DefListExtension(configs=configs)

