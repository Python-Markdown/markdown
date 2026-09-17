"""Generate Markdown isolated from our current document options."""

# Code copied from 
# https://github.com/facelessuser/pymdown-extensions/blob/0701c57263b154d60eabf7c64091169619255403/tools/pymdownx_md_render.py
# with modifications.

import markdown
import yaml
import re
import ast
import sys
from io import StringIO
from collections import OrderedDict
from markdown.util import code_escape


def yaml_load(stream, loader=yaml.Loader):
    """
    Custom YAML loader.

    Load all strings as Unicode.
    http://stackoverflow.com/a/2967461/3609487
    """

    def construct_yaml_str(self, node):
        """Override the default string handling function to always return Unicode objects."""

        return self.construct_scalar(node)

    class Loader(loader):
        """Custom Loader."""

    Loader.add_constructor(
        'tag:yaml.org,2002:str',
        construct_yaml_str
    )

    return yaml.load(stream, Loader)


def get_frontmatter(text):
    """Get front matter from string."""

    frontmatter = OrderedDict()

    if text.startswith("---"):
        m = re.search(r'^(-{3}\r?\n(?!\r?\n)(.*?)(?<=\n)(?:-{3}|\.{3})\r?\n)', text, re.DOTALL)
        if m:
            yaml_okay = True
            try:
                frontmatter = yaml_load(m.group(2))
                if frontmatter is None:
                    frontmatter = OrderedDict()
                # If we didn't get a dictionary, we don't want this as it isn't front matter.
                assert isinstance(frontmatter, (dict, OrderedDict)), TypeError
            except Exception:
                # We had a parsing error. This is not the YAML we are looking for.
                yaml_okay = False
                frontmatter = OrderedDict()

            if yaml_okay:
                text = text[m.end(1):]

    return frontmatter, text


def md_render(src="", language="", class_name=None, options=None, md="", **kwargs):
    """ Render Markdown in code block and rendered output in result code block. """
    try:
        fm, text = get_frontmatter(src)
        html = markdown.markdown(
            text,
            extensions=fm.get('extensions', []),
            extension_configs=fm.get('extension_configs', {})
        )
    except Exception:
        import traceback
        print(traceback.format_exc())
        raise

    options = options or {}
    if 'title' not in options:
        options['title'] = 'Markdown Source'
    result_options = options.copy()
    result_options['title'] = 'HTML Output'

    source = md.preprocessors['fenced_code_block'].highlight(text, 'markdown', options, md, **kwargs)
    output = md.preprocessors['fenced_code_block'].highlight(html, 'html', result_options, md, **kwargs)
    return f'{source}\n<div class="result">{output}</div>'


class PyExecNamespace():
    def __init__(self, globals=None, locals=None):
        self.globals = globals or {}
        self.locals = locals or {}

    def exec(self, source):
        """ 
        Execute code in namespace.

        If code outputs to stdout, that output is captured and returned.
        If nothing it output to stdout, then the last line of code is checked
        for a variable assignment. If one exists, then the value of that variable
        is returned. If that fails, then `None` is returned.
        """

        # Temporarily redirect stdout
        save_stdout = sys.stdout
        sys.stdout = StringIO()

        # Run code
        try:
            exec(source, self.globals, self.locals)
        except KeyboardInterrupt:
            sys.stdout.close()
            sys.stdout = save_stdout
            raise
        except BaseException as exc:
            sys.stdout.close()
            sys.stdout = save_stdout
            import traceback
            tb = traceback.format_exception(exc, exc, exc.__traceback__.tb_next)
            return 'traceback', '\n'.join(tb)

        # Retreive anything sent to stdout and restore system default
        out = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = save_stdout

        if out:
            # Return text sent to stdout
            return 'stdout', out
        else:
            # Nothing sent to stdout. Try to get value of last variable assignment
            target = None
            a = ast.parse(source)
            if a.body:
                if isinstance(a_last := a.body[-1], ast.Assign):
                    target = ast.unparse(a_last.targets[0])
                elif isinstance(a_last, (ast.AnnAssign, ast.AugAssign)):
                    target = ast.unparse(a_last.target)
            if target and target in self.locals:
                return target, self.locals[target]
        return None, None


def py_render(src="", language="", class_name=None, options=None, md="", **kwargs):
    """ Render Python in a code block and output of the code in a result code block. """

    if not hasattr(md, 'py_namespace'):
        # This is the first instance of a Python render block on the page. 
        # Create namespace for this and all future blocks to run in.
        md.py_namespace = PyExecNamespace()
    target, result = md.py_namespace.exec(src)

    # Retreive and remove output language from attrs
    output_lang = kwargs['attrs'].pop('output-lang', '')

    options = options or {}
    if 'title' not in options:
        options['title'] = 'Python'

    source = md.preprocessors['fenced_code_block'].highlight(src, 'python', options, md, **kwargs)

    if result is not None:
        result_options = options.copy()
        if target == 'traceback':
            result_options['title'] = 'Error Raised'
            output_lang = 'py3tb'  # PythonTracebackLexer
        elif target == 'stdout':
            result_options['title'] = 'Text Written to STDOUT'
        elif target is not None:
            # Store title in stash to avoid it being escaped by Pygments.
            result_options['title'] = md.htmlStash.store(f'Value of <code>{code_escape(target)}</code>')
        
        output = md.preprocessors['fenced_code_block'].highlight(result, output_lang, result_options, md, **kwargs)
        return f'{source}\n<div class="result">{output}</div>'
    # No result so only render source
    return source
