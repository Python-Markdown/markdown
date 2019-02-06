"""
AutoDirection Extension for Python-Markdown
===========================================

Add dir="auto" attribute to paragraphs,
Tthis will help browser to set text direction based on the content

See <https://Python-Markdown.github.io/extensions/autodirection>
for documentation.

All changes Copyright 2019 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""
from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..treeprocessors import Treeprocessor


class AutoDirectionTreeprocessor(Treeprocessor):
    def run(self, root):
        blocks = root.iter('p')
        for block in blocks:
            block.set('dir', 'auto')


class AutoDirectionExtension(Extension):
    def extendMarkdown(self, md):
        autodirection = AutoDirectionTreeprocessor(md)
        md.treeprocessors.register(autodirection, 'autodirection', 50)
        md.registerExtension(self)


def makeExtension(**kwargs):  # pragma: no cover
    return AutoDirectionExtension(**kwargs)
