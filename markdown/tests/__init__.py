import os
import markdown
import codecs
import difflib
import nose
import util 
from plugins import HtmlOutput, Markdown

test_dir = os.path.abspath(os.path.dirname(__file__))

def normalize(text):
    """ normalize lines for better diff output. """
    return ['%s\n' % l for l in text.strip().split('\n')]

def get_args(file, config):
    """ Get args to pass to markdown from config for a given file. """
    args = {}
    filename = os.path.basename(file)
    if config.has_section(filename):
        section = filename
    else:
        section = 'DEFAULT'
    for key in ['extensions', 'safe_mode', 'output_format']:
        args[key] = config.get(section, key)
    return args

def check_syntax(file, config):
    """ Compare expected output to actual output and report result. """
    input_file = file + ".txt"
    input = codecs.open(input_file, encoding="utf-8").read()
    output_file = file + ".html"
    expected_output = codecs.open(output_file, encoding="utf-8").read()
    output = normalize(markdown.markdown(input, **get_args(file, config)))
    diff = [l for l in difflib.unified_diff(normalize(expected_output),
                                            output, output_file, 
                                            'actual_output.html', n=3)]
    if diff:
        raise util.MarkdownSyntaxError('Output from "%s" failed to match expected '
                                       'output.\n\n%s' % (input_file, ''.join(diff)))

def TestSyntax():
    for dir_name, sub_dirs, files in os.walk(test_dir):
        # Get dir specific config settings.
        config = util.CustomConfigParser({'extensions': '', 
                                          'safe_mode': False,
                                          'output_format': 'xhtml1'})
        config.read(os.path.join(dir_name, 'test.cfg'))
        # Loop through files and generate tests.
        for file in files:
            root, ext = os.path.splitext(file)
            if ext == '.txt':
                # check_syntax.description = root
                yield check_syntax, os.path.join(dir_name, root), config

def run():
    nose.main(addplugins=[HtmlOutput(), Markdown()])

# Hack to make nose run with extensions. Once extensions can be added from
# setup.cfg, the below line can be removed. 
# See nose [Issue 271](http://code.google.com/p/python-nose/issues/detail?id=271)
run()
