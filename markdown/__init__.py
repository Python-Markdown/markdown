"""
Python Markdown
===============

Python Markdown converts Markdown to HTML and can be used as a library or
called from the command line.

## Basic usage as a module:

    import markdown
    md = Markdown()
    html = md.convert(your_text_string)

## Basic use from the command line:

    python markdown.py source.txt > destination.html

Run "python markdown.py --help" to see more options.

## Extensions

See <http://www.freewisdom.org/projects/python-markdown/> for more
information and instructions on how to extend the functionality of
Python Markdown.  Read that before you try modifying this file.

## Authors and License

Started by [Manfred Stienstra](http://www.dwerg.net/).  Continued and
maintained  by [Yuri Takhteyev](http://www.freewisdom.org), [Waylan
Limberg](http://achinghead.com/) and [Artem Yunusov](http://blog.splyer.com).

Contact: markdown@freewisdom.org

Copyright 2007, 2008 The Python Markdown Project (v. 1.7 and later)
Copyright 200? Django Software Foundation (OrderedDict implementation)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see docs/LICENSE for details).
"""

version = "2.0-alpha"
version_info = (2,0,0, "beta")

import re
#import sys
import codecs
import logging
from logging import DEBUG, INFO, WARN, ERROR, CRITICAL


"""
CONSTANTS
=============================================================================
"""

"""
Constants you might want to modify
-----------------------------------------------------------------------------
"""

# default logging level for command-line use
COMMAND_LINE_LOGGING_LEVEL = CRITICAL
TAB_LENGTH = 4               # expand tabs to this many spaces
ENABLE_ATTRIBUTES = True     # @id = xyz -> <... id="xyz">
SMART_EMPHASIS = True        # this_or_that does not become this<i>or</i>that
HTML_REMOVED_TEXT = "[HTML_REMOVED]" # text used instead of HTML in safe mode
BLOCK_LEVEL_ELEMENTS = re.compile("p|div|h[1-6]|blockquote|pre|table|dl|ol|ul"
                                  +"|script|noscript|form|fieldset|iframe|math"
                                  +"|ins|del|hr|hr/|style|li|dt|dd|tr")

import linepreprocessors, blockprocessors, treeprocessors, inlinepatterns, blockparser

"""
Constants you probably do not need to change
-----------------------------------------------------------------------------
"""

RTL_BIDI_RANGES = ( (u'\u0590', u'\u07FF'),
                     # Hebrew (0590-05FF), Arabic (0600-06FF),
                     # Syriac (0700-074F), Arabic supplement (0750-077F),
                     # Thaana (0780-07BF), Nko (07C0-07FF).
                    (u'\u2D30', u'\u2D7F'), # Tifinagh
                    )

# Placeholders
STX = u'\u0002'  # Use STX ("Start of text") for start-of-placeholder
ETX = u'\u0003'  # Use ETX ("End of text") for end-of-placeholder
HTML_PLACEHOLDER_PREFIX = STX+"wzxhzdk:"
HTML_PLACEHOLDER = HTML_PLACEHOLDER_PREFIX + "%d" + ETX
INLINE_PLACEHOLDER_PREFIX = STX+"klzzwxh:"
INLINE_PLACEHOLDER = INLINE_PLACEHOLDER_PREFIX + "%s" + ETX
AMP_SUBSTITUTE = STX+"amp"+ETX


"""
AUXILIARY GLOBAL FUNCTIONS
=============================================================================
"""

def message(level, text):
    """ A wrapper method for logging debug messages. """
    logging.getLogger('MARKDOWN').log(level, text)

## Import
def importETree():
    """Import the best implementation of ElementTree, return a module object."""
    etree_in_c = None
    try: # Is it Python 2.5+ with C implemenation of ElementTree installed?
        import xml.etree.cElementTree as etree_in_c
    except ImportError:
        try: # Is it Python 2.5+ with Python implementation of ElementTree?
            import xml.etree.ElementTree as etree
        except ImportError:
            try: # An earlier version of Python with cElementTree installed?
                import cElementTree as etree_in_c
            except ImportError:
                try: # An earlier version of Python with Python ElementTree?
                    import elementtree.ElementTree as etree
                except ImportError:
                    message(CRITICAL, "Failed to import ElementTree")
                    sys.exit(1)
    if etree_in_c and etree_in_c.VERSION < "1.0":
        message(CRITICAL, "For cElementTree version 1.0 or higher is required.")
        sys.exit(1)
    elif etree_in_c :
        return etree_in_c
    elif etree.VERSION < "1.1":
        message(CRITICAL, "For ElementTree version 1.1 or higher is required")
        sys.exit(1)
    else :
        return etree

