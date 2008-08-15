"""
========================= FOOTNOTES =================================

This section adds footnote handling to markdown.  It can be used as
an example for extending python-markdown with relatively complex
functionality.  While in this case the extension is included inside
the module itself, it could just as easily be added from outside the
module.  Not that all markdown classes above are ignorant about
footnotes.  All footnote functionality is provided separately and
then added to the markdown instance at the run time.

Footnote functionality is attached by calling extendMarkdown()
method of FootnoteExtension.  The method also registers the
extension to allow it's state to be reset by a call to reset()
method.

Example:
    Footnotes[^1] have a label[^label] and a definition[^!DEF].

    [^1]: This is a footnote
    [^label]: A footnote on "label"
    [^!DEF]: The footnote for definition

"""

FN_BACKLINK_TEXT = "zz1337820767766393qq"


import re, markdown, random
from markdown import etree

class FootnoteExtension (markdown.Extension):

    DEF_RE = re.compile(r'(\ ?\ ?\ ?)\[\^([^\]]*)\]:\s*(.*)')
    SHORT_USE_RE = re.compile(r'\[\^([^\]]*)\]', re.M) # [^a]

    def __init__ (self, configs) :

        self.config = {'PLACE_MARKER' :
                       ["///Footnotes Go Here///",
                        "The text string that marks where the footnotes go"]}

        for key, value in configs :
            self.config[key][0] = value
            
        self.reset()

    def extendMarkdown(self, md, md_globals) :

        self.md = md

        # Stateless extensions do not need to be registered
        md.registerExtension(self)

        # Insert a preprocessor before ReferencePreprocessor
        index = md.preprocessors.index(md_globals['REFERENCE_PREPROCESSOR'])
        preprocessor = FootnotePreprocessor(self)
        preprocessor.md = md
        md.preprocessors.insert(index, preprocessor)

        # Insert an inline pattern before ImageReferencePattern
        FOOTNOTE_RE = r'\[\^([^\]]*)\]' # blah blah [^1] blah
        index = md.inlinePatterns.index(md_globals['IMAGE_REFERENCE_PATTERN'])
        md.inlinePatterns.insert(index, FootnotePattern(FOOTNOTE_RE, self))

        # Insert a post-processor that would actually add the footnote div
        postprocessor = FootnotePostprocessor(self)
        postprocessor.extension = self

        md.postprocessors.append(postprocessor)
        
        textPostprocessor = FootnoteTextPostprocessor(self)

        md.textPostprocessors.append(textPostprocessor)


    def reset(self) :
        # May be called by Markdown is state reset is desired

        self.footnote_suffix = "-" + str(int(random.random()*1000000000))
        self.used_footnotes={}
        self.footnotes = {}

    def findFootnotesPlaceholder(self, root):
        
        def finder(element):
            for child in element:
                if child.text:
                    if child.text.find(self.getConfig("PLACE_MARKER")) > -1:
                        return child, True
                if child.tail:
                    if child.tail.find(self.getConfig("PLACE_MARKER")) > -1:
                        return (child, element), False
                finder(child)
            return None
                
        res = finder(root)
        return res


    def setFootnote(self, id, text) :
        self.footnotes[id] = text

    def makeFootnoteId(self, num) :
        return 'fn%d%s' % (num, self.footnote_suffix)

    def makeFootnoteRefId(self, num) :
        return 'fnr%d%s' % (num, self.footnote_suffix)

    def makeFootnotesDiv (self, root) :
        """Creates the div with class='footnote' and populates it with
           the text of the footnotes.

           @returns: the footnote div as a dom element """

        if not self.footnotes.keys() :
            return None

        div = etree.Element("div")
        div.set('class', 'footnote')
        hr = etree.SubElement(div, "hr")
        ol = etree.SubElement(div, "ol")
        

        footnotes = [(self.used_footnotes[id], id)
                     for id in self.footnotes.keys()]
        footnotes.sort()

        for i, id in footnotes :
            li = etree.SubElement(ol, "li")
            li.set("id", self.makeFootnoteId(i))

            self.md._processSection(li, self.footnotes[id].split("\n"), looseList=1)

            backlink = etree.Element("a")
            backlink.set("href", "#" + self.makeFootnoteRefId(i))
            backlink.set("class", "footnoteBackLink")
            backlink.set("title",
                                  "Jump back to footnote %d in the text" % i)
            backlink.text = FN_BACKLINK_TEXT

            if li.getchildren():
                node = li[-1]
                if node.text:
		            li.append(backlink)
                elif node.tag == "p":
                    node.append(backlink)
                else:
                    p = etree.SubElement(li, "p")
                    p.append(backlink)
        div = self.md.applyInlinePatterns(etree.ElementTree(div)).getroot()
        return div


