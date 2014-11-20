import os
import markdown
import codecs
import difflib
try:
    import nose
except ImportError as e:
    msg = e.args[0]
    msg = msg + ". The nose testing framework is required to run the Python-" \
        "Markdown tests. Run `pip install nose` to install the latest version."
    e.args = (msg,) + e.args[1:]
    raise
from .plugins import HtmlOutput, Markdown, MarkdownSyntaxError
try:
    import tidylib
except ImportError:
    tidylib = None
try:
    import yaml
except ImportError as e:
    msg = e.args[0]
    msg = msg + ". A YAML library is required to run the Python-Markdown " \
        "tests. Run `pip install pyyaml` to install the latest version."
    e.args = (msg,) + e.args[1:]
    raise

test_dir = os.path.abspath(os.path.dirname(__file__))


class YamlConfig():
    def __init__(self, defaults, filename):
        """ Set defaults and load config file if it exists. """
        self.DEFAULT_SECTION = 'DEFAULT'
        self._defaults = defaults
        self._config = {}
        if os.path.exists(filename):
            with codecs.open(filename, encoding="utf-8") as f:
                self._config = yaml.load(f)

    def get(self, section, option):
        """ Get config value for given section and option key. """
        if section in self._config and option in self._config[section]:
            return self._config[section][option]
        return self._defaults[option]

    def get_section(self, file):
        """ Get name of config section for given file. """
        filename = os.path.basename(file)
        if filename in self._config:
            return filename
        else:
            return self.DEFAULT_SECTION

    def get_args(self, file):
        """ Get args to pass to markdown from config for a given file. """
        args = {}
        section = self.get_section(file)
        if section in self._config:
            for key in self._config[section].keys():
                # Filter out args unique to testing framework
                if key not in self._defaults.keys():
                    args[key] = self.get(section, key)
        return args


def get_config(dir_name):
    """ Get config for given directory name. """
    defaults = {
        'normalize': False,
        'skip': False,
        'input_ext': '.txt',
        'output_ext': '.html'
    }
    config = YamlConfig(defaults, os.path.join(dir_name, 'test.cfg'))
    return config


def normalize(text):
    """ Normalize whitespace for a string of html using tidylib. """
    output, errors = tidylib.tidy_fragment(text, options={
        'drop_empty_paras': 0,
        'fix_backslash': 0,
        'fix_bad_comments': 0,
        'fix_uri': 0,
        'join_styles': 0,
        'lower_literals': 0,
        'merge_divs': 0,
        'output_xhtml': 1,
        'quote_ampersand': 0,
        'newline': 'LF'
    })
    return output


class CheckSyntax(object):
    def __init__(self, description=None):
        if description:
            self.description = 'TestSyntax: "%s"' % description

    def __call__(self, file, config):
        """ Compare expected output to actual output and report result. """
        cfg_section = config.get_section(file)
        if config.get(cfg_section, 'skip'):
            raise nose.plugins.skip.SkipTest('Test skipped per config.')
        input_file = file + config.get(cfg_section, 'input_ext')
        with codecs.open(input_file, encoding="utf-8") as f:
            input = f.read()
        output_file = file + config.get(cfg_section, 'output_ext')
        with codecs.open(output_file, encoding="utf-8") as f:
            # Normalize line endings
            # (on windows, git may have altered line endings).
            expected_output = f.read().replace("\r\n", "\n")
        output = markdown.markdown(input, **config.get_args(file))
        if tidylib and config.get(cfg_section, 'normalize'):
            # Normalize whitespace with tidylib before comparing.
            expected_output = normalize(expected_output)
            output = normalize(output)
        elif config.get(cfg_section, 'normalize'):
            # Tidylib is not available. Skip this test.
            raise nose.plugins.skip.SkipTest(
                'Test skipped. Tidylib not available on system.'
            )
        diff = [l for l in difflib.unified_diff(
            expected_output.splitlines(True),
            output.splitlines(True),
            output_file,
            'actual_output.html',
            n=3
        )]
        if diff:
            raise MarkdownSyntaxError(
                'Output from "%s" failed to match expected '
                'output.\n\n%s' % (input_file, ''.join(diff))
            )


def TestSyntax():
    for dir_name, sub_dirs, files in os.walk(test_dir):
        # Get dir specific config settings.
        config = get_config(dir_name)
        # Loop through files and generate tests.
        for file in files:
            root, ext = os.path.splitext(file)
            if ext == config.get(config.get_section(file), 'input_ext'):
                path = os.path.join(dir_name, root)
                check_syntax = CheckSyntax(
                    description=os.path.relpath(path, test_dir)
                )
                yield check_syntax, path, config


def generate(file, config):
    """ Write expected output file for given input. """
    cfg_section = config.get_section(file)
    if config.get(cfg_section, 'skip') or config.get(cfg_section, 'normalize'):
        print('Skipping:', file)
        return None
    input_file = file + config.get(cfg_section, 'input_ext')
    output_file = file + config.get(cfg_section, 'output_ext')
    if not os.path.isfile(output_file) or \
            os.path.getmtime(output_file) < os.path.getmtime(input_file):
        print('Generating:', file)
        markdown.markdownFromFile(input=input_file, output=output_file,
                                  encoding='utf-8', **config.get_args(file))
    else:
        print('Already up-to-date:', file)


def generate_all():
    """ Generate expected output for all outdated tests. """
    for dir_name, sub_dirs, files in os.walk(test_dir):
        # Get dir specific config settings.
        config = get_config(dir_name)
        # Loop through files and generate tests.
        for file in files:
            root, ext = os.path.splitext(file)
            if ext == config.get(config.get_section(file), 'input_ext'):
                generate(os.path.join(dir_name, root), config)


def run():
    nose.main(addplugins=[HtmlOutput(), Markdown()])
