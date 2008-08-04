from distutils.core import setup

setup(
    name = 'Markdown',
    version = '2.0-alpha',
    description = "Python implementation of Markdown.",
    author = "Manfred Stienstra and Yuri takhteyev",
    author_email = "yuri [at] freewisdom.org",
    maintainer = "Waylan Limberg",
    maintainer_email = "waylan [at] gmail.com",
    url = "http://www.freewisdom.org/projects/python-markdown",
    license = "BSD License, GNU Public License (GPL)",
    py_modules = ["markdown",
                "mdx_codehilite",
                "mdx_fenced_code",
                "mdx_footnotes",
                "mdx_headerid",
                "mdx_imagelinks",
                "mdx_meta",
                "mdx_rss",
                "mdx_tables",
                "mdx_wikilink",
                ],
    ) 
