#!/usr/bin/env python

from setuptools import setup
import os
import imp


def get_version():
    " Get version & version_info without importing markdown.__init__ "
    path = os.path.join(os.path.dirname(__file__), 'markdown')
    fp, pathname, desc = imp.find_module('__version__', [path])
    try:
        v = imp.load_module('__version__', fp, pathname, desc)
    finally:
        fp.close()

    dev_status_map = {
        'alpha': '3 - Alpha',
        'beta':  '4 - Beta',
        'rc':    '4 - Beta',
        'final': '5 - Production/Stable'
    }
    if v.version_info[3] == 'alpha' and v.version_info[4] == 0:
        status = '2 - Pre-Alpha'
    else:
        status = dev_status_map[v.version_info[3]]
    return v.version, v.version_info, status


version, version_info, DEVSTATUS = get_version()


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

You may ask for help and discuss various other issues on the
`mailing list`_ and report bugs on the `bug tracker`_.

.. _`mailing list`: http://lists.sourceforge.net/lists/listinfo/python-markdown-discuss
.. _`bug tracker`: http://github.com/Python-Markdown/markdown/issues
'''


setup(
    name='Markdown',
    version=version,
    url='https://Python-Markdown.github.io/',
    download_url='http://pypi.python.org/packages/source/M/Markdown/Markdown-%s-py2.py3-none-any.whl' % version,
    description='Python implementation of Markdown.',
    long_description=long_description,
    author='Manfred Stienstra, Yuri takhteyev and Waylan limberg',
    author_email='waylan.limberg@icloud.com',
    maintainer='Waylan Limberg',
    maintainer_email='waylan.limberg@icloud.com',
    license='BSD License',
    packages=['markdown', 'markdown.extensions'],
    entry_points={
        'console_scripts': [
            '%s = markdown.__main__:run' % SCRIPT_NAME,
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
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: Email :: Filters',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
