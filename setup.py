#!/usr/bin/env python

from __future__ import with_statement
import sys
import os
from distutils.core import setup
from distutils.command.install_scripts import install_scripts
import imp


def get_version():
    " Get version & version_info without importing markdown.__init__ "
    path = os.path.join(os.path.dirname(__file__), 'markdown')
    fp, pathname, desc = imp.find_module('__version__', [path])
    try:
        v = imp.load_module('__version__', fp, pathname, desc)
        return v.version, v.version_info
    finally:
        fp.close()


version, version_info = get_version()

# Get development Status for classifiers
dev_status_map = {
    'alpha': '3 - Alpha',
    'beta':  '4 - Beta',
    'rc':    '4 - Beta',
    'final': '5 - Production/Stable'
}
if version_info[3] == 'alpha' and version_info[4] == 0:
    DEVSTATUS = '2 - Pre-Alpha'
else:
    DEVSTATUS = dev_status_map[version_info[3]]

# The command line script name.  Currently set to "markdown_py" so as not to
# conflict with the perl implimentation (which uses "markdown").  We can't use
# "markdown.py" as the default config on some systems will cause the script to
# try to import itself rather than the library which will raise an error.
SCRIPT_NAME = 'markdown_py'


class md_install_scripts(install_scripts):

    """ Customized install_scripts. Create markdown_py.bat for win32. """

    def run(self):
        install_scripts.run(self)

        if sys.platform == 'win32':
            try:
                script_dir = os.path.join(sys.prefix, 'Scripts')
                script_path = os.path.join(script_dir, SCRIPT_NAME)
                bat_str = '@"%s" "%s" %%*' % (sys.executable, script_path)
                bat_path = os.path.join(
                    self.install_dir, '%s.bat' % SCRIPT_NAME
                )
                f = open(bat_path, 'w')
                f.write(bat_str)
                f.close()
                print('Created: %s' % bat_path)
            except Exception:
                _, err, _ = sys.exc_info()  # for both 2.x & 3.x compatability
                print('ERROR: Unable to create %s: %s' % (bat_path, err))


long_description = '''
This is a Python implementation of John Gruber's Markdown_.
It is almost completely compliant with the reference implementation,
though there are a few known issues. See Features_ for information
on what exactly is supported and what is not. Additional features are
supported by the `Available Extensions`_.

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Features: https://Python-Markdown.github.io#Features
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
    download_url='http://pypi.python.org/packages/source/M/Markdown/Markdown-%s.tar.gz' % version,
    description='Python implementation of Markdown.',
    long_description=long_description,
    author='Manfred Stienstra, Yuri takhteyev and Waylan limberg',
    author_email='waylan.limberg@icloud.com',
    maintainer='Waylan Limberg',
    maintainer_email='waylan.limberg@icloud.com',
    license='BSD License',
    packages=['markdown', 'markdown.extensions'],
    scripts=['bin/%s' % SCRIPT_NAME],
    cmdclass={
        'install_scripts': md_install_scripts
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