class FootnotePreprocessor :

    def __init__ (self, footnotes) :
        self.footnotes = footnotes

    def run(self, lines) :

        self.blockGuru = markdown.BlockGuru()
        lines = self._handleFootnoteDefinitions (lines)

        # Make a hash of all footnote marks in the text so that we
        # know in what order they are supposed to appear.  (This
        # function call doesn't really substitute anything - it's just
        # a way to get a callback for each occurence.

        text = "\n".join(lines)
        self.footnotes.SHORT_USE_RE.sub(self.recordFootnoteUse, text)

        return text.split("\n")


    def recordFootnoteUse(self, match) :

        id = match.group(1)
        id = id.strip()
        nextNum = len(self.footnotes.used_footnotes.keys()) + 1
        self.footnotes.used_footnotes[id] = nextNum


    def _handleFootnoteDefinitions(self, lines) :
        """Recursively finds all footnote definitions in the lines.

            @param lines: a list of lines of text
            @returns: a string representing the text with footnote
                      definitions removed """

        i, id, footnote = self._findFootnoteDefinition(lines)

        if id :

            plain = lines[:i]

            detabbed, theRest = self.blockGuru.detectTabbed(lines[i+1:])
   
            self.footnotes.setFootnote(id,
                                       footnote + "\n"
                                       + "\n".join(detabbed))

            more_plain = self._handleFootnoteDefinitions(theRest)
            return plain + [""] + more_plain

        else :
            return lines

    def _findFootnoteDefinition(self, lines) :
        """Finds the first line of a footnote definition.

            @param lines: a list of lines of text
            @returns: the index of the line containing a footnote definition """

        counter = 0
        for line in lines :
            m = self.footnotes.DEF_RE.match(line)
            if m :
                return counter, m.group(2), m.group(3)
            counter += 1
        return counter, None, None


class FootnotePattern (markdown.Pattern) :

    def __init__ (self, pattern, footnotes) :

        markdown.Pattern.__init__(self, pattern)
        self.footnotes = footnotes

    def handleMatch(self, m) :
        sup = etree.Element("sup")
        a = etree.SubElement(sup, "a")
        id = m.group(2)
        num = self.footnotes.used_footnotes[id]
        sup.set('id', self.footnotes.makeFootnoteRefId(num))
        a.set('href', '#' + self.footnotes.makeFootnoteId(num))
        a.text = str(num)
        return sup

class FootnotePostprocessor (markdown.Postprocessor):

    def __init__ (self, footnotes) :
        self.footnotes = footnotes

    def run(self, root):
        footnotesDiv = self.footnotes.makeFootnotesDiv(root)
        if footnotesDiv:
            result = self.extension.findFootnotesPlaceholder(root)

            if result:
                node, isText = result
                if isText:
                    node.text = None
                    node.getchildren().insert(0, footnotesDiv)
                else:
                    child, element = node
                    ind = element.getchildren().find(child)
                    element.getchildren().insert(ind + 1, footnotesDiv)
                    child.tail = None
                    
                fnPlaceholder.parent.replaceChild(fnPlaceholder, footnotesDiv)
            else :
                root.append(footnotesDiv)

class FootnoteTextPostprocessor (markdown.Postprocessor):

    def __init__ (self, footnotes) :
        self.footnotes = footnotes

    def run(self, text) :
        return text.replace(FN_BACKLINK_TEXT, "&#8617;")

def makeExtension(configs=[]):
    return FootnoteExtension(configs=configs)

