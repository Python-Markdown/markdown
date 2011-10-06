Available Extensions
====================

Python Markdown offers a flexible extension mechanism, which makes it possible 
to change and/or extend the behavior of the parser without having to edit the 
actual source files. 

To use an extension, pass it's name to markdown with the `extensions` keyword.
See [Using Markdown as a Python Library](../using_as_module.html) for more 
details. 

    markdown.markdown(some_text, extensions=['extra', 'nl2br'])

From the command line, specify an extension with the `-x` option.
See [Using Python-Markdown on the Command Line](../command_line.html) or use the
`--help` option for more details.

    python -m markdown -x extra input.txt > output.html

Officially Supported Extensions
-------------------------------

The extensions lists below are included with (at least) the most recent release
and are officially supported by Python-Markdown. Any documentation is 
maintained here and all bug reports should be made to the project. If you 
have a typical install of Python-Markdown, these extensions are already 
available to you.

* [Extra](extra.html)
    * [Abbreviations](abbreviations.html)
    * [Attribute Lists](attr_list.html)
    * [Definition Lists](definition_lists.html)
    * [Fenced Code Blocks](fenced_code_blocks.html)
    * [Footnotes](footnotes.html)
    * [Tables](tables.html)
    * [Smart Strong](smart_strong.html)
* [CodeHilite](code_hilite.html)
* [HTML Tidy](html_tidy.html)
* [HeaderId](header_id.html)
* [Meta-Data](meta_data.html)
* [New Line to Break](nl2br.html)
* [RSS](rss.html)
* [Table of Contents](toc.html)
* [WikiLinks](wikilinks.html)

Third Party Extensions
----------------------

Various individuals and/or organizations have developed extensions which they
have made available to the public.  A [list of third party 
extensions](http://freewisdom.org/projects/python-markdown/Available_Extensions)
is maintained on the wiki for your convenience. The Python-Markdown team 
offers no official support for these extensions. Please see the developer of 
each extension for support.

If you would like to write your own extensions, see the 
[Extensions API](../writing_extensions.html) for details.
