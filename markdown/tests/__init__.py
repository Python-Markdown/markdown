import os
import markdown
import codecs
import difflib
import nose
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
    for key in ['extensions', 'safe_mode', 'output_format']:
        args[key] = config.get(section, key)
    return args

def normalize(text):
    """ Normalize whitespace for a string of html using tidy. """
    return unicode(tidy.parseString(text.encode('utf-8'), 
                                    drop_empty_paras=0,
                                    fix_backslash=0,
                                    fix_bad_comments=0,
                                    fix_uri=0,
                                    join_styles=0,
                                    lower_literals=0,
                                    merge_divs=0,
                                    #merge_spans=0,
                                    output_xhtml=1,
                                    #preserve_entities=1,
                                    quote_ampersand=0,
                                    show_body_only=1,
                                    char_encoding='utf8',
                                    newline='LF'))

class CheckSyntax(object):
    def __init__(self, description=None):
        if description:
            self.description = 'TestSyntax: "%s"' % description

    def __call__(self, file, config):
        """ Compare expected output to actual output and report result. """
        input_file = file + ".txt"
        input = codecs.open(input_file, encoding="utf-8").read()
        output_file = file + ".html"
        expected_output = codecs.open(output_file, encoding="utf-8").read()
        output = markdown.markdown(input, **get_args(file, config))
        if tidy and config.getboolean(get_section(file, config), 'normalize'):
            # Normalize whitespace before comparing.
            expected_output = normalize(expected_output)
            output = normalize(output)
        elif config.getboolean(get_section(file, config), 'normalize'):
            # Tidy is not available. Skip this test.
            raise nose.plugins.skip.SkipTest, 'Skipped test. Tidy not available in system.'
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
        config = util.CustomConfigParser({'extensions': '', 
                                          'safe_mode': False,
                                          'output_format': 'xhtml1',
                                          'normalize': '0'})
        config.read(os.path.join(dir_name, 'test.cfg'))
        # Loop through files and generate tests.
        for file in files:
            root, ext = os.path.splitext(file)
            if ext == '.txt':
                path = os.path.join(dir_name, root)
                check_syntax = CheckSyntax(description=relpath(path, test_dir))
                yield check_syntax, path, config

def run():
    nose.main(addplugins=[HtmlOutput(), Markdown()])

# Hack to make nose run with extensions. Once extensions can be added from
# setup.cfg, the below line can be removed. 
# See nose [Issue 271](http://code.google.com/p/python-nose/issues/detail?id=271)
run()
