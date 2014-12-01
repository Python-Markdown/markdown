"""
Meta Data Extension for Python-Markdown
=======================================

This extension adds Meta Data handling to markdown.

See <https://pythonhosted.org/Markdown/extensions/meta_data.html>
for documentation.

Original code Copyright 2007-2008 [Waylan Limberg](http://achinghead.com).

All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..preprocessors import Preprocessor
import re
import logging

try:  # pragma: no cover
    import yaml
    try:
        from yaml import CSafeLoader as SafeLoader
    except ImportError:
        from yaml import SafeLoader
except ImportError:
    yaml = None

log = logging.getLogger('MARKDOWN')

# Global Vars
META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')
META_MORE_RE = re.compile(r'^[ ]{4,}(?P<value>.*)')
YAML_BEGIN_RE = re.compile(r'^-{3}(\s.*)?')
YAML_END_RE = re.compile(r'^(-{3}|\.{3})(\s.*)?')


class MetaExtension (Extension):
    """ Meta-Data extension for Python-Markdown. """
    def __init__(self, *args, **kwargs):
        self.config = {
            'yaml': [False, "Parse meta data specified as a "
                            "'---' delimited YAML front matter"],
            }
        super(MetaExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add MetaPreprocessor to Markdown instance. """
        md.preprocessors.add("meta",
                             MetaPreprocessor(md, self.getConfigs()),
                             ">normalize_whitespace")


class MetaPreprocessor(Preprocessor):
    """ Get Meta-Data. """

    def __init__(self, md, config):
        self.config = config
        super(MetaPreprocessor, self).__init__(md)

    def run(self, lines):
        """ Parse Meta-Data and store in Markdown.Meta. """
        meta = {}
        key = None
        yaml_block = []
        have_yaml = False
        if lines and YAML_BEGIN_RE.match(lines[0]):
            have_yaml = True
            lines.pop(0)
            if self.config['yaml'] and not yaml:  # pragma: no cover
                log.warning('Document with YAML header, but PyYAML unavailable')
        while lines:
            line = lines.pop(0)
            m1 = META_RE.match(line)
            if line.strip() == '' or have_yaml and YAML_END_RE.match(line):
                break  # blank line or end of YAML header - done
            elif have_yaml and self.config['yaml'] and yaml:
                yaml_block.append(line)
            elif m1:
                key = m1.group('key').lower().strip()
                value = m1.group('value').strip()
                try:
                    meta[key].append(value)
                except KeyError:
                    meta[key] = [value]
            else:
                m2 = META_MORE_RE.match(line)
                if m2 and key:
                    # Add another line to existing key
                    meta[key].append(m2.group('value').strip())
                else:
                    lines.insert(0, line)
                    break  # no meta data - done
        if yaml_block:
            meta = yaml.load('\n'.join(yaml_block), SafeLoader)
        self.markdown.Meta = meta
        return lines


def makeExtension(*args, **kwargs):
    return MetaExtension(*args, **kwargs)
