"""
Python Markdown

A Python implementation of John Gruber's Markdown.

Documentation: https://python-markdown.github.io/
GitHub: https://github.com/Python-Markdown/markdown/
PyPI: https://pypi.org/project/Markdown/

Started by Manfred Stienstra (http://www.dwerg.net/).
Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
Currently maintained by Waylan Limberg (https://github.com/waylan),
Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

Copyright 2007-2021 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

import sys

def set_parser(parser):
  """ Set parser to alternative like e.g. lxml.etree
  usage:

  import markdown
  import lxml.etree
  markdown.etree.set_parser(lxml.etree)
  """
  setattr(sys.modules[__name__], 'etree', parser)
  

def reset_parser(parser):
  """ Reset the ElementTree parser back to default """

  import xml.etree.ElementTree as etree

def __getattr__(name):
    """Get attribute."""
    return getattr(etree, name)
  
if not hasattr(sys.modules[__name__], 'etree'):
  import xml.etree.ElementTree as etree