def isBlockLevel(tag):
    """Check if the tag is a block level HTML tag."""
    return BLOCK_LEVEL_ELEMENTS.match(tag)


"""
OVERALL DESIGN
=============================================================================

Markdown processing takes place in four steps:

1. A bunch of "preprocessors" munge the input text.
2. BlockParser() parses the high-level structural elements of the
   pre-processed text into an ElementTree.
3. A bunch of "treeprocessors" are run against the ElementTree. One such
   treeprocessor runs InlinePatterns against the ElementTree, detecting inline
   markup.
4. Some post-processors are run against the text after the ElementTree has
   been serialized into text.
5. The output is written to a string.

Those steps are put together by the Markdown() class.

The code below is organized as follows:

1. BlockParser and it's BlockProcessors - does core block parsing.
2. All the preprocessors, patterns, treeprocessors, and postprocessors.
3. Markdown class - does the high-level wrapping.
"""





"""
POST-PROCESSORS
=============================================================================

Markdown also allows post-processors, which are similar to preprocessors in
that they need to implement a "run" method. However, they are run after core
processing.

There are two types of post-processors: Treeprocessor and Postprocessor
"""

class Processor:
    def __init__(self, markdown_instance=None):
        if markdown_instance:
            self.markdown = markdown_instance


class Postprocessor(Processor):
    """
    Postprocessors are run after the ElementTree it converted back into text.

    Each Postprocessor implements a "run" method that takes a pointer to a
    text string, modifies it as necessary and returns a text string.

    Postprocessors must extend markdown.Postprocessor.

    """

    def run(self, text):
        """
        Subclasses of Postprocessor should implement a `run` method, which
        takes the html document as a single text string and returns a
        (possibly modified) string.

        """
        pass



class RawHtmlPostprocessor(Postprocessor):
    """ Restore raw html to the document. """

    def run(self, text):
        """ Iterate over html stash and restore "safe" html. """
        for i in range(self.markdown.htmlStash.html_counter):
            html, safe  = self.markdown.htmlStash.rawHtmlBlocks[i]
            if self.markdown.safeMode and not safe:
                if str(self.markdown.safeMode).lower() == 'escape':
                    html = self.escape(html)
                elif str(self.markdown.safeMode).lower() == 'remove':
                    html = ''
                else:
                    html = HTML_REMOVED_TEXT
            if safe or not self.markdown.safeMode:
                text = text.replace("<p>%s</p>" % (HTML_PLACEHOLDER % i),
                                    html + "\n")
            text =  text.replace(HTML_PLACEHOLDER % i, html)
        return text

    def escape(self, html):
        """ Basic html escaping """
        html = html.replace('&', '&amp;')
        html = html.replace('<', '&lt;')
        html = html.replace('>', '&gt;')
        return html.replace('"', '&quot;')


class AndSubstitutePostprocessor(Postprocessor):
    """ Restore valid entities """
    def __init__(self):
        pass

    def run(self, text):
        text =  text.replace(AMP_SUBSTITUTE, "&")
        return text


"""
MISC AUXILIARY CLASSES
=============================================================================
"""

class AtomicString(unicode):
    """A string which should not be further processed."""
    pass


class HtmlStash:
    """
    This class is used for stashing HTML objects that we extract
    in the beginning and replace with place-holders.
    """

    def __init__ (self):
        """ Create a HtmlStash. """
        self.html_counter = 0 # for counting inline html segments
        self.rawHtmlBlocks=[]

    def store(self, html, safe=False):
        """
        Saves an HTML segment for later reinsertion.  Returns a
        placeholder string that needs to be inserted into the
        document.

        Keyword arguments:

        * html: an html segment
        * safe: label an html segment as safe for safemode

        Returns : a placeholder string

        """
        self.rawHtmlBlocks.append((html, safe))
        placeholder = HTML_PLACEHOLDER % self.html_counter
        self.html_counter += 1
        return placeholder

    def reset(self):
        self.html_counter = 0
        self.rawHtmlBlocks = []

