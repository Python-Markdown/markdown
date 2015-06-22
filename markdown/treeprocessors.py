from __future__ import unicode_literals
from __future__ import absolute_import
import re
from . import util
from . import odict


def build_treeprocessors(md, **kwargs):
    """ Build the default treeprocessors for Markdown. """
    treeprocessors = odict.OrderedDict()
    treeprocessors["inline"] = InlineProcessor(md)
    treeprocessors["prettify"] = PrettifyTreeprocessor(md)
    return treeprocessors


def isString(s):
    """ Check if it's string """
    if not isinstance(s, util.AtomicString):
        return isinstance(s, util.string_type)
    return False


class Treeprocessor(util.Processor):
    """
    Treeprocessors are run on the ElementTree object before serialization.

    Each Treeprocessor implements a "run" method that takes a pointer to an
    ElementTree, modifies it as necessary and returns an ElementTree
    object.

    Treeprocessors must extend markdown.Treeprocessor.

    """
    def run(self, root):
        """
        Subclasses of Treeprocessor should implement a `run` method, which
        takes a root ElementTree. This method can return another ElementTree
        object, and the existing root ElementTree will be replaced, or it can
        modify the current tree and return None.
        """
        pass  # pragma: no cover


class InlineProcessor(Treeprocessor):
    """
    A Treeprocessor that traverses a tree, applying inline patterns.
    """
    
    def __init__(self, md):
        super(InlineProcessor, self).__init__(md)
        self.TOKEN_RE = re.compile(r'|'.join('\\{0}'.format(x) for x in md.ESCAPED_CHARS + ['  \n']))

    def apply_patterns(self, text):
        """
        Match patterns at begining og given text.
        
        """

        match = node = None
        for pattern in self.md.inlinePatterns.values():
            match = pattern.getCompiledRegExp().match(text)
            if match:
                node = pattern.handleMatch(match)
                if node is not None:
                    text = text[match.end():]
                break
        
        if not match or node is None:
            # Step forward one character
            return text[0], None, text[1:]

        if isString(node):
            return node, None, text

        return '', node,  text

    def handle_inline(self, text):
        """
        Apply inline patterns to the given text.
        
        """

        elem_text = ''
        children = []
        while text:
            m = self.TOKEN_RE.search(text)
            if m:
                if children:
                    children[-1].tail = children[-1].tail + text[:m.start()] if children[-1].tail else text[:m.start()]
                else:
                    elem_text += text[:m.start()]

                pre_text, node, text = self.apply_patterns(text[m.start():])

                if children:
                    children[-1].tail = children[-1].tail + pre_text if children[-1].tail else pre_text
                else:
                    elem_text += pre_text

                if node is not None:
                    children.append(node)
            else:
                # No more matches.
                if children:
                    children[-1].tail = children[-1].tail + text if children[-1].tail else text
                else:
                    elem_text += text
                break
        return elem_text, children
    
    def handle_elem(self, elem, parent, pos):
        """
        Apply patterns to an element and its children recursively.
        
        """
    
        if elem.text and elem.text.strip() and not isinstance(elem.text, util.AtomicString):
            text = elem.text
            elem.text = None
            elem.text, children = self.handle_inline(text)
            elem.extend(children)
        if elem.tail and elem.tail.strip() and not isinstance(elem.tail, util.AtomicString):
            tail = elem.tail
            elem.tail = None
            elem.tail, siblings = self.handle_inline(tail)
            parent.extend(siblings) #  TODO: maybe fix this?

        # Recursively step through children
        for cpos, child in enumerate(elem):
            self.handle_elem(child, elem, cpos)
    
    def run(self, tree):
        """
        Apply inline patterns to a parsed Markdown tree.

        Iterate over ElementTree, find elements with inline tag, apply inline
        patterns and append newly created Elements to tree.  If you don't
        want to process your data with inline paterns, instead of normal
        string, use subclass AtomicString:

            node.text = markdown.util.AtomicString("This will not be processed.")

        Arguments:

        * tree: ElementTree object, representing Markdown tree.

        Returns: None.

        """

        for pos, child in enumerate(tree):
            self.handle_elem(child, tree, pos)

