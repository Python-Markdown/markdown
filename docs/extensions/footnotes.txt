Footnotes
=========

Summary
-------

An extension to Python-Markdown that adds footnote syntax. This extension has 
been included with Python-Markdown since 1.7 and should be available to anyone 
who has a typical install of Python-Markdown.

Syntax
------

Python-Markdown's Footnote syntax follows the generally accepted syntax of the 
Markdown community at large and almost exactly matches [PHP Markdown Extra][]'s
implementation of footnotes. The only differences involve a few subtleties in 
the output.

[PHP Markdown Extra]: http://michelf.com/projects/php-markdown/extra/#footnotes

Example:

    Footnotes[^1] have a label[^label] and a definition[^!DEF].

    [^1]: This is a footnote
    [^label]: A footnote on "label"
    [^!DEF]: The definition of a footnote.

A footnote definition may contain multiple lines, paragraphs, code blocks, 
blockquotes and most any other markdown syntax. The additional line simply 
must be indented at least an additional four spaces.

    [^1]: The first paragraph of the definition.

        Paragraph two of the definition.

        > A blockquote with
        > multiple lines.

            a code block

        A final paragraph.

By default, the footnote definitions are placed at the end of the resulting 
HTML document. However, you may want the footnotes in another location within 
the document. Simply place the following text at that location within your 
markdown document (See how to configure this text below):

    ///Footnotes Go Here///

Usage
-----

From the Python interpreter:

    >>> html = markdown.markdown(text, ['footnotes'])

To configure the place marker for footnote definitions (just be sure not to 
use any existing markdown syntax):

    >>> html = markdown.markdown(text, ['footnotes(PLACE_MARKER=+++my marker+++)'])