class OrderedDict(dict):
    """
    A dictionary that keeps its keys in the order in which they're inserted.
    
    Copied from Django's SortedDict with some modifications.

    """
    def __new__(cls, *args, **kwargs):
        instance = super(OrderedDict, cls).__new__(cls, *args, **kwargs)
        instance.keyOrder = []
        return instance

    def __init__(self, data=None):
        if data is None:
            data = {}
        super(OrderedDict, self).__init__(data)
        if isinstance(data, dict):
            self.keyOrder = data.keys()
        else:
            self.keyOrder = []
            for key, value in data:
                if key not in self.keyOrder:
                    self.keyOrder.append(key)

    def __deepcopy__(self, memo):
        from copy import deepcopy
        return self.__class__([(key, deepcopy(value, memo))
                               for key, value in self.iteritems()])

    def __setitem__(self, key, value):
        super(OrderedDict, self).__setitem__(key, value)
        if key not in self.keyOrder:
            self.keyOrder.append(key)

    def __delitem__(self, key):
        super(OrderedDict, self).__delitem__(key)
        self.keyOrder.remove(key)

    def __iter__(self):
        for k in self.keyOrder:
            yield k

    def pop(self, k, *args):
        result = super(OrderedDict, self).pop(k, *args)
        try:
            self.keyOrder.remove(k)
        except ValueError:
            # Key wasn't in the dictionary in the first place. No problem.
            pass
        return result

    def popitem(self):
        result = super(OrderedDict, self).popitem()
        self.keyOrder.remove(result[0])
        return result

    def items(self):
        return zip(self.keyOrder, self.values())

    def iteritems(self):
        for key in self.keyOrder:
            yield key, super(OrderedDict, self).__getitem__(key)

    def keys(self):
        return self.keyOrder[:]

    def iterkeys(self):
        return iter(self.keyOrder)

    def values(self):
        return [super(OrderedDict, self).__getitem__(k) for k in self.keyOrder]

    def itervalues(self):
        for key in self.keyOrder:
            yield super(OrderedDict, self).__getitem__(key)

    def update(self, dict_):
        for k, v in dict_.items():
            self.__setitem__(k, v)

    def setdefault(self, key, default):
        if key not in self.keyOrder:
            self.keyOrder.append(key)
        return super(OrderedDict, self).setdefault(key, default)

    def value_for_index(self, index):
        """Return the value of the item at the given zero-based index."""
        return self[self.keyOrder[index]]

    def insert(self, index, key, value):
        """Insert the key, value pair before the item with the given index."""
        if key in self.keyOrder:
            n = self.keyOrder.index(key)
            del self.keyOrder[n]
            if n < index:
                index -= 1
        self.keyOrder.insert(index, key)
        super(OrderedDict, self).__setitem__(key, value)

    def copy(self):
        """Return a copy of this object."""
        # This way of initializing the copy means it works for subclasses, too.
        obj = self.__class__(self)
        obj.keyOrder = self.keyOrder[:]
        return obj

    def __repr__(self):
        """
        Replace the normal dict.__repr__ with a version that returns the keys
        in their sorted order.
        """
        return '{%s}' % ', '.join(['%r: %r' % (k, v) for k, v in self.items()])

    def clear(self):
        super(OrderedDict, self).clear()
        self.keyOrder = []

    def index(self, key):
        """ Return the index of a given key. """
        return self.keyOrder.index(key)

    def index_for_location(self, location):
        """ Return index or None for a given location. """
        if location == '_begin':
            i = 0
        elif location == '_end':
            i = None
        elif location.startswith('<') or location.startswith('>'):
            i = self.index(location[1:])
            if location.startswith('>'):
                if i >= len(self):
                    # last item
                    i = None
                else:
                    i += 1
        else:
            raise ValueError('Not a valid location: "%s". Location key '
                             'must start with a ">" or "<".' % location)
        return i

    def add(self, key, value, location):
        """ Insert by key location. """
        i = self.index_for_location(location)
        if i is not None:
            self.insert(i, key, value)
        else:
            self.__setitem__(key, value)

    def link(self, key, location):
        """ Change location of an existing item. """
        n = self.keyOrder.index(key)
        del self.keyOrder[n]
        i = self.index_for_location(location)
        try:
            if i is not None:
                self.keyOrder.insert(i, key)
            else:
                self.keyOrder.append(key)
        except Error:
            # restore to prevent data loss and reraise
            self.keyOrder.insert(n, key)
            raise Error


