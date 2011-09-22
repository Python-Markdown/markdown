Python-Markdown Extra
=====================

Summary
-------

A compilation of various Python-Markdown extensions that (mostly) imitates
[PHP Markdown Extra](http://michelf.com/projects/php-markdown/extra/).

The supported extensions include:

* [Abbreviations](abbreviations.html)
* [Attribute Lists](attr_list.html)
* [Definition Lists](definition_lists.html)
* [Fenced Code Blocks](fenced_code_blocks.html)
* [Footnotes](footnotes.html)
* [Tables](tables.html)
* [Smart Strong](smart_strong.html)

See each individual extension for syntax documentation. Extra and all its 
supported extensions are included in the standard Markdown library.

Usage
-----

From the Python interpreter:

    >>> import markdown
    >>> html = markdown.markdown(text, ['extra'])

In the unlikely event that one or more of the supported extensions are not
available for import, Markdown will simply continue without that
extension. If you would like to be notified of such failures,
you may set Python-Markdown's logger level to "WARN".

There may be [additional extensions](index.html) that are distributed with
Python-Markdown that are not included here in Extra. The features 
of those extensions are not part of PHP Markdown Extra, and 
therefore, not part of Python-Markdown Extra. If you really would 
like Extra to include additional extensions, we suggest creating 
your own clone of Extra under a different name 
(see [Writing Extensions](../writing_extensions.html)).  
