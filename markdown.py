#!/usr/bin/env python
"""
Python Markdown, the Command Line Script
========================================

This is the command line script for Python Markdown.

Basic use from the command line:

    python markdown.py source.txt > destination.html

Run "python markdown.py --help" to see more options.

See markdown/__init__.py for information on using Python Markdown as a module.

## Authors and License

Started by [Manfred Stienstra](http://www.dwerg.net/).  Continued and
maintained  by [Yuri Takhteyev](http://www.freewisdom.org), [Waylan
Limberg](http://achinghead.com/) and [Artem Yunusov](http://blog.splyer.com).

Contact: markdown@freewisdom.org

Copyright 2007, 2008 The Python Markdown Project (v. 1.7 and later)
Copyright 200? Django Software Foundation (OrderedDict implementation)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see docs/LICENSE for details).
"""

import sys, os
if sys.platform == 'win32':
        # We have to remove the Scripts dir from path on windows.
        # If we don't, it will try to import itself rather than markdown lib.
        # This appears to *not* be a problem on *nix systems, only Windows.
        try:
            sys.path.remove(os.path.dirname(__file__))
        except (ValueError, NameError):
            pass

# Now we can import the markdown lib.
import logging
from markdown import COMMAND_LINE_LOGGING_LEVEL
from markdown import commandline

# Setup a logger manually for compatibility with Python 2.3
logger = logging.getLogger('MARKDOWN')
logger.setLevel(COMMAND_LINE_LOGGING_LEVEL)
logger.addHandler(logging.StreamHandler())

if __name__ == '__main__':
    commandline.run()
