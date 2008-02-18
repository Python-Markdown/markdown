from distutils.core import setup

setup(
    name = 'markdown',
    version = '1.7',
    description = "Python implementation of Markdown.",
    author = "Manfred Stienstra and Yuri takhteyev",
    author_email = "yuri [at] freewisdom.org",
    maintainer = "Waylan Limberg",
    maintainer_email = "waylan [at] gmail.com",
    url = "http://www.freewisdom.org/projects/python-markdown",
    license = "BSD License, GNU Public License (GPL)",
    py_modules = ["markdown","mdx_footnotes", "mdx_rss"],
    ) 
