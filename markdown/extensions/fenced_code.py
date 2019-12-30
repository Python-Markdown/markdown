"""
Fenced Code Extension for Python Markdown
=========================================

This extension adds Fenced Code Blocks to Python-Markdown.

See <https://Python-Markdown.github.io/extensions/fenced_code_blocks>
for documentation.

Original code Copyright 2007-2008 [Waylan Limberg](http://achinghead.com/).


All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](https://opensource.org/licenses/bsd-license.php)
"""


from textwrap import dedent
from . import Extension
from ..preprocessors import Preprocessor
from .codehilite import CodeHilite, CodeHiliteExtension, parse_hl_lines
from .attr_list import get_attrs
import re


class FencedCodeExtension(Extension):

    def extendMarkdown(self, md):
        """ Add FencedBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.register(FencedBlockPreprocessor(md), 'fenced_code_block', 25)


class FencedBlockPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(
        dedent(r'''
            (?P<fence>^(?:~{3,}|`{3,}))[ ]*                      # opening fence
            ((\{(?P<attrs>[^\}\n]*)\})?|                         # (optional {attrs} or
            (\.?(?P<lang>[\w#.+-]*))?[ ]*                        # optional (.)lang
            (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?) # optional hl_lines)
            [ ]*\n                                               # newline (end of opening fence)
            (?P<code>.*?)(?<=\n)                                 # the code block
            (?P=fence)[ ]*$                                      # closing fence
        '''),
        re.MULTILINE | re.DOTALL | re.VERBOSE
    )

    def __init__(self, md):
        super().__init__(md)

        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        """ Match and store Fenced Code Blocks in the HtmlStash. """

        # Check for codehilite extension
        if not self.checked_for_codehilite:
            for ext in self.md.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.getConfigs()
                    break

            self.checked_for_codehilite = True

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                lang, id, classes, config = None, '', [], {}
                if m.group('attrs'):
                    id, classes, config = self.handle_attrs(get_attrs(m.group('attrs')))
                    if len(classes):
                        lang = classes[0]
                else:
                    if m.group('lang'):
                        lang = m.group('lang')
                        classes.append(lang)
                    if m.group('hl_lines'):
                        # Support hl_lines outside of attrs for backward-compatibility
                        config['hl_lines'] = parse_hl_lines(m.group('hl_lines'))

                # If config is not empty, then the codehighlite extension
                # is enabled, so we call it to highlight the code
                if self.codehilite_conf:
                    local_config = self.codehilite_conf.copy()
                    local_config.update(config)
                    # Combine classes with cssclass. Ensure cssclass is at end
                    # as pygments appends a suffix under certain circumstances.
                    # Ignore ID as Pygments does not offer an option to set it.
                    if classes:
                        local_config['css_class'] = '{} {}'.format(
                            ' '.join(classes),
                            local_config['css_class']
                        )
                    highliter = CodeHilite(
                        m.group('code'),
                        lang=lang,
                        style=local_config.pop('pygments_style'),
                        **local_config
                    )

                    code = highliter.hilite()
                else:
                    id_attr = class_attr = ''
                    if classes:
                        class_attr = ' class="{}"'.format('language-' + ' '.join(classes))
                    if id:
                        id_attr = ' id="{}"'.format(id)
                    code = '<pre><code{id}{cls}>{code}</code></pre>'.format(
                        id=id_attr,
                        cls=class_attr,
                        code=self._escape(m.group('code'))
                    )

                placeholder = self.md.htmlStash.store(code)
                text = '{}\n{}\n{}'.format(text[:m.start()],
                                           placeholder,
                                           text[m.end():])
            else:
                break
        return text.split("\n")

    def handle_attrs(self, attrs):
        """ Return tuple: (id, [list, of, classes], {configs}) """
        id = ''
        classes = []
        configs = {}
        for k, v in attrs:
            if k == 'id':
                id = v
            elif k == '.':
                classes.append(v)
            elif k == 'hl_lines':
                configs[k] = parse_hl_lines(v)
            else:
                configs[k] = v
        return id, classes, configs

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt


def makeExtension(**kwargs):  # pragma: no cover
    return FencedCodeExtension(**kwargs)