"""
Markdown
=============================================================================
"""

class Markdown:
    """Convert Markdown to HTML."""

    def __init__(self,
                 extensions=[],
                 extension_configs={},
                 safe_mode = False):
        """
        Creates a new Markdown instance.

        Keyword arguments:

        * extensions: A list of extensions.
           If they are of type string, the module mdx_name.py will be loaded.
           If they are a subclass of markdown.Extension, they will be used
           as-is.
        * extension-configs: Configuration setting for extensions.
        * safe_mode: Disallow raw html. One of "remove", "replace" or "escape".

        """
        self.parser = blockparser.BlockParser()
        self.safeMode = safe_mode
        self.registeredExtensions = []
        self.docType = ""
        self.stripTopLevelTags = True

        self.preprocessors = OrderedDict()
        self.preprocessors["html_block"] =  linepreprocessors.HtmlBlockPreprocessor(self)
        self.preprocessors["reference"] = linepreprocessors.ReferencePreprocessor(self)
        # footnote preprocessor will be inserted with "<reference"

        self.treeprocessors = OrderedDict()
        self.treeprocessors["inline"] = treeprocessors.InlineProcessor(self)
        self.treeprocessors["prettify"] = treeprocessors.PrettifyTreeprocessor(self)

        self.postprocessors = OrderedDict()
        self.postprocessors["raw_html"] = RawHtmlPostprocessor(self)
        self.postprocessors["amp_substitute"] = AndSubstitutePostprocessor()
        # footnote postprocessor will be inserted with ">amp_substitute"

        self.prePatterns = []

        self.inlinePatterns = OrderedDict()
        self.inlinePatterns["backtick"] = inlinepatterns.BacktickPattern(inlinepatterns.BACKTICK_RE)
        self.inlinePatterns["escape"] = inlinepatterns.SimpleTextPattern(inlinepatterns.ESCAPE_RE)
        self.inlinePatterns["reference"] = inlinepatterns.ReferencePattern(inlinepatterns.REFERENCE_RE, self)
        self.inlinePatterns["link"] = inlinepatterns.LinkPattern(inlinepatterns.LINK_RE, self)
        self.inlinePatterns["image_link"] = inlinepatterns.ImagePattern(inlinepatterns.IMAGE_LINK_RE, self)
        self.inlinePatterns["image_reference"] = \
                            inlinepatterns.ImageReferencePattern(inlinepatterns.IMAGE_REFERENCE_RE, self)
        self.inlinePatterns["autolink"] = inlinepatterns.AutolinkPattern(inlinepatterns.AUTOLINK_RE, self)
        self.inlinePatterns["automail"] = inlinepatterns.AutomailPattern(inlinepatterns.AUTOMAIL_RE, self)
        self.inlinePatterns["linebreak2"] = \
                            inlinepatterns.SubstituteTagPattern(inlinepatterns.LINE_BREAK_2_RE, 'br')
        self.inlinePatterns["linebreak"] = \
                            inlinepatterns.SubstituteTagPattern(inlinepatterns.LINE_BREAK_RE, 'br')
        self.inlinePatterns["html"] = inlinepatterns.HtmlPattern(inlinepatterns.HTML_RE, self)
        self.inlinePatterns["entity"] = inlinepatterns.HtmlPattern(inlinepatterns.ENTITY_RE, self)
        self.inlinePatterns["not_strong"] = inlinepatterns.SimpleTextPattern(inlinepatterns.NOT_STRONG_RE)
        self.inlinePatterns["strong_em"] = \
                            inlinepatterns.DoubleTagPattern(inlinepatterns.STRONG_EM_RE, 'strong,em')
        self.inlinePatterns["strong"] = inlinepatterns.SimpleTagPattern(inlinepatterns.STRONG_RE, 'strong')
        self.inlinePatterns["emphasis"] = inlinepatterns.SimpleTagPattern(inlinepatterns.EMPHASIS_RE, 'em')
        self.inlinePatterns["emphasis2"] = \
                            inlinepatterns.SimpleTagPattern(inlinepatterns.EMPHASIS_2_RE, 'em')
        # The order of the handlers matters!!!

        self.references = {}
        self.htmlStash = HtmlStash()
        self.registerExtensions(extensions = extensions,
                                configs = extension_configs)
        self.reset()

    def registerExtensions(self, extensions, configs):
        """
        Register extensions with this instance of Markdown.

        Keyword aurguments:

        * extensions: A list of extensions, which can either
           be strings or objects.  See the docstring on Markdown.
        * configs: A dictionary mapping module names to config options.

        """
        for ext in extensions:
            if isinstance(ext, basestring):
                ext = load_extension(ext, configs.get(ext, []))
            elif hasattr(ext, 'extendMarkdown'):
                # Looks like an Extension.
                # Nothing to do here.
                pass
            else:
                message(ERROR, "Incorrect type! Extension '%s' is "
                               "neither a string or an Extension." %(repr(ext)))
                continue
            ext.extendMarkdown(self, globals())

    def registerExtension(self, extension):
        """ This gets called by the extension """
        self.registeredExtensions.append(extension)

    def reset(self):
        """
        Resets all state variables so that we can start with a new text.
        """
        self.htmlStash.reset()
        self.references.clear()

        for extension in self.registeredExtensions:
            extension.reset()

    def convert (self, source):
        """Convert markdown to serialized XHTML."""

        # Fixup the source text
        if not source:
            return u""  # a blank unicode string
        try:
            source = unicode(source)
        except UnicodeDecodeError:
            message(CRITICAL, 'UnicodeDecodeError: Markdown only accepts unicode or ascii input.')
            return u""

        source = source.replace(STX, "").replace(ETX, "")
        source = source.replace("\r\n", "\n").replace("\r", "\n") + "\n\n"
        source = re.sub(r'\n\s+\n', '\n\n', source)
        source = source.expandtabs(TAB_LENGTH)

        # Split into lines and run the line preprocessors.
        self.lines = source.split("\n")
        for prep in self.preprocessors.values():
            self.lines = prep.run(self.lines)

        # Parse the high-level elements.
        root = self.parser.parseDocument(self.lines).getroot()

        # Run the tree-processors
        for treeprocessor in self.treeprocessors.values():
            newRoot = treeprocessor.run(root)
            if newRoot:
                root = newRoot

        # Serialize _properly_.  Strip top-level tags.
        xml, length = codecs.utf_8_decode(etree.tostring(root, encoding="utf8"))
        if self.stripTopLevelTags:
            xml = xml.strip()[44:-7] + "\n"

        # Run the text post-processors
        for pp in self.postprocessors.values():
            xml = pp.run(xml)

        return xml.strip()

    def convertFile(self, input = None, output = None, encoding = None):
        """Converts a markdown file and returns the HTML as a unicode string.

        Decodes the file using the provided encoding (defaults to utf-8),
        passes the file content to markdown, and outputs the html to either
        the provided stream or the file with provided name, using the same
        encoding as the source file.

        **Note:** This is the only place that decoding and encoding of unicode
        takes place in Python-Markdown.  (All other code is unicode-in /
        unicode-out.)

        Keyword arguments:

        * input: Name of source text file.
        * output: Name of output file. Writes to stdout if `None`.
        * extensions: A list of extension names (may contain config args).
        * encoding: Encoding of input and output files. Defaults to utf-8.
        * safe_mode: Disallow raw html. One of "remove", "replace" or "escape".

        """

        encoding = encoding or "utf-8"

        # Read the source
        input_file = codecs.open(input, mode="r", encoding=encoding)
        text = input_file.read()
        input_file.close()
        text = text.lstrip(u'\ufeff') # remove the byte-order mark

        # Convert
        html = self.convert(text)

        # Write to file or stdout
        if type(output) == type("string"):
            output_file = codecs.open(output, "w", encoding=encoding)
            output_file.write(html)
            output_file.close()
        else:
            output.write(html.encode(encoding))


"""
Extensions
-----------------------------------------------------------------------------
"""

class Extension:
    """ Base class for extensions to subclass. """
    def __init__(self, configs = {}):
        """Create an instance of an Extention.

        Keyword arguments:

        * configs: A dict of configuration setting used by an Extension.
        """
        self.config = configs

    def getConfig(self, key):
        """ Return a setting for the given key or an empty string. """
        if self.config.has_key(key):
            return self.config[key][0]
        else:
            return ""

    def getConfigInfo(self):
        """ Return all config settings as a list of tuples. """
        return [(key, self.config[key][1]) for key in self.config.keys()]

    def setConfig(self, key, value):
        """ Set a config setting for `key` with the given `value`. """
        self.config[key][0] = value

    def extendMarkdown(self, md, md_globals):
        """
        Add the various proccesors and patterns to the Markdown Instance.

        This method must be overriden by every extension.

        Keyword arguments:

        * md: The Markdown instance.

        * md_globals: Global variables in the markdown module namespace.

        """
        pass

def load_extension(ext_name, configs = []):
    """Load extension by name, then return the module.

    The extension name may contain arguments as part of the string in the
    following format: "extname(key1=value1,key2=value2)"

    """

    # Parse extensions config params (ignore the order)
    configs = dict(configs)
    pos = ext_name.find("(") # find the first "("
    if pos > 0:
        ext_args = ext_name[pos+1:-1]
        ext_name = ext_name[:pos]
        pairs = [x.split("=") for x in ext_args.split(",")]
        configs.update([(x.strip(), y.strip()) for (x, y) in pairs])

    # Setup the module names
    ext_module = 'markdown_extensions'
    module_name_new_style = '.'.join([ext_module, ext_name])
    module_name_old_style = '_'.join(['mdx', ext_name])

    # Try loading the extention first from one place, then another
    try: # New style (markdown_extensons.<extension>)
        module = __import__(module_name_new_style, {}, {}, [ext_module])
    except ImportError:
        try: # Old style (mdx.<extension>)
            module = __import__(module_name_old_style)
        except ImportError:
           message(CRITICAL, "Failed loading extension '%s' from '%s' or '%s'"
               % (ext_name, module_name_new_style, module_name_old_style))

    # If the module is loaded successfully, we expect it to define a
    # function called makeExtension()
    try:
        return module.makeExtension(configs.items())
    except:
        message(CRITICAL, "Failed to instantiate extension '%s'" % ext_name)

