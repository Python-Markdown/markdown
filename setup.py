#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'Markdown',
    version = '2.0-beta-2',
    url = 'http://www.freewisdom.org/projects/python-markdown',
    download_url = 'http://pypi.python.org/packages/source/M/Markdown/markdown-1.7.tar.gz',
    description = "Python implementation of Markdown.",
    author = "Manfred Stienstra and Yuri takhteyev",
    author_email = "yuri [at] freewisdom.org",
    maintainer = "Waylan Limberg",
    maintainer_email = "waylan [at] gmail.com",
    url = "http://www.freewisdom.org/projects/python-markdown",
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
