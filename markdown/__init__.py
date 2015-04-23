"""
Python Markdown
===============

Python Markdown converts Markdown to HTML and can be used as a library or
called from the command line.

## Basic usage as a module:

    import markdown
    html = markdown.markdown(your_text_string)

See <https://pythonhosted.org/Markdown/> for more
information and instructions on how to extend the functionality of
Python Markdown.  Read that before you try modifying this file.

## Authors and License

Started by [Manfred Stienstra](http://www.dwerg.net/).  Continued and
maintained  by [Yuri Takhteyev](http://www.freewisdom.org), [Waylan
Limberg](http://achinghead.com/) and [Artem Yunusov](http://blog.splyer.com).

Contact: markdown@freewisdom.org

Copyright 2007-2013 The Python Markdown Project (v. 1.7 and later)
Copyright 200? Django Software Foundation (OrderedDict implementation)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE for details).
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from .core import Markdown, markdown, markdownFromFile

__all__ = ['Markdown', 'markdown', 'markdownFromFile']

# version_info should conform to PEP 386
# (major, minor, micro, alpha/beta/rc/final, #)
# (1, 1, 2, 'alpha', 0) => "1.1.2.dev"
# (1, 2, 0, 'beta', 2) => "1.2b2"
__version_info__ = (3, 0, 0, 'alpha', 0)


def _get_version():  # pragma: no cover
    " Returns a PEP 386-compliant version number from version_info. "
    assert len(__version_info__) == 5
    assert __version_info__[3] in ('alpha', 'beta', 'rc', 'final')

    parts = 2 if __version_info__[2] == 0 else 3
    main = '.'.join(map(str, __version_info__[:parts]))

    sub = ''
    if __version_info__[3] == 'alpha' and __version_info__[4] == 0:
        # TODO: maybe append some sort of git info here??
        sub = '.dev'
    elif __version_info__[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[__version_info__[3]] + str(__version_info__[4])

    return str(main + sub)


__version__ = _get_version()
