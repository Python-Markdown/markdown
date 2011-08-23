Installing Python-Markdown
==========================

Checking Dependencies
---------------------

Python-Markdown requires the ElementTree module to be installed. In Python2.5+ 
ElementTree is included as part of the standard library. For earlier versions 
of Python, open a Python shell and type the following:

    >>> import cElementTree
    >>> import ElementTree

If at least one of those does not generate any errors, then you have a working
copy of ElementTree installed on your system. As cElementTree is faster, you
may want to install that if you don't already have it and it's available for 
your system.

See <http://effbot.org/zone/element-index.htm> for more information or to 
download the latest version of ElementTree.

The Easy Way
------------

As an Admin/Root user on your system do:

    pip install markdown

or

    easy_install markdown

Installing on Windows
---------------------

Download the Windows installer (.exe) from PyPI: 
<http://pypi.python.org/pypi/Markdown>

Double-click the file and follow the instructions.

If you prefer to manually install Python-Markdown in Windows, download the
Zip file, unzip it, and on the command line in the directory you unzipped to:

    python setup.py install

If you plan to use the provided command line script, you need to make sure your
script directory is on your system path. On a typical Python install of Windows
the Scripts directory is `C:\Python25\Scripts\`. Adjust according to your 
system and add that to your system path.

Installing on *nix Systems
--------------------------

From the command line do the following (where 2.x is the version number):

    wget http://pypi.python.org/packages/source/M/Markdown/Markdown-2.x.tar.gz
    tar xvzf Markdown-2.x.tar.gz
    cd markdown-2.x/
    sudo python setup.py install

See [PyPI](http://pypi.python.org/pypi/Markdown) for all available versions.

Using the Git Repository
------------------------

If you're the type that likes to live on the edge, you may want to keep up with 
the latest additions and bug fixes in the repository between releases.
Python-Markdown is maintained in a Git repository on github.com. To
get a copy of Python-Markdown from the repository do the following from the
command line:

    git clone git://github.com/waylan/Python-Markdown.git python-markdown
    cd python-markdown
    python setup.py install

