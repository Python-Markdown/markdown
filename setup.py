#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

Copyright 2007-2018 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""


from setuptools import setup
from markdown import __version__, __version_info__


# Get development Status for classifiers
dev_status_map = {
    'dev':   '2 - Pre-Alpha',
    'alpha': '3 - Alpha',
    'beta':  '4 - Beta',
    'rc':    '4 - Beta',
    'final': '5 - Production/Stable'
}
DEVSTATUS = dev_status_map[__version_info__[3]]

# The command line script name.  Currently set to "markdown_py" so as not to
# conflict with the perl implimentation (which uses "markdown").
SCRIPT_NAME = 'markdown_py'


long_description = '''
This is a Python implementation of John Gruber's Markdown_.
It is almost completely compliant with the reference implementation,
though there are a few known issues. See Features_ for information
on what exactly is supported and what is not. Additional features are
supported by the `Available Extensions`_.

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Features: https://Python-Markdown.github.io#features
.. _`Available Extensions`: https://Python-Markdown.github.io/extensions/

Support
=======

You may report bugs, ask for help, and discuss various other issues on
the `bug tracker`_.

.. _`bug tracker`: http://github.com/Python-Markdown/markdown/issues
'''


setup(
    name='Markdown',
    version=__version__,
    url='https://Python-Markdown.github.io/',
    download_url='http://pypi.python.org/packages/source/M/Markdown/Markdown-%s-py2.py3-none-any.whl' % __version__,
    description='Python implementation of Markdown.',
    long_description=long_description,
    author='Manfred Stienstra, Yuri takhteyev and Waylan limberg',
    author_email='waylan.limberg@icloud.com',
    maintainer='Waylan Limberg',
    maintainer_email='waylan.limberg@icloud.com',
    license='BSD License',
    packages=['markdown', 'markdown.extensions'],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=['setuptools >= 36'],
    extras_require={
        'testing': [
            'coverage',
            'pyyaml',
        ],
    },
    entry_points={
        'console_scripts': [
            '%s = markdown.__main__:run' % SCRIPT_NAME,
        ],
        # Register the built in extensions
        'markdown.extensions': [
            'abbr = markdown.extensions.abbr:AbbrExtension',
            'admonition = markdown.extensions.admonition:AdmonitionExtension',
            'attr_list = markdown.extensions.attr_list:AttrListExtension',
            'codehilite = markdown.extensions.codehilite:CodeHiliteExtension',
            'def_list = markdown.extensions.def_list:DefListExtension',
            'extra = markdown.extensions.extra:ExtraExtension',
            'fenced_code = markdown.extensions.fenced_code:FencedCodeExtension',
            'footnotes = markdown.extensions.footnotes:FootnoteExtension',
            'meta = markdown.extensions.meta:MetaExtension',
            'nl2br = markdown.extensions.nl2br:Nl2BrExtension',
            'sane_lists = markdown.extensions.sane_lists:SaneListExtension',
            'smarty = markdown.extensions.smarty:SmartyExtension',
            'tables = markdown.extensions.tables:TableExtension',
            'toc = markdown.extensions.toc:TocExtension',
            'wikilinks = markdown.extensions.wikilinks:WikiLinkExtension',
            'legacy_attrs = markdown.extensions.legacy_attrs:LegacyAttrExtension',
            'legacy_em = markdown.extensions.legacy_em:LegacyEmExtension',
        ]
    },
    classifiers=[
        'Development Status :: %s' % DEVSTATUS,
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications :: Email :: Filters',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
