import os
import markdown
import codecs
import difflib
try:
    import nose
except ImportError:
    raise ImportError, "The nose testing framework is required to run " \
                       "Python-Markdown tests. Run `easy_install nose` " \
                       "to install the latest version."
import util 
from plugins import HtmlOutput, Markdown
try:
    import tidy
except ImportError:
    tidy = None


test_dir = os.path.abspath(os.path.dirname(__file__))

def relpath(path, start=test_dir):
    """ reimplement relpath for python 2.3-2.5 from 2.6 """
    if not path:
        raise ValueError('no path secified')
    start_list = os.path.abspath(start).split(os.path.sep)
    path_list = os.path.abspath(path).split(os.path.sep)
    # Work out how much of the filepath is shared by start and path.
    i = len(os.path.commonprefix([start_list, path_list]))
    rel_list = [os.path.pardir] * (len(start_list)-i) + path_list[i:]
    if not rel_list:
        return test_dir
    return os.path.join(*rel_list)

def get_config(dir_name):
    """ Get config for given directory name. """
    config = util.CustomConfigParser({'normalize': '0',
                                      'skip': '0',
                                      'input_ext': '.txt',
                                      'output_ext': '.html'})
    config.read(os.path.join(dir_name, 'test.cfg'))
    return config

def get_section(file, config):
    """ Get name of config section for given file. """
    filename = os.path.basename(file)
    if config.has_section(filename):
        return filename
    else:
        return 'DEFAULT'

def get_args(file, config):
    """ Get args to pass to markdown from config for a given file. """
    args = {}
    section = get_section(file, config)
    for key, v in config.items(section):
        # Filter out args unique to testing framework
        if key not in ['normalize', 'skip', 'input_ext', 'output_ext']:
            args[key] = config.get(section, key)
    return args

def normalize(text):
    """ Normalize whitespace for a string of html using tidy. """
    return str(tidy.parseString(text.encode('utf-8', 'xmlcharrefreplace'), 
                                    drop_empty_paras=0,
                                    fix_backslash=0,
                                    fix_bad_comments=0,
                                    fix_uri=0,
                                    join_styles=0,
                                    lower_literals=0,
                                    merge_divs=0,
                                    output_xhtml=1,
                                    quote_ampersand=0,
                                    show_body_only=1,
                                    char_encoding='utf8',
                                    newline='LF')).decode('string-escape')

class CheckSyntax(object):
    def __init__(self, description=None):
        if description:
            self.description = 'TestSyntax: "%s"' % description

    def __call__(self, file, config):
        """ Compare expected output to actual output and report result. """
        cfg_section = get_section(file, config)
        if config.get(cfg_section, 'skip'):
            raise nose.plugins.skip.SkipTest, 'Test skipped per config.'
        input_file = file + config.get(cfg_section, 'input_ext')
        input = codecs.open(input_file, encoding="utf-8").read()
        output_file = file + config.get(cfg_section, 'output_ext') 
        expected_output = codecs.open(output_file, encoding="utf-8").read()
        output = markdown.markdown(input, **get_args(file, config))
        if tidy and config.get(cfg_section, 'normalize'):
            # Normalize whitespace before comparing.
            expected_output = normalize(expected_output)
            output = normalize(output)
        elif config.get(cfg_section, 'normalize'):
            # Tidy is not available. Skip this test.
            raise nose.plugins.skip.SkipTest, 'Test skipped. Tidy not available in system.'
        diff = [l for l in difflib.unified_diff(expected_output.splitlines(True),
                                                output.splitlines(True), 
                                                output_file, 
                                                'actual_output.html', 
                                                n=3)]
        if diff:
            raise util.MarkdownSyntaxError('Output from "%s" failed to match expected '
                                           'output.\n\n%s' % (input_file, ''.join(diff)))

def TestSyntax():
    for dir_name, sub_dirs, files in os.walk(test_dir):
        # Get dir specific config settings.
        config = get_config(dir_name)
        # Loop through files and generate tests.
        for file in files:
            root, ext = os.path.splitext(file)
            if ext == config.get(get_section(file, config), 'input_ext'):
                path = os.path.join(dir_name, root)
                check_syntax = CheckSyntax(description=relpath(path, test_dir))
                yield check_syntax, path, config

def generate(file, config):
    """ Write expected output file for given input. """
    cfg_section = get_section(file, config)
    if config.get(cfg_section, 'skip'):
        print 'Skipping:', file
        return None
    input_file = file + config.get(cfg_section, 'input_ext')
    output_file = file + config.get(cfg_section, 'output_ext') 
    if not os.path.isfile(output_file) or \
            os.path.getmtime(output_file) < os.path.getmtime(input_file):
        print 'Generating:', file
        markdown.markdownFromFile(input=input_file, output=output_file, 
                                  encoding='utf-8', **get_args(file, config))
    else:
        print 'Already up-to-date:', file

def generate_all():
    """ Generate expected output for all outdated tests. """
    for dir_name, sub_dirs, files in os.walk(test_dir):
        # Get dir specific config settings.
        config = get_config(dir_name)
        # Loop through files and generate tests.
        for file in files:
            root, ext = os.path.splitext(file)
            if ext == config.get(get_section(file, config), 'input_ext'):
                generate(os.path.join(dir_name, root), config)


def run():
    nose.main(addplugins=[HtmlOutput(), Markdown()])

