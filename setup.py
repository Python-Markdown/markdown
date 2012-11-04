#!/usr/bin/env python

from __future__ import with_statement
import sys, os
from distutils.core import setup
from distutils.command.install_scripts import install_scripts
from distutils.command.build import build
from distutils.core import Command
from distutils.util import change_root, newer
import codecs

# Try to run 2to3 automaticaly when building in Python 3.x
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    if sys.version_info >= (3, 0):
        raise ImportError("build_py_2to3 is required to build in Python 3.x.")
    from distutils.command.build_py import build_py

version = '2.2.1'

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
                bat_path = os.path.join(self.install_dir, '%s.bat' %SCRIPT_NAME)
                f = open(bat_path, 'w')
                f.write(bat_str)
                f.close()
                print ('Created: %s' % bat_path)
            except Exception:
                _, err, _ = sys.exc_info() # for both 2.x & 3.x compatability
                print ('ERROR: Unable to create %s: %s' % (bat_path, err))


class build_docs(Command):
    """ Build markdown documentation into html."""

    description = '"build" documentation (convert markdown text to html)'

    user_options = [
        ('build-base=', 'd', 'directory to "build" to'),
        ('force', 'f', 'forcibly build everything (ignore file timestamps)'),
        ]

    boolean_options = ['force']

    def initialize_options(self):
        self.build_base = None
        self.force = None
        self.docs = None
        self.sitemap = ''

    def finalize_options(self):
        self.set_undefined_options('build',
                                    ('build_base', 'build_base'),
                                    ('force', 'force'))
        self.docs = self._get_docs()

    def _get_docs(self):
        for root, dirs, files in os.walk('docs'):
            for file in files:
                if not file.startswith('_'):
                    path = os.path.join(root, file)
                    yield path

    def _get_context(self, src, path):
        """ Build and return context to pass to template. """
        # set defaults
        c = {
            'title'      : '',
            'prev_url'   : '',
            'prev_title' : '',
            'next_url'   : '',
            'next_title' : '',
            'crumb'      : '',
            'version'    : version,
        }
        c['body'] = self.md.convert(src)
        c['toc'] = self.md.toc
        for k, v in self.md.Meta.items():
            c[k] = ' '.join(v)
        self.md.reset()
        # Manipulate path
        path = path[len(os.path.join(self.build_base, 'docs/')):]
        dir, file = os.path.split(path)
        name, ext = os.path.splitext(file)
        parts = [x for x in dir.split(os.sep) if x]
        c['source'] = '%s.txt' % name
        c['base'] = '../'*len(parts)
        # Build page title
        if name.lower() != 'index' or parts:
            c['page_title'] = '%s &#8212; Python Markdown' % c['title']
        else:
            c['page_title'] = 'Python Markdown'
        # Build crumb trail
        crumbs = []
        ctemp = '<li><a href="%s">%s</a> &raquo;</li>'
        for n, part in enumerate(parts):
            href = ('../'*n) + 'index.html'
            label = part.replace('_', ' ').capitalize()
            crumbs.append(ctemp % (href, label))
        if c['title'] and name.lower() != 'index':
            crumbs.append(ctemp % (file, c['title']))
        c['crumb'] = '\n'.join(crumbs)
        return c

    def run(self):
        # Before importing markdown, tweak sys.path to import from the
        # build directory (2to3 might have run on the library).
        bld_cmd = self.get_finalized_command("build")
        sys.path.insert(0, bld_cmd.build_lib)
        try:
            import markdown
        except ImportError:
            print ('skipping build_docs: Markdown "import" failed!')
        else:
            with codecs.open('docs/_template.html', encoding='utf-8') as f:
                template = f.read()
            self.md = markdown.Markdown(extensions=['extra', 'toc', 'meta'])
            for infile in self.docs:
                outfile, ext = os.path.splitext(infile)
                if ext == '.txt':
                    # Copy src to .txt file
                    srcfile = outfile + '.txt'
                    srcfile = change_root(self.build_base, srcfile)
                    self.mkpath(os.path.split(srcfile)[0])
                    self.copy_file(infile, srcfile)
                    # Render html file
                    outfile += '.html'
                    outfile = change_root(self.build_base, outfile)
                    self.mkpath(os.path.split(outfile)[0])
                    if self.force or newer(infile, outfile):
                        if self.verbose:
                            print ('Converting %s -> %s' % (infile, outfile))
                        if not self.dry_run:
                            with codecs.open(infile, encoding='utf-8') as f:
                                src = f.read()
                            out = template % self._get_context(src, outfile)
                            doc = open(outfile, 'wb')
                            doc.write(out.encode('utf-8'))
                            doc.close()
                else:
                    outfile = change_root(self.build_base, infile)
                    self.mkpath(os.path.split(outfile)[0])
                    self.copy_file(infile, outfile)


class md_build(build):
    """ Run "build_docs" command from "build" command. """
    def has_docs(self):
        return True

    sub_commands = build.sub_commands + [('build_docs', has_docs)]

long_description = \
'''This is a Python implementation of John Gruber's Markdown_. 
It is almost completely compliant with the reference implementation,
though there are a few known issues. See Features_ for information 
on what exactly is supported and what is not. Additional features are 
supported by the `Available Extensions`_.

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Features: http://packages.python.org/Markdown/index.html#Features
.. _`Available Extensions`: http://packages.python.org/Markdown/extensions/index.html

Support
=======

You may ask for help and discuss various other issues on the
`mailing list`_ and report bugs on the `bug tracker`_.

.. _`mailing list`: http://lists.sourceforge.net/lists/listinfo/python-markdown-discuss
.. _`bug tracker`: http://github.com/waylan/Python-Markdown/issues
'''

data = dict(
    name =          'Markdown',
    version =       version,
    url =           'http://packages.python.org/Markdown/',
    download_url =  'http://pypi.python.org/packages/source/M/Markdown/Markdown-%s.tar.gz' % version,
    description =   'Python implementation of Markdown.',
    long_description = long_description,
    author =        'Manfred Stienstra, Yuri takhteyev and Waylan limberg',
    author_email =  'markdown [at] freewisdom.org',
    maintainer =    'Waylan Limberg',
    maintainer_email = 'waylan [at] gmail.com',
    license =       'BSD License',
    packages =      ['markdown', 'markdown.extensions'],
    scripts =       ['bin/%s' % SCRIPT_NAME],
    cmdclass =      {'install_scripts': md_install_scripts,
                     'build_py': build_py,
                     'build_docs': build_docs,
                     'build': md_build},
    classifiers =   ['Development Status :: 5 - Production/Stable',
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 2.5',
                     'Programming Language :: Python :: 2.6',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3',
                     'Programming Language :: Python :: 3.1',
                     'Programming Language :: Python :: 3.2',
                     'Topic :: Communications :: Email :: Filters',
                     'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                     'Topic :: Internet :: WWW/HTTP :: Site Management',
                     'Topic :: Software Development :: Documentation',
                     'Topic :: Software Development :: Libraries :: Python Modules',
                     'Topic :: Text Processing :: Filters',
                     'Topic :: Text Processing :: Markup :: HTML',
                    ],
    )

if sys.version[:3] < '2.5':
    data['install_requires'] = ['elementtree']

setup(**data)

