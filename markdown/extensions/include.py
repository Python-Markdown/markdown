#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  include.py
#
#  Copyright 2015 Christopher MacMackin <cmacmackin@gmail.com>
#  Modify by William <buaabyl@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
from __future__ import print_function

import re
import os.path
from codecs import open
from . import Extension
from ..preprocessors import Preprocessor
from pygments.lexers import get_lexer_for_filename

#TODO:
# by buaabyl
#   it is better just include code file
#   not include markdown file
#   because this macro can process 
#   included file have 'include macro'!
#   or using pycparse to process...
#
# syntax `{!file.md!}` is pre code, not a macro! so ignore
PATTERN_IGO_SYNTAX = re.compile(r'`\{!\s*(.+?)\s*!\}`')

# syntax: {!file.md!}
PATTERN_INC_SYNTAX = re.compile(r'\{!\s*(.+?)\s*!\}')


class MarkdownInclude(Extension):
    def __init__(self, configs={}):
        self.config = {
            'base_path': ['.', 'Default location from which to evaluate ' \
                'relative paths for the include statement.'],
            'encoding': ['utf-8', 'Encoding of the files used by the include ' \
                'statement.']
        }
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add(
            'include', IncludePreprocessor(md,self.getConfigs()),'_begin'
        )


class IncludePreprocessor(Preprocessor):
    '''
    This provides an "include" function for Markdown, similar to that found in
    LaTeX (also the C pre-processor and Fortran). The syntax is {!filename!},
    which will be replaced by the contents of filename. Any such statements in
    filename will also be replaced. This replacement is done prior to any other
    Markdown processing. All file-names are evaluated relative to the location
    from which Markdown is being called.

    buaabyl: extend to include code file, and format it to match highlight
    '''
    def __init__(self, md, config):
        super(IncludePreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def run(self, lines):
        all_parsed = False
        lineno = 0

        while not all_parsed:
            nr_lines = len(lines)

            while (lineno < nr_lines):
                md_line = lines[lineno]

                #check 'include' syntax
                res = PATTERN_IGO_SYNTAX.search(md_line)
                if res:
                    lineno = lineno + 1
                    continue

                res = PATTERN_INC_SYNTAX.search(md_line)
                if not res:
                    lineno = lineno + 1
                    continue

                #match 'include' syntax
                filename = res.group(1)
                filename = os.path.expanduser(filename)
                if not os.path.isabs(filename):
                    filename = os.path.normpath(
                        os.path.join(self.base_path,filename)
                    )
                try:
                    with open(filename, 'r', encoding=self.encoding) as r:
                        file_lines = r.readlines()
                except Exception as e:
                    print('Warning: could not find file {}. Ignoring '
                        'include statement. Error: {}'.format(filename, e))
                    lines[lineno] = PATTERN_INC_SYNTAX.sub('', md_line)
                    break

                #split "abce{!file!}fgh" to ["abce", "fgh"]
                line_split = PATTERN_INC_SYNTAX.split(md_line, maxsplit=0)
                before_macro = line_split[0]
                after_macro  = line_split[2]

                #check empty line
                #file_lines is list of lines!
                if len(file_lines) == 0:
                    file_lines.append('')

                #remove '\n' at the end of every file lines
                #because readlines included '\n' at the end
                for i in range(len(file_lines)):
                    if file_lines[i][-1] == '\n':
                        file_lines[i] = file_lines[i][0:-1]

                #check code or md file.
                ext = os.path.splitext(filename)[1]
                lexer = None
                if ext != '.md':
                    try:
                        lexer = get_lexer_for_filename(filename, stripall=True)
                    except ClassNotFound:
                        pass

                if lexer != None:
                    #add four ' ' to all lines
                    for i in range(len(file_lines)):
                        file_lines[i] = '    ' + file_lines[i]

                    file_lines.insert(0, before_macro)
                    file_lines.insert(1, '    :::%s' % lexer.name)
                    file_lines.append(after_macro)
                    file_lines.append('&nbsp;')
                else:
                    file_lines[0]  = before_macro + file_lines[0]
                    file_lines[-1] = file_lines[-1] + after_macro

                #Debug:
                #
                #print('Included file "%s":' % filename)
                #for tmp in file_lines:
                #    print(">%s" % tmp)
                #
                #example of merged list:
                # orginal       final
                # -------------------------------
                # .A.           .A.
                # lineno        file_lines[0]
                # .B.           file_lines[...]
                # ...           .B.
                # ...           ...
                lines = lines[:lineno] + file_lines + lines[lineno+1:]

                #recheck when included '.md' file.
                #else check next line
                if ext != '.md':
                    lineno = lineno + 1

                break

            if (lineno == nr_lines):
                all_parsed = True

        return lines


def makeExtension(*args,**kwargs):
    return MarkdownInclude(kwargs)


