#!/usr/bin/env python
"""
Sane List Extension for Python-Markdown
=======================================

Modify the behavior of Lists in Python-Markdown t act in a sane manor.

In standard Markdown sytex, the following would constitute a single 
ordered list. However, with this extension, the output would include 
two lists, the first an ordered list and the second and unordered list.

    1. ordered
    2. list

    * unordered
    * list

Copyright 2011 - [Waylan Limberg](http://achinghead.com)

"""

import re
import markdown


class SaneOListProcessor(markdown.blockprocessors.OListProcessor):
    
    SIBLING_TAGS = ['ol']
    
    def __init__(self, *args):
        markdown.blockprocessors.OListProcessor.__init__(self, *args)
        self.CHILD_RE = re.compile(r'^[ ]{0,%s}((\d+\.))\s+(.*)' % (self.tab_length-1))


class SaneUListProcessor(markdown.blockprocessors.UListProcessor):
    
    SIBLING_TAGS = ['ul']
    
    def __init__(self, *args):
        markdown.blockprocessors.UListProcessor.__init__(self, *args)
        self.CHILD_RE = re.compile(r'^[ ]{0,%s}(([*+-]))\s+(.*)' % (self.tab_length-1))


class SaneListExtension(markdown.Extension):
    """ Add sane lists to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Override existing Processors. """
        md.parser.blockprocessors['olist'] = SaneOListProcessor(md.parser)
        md.parser.blockprocessors['ulist'] = SaneUListProcessor(md.parser)


def makeExtension(configs={}):
    return SaneListExtension(configs=configs)

