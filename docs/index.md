Python-Markdown
===============

This is a Python implementation of John Gruber's 
[Markdown](http://daringfireball.net/projects/markdown/). 
It is almost completely compliant with the reference implementation,
though there are a few very minor differences. See John's 
[Syntax Documentation](http://daringfireball.net/projects/markdown/syntax) 
for the syntax rules.

See the [installation instructions](install.html) to get started.

Features
--------

In addition to the basic markdown syntax, Python-Markdown supports the following
features:

* International Input

    Python-Markdown will accept input in any language supported by Unicode 
    including bi-directional text. In fact the test suite includes documents 
    written in Russian and Arabic.

* Middle-Word Emphasis

    Python-Markdown defaults to ignoring middle-word emphasis. In other words,
    `some_long_filename.txt` will not become `some<em>long</em>filename.txt`.
    This can be switched off if desired. See the 
    [Library Reference](using_as_module.html) for details.

* Extensions

    Various [extensions](extensions/) are provided (including 
    [extra](extensions/extra.html)) to expand the base syntax. Additionally, 
    a public [Extension API](writing_extensions.html) is available to write 
    your own extensions.

* Output Formats

    Python-Markdown can output documents in HTML4, XHTML and HTML5.

* "Safe Mode"

    When using Python-Markdown to parse input from untrusted users on the web,
    the handling of raw HTML can be controlled in various ways to prevent 
    harmful code from being injected into your site.

* Command Line Interface

    In addition to being a Python Library, a 
    [command line script](command_line.html) is available for your convenience.

Support
-------

You may ask for help and discuss various other issues on the [mailing list][] 
and report bugs on the [bug tracker][].

[mailing list]: http://lists.sourceforge.net/lists/listinfo/python-markdown-discuss
[bug tracker]: http://github.com/waylan/Python-Markdown/issues 
