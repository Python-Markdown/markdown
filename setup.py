#!/usr/bin/env python

from distutils.core import setup
from markdown import version

setup(
    name = 'Markdown',
    version = version,
    url = 'http://www.freewisdom.org/projects/python-markdown',
    download_url = 'http://pypi.python.org/packages/source/M/Markdown/Markdown-2.0.tar.gz',
    description = "Python implementation of Markdown.",
    author = "Manfred Stienstra and Yuri takhteyev",
    author_email = "yuri [at] freewisdom.org",
    maintainer = "Waylan Limberg",
    maintainer_email = "waylan [at] gmail.com",
    license = "BSD License",
    packages = ['markdown', 'markdown.extensions'],
    scripts = ['markdown.py'],
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Communications :: Email :: Filters',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: Site Management',
                   'Topic :: Software Development :: Documentation',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Text Processing :: Filters',
                   'Topic :: Text Processing :: Markup :: HTML',
                  ],
    ) 
