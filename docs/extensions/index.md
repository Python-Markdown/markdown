title: Extensions

Available Extensions
====================

Python Markdown offers a flexible extension mechanism, which makes it possible
to change and/or extend the behavior of the parser without having to edit the
actual source files.

To use an extension, pass it to markdown with the `extensions` keyword.

```python
markdown.markdown(some_text, extensions=[MyExtension(), 'path.to.my.ext', 'markdown.extensions.footnotes'])
```

See the [Library Reference](../reference.md#extensions) for more details.

From the command line, specify an extension with the `-x` option.

```bash
python -m markdown -x markdown.extensions.footnotes -x markdown.extensions.tables input.txt > output.html
```

See the [Command Line docs](../cli.md) or use the `--help` option for more details.

!!! seealso "See Also"
    If you would like to write your own extensions, see the
    [Extension API](api.md) for details.

Officially Supported Extensions
-------------------------------

The extensions listed below are included with (at least) the most recent release
and are officially supported by Python-Markdown. Any documentation is
maintained here and all bug reports should be made to the project. If you
have a typical install of Python-Markdown, these extensions are already
available to you using the "name" listed in the second column below.

Extension                            | "Name"
------------------------------------ | ---------------
[Extra]                              | `markdown.extensions.extra`
&nbsp; &nbsp; [Abbreviations][]      | `markdown.extensions.abbr`
&nbsp; &nbsp; [Attribute Lists][]    | `markdown.extensions.attr_list`
&nbsp; &nbsp; [Definition Lists][]   | `markdown.extensions.def_list`
&nbsp; &nbsp; [Fenced Code Blocks][] | `markdown.extensions.fenced_code`
&nbsp; &nbsp; [Footnotes][]          | `markdown.extensions.footnotes`
&nbsp; &nbsp; [Tables][]             | `markdown.extensions.tables`
&nbsp; &nbsp; [Smart Strong][]       | `markdown.extensions.smart_strong`
[Admonition][]                       | `markdown.extensions.admonition`
[CodeHilite][]                       | `markdown.extensions.codehilite`
[HeaderId]                           | `markdown.extensions.headerid`
[Meta-Data]                          | `markdown.extensions.meta`
[New Line to Break]                  | `markdown.extensions.nl2br`
[Sane Lists]                         | `markdown.extensions.sane_lists`
[SmartyPants]                        | `markdown.extensions.smarty`
[Table of Contents]                  | `markdown.extensions.toc`
[WikiLinks]                          | `markdown.extensions.wikilinks`

[Extra]: extra.md
[Abbreviations]: abbreviations.md
[Attribute Lists]: attr_list.md
[Definition Lists]: definition_lists.md
[Fenced Code Blocks]: fenced_code_blocks.md
[Footnotes]: footnotes.md
[Tables]: tables.md
[Smart Strong]: smart_strong.md
[Admonition]: admonition.md
[CodeHilite]: code_hilite.md
[HeaderId]: header_id.md
[Meta-Data]: meta_data.md
[New Line to Break]: nl2br.md
[Sane Lists]: sane_lists.md
[SmartyPants]: smarty.md
[Table of Contents]: toc.md
[WikiLinks]: wikilinks.md

Third Party Extensions
----------------------

Various individuals and/or organizations have developed extensions which they
have made available to the public. A [list of third party extensions][list]
is maintained on the wiki for your convenience. The Python-Markdown team
offers no official support for these extensions. Please see the developer of
each extension for support.

[list]: https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions
