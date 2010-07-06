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

    markdown source.txt > destination.html

Run "markdown --help" to see more options.

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

version = "2.0.3"
version_info = (2,0,3, "Final")

import re
import codecs

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

"""


from logging import DEBUG, INFO, WARN, ERROR, CRITICAL
from md_logging import message
import util
import preprocessors
import blockprocessors
import treeprocessors
import inlinepatterns
import postprocessors
import blockparser
import odict
from extensions import Extension, load_extension, load_extensions

# For backwards compatibility in the 2.0.x series
# The things defined in these modules started off in __init__.py so third
# party code might need to access them here.
from util import *

# Adds the ability to output html4
import html4


class Markdown:
    """Convert Markdown to HTML."""

    def __init__(self,
                 extensions=[],
                 extension_configs={},
                 safe_mode = False,
                 output_format=util.DEFAULT_OUTPUT_FORMAT):
        """
        Creates a new Markdown instance.

        Keyword arguments:

        * extensions: A list of extensions.
           If they are of type string, the module mdx_name.py will be loaded.
           If they are a subclass of markdown.Extension, they will be used
           as-is.
        * extension-configs: Configuration setting for extensions.
        * safe_mode: Disallow raw html. One of "remove", "replace" or "escape".
        * output_format: Format of output. Supported formats are:
            * "xhtml1": Outputs XHTML 1.x. Default.
            * "xhtml": Outputs latest supported version of XHTML (currently XHTML 1.1).
            * "html4": Outputs HTML 4
            * "html": Outputs latest supported version of HTML (currently HTML 4).
            Note that it is suggested that the more specific formats ("xhtml1"
            and "html4") be used as "xhtml" or "html" may change in the future
            if it makes sense at that time.

        """

        self.safeMode = safe_mode
        self.registeredExtensions = []
        self.docType = ""
        self.stripTopLevelTags = True

        # Preprocessors
        self.preprocessors = odict.OrderedDict()
        self.preprocessors["html_block"] = \
                preprocessors.HtmlBlockPreprocessor(self)
        self.preprocessors["reference"] = \
                preprocessors.ReferencePreprocessor(self)
        # footnote preprocessor will be inserted with "<reference"

        # Block processors - ran by the parser
        self.parser = blockparser.BlockParser()
        self.parser.blockprocessors['empty'] = \
                blockprocessors.EmptyBlockProcessor(self.parser)
        self.parser.blockprocessors['indent'] = \
                blockprocessors.ListIndentProcessor(self.parser)
        self.parser.blockprocessors['code'] = \
                blockprocessors.CodeBlockProcessor(self.parser)
        self.parser.blockprocessors['hashheader'] = \
                blockprocessors.HashHeaderProcessor(self.parser)
        self.parser.blockprocessors['setextheader'] = \
                blockprocessors.SetextHeaderProcessor(self.parser)
        self.parser.blockprocessors['hr'] = \
                blockprocessors.HRProcessor(self.parser)
        self.parser.blockprocessors['olist'] = \
                blockprocessors.OListProcessor(self.parser)
        self.parser.blockprocessors['ulist'] = \
                blockprocessors.UListProcessor(self.parser)
        self.parser.blockprocessors['quote'] = \
                blockprocessors.BlockQuoteProcessor(self.parser)
        self.parser.blockprocessors['paragraph'] = \
                blockprocessors.ParagraphProcessor(self.parser)


        #self.prePatterns = []

        # Inline patterns - Run on the tree
        self.inlinePatterns = odict.OrderedDict()
        self.inlinePatterns["backtick"] = \
                inlinepatterns.BacktickPattern(inlinepatterns.BACKTICK_RE)
        self.inlinePatterns["escape"] = \
                inlinepatterns.SimpleTextPattern(inlinepatterns.ESCAPE_RE)
        self.inlinePatterns["reference"] = \
            inlinepatterns.ReferencePattern(inlinepatterns.REFERENCE_RE, self)
        self.inlinePatterns["link"] = \
                inlinepatterns.LinkPattern(inlinepatterns.LINK_RE, self)
        self.inlinePatterns["image_link"] = \
                inlinepatterns.ImagePattern(inlinepatterns.IMAGE_LINK_RE, self)
        self.inlinePatterns["image_reference"] = \
            inlinepatterns.ImageReferencePattern(inlinepatterns.IMAGE_REFERENCE_RE, self)
        self.inlinePatterns["autolink"] = \
            inlinepatterns.AutolinkPattern(inlinepatterns.AUTOLINK_RE, self)
        self.inlinePatterns["automail"] = \
            inlinepatterns.AutomailPattern(inlinepatterns.AUTOMAIL_RE, self)
        self.inlinePatterns["linebreak2"] = \
            inlinepatterns.SubstituteTagPattern(inlinepatterns.LINE_BREAK_2_RE, 'br')
        self.inlinePatterns["linebreak"] = \
            inlinepatterns.SubstituteTagPattern(inlinepatterns.LINE_BREAK_RE, 'br')
        self.inlinePatterns["html"] = \
                inlinepatterns.HtmlPattern(inlinepatterns.HTML_RE, self)
        self.inlinePatterns["entity"] = \
                inlinepatterns.HtmlPattern(inlinepatterns.ENTITY_RE, self)
        self.inlinePatterns["not_strong"] = \
                inlinepatterns.SimpleTextPattern(inlinepatterns.NOT_STRONG_RE)
        self.inlinePatterns["strong_em"] = \
            inlinepatterns.DoubleTagPattern(inlinepatterns.STRONG_EM_RE, 'strong,em')
        self.inlinePatterns["strong"] = \
            inlinepatterns.SimpleTagPattern(inlinepatterns.STRONG_RE, 'strong')
        self.inlinePatterns["emphasis"] = \
            inlinepatterns.SimpleTagPattern(inlinepatterns.EMPHASIS_RE, 'em')
        self.inlinePatterns["emphasis2"] = \
            inlinepatterns.SimpleTagPattern(inlinepatterns.EMPHASIS_2_RE, 'em')
        # The order of the handlers matters!!!


        # Tree processors - run once we have a basic parse.
        self.treeprocessors = odict.OrderedDict()
        self.treeprocessors["inline"] = treeprocessors.InlineProcessor(self)
        self.treeprocessors["prettify"] = \
                treeprocessors.PrettifyTreeprocessor(self)

        # Postprocessors - finishing touches.
        self.postprocessors = odict.OrderedDict()
        self.postprocessors["raw_html"] = \
                postprocessors.RawHtmlPostprocessor(self)
        self.postprocessors["amp_substitute"] = \
                postprocessors.AndSubstitutePostprocessor()
        # footnote postprocessor will be inserted with ">amp_substitute"

        # Map format keys to serializers
        self.output_formats = {
            'html'  : html4.to_html_string,
            'html4' : html4.to_html_string,
            'xhtml' : util.etree.tostring,
            'xhtml1': util.etree.tostring,
        }

        self.references = {}
        self.htmlStash = util.HtmlStash()
        self.registerExtensions(extensions = extensions,
                                configs = extension_configs)
        self.set_output_format(output_format)
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
            if isinstance(ext, Extension):
                try:
                    ext.extendMarkdown(self, globals())
                except NotImplementedError, e:
                    message(ERROR, e)
            else:
                message(ERROR,
                'Extension "%s.%s" must be of type: "markdown.Extension".' \
                    % (ext.__class__.__module__, ext.__class__.__name__))

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
            if hasattr(extension, 'reset'):
                extension.reset()

    def set_output_format(self, format):
        """ Set the output format for the class instance. """
        try:
            self.serializer = self.output_formats[format.lower()]
        except KeyError:
            message(CRITICAL,
                    'Invalid Output Format: "%s". Use one of %s.' \
                               % (format, self.output_formats.keys()))

    def convert(self, source):
        """
        Convert markdown to serialized XHTML or HTML.

        Keyword arguments:

        * source: Source text as a Unicode string.

        """

        # Fixup the source text
        if not source.strip():
            return u""  # a blank unicode string
        try:
            source = unicode(source)
        except UnicodeDecodeError:
            message(CRITICAL,
                    'UnicodeDecodeError: Markdown only accepts unicode or ascii input.')
            return u""

        source = source.replace(util.STX, "").replace(util.ETX, "")
        source = source.replace("\r\n", "\n").replace("\r", "\n") + "\n\n"
        source = re.sub(r'\n\s+\n', '\n\n', source)
        source = source.expandtabs(util.TAB_LENGTH)

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
        output, length = codecs.utf_8_decode(self.serializer(root, encoding="utf-8"))
        if self.stripTopLevelTags:
            try:
                start = output.index('<%s>'%util.DOC_TAG)+len(util.DOC_TAG)+2
                end = output.rindex('</%s>'%util.DOC_TAG)
                output = output[start:end].strip()
            except ValueError:
                if output.strip().endswith('<%s />'%util.DOC_TAG):
                    # We have an empty document
                    output = ''
                else:
                    # We have a serious problem
                    message(CRITICAL, 'Failed to strip top level tags.')

        # Run the text post-processors
        for pp in self.postprocessors.values():
            output = pp.run(output)

        return output.strip()

    def convertFile(self, input=None, output=None, encoding=None):
        """Converts a markdown file and returns the HTML as a unicode string.

        Decodes the file using the provided encoding (defaults to utf-8),
        passes the file content to markdown, and outputs the html to either
        the provided stream or the file with provided name, using the same
        encoding as the source file.

        **Note:** This is the only place that decoding and encoding of unicode
        takes place in Python-Markdown.  (All other code is unicode-in /
        unicode-out.)

        Keyword arguments:

        * input: File object or path of file as string.
        * output: Name of output file. Writes to stdout if `None`.
        * encoding: Encoding of input and output files. Defaults to utf-8.

        """

        encoding = encoding or "utf-8"

        # Read the source
        if isinstance(input, basestring):
            input_file = codecs.open(input, mode="r", encoding=encoding)
        else:
            input_file = input
        text = input_file.read()
        input_file.close()
        text = text.lstrip(u'\ufeff') # remove the byte-order mark

        # Convert
        html = self.convert(text)

        # Write to file or stdout
        if isinstance(output, (str, unicode)):
            output_file = codecs.open(output, "w", encoding=encoding)
            output_file.write(html)
            output_file.close()
        else:
            output.write(html.encode(encoding))


"""
EXPORTED FUNCTIONS
=============================================================================

