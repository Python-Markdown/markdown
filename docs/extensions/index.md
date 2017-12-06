title: Extensions

Available Extensions
====================

Python Markdown offers a flexible extension mechanism, which makes it possible
to change and/or extend the behavior of the parser without having to edit the
actual source files.

To use an extension, pass it to markdown with the `extensions` keyword.

    markdown.markdown(some_text, extensions=[MyExtension(), 'path.to.my.ext', 'markdown.extensions.footnotes'])

See the [Library Reference](../reference.md#extensions) for more details.

From the command line, specify an extension with the `-x` option. 

    $ python -m markdown -x markdown.extensions.footnotes -x markdown.extensions.tables input.txt > output.html

See the [Command Line docs](../cli.md) or use the `--help` option for more details.

!!! seealso "See Also"
    If you would like to write your own extensions, see the
    [Extension API](api.md) for details.

Officially Supported Extensions
-------------------------------

The extensions listed below are maintained and officially supported by
the Python-Markdown team. However, no extensions ship with Python-Markdown
by default. If you would like to use any of the extensions listed below,
you will need to install each of them individually.  See the documentation
for each extension for specifics in instalation and usage. 

Extension                            | "Name"
------------------------------------ | ---------------
[Extra]                              | `extra`
&nbsp; &nbsp; [Abbreviations][]      | `abbr`
&nbsp; &nbsp; [Attribute Lists][]    | `attr_list`
&nbsp; &nbsp; [Definition Lists][]   | `def_list`
&nbsp; &nbsp; [Fenced Code Blocks][] | `fenced_code`
&nbsp; &nbsp; [Footnotes][]          | `footnotes`
&nbsp; &nbsp; [Tables][]             | `tables`
&nbsp; &nbsp; [Smart Strong][]       | `smart_strong`
[Admonition][]                       | `admonition`
[CodeHilite][]                       | `codehilite`
[Meta-Data]                          | `meta`
[New Line to Break]                  | `nl2br`
[Sane Lists]                         | `sane_lists`
[SmartyPants]                        | `smarty`
[Table of Contents]                  | `toc`
[WikiLinks]                          | `wikilinks`

[Extra]: https://github.com/Python-Markdown/mdx_extra
[Abbreviations]: https://github.com/Python-Markdown/mdx_abbreviations
[Attribute Lists]: https://github.com/Python-Markdown/mdx_attr_list
[Definition Lists]: https://github.com/Python-Markdown/mdx_definition_lists
[Fenced Code Blocks]: https://github.com/Python-Markdown/mdx_fenced_code_blocks
[Footnotes]: https://github.com/Python-Markdown/mdx_footnotes
[Tables]: https://github.com/Python-Markdown/mdx_tables
[Smart Strong]: https://github.com/Python-Markdown/mdx_smart_strong
[Admonition]: https://github.com/Python-Markdown/mdx_admonition
[CodeHilite]: https://github.com/Python-Markdown/mdx_code_hilite
[Meta-Data]: https://github.com/Python-Markdown/mdx_meta_data
[New Line to Break]: https://github.com/Python-Markdown/mdx_nl2br
[Sane Lists]: https://github.com/Python-Markdown/mdx_sane_lists
[SmartyPants]: https://github.com/Python-Markdown/mdx_smarty
[Table of Contents]: https://github.com/Python-Markdown/mdx_toc
[WikiLinks]: https://github.com/Python-Markdown/mdx_wikilinks

Third Party Extensions
----------------------

Various individuals and/or organizations have developed extensions which they
have made available to the public. A [list of third party extensions][list]
is maintained on the wiki for your convenience. The Python-Markdown team
offers no official support for these extensions. Please see the developer of
each extension for support.

[list]: https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions
