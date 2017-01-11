"""
Tables Extension for Python-Markdown
====================================

Added parsing of tables to Python-Markdown.

See <https://pythonhosted.org/Markdown/extensions/tables.html>
for documentation.

Original code Copyright 2009 [Waylan Limberg](http://achinghead.com)

All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension
from ..blockprocessors import BlockProcessor
from ..util import etree
import re


class TableProcessor(BlockProcessor):
    """ Process Tables. """

    RE_CODE_PIPES = re.compile(r'(?:(\\\\)|(\\`+)|(`+)|(\\\|)|(\|))')

    def test(self, parent, block):
        rows = block.split('\n')
        return (len(rows) > 1 and '|' in rows[0] and
                '|' in rows[1] and '-' in rows[1] and
                rows[1].strip()[0] in ['|', ':', '-'] and
                set(rows[1]) <= set('|:- '))

    def run(self, parent, blocks):
        """ Parse a table block and build table. """
        block = blocks.pop(0).split('\n')
        header = block[0].strip()
        seperator = block[1].strip()
        rows = [] if len(block) < 3 else block[2:]
        # Get format type (bordered by pipes or not)
        border = False
        if header.startswith('|'):
            border = True
        # Get alignment of columns
        align = []
        for c in self._split_row(seperator, border):
            c = c.strip()
            if c.startswith(':') and c.endswith(':'):
                align.append('center')
            elif c.startswith(':'):
                align.append('left')
            elif c.endswith(':'):
                align.append('right')
            else:
                align.append(None)
        # Build table
        table = etree.SubElement(parent, 'table')
        thead = etree.SubElement(table, 'thead')
        self._build_row(header, thead, align, border)
        tbody = etree.SubElement(table, 'tbody')
        for row in rows:
            self._build_row(row.strip(), tbody, align, border)

    def _build_row(self, row, parent, align, border):
        """ Given a row of text, build table cells. """
        tr = etree.SubElement(parent, 'tr')
        tag = 'td'
        if parent.tag == 'thead':
            tag = 'th'
        cells = self._split_row(row, border)
        # We use align here rather than cells to ensure every row
        # contains the same number of columns.
        for i, a in enumerate(align):
            c = etree.SubElement(tr, tag)
            try:
                c.text = cells[i].strip()
            except IndexError:  # pragma: no cover
                c.text = ""
            if a:
                c.set('align', a)

    def _split_row(self, row, border):
        """ split a row of text into list of cells. """
        if border:
            if row.startswith('|'):
                row = row[1:]
            if row.endswith('|'):
                row = row[:-1]
        return self._split(row)

    def _split(self, row):
        """ split a row of text with some code into a list of cells. """
        elements = []
        pipes = []
        tics = []
        tic_points = []
        tic_region = []
        good_pipes = []

        # Parse row
        # Throw out \\, \`, and \|
        for m in self.RE_CODE_PIPES.finditer(row):
            # Store ` data (len, start_pos, end_pos)
            if m.group(2):
                # \`+
                # Store length of each tic group
                tics.append(len(m.group(2)) - 1)
                # Store start and end of tic group
                tic_points.append((m.start(3), m.end(3) - 1))
            elif m.group(3):
                # `+
                # Store length of each tic group
                tics.append(len(m.group(3)))
                # Store start and end of tic group
                tic_points.append((m.start(3), m.end(3) - 1))
            # Store pipe location
            elif m.group(5):
                pipes.append(m.start(5))

        # Pair up tics according to size if possible
        # Walk through tic list and see if tic has a close.
        # Store the tic region (start of region, end of region).
        pos = 0
        tic_len = len(tics)
        while pos < tic_len:
            try:
                index = tics[pos + 1:].index(tics[pos]) + 1
                tic_region.append((tic_points[pos][0], tic_points[pos + index][1]))
                pos += index + 1
            except ValueError:
                pos += 1

        # Resolve pipes.  Check if they are within a tic pair region.
        # Walk through pipes comparing them to each region.
        #     - If pipe position is less that a region, it isn't in a region
        #     - If it is within a region, we don't want it, so throw it out
        #     - If we didn't throw it out, it must be a table pipe
        for pipe in pipes:
            throw_out = False
            for region in tic_region:
                if pipe < region[0]:
                    # Pipe is not in a region
                    break
                elif region[0] <= pipe <= region[1]:
                    # Pipe is within a code region.  Throw it out.
                    throw_out = True
                    break
            if not throw_out:
                good_pipes.append(pipe)

        # Split row according to table delimeters.
        pos = 0
        for pipe in good_pipes:
            elements.append(row[pos:pipe])
            pos = pipe + 1
        elements.append(row[pos:])
        return elements


class TableExtension(Extension):
    """ Add tables to Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add an instance of TableProcessor to BlockParser. """
        md.parser.blockprocessors.add('table',
                                      TableProcessor(md.parser),
                                      '<hashheader')


def makeExtension(*args, **kwargs):
    return TableExtension(*args, **kwargs)