Those are the two functions we really mean to export: markdown() and
markdownFromFile().
"""

def markdown(text,
             extensions = [],
             safe_mode = False,
             output_format = util.DEFAULT_OUTPUT_FORMAT):
    """Convert a markdown string to HTML and return HTML as a unicode string.

    This is a shortcut function for `Markdown` class to cover the most
    basic use case.  It initializes an instance of Markdown, loads the
    necessary extensions and runs the parser on the given text.

    Keyword arguments:

    * text: Markdown formatted text as Unicode or ASCII string.
    * extensions: A list of extensions or extension names (may contain config args).
    * safe_mode: Disallow raw html.  One of "remove", "replace" or "escape".
    * output_format: Format of output. Supported formats are:
        * "xhtml1": Outputs XHTML 1.x. Default.
        * "xhtml": Outputs latest supported version of XHTML (currently XHTML 1.1).
        * "html4": Outputs HTML 4
        * "html": Outputs latest supported version of HTML (currently HTML 4).
        Note that it is suggested that the more specific formats ("xhtml1"
        and "html4") be used as "xhtml" or "html" may change in the future
        if it makes sense at that time.

    Returns: An HTML document as a string.

    """
    md = Markdown(extensions=load_extensions(extensions),
                  safe_mode=safe_mode,
                  output_format=output_format)
    return md.convert(text)


def markdownFromFile(input = None,
                     output = None,
                     extensions = [],
                     encoding = None,
                     safe_mode = False,
                     output_format = util.DEFAULT_OUTPUT_FORMAT):
    """Read markdown code from a file and write it to a file or a stream."""
    md = Markdown(extensions=load_extensions(extensions),
                  safe_mode=safe_mode,
                  output_format=output_format)
    md.convertFile(input, output, encoding)



