Using Python-Markdown on the Command Line
=========================================

While Python-Markdown is primarily a python library, a command line script is 
included as well. While there are many other command line implementations 
of Markdown, you may not have them installed, or you may prefer to use 
Python-Markdown's various extensions.

Generally, you will want to have the Markdown library fully installed on your
system (``setup.py install`` or ``easy_install markdown``) to run the command 
line script. 

Assuming the `python` executable is on your system path, just run the following:

    python -m markdown [options] [args]

That will run the module as a script. Note that on older python versions (2.5 
and 2.6), you may need to specify the appropriate module:

    python -m markdown.__main__ [options] [args]

Use the `--help` option for available options:

    python -m markdown --help

If you are using Python 2.4 or you don't want to have to call the python
executable directly, follow the instructions below:

Setup
-----

Upon installation, the ``markdown_py`` script will have been copied to
your Python "Scripts" directory. Different systems require different methods to
ensure that any files in the Python "Scripts" directory are on your system 
path.

* **Windows**:

    Assuming a default install of Python on Windows, your "Scripts" directory 
    is most likely something like ``C:\\Python26\Scripts``. Verify the location
    of your "Scripts" directory and add it to you system path.

    Calling ``markdown_py`` from the command line will call the wrapper batch 
    file ``markdown_py.bat`` in the "Scripts" directory created during install.

* __*nix__ (Linux, OSX, BSD, Unix, etc.):

    As each *nix distribution is different and we can't possibly document all 
    of them here, we'll provide a few helpful pointers:

    * Some systems will automatically install the script on your path. Try it 
      and see if it works. Just run ``markdown_py`` from the command line.

    * Other systems may maintain a separate "Scripts" directory which you
      need to add to your path. Find it (check with your distribution) and
      either add it to your path or make a symbolic link to it from your path.

    * If you are sure ``markdown_py`` is on your path, but it still isn't being
      found, check the permissions of the file and make sure it is executable.

    As an alternative, you could just ``cd`` into the directory which contains
    the source distribution, and run it from there. However, remember that your
    markdown text files will not likely be in that directory, so it is much 
    more convenient to have ``markdown_py`` on your path.

__Note:__ Python-Markdown uses "markdown_py" as a script name because
the Perl implementation has already taken the more obvious name "markdown".
Additionally, the default Python configuration on some systems would cause a 
script named "markdown.py" to fail by importing itself rather than the markdown
library. Therefore, the script has been named "markdown_py" as a compromise. If
you prefer a different name for the script on your system, it is suggested that
you create a symbolic link to `markdown_py` with your preferred name.

Usage
-----

To use ``markdown_py`` from the command line, run it as 

    $ markdown_py input_file.txt

or 

    $ markdown_py input_file.txt > output_file.html

For a complete list of options, run

    $ markdown_py --help

Using Extensions
----------------

For an extension to be run from the command line it must be provided in a module
which should be in your python path (see [writing_extensions](writing_extensions.html)
for details). It can then be invoked by the name of that module:

    $ markdown_py -x footnotes text_with_footnotes.txt > output.html

If the extension supports config options, you can pass them in as well:

    $ markdown_py -x "footnotes(PLACE_MARKER=~~~~~~~~)" input.txt