class _InlineProcessor(Treeprocessor):
    """
    A Treeprocessor that traverses a tree, applying inline patterns.
    """

    def __init__(self, md):
        self.__placeholder_prefix = util.INLINE_PLACEHOLDER_PREFIX
        self.__placeholder_suffix = util.ETX
        self.__placeholder_length = 4 + len(self.__placeholder_prefix) \
                                      + len(self.__placeholder_suffix)
        self.__placeholder_re = util.INLINE_PLACEHOLDER_RE
        self.md = md
        self.inlinePatterns = md.inlinePatterns

    def __makePlaceholder(self, type):
        """ Generate a placeholder """
        id = "%04d" % len(self.stashed_nodes)
        hash = util.INLINE_PLACEHOLDER % id
        return hash, id

    def __findPlaceholder(self, data, index):
        """
        Extract id from data string, start from index

        Keyword arguments:

        * data: string
        * index: index, from which we start search

        Returns: placeholder id and string index, after the found placeholder.

        """
        m = self.__placeholder_re.search(data, index)
        if m:
            return m.group(1), m.end()
        else:
            return None, index + 1

    def __stashNode(self, node, type):
        """ Add node to stash """
        placeholder, id = self.__makePlaceholder(type)
        self.stashed_nodes[id] = node
        return placeholder

    def __handleInline(self, data, patternIndex=0):
        """
        Process string with inline patterns and replace it
        with placeholders

        Keyword arguments:

        * data: A line of Markdown text
        * patternIndex: The index of the inlinePattern to start with

        Returns: String with placeholders.

        """
        if not isinstance(data, util.AtomicString):
            startIndex = 0
            while patternIndex < len(self.inlinePatterns):
                data, matched, startIndex = self.__applyPattern(
                    self.inlinePatterns.value_for_index(patternIndex),
                    data, patternIndex, startIndex)
                if not matched:
                    patternIndex += 1
        return data

    def __processElementText(self, node, subnode, isText=True):
        """
        Process placeholders in Element.text or Element.tail
        of Elements popped from self.stashed_nodes.

        Keywords arguments:

        * node: parent node
        * subnode: processing node
        * isText: bool variable, True - it's text, False - it's tail

        Returns: None

        """
        if isText:
            text = subnode.text
            subnode.text = None
        else:
            text = subnode.tail
            subnode.tail = None

        childResult = self.__processPlaceholders(text, subnode, isText)

        if not isText and node is not subnode:
            pos = list(node).index(subnode) + 1
        else:
            pos = 0

        childResult.reverse()
        for newChild in childResult:
            node.insert(pos, newChild)

    def __processPlaceholders(self, data, parent, isText=True):
        """
        Process string with placeholders and generate ElementTree tree.

        Keyword arguments:

        * data: string with placeholders instead of ElementTree elements.
        * parent: Element, which contains processing inline data

        Returns: list with ElementTree elements with applied inline patterns.

        """
        def linkText(text):
            if text:
                if result:
                    if result[-1].tail:
                        result[-1].tail += text
                    else:
                        result[-1].tail = text
                elif not isText:
                    if parent.tail:
                        parent.tail += text
                    else:
                        parent.tail = text
                else:
                    if parent.text:
                        parent.text += text
                    else:
                        parent.text = text
        result = []
        strartIndex = 0
        while data:
            index = data.find(self.__placeholder_prefix, strartIndex)
            if index != -1:
                id, phEndIndex = self.__findPlaceholder(data, index)

                if id in self.stashed_nodes:
                    node = self.stashed_nodes.get(id)

                    if index > 0:
                        text = data[strartIndex:index]
                        linkText(text)

                    if not isString(node):  # it's Element
                        for child in [node] + list(node):
                            if child.tail:
                                if child.tail.strip():
                                    self.__processElementText(
                                        node, child, False
                                    )
                            if child.text:
                                if child.text.strip():
                                    self.__processElementText(child, child)
                    else:  # it's just a string
                        linkText(node)
                        strartIndex = phEndIndex
                        continue

                    strartIndex = phEndIndex
                    result.append(node)

                else:  # wrong placeholder
                    end = index + len(self.__placeholder_prefix)
                    linkText(data[strartIndex:end])
                    strartIndex = end
            else:
                text = data[strartIndex:]
                if isinstance(data, util.AtomicString):
                    # We don't want to loose the AtomicString
                    text = util.AtomicString(text)
                linkText(text)
                data = ""

        return result

    def __applyPattern(self, pattern, data, patternIndex, startIndex=0):
        """
        Check if the line fits the pattern, create the necessary
        elements, add it to stashed_nodes.

        Keyword arguments:

        * data: the text to be processed
        * pattern: the pattern to be checked
        * patternIndex: index of current pattern
        * startIndex: string index, from which we start searching

        Returns: String with placeholders instead of ElementTree elements.

        """
        match = pattern.getCompiledRegExp().match(data[startIndex:])
        leftData = data[:startIndex]

        if not match:
            return data, False, 0

        node = pattern.handleMatch(match)

        if node is None:
            return data, True, len(leftData)+match.span(len(match.groups()))[0]

        if not isString(node):
            if not isinstance(node.text, util.AtomicString):
                # We need to process current node too
                for child in [node] + list(node):
                    if not isString(node):
                        if child.text:
                            child.text = self.__handleInline(
                                child.text, patternIndex + 1
                            )
                        if child.tail:
                            child.tail = self.__handleInline(
                                child.tail, patternIndex
                            )

        placeholder = self.__stashNode(node, pattern.type())

        return "%s%s%s%s" % (leftData,
                             match.group(1),
                             placeholder, match.groups()[-1]), True, 0

    def run(self, tree):
        """Apply inline patterns to a parsed Markdown tree.

        Iterate over ElementTree, find elements with inline tag, apply inline
        patterns and append newly created Elements to tree.  If you don't
        want to process your data with inline paterns, instead of normal
        string, use subclass AtomicString:

            node.text = markdown.util.AtomicString("This will not be processed.")

        Arguments:

        * tree: ElementTree object, representing Markdown tree.

        Returns: ElementTree object with applied inline patterns.

        """
        self.stashed_nodes = {}

        stack = [tree]

        while stack:
            currElement = stack.pop()
            insertQueue = []
            for child in currElement:
                if child.text and not isinstance(
                    child.text, util.AtomicString
                ):
                    text = child.text
                    child.text = None
                    lst = self.__processPlaceholders(
                        self.__handleInline(text), child
                    )
                    stack += lst
                    insertQueue.append((child, lst))
                if child.tail:
                    tail = self.__handleInline(child.tail)
                    dumby = util.etree.Element('d')
                    child.tail = None
                    tailResult = self.__processPlaceholders(tail, dumby, False)
                    if dumby.tail:
                        child.tail = dumby.tail
                    pos = list(currElement).index(child) + 1
                    tailResult.reverse()
                    for newChild in tailResult:
                        currElement.insert(pos, newChild)
                if len(child):
                    stack.append(child)

            for element, lst in insertQueue:
                for i, newChild in enumerate(lst):
                    element.insert(i, newChild)
        return tree


class PrettifyTreeprocessor(Treeprocessor):
    """ Add linebreaks to the html document. """

    def _prettifyETree(self, elem):
        """ Recursively add linebreaks to ElementTree children. """

        i = "\n"
        if util.isBlockLevel(elem.tag) and elem.tag not in ['code', 'pre']:
            if (not elem.text or not elem.text.strip()) \
                    and len(elem) and util.isBlockLevel(elem[0].tag):
                elem.text = i
            for e in elem:
                if util.isBlockLevel(e.tag):
                    self._prettifyETree(e)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        if not elem.tail or not elem.tail.strip():
            elem.tail = i

    def run(self, root):
        """ Add linebreaks to ElementTree root object. """

        self._prettifyETree(root)
        # Do <br />'s seperately as they are often in the middle of
        # inline content and missed by _prettifyETree.
        brs = root.getiterator('br')
        for br in brs:
            if not br.tail or not br.tail.strip():
                br.tail = '\n'
            else:
                br.tail = '\n%s' % br.tail
        # Clean up extra empty lines at end of code blocks.
        pres = root.getiterator('pre')
        for pre in pres:
            if len(pre) and pre[0].tag == 'code':
                pre[0].text = util.AtomicString(pre[0].text.rstrip() + '\n')
