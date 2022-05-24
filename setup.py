#!/usr/bin/env python
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


import os
from setuptools import setup


def get_version():
    """Get version and version_info from markdown/__meta__.py file."""
    module_path = os.path.join(os.path.dirname('__file__'), 'markdown', '__meta__.py')

    import importlib.util
    spec = importlib.util.spec_from_file_location('__meta__', module_path)
    meta = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(meta)
    return meta.__version__, meta.__version_info__


__version__, __version_info__ = get_version()

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
# conflict with the perl implementation (which uses "markdown").
SCRIPT_NAME = 'markdown_py'

with open('README.md') as f:
    long_description = f.read()

setup(
    name='Markdown',
    version=__version__,
    url='https://Python-Markdown.github.io/',
    project_urls={
        'Documentation': 'https://Python-Markdown.github.io/',
        'GitHub Project': 'https://github.com/Python-Markdown/markdown',
        'Issue Tracker': 'https://github.com/Python-Markdown/markdown/issues'
    },
    description='Python implementation of Markdown.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Manfred Stienstra, Yuri takhteyev and Waylan limberg',
    author_email='python.markdown@gmail.com',
    maintainer='Waylan Limberg',
    maintainer_email='python.markdown@gmail.com',
    license='BSD License',
    packages=['markdown', 'markdown.extensions'],
    python_requires='>=3.7',
    install_requires=["importlib-metadata>=4.4;python_version<'3.10'"],
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
            'md_in_html = markdown.extensions.md_in_html:MarkdownInHtmlExtension',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Communications :: Email :: Filters',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: Markdown'
    ]
)
