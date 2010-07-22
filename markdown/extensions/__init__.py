from markdown.md_logging import message
from logging import DEBUG, INFO, WARN, ERROR, CRITICAL

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
        if key in self.config:
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
        raise NotImplementedError, 'Extension "%s.%s" must define an "extendMarkdown"' \
            'method.' % (self.__class__.__module__, self.__class__.__name__)


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
    ext_module = 'markdown.extensions'
    module_name_new_style = '.'.join([ext_module, ext_name])
    module_name_old_style = '_'.join(['mdx', ext_name])

    # Try loading the extention first from one place, then another
    try: # New style (markdown.extensons.<extension>)
        module = __import__(module_name_new_style, {}, {}, [ext_module])
    except ImportError:
        try: # Old style (mdx.<extension>)
            module = __import__(module_name_old_style)
        except ImportError:
           message(WARN, "Failed loading extension '%s' from '%s' or '%s'"
               % (ext_name, module_name_new_style, module_name_old_style))
           # Return None so we don't try to initiate none-existant extension
           return None

    # If the module is loaded successfully, we expect it to define a
    # function called makeExtension()
    try:
        return module.makeExtension(configs.items())
    except AttributeError, e:
        message(CRITICAL, "Failed to initiate extension '%s': %s" % (ext_name, e))


def load_extensions(ext_names):
    """Loads multiple extensions"""
    extensions = []
    for ext_name in ext_names:
        extension = load_extension(ext_name)
        if extension:
            extensions.append(extension)
    return extensions
