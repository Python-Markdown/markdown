#!/usr/bin/env python

"""
Table extension for Python-Markdown
"""

import markdown
from markdown import etree

class TablePattern(markdown.Pattern) :
    def __init__ (self, md):
        markdown.Pattern.__init__(self, r'(^|\n)\|([^\n]*)\|')
        self.md = md

    def handleMatch(self, m):

        # a single line represents a row
        tr = etree.Element('tr')
        
        # chunks between pipes represent cells

        for t in m.group(3).split('|'): 
     
            if len(t) >= 2 and t.startswith('*') and t.endswith('*'):
                # if a cell is bounded by asterisks, it is a <th>
                td = etree.Element('th')
                t = t[1:-1]
            else:
                # otherwise it is a <td>
                td = etree.Element('td')
            
            # add text ot inline section, later it will be
            # processed by core

            td.text = t
            tr.append(td)
            tr.tail = "\n"
 
        return tr


class TablePostprocessor:
    
    def _findElement(self, element, name):
        result = []
        for child in element:
            if child.tag == name:
                result.append(child)
            result += self._findElement(child, name)
        return result
    
    def run(self, root):

        for element in self._findElement(root, "p"):
             for child in element:
                 if child.tail:
                     element.tag = "table"
                     break
        
                


class TableExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.insert(0, TablePattern(md))
        md.postprocessors.append(TablePostprocessor())


def makeExtension(configs):
    return TableExtension(configs)

