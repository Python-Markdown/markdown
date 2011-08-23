Abbreviations
-------------

Summary
-------

The Markdown Abbreviation Extension adds the ability to define abbreviations. 
Specifically, any defined abbreviation is wrapped in  an `<abbr>` tag.

The Abbreviation extension is included in the standard Markdown library.

Syntax
------

Abbreviations are defined using the syntax established in 
[PHP Markdown Extra][php].

[php]: http://www.michelf.com/projects/php-markdown/extra/#abbr

Thus, the following text (taken from the above referenced PHP documentation):

    The HTML specification 
    is maintained by the W3C.
        
    *[HTML]: Hyper Text Markup Language
    *[W3C]:  World Wide Web Consortium

will be rendered like so:

    <p>The <abbr title="Hyper Text Markup Language">HTML</abbr> specification 
    is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.</p>

Usage
-----

From the Python interpreter:

    >>> import markdown
    >>> text = """
    ... Some text with an ABBR.
    ...
    ... *[ABBR]: Abbreviation
    ... """
    >>> html = markdown.markdown(text, ['abbr'])

To use with other extensions, just add them to the list, like this:

    >>> html = markdown.markdown(text, ['abbr', 'footnotes'])

Abbreviations can also be called from the command line using Markdown's `-x` 
parameter, like so:

    markdown.py -x abbr source.txt > output.html
