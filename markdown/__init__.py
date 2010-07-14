"""
Python Markdown
===============

Python Markdown converts Markdown to HTML and can be used as a library or
called from the command line.

## Basic usage as a module:

    import markdown
    html = markdown.markdown(your_text_string)

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

License: BSD (see LICENSE for details).
"""

version = "2.1.0"
version_info = (2,1,0, "Dev")

import re
import codecs
from logging import DEBUG, INFO, WARN, ERROR, CRITICAL
from md_logging import message
import util
from preprocessors import build_preprocessors
from blockprocessors import build_block_parser
from treeprocessors import build_treeprocessors
from inlinepatterns import build_inlinepatterns
from postprocessors import build_postprocessors
from extensions import Extension, load_extension, load_extensions
import html4

# For backwards compatibility in the 2.0.x series
# The things defined in these modules started off in __init__.py so third
# party code might need to access them here.
from util import *


class Markdown:
    """Convert Markdown to HTML."""

    doc_tag = "div"     # Element used to wrap document - later removed
    
    option_defaults = {
        'html_replacement_text' : '[HTML_REMOVED]',
        'tab_length'            : 4,
        'enable_attributes'     : True,
        'smart_emphasis'        : True,
    }
    
    output_formats = {
        'html'  : html4.to_html_string,
        'html4' : html4.to_html_string,
        'xhtml' : util.etree.tostring,
        'xhtml1': util.etree.tostring,
    }

    def __init__(self, extensions=[], **kwargs):
        """
        Creates a new Markdown instance.

        Keyword arguments:

        * extensions: A list of extensions.
           If they are of type string, the module mdx_name.py will be loaded.
           If they are a subclass of markdown.Extension, they will be used
           as-is.
        * extension-configs: Configuration settingis for extensions.
        * output_format: Format of output. Supported formats are:
            * "xhtml1": Outputs XHTML 1.x. Default.
            * "xhtml": Outputs latest supported version of XHTML (currently XHTML 1.1).
            * "html4": Outputs HTML 4
            * "html": Outputs latest supported version of HTML (currently HTML 4).
            Note that it is suggested that the more specific formats ("xhtml1"
            and "html4") be used as "xhtml" or "html" may change in the future
            if it makes sense at that time.
        * safe_mode: Disallow raw html. One of "remove", "replace" or "escape".
        * html_replacement_text: Text used when safe_mode is set to "replace".
        * tab_length: Length of tabs in the source. Default: 4
        * enable_attributes: Enable the conversion of attributes. Default: True
        * smart_emphsasis: Treat `_connected_words_` intelegently Default: True

        """

        for option, default in self.option_defaults.items():
            setattr(self, option, kwargs.get(option, default)) 

        self.safeMode = kwargs.get('safe_mode', False)
        self.registeredExtensions = []
        self.docType = ""
        self.stripTopLevelTags = True

        self.build_parser()

        self.references = {}
        self.htmlStash = util.HtmlStash()
        self.registerExtensions(extensions = extensions,
                                configs = kwargs.get('extension_configs', {}))
        self.set_output_format(kwargs.get('output_format', 'xhtml1'))
        self.reset()

    def build_parser(self):
        """ Build the parser from the various parts. """
        self.preprocessors = build_preprocessors(self)
        self.parser = build_block_parser(self) 
        self.inlinePatterns = build_inlinepatterns(self)
        self.treeprocessors = build_treeprocessors(self)
        self.postprocessors = build_postprocessors(self)

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

        Markdown processing takes place in five steps:

        1. A bunch of "preprocessors" munge the input text.
        2. BlockParser() parses the high-level structural elements of the
           pre-processed text into an ElementTree.
        3. A bunch of "treeprocessors" are run against the ElementTree. One 
           such treeprocessor runs InlinePatterns against the ElementTree, 
           detecting inline markup.
        4. Some post-processors are run against the text after the ElementTree 
           has been serialized into text.
        5. The output is written to a string.

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
        source = source.expandtabs(self.tab_length)

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
                start = output.index('<%s>'%self.doc_tag)+len(self.doc_tag)+2
                end = output.rindex('</%s>'%self.doc_tag)
                output = output[start:end].strip()
            except ValueError:
                if output.strip().endswith('<%s />'%self.doc_tag):
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
             output_format = 'xhtml1'):
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
                     output_format = 'xhtml1'):
    """Read markdown code from a file and write it to a file or a stream."""
    md = Markdown(extensions=load_extensions(extensions),
                  safe_mode=safe_mode,
                  output_format=output_format)
    md.convertFile(input, output, encoding)