def load_extensions(ext_names):
    """Loads multiple extensions"""
    extensions = []
    for ext_name in ext_names:
        extension = load_extension(ext_name)
        if extension:
            extensions.append(extension)
    return extensions

# Extensions should use "markdown.etree" instead of "etree" (or do `from
# markdown import etree`).  Do not import it by yourself.

etree = importETree()

"""
EXPORTED FUNCTIONS
=============================================================================

Those are the two functions we really mean to export: markdown() and
markdownFromFile().
"""

def markdown(text,
             extensions = [],
             safe_mode = False):
    """Convert a markdown string to HTML and return HTML as a unicode string.

    This is a shortcut function for `Markdown` class to cover the most
    basic use case.  It initializes an instance of Markdown, loads the
    necessary extensions and runs the parser on the given text.

    Keyword arguments:

    * text: Markdown formatted text as Unicode or ASCII string.
    * extensions: A list of extensions or extension names (may contain config args).
    * safe_mode: Disallow raw html.  One of "remove", "replace" or "escape".

    Returns: An HTML document as a string.

    """
    md = Markdown(extensions=load_extensions(extensions),
                  safe_mode = safe_mode)
    return md.convert(text)


def markdownFromFile(input = None,
                     output = None,
                     extensions = [],
                     encoding = None,
                     safe = False):
    """Read markdown code from a file and write it to a file or a stream."""
    md = Markdown(extensions=load_extensions(extensions), safe_mode = safe)
    md.convertFile(input, output, encoding)



