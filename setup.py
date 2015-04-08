#!/usr/bin/env python

import sys
import os
from setuptools import setup
from distutils.core import Command
from distutils.util import change_root, newer
import codecs
from markdown import __version__, __version_info__


# Get development Status for classifiers
dev_status_map = {
    'alpha': '3 - Alpha',
    'beta':  '4 - Beta',
    'rc':    '4 - Beta',
    'final': '5 - Production/Stable'
}
if __version_info__[3] == 'alpha' and __version_info__[4] == 0:
    DEVSTATUS = '2 - Pre-Alpha'
else:
    DEVSTATUS = dev_status_map[__version_info__[3]]


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
        self.set_undefined_options(
            'build',
            ('build_base', 'build_base'),
            ('force', 'force')
        )
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
            'title':      '',
            'prev_url':   '',
            'prev_title': '',
            'next_url':   '',
            'next_title': '',
            'crumb':      '',
            'version':    __version__,
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
        c['base'] = '../' * len(parts)
        # Build page title
        if name.lower() != 'index' or parts:
            c['page_title'] = '%s &#8212; Python Markdown' % c['title']
        else:
            c['page_title'] = 'Python Markdown'
        # Build crumb trail
        crumbs = []
        ctemp = '<li><a href="%s">%s</a> &raquo;</li>'
        for n, part in enumerate(parts):
            href = ('../' * n) + 'index.html'
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
            print('skipping build_docs: Markdown "import" failed!')
        else:
            with codecs.open('docs/_template.html', encoding='utf-8') as f:
                template = f.read()
            self.md = markdown.Markdown(
                extensions=[
                    'extra',
                    'toc',
                    'meta',
                    'admonition',
                    'smarty'
                ],
                extension_configs={
                    'toc': {'permalink': True}
                }
            )
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
                            print('Converting %s -> %s' % (infile, outfile))
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


long_description = '''
This is a Python implementation of John Gruber's Markdown_.
It is almost completely compliant with the reference implementation,
though there are a few known issues. See Features_ for information
on what exactly is supported and what is not. Additional features are
supported by the `Available Extensions`_.

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Features: https://pythonhosted.org/Markdown/index.html#Features
.. _`Available Extensions`: https://pythonhosted.org/Markdown/extensions/index.html

Support
=======

You may ask for help and discuss various other issues on the
`mailing list`_ and report bugs on the `bug tracker`_.

.. _`mailing list`: http://lists.sourceforge.net/lists/listinfo/python-markdown-discuss
.. _`bug tracker`: http://github.com/waylan/Python-Markdown/issues
'''

setup(
    name='Markdown',
    version=__version__,
    url='https://pythonhosted.org/Markdown/',
    download_url='http://pypi.python.org/packages/source/M/Markdown/Markdown-%s.tar.gz' % __version__,
    description='Python implementation of Markdown.',
    long_description=long_description,
    author='Manfred Stienstra, Yuri takhteyev and Waylan limberg',
    author_email='waylan.limberg [at] icloud.com',
    maintainer='Waylan Limberg',
    maintainer_email='waylan.limberg [at] icloud.com',
    license='BSD License',
    packages=['markdown', 'markdown.extensions'],
    cmdclass={
        'build_docs': build_docs,
    },
    entry_points={
        'console_scripts': [
            'markdown = markdown.__main__:run',
            'mdtests = markdown.test:main'
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
            'headerid = markdown.extensions.headerid:HeaderIdExtension',
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
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: Email :: Filters',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)
