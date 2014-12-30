"""
Table of Contents Extension for Python-Markdown
===============================================

See <https://pythonhosted.org/Markdown/extensions/toc.html>
for documentation.

Oringinal code Copyright 2008 [Jack Miller](http://codezen.org)

All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..treeprocessors import Treeprocessor
from ..util import etree, parseBoolValue, AMP_SUBSTITUTE
from .headerid import slugify, unique, itertext, stashedHTML2text
import re


def order_toc_list(toc_list):
    """Given an unsorted list with errors and skips, return a nested one.
    [{'level': 1}, {'level': 2}]
    =>
    [{'level': 1, 'children': [{'level': 2, 'children': []}]}]

    A wrong list is also converted:
    [{'level': 2}, {'level': 1}]
    =>
    [{'level': 2, 'children': []}, {'level': 1, 'children': []}]
    """

    ordered_list = []
    if len(toc_list):
        # Initialize everything by processing the first entry
        last = toc_list.pop(0)
        last['children'] = []
        levels = [last['level']]
        ordered_list.append(last)
        parents = []

        # Walk the rest nesting the entries properly
        while toc_list:
            t = toc_list.pop(0)
            current_level = t['level']
            t['children'] = []

            # Reduce depth if current level < last item's level
            if current_level < levels[-1]:
                # Pop last level since we know we are less than it
                levels.pop()

                # Pop parents and levels we are less than or equal to
                to_pop = 0
                for p in reversed(parents):
                    if current_level <= p['level']:
                        to_pop += 1
                    else:  # pragma: no cover
                        break
                if to_pop:
                    levels = levels[:-to_pop]
                    parents = parents[:-to_pop]

                # Note current level as last
                levels.append(current_level)

            # Level is the same, so append to
            # the current parent (if available)
            if current_level == levels[-1]:
                (parents[-1]['children'] if parents
                 else ordered_list).append(t)

            # Current level is > last item's level,
            # So make last item a parent and append current as child
            else:
                last['children'].append(t)
                parents.append(last)
                levels.append(current_level)
            last = t

    return ordered_list


class TocTreeprocessor(Treeprocessor):
    def __init__(self, md, config):
        super(TocTreeprocessor, self).__init__(md)

        self.marker = config["marker"]
        self.title = config["title"]
        self.slugify = config["slugify"]
        self.use_anchors = parseBoolValue(config["anchorlink"])
        self.use_permalinks = parseBoolValue(config["permalink"], False)
        if self.use_permalinks is None:
            self.use_permalinks = config["permalink"]

        self.header_rgx = re.compile("[Hh][123456]")

    def iterparent(self, root):
        ''' Iterator wrapper to get parent and child all at once. '''
        for parent in root.iter():
            for child in parent:
                yield parent, child

    def replace_marker(self, root, elem):
        ''' Replace marker with elem. '''
        for (p, c) in self.iterparent(root):
            text = ''.join(itertext(c)).strip()
            if not text:
                continue

            # To keep the output from screwing up the
            # validation by putting a <div> inside of a <p>
            # we actually replace the <p> in its entirety.
            # We do not allow the marker inside a header as that
            # would causes an enless loop of placing a new TOC
            # inside previously generated TOC.
            if c.text and c.text.strip() == self.marker and \
               not self.header_rgx.match(c.tag) and c.tag not in ['pre', 'code']:
                for i in range(len(p)):
                    if p[i] == c:
                        p[i] = elem
                        break

    def add_anchor(self, c, elem_id):  # @ReservedAssignment
        anchor = etree.Element("a")
        anchor.text = c.text
        anchor.attrib["href"] = "#" + elem_id
        anchor.attrib["class"] = "toclink"
        c.text = ""
        for elem in c.getchildren():
            anchor.append(elem)
            c.remove(elem)
        c.append(anchor)

    def add_permalink(self, c, elem_id):
        permalink = etree.Element("a")
        permalink.text = ("%spara;" % AMP_SUBSTITUTE
                          if self.use_permalinks is True
                          else self.use_permalinks)
        permalink.attrib["href"] = "#" + elem_id
        permalink.attrib["class"] = "headerlink"
        permalink.attrib["title"] = "Permanent link"
        c.append(permalink)

    def build_toc_etree(self, div, toc_list):
        # Add title to the div
        if self.title:
            header = etree.SubElement(div, "span")
            header.attrib["class"] = "toctitle"
            header.text = self.title

        def build_etree_ul(toc_list, parent):
            ul = etree.SubElement(parent, "ul")
            for item in toc_list:
                # List item link, to be inserted into the toc div
                li = etree.SubElement(ul, "li")
                link = etree.SubElement(li, "a")
                link.text = item.get('name', '')
                link.attrib["href"] = '#' + item.get('id', '')
                if item['children']:
                    build_etree_ul(item['children'], li)
            return ul

        return build_etree_ul(toc_list, div)

    def run(self, doc):
        # Get a list of id attributes
        used_ids = set()
        for el in doc.iter():
            if "id" in el.attrib:
                used_ids.add(el.attrib["id"])

        div = etree.Element("div")
        div.attrib["class"] = "toc"
        self.replace_marker(doc, div)

        toc_list = []
        for el in doc.iter():
            if self.header_rgx.match(el.tag):
                text = ''.join(itertext(el)).strip()

                # Do not override pre-existing ids
                if "id" not in el.attrib:
                    elem_id = stashedHTML2text(text, self.markdown)
                    elem_id = unique(self.slugify(elem_id, '-'), used_ids)
                    el.attrib["id"] = elem_id
                else:
                    elem_id = el.attrib["id"]

                toc_list.append({'level': int(el.tag[-1]),
                                 'id': elem_id,
                                 'name': text})

                if self.use_anchors:
                    self.add_anchor(el, elem_id)
                if self.use_permalinks:
                    self.add_permalink(el, elem_id)

        toc_list_nested = order_toc_list(toc_list)
        self.build_toc_etree(div, toc_list_nested)
        prettify = self.markdown.treeprocessors.get('prettify')
        if prettify:
            prettify.run(div)

        # serialize and attach to markdown instance.
        toc = self.markdown.serializer(div)
        for pp in self.markdown.postprocessors.values():
            toc = pp.run(toc)
        self.markdown.toc = toc


class TocExtension(Extension):

    TreeProcessorClass = TocTreeprocessor

    def __init__(self, *args, **kwargs):
        self.config = {
            "marker": ["[TOC]",
                       "Text to find and replace with Table of Contents - "
                       "Defaults to \"[TOC]\""],
            "slugify": [slugify,
                        "Function to generate anchors based on header text - "
                        "Defaults to the headerid ext's slugify function."],
            "title": ["",
                      "Title to insert into TOC <div> - "
                      "Defaults to an empty string"],
            "anchorlink": [False,
                           "True if header should be a self link - "
                           "Defaults to False"],
            "permalink": [0,
                          "True or link text if a Sphinx-style permalink should "
                          "be added - Defaults to False"]
        }

        super(TocExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        self.md = md
        self.reset()
        tocext = self.TreeProcessorClass(md, self.getConfigs())
        # Headerid ext is set to '>prettify'. With this set to '_end',
        # it should always come after headerid ext (and honor ids assinged
        # by the header id extension) if both are used. Same goes for
        # attr_list extension. This must come last because we don't want
        # to redefine ids after toc is created. But we do want toc prettified.
        md.treeprocessors.add("toc", tocext, "_end")

    def reset(self):
        self.md.toc = ''


def makeExtension(*args, **kwargs):
    return TocExtension(*args, **kwargs)
