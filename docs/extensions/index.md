title: Extensions

# Extensions

Python Markdown offers a flexible extension mechanism, which makes it possible
to change and/or extend the behavior of the parser without having to edit the
actual source files.

To use an extension, pass it to markdown with the `extensions` keyword.

```python
markdown.markdown(some_text, extensions=[MyExtClass(), 'myext', 'path.to.my.ext:MyExtClass'])
```

See the [Library Reference](../reference.md#extensions) for more details.

From the command line, specify an extension with the `-x` option.

```bash
python -m markdown -x myext -x path.to.module:MyExtClass input.txt > output.html
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
available to you using the "Entry Point" name listed in the second column below.

Extension                          | Entry Point    | Dot Notation
---------------------------------- | -------------- | ------------
[Extra]                            | `extra`        | `markdown.extensions.extra`
&nbsp; &nbsp; [Abbreviations]      | `abbr`         | `markdown.extensions.abbr`
&nbsp; &nbsp; [Attribute Lists]    | `attr_list`    | `markdown.extensions.attr_list`
&nbsp; &nbsp; [Definition Lists]   | `def_list`     | `markdown.extensions.def_list`
&nbsp; &nbsp; [Fenced Code Blocks] | `fenced_code`  | `markdown.extensions.fenced_code`
&nbsp; &nbsp; [Footnotes]          | `footnotes`    | `markdown.extensions.footnotes`
&nbsp; &nbsp; [Markdown in HTML]   | `md_in_html`   | `markdown.extensions.md_in_html`
&nbsp; &nbsp; [Tables]             | `tables`       | `markdown.extensions.tables`
[Admonition]                       | `admonition`   | `markdown.extensions.admonition`
[CodeHilite]                       | `codehilite`   | `markdown.extensions.codehilite`
[Legacy Attributes]                | `legacy_attrs`  | `markdown.extensions.legacy_attrs`
[Legacy Emphasis]                  | `legacy_em`    | `markdown.extensions.legacy_em`
[Meta-Data]                        | `meta`         | `markdown.extensions.meta`
[New Line to Break]                | `nl2br`        | `markdown.extensions.nl2br`
[Sane Lists]                       | `sane_lists`   | `markdown.extensions.sane_lists`
[SmartyPants]                      | `smarty`       | `markdown.extensions.smarty`
[Table of Contents]                | `toc`          | `markdown.extensions.toc`
[WikiLinks]                        | `wikilinks`    | `markdown.extensions.wikilinks`

[Extra]: extra.md
[Abbreviations]: abbreviations.md
[Attribute Lists]: attr_list.md
[Definition Lists]: definition_lists.md
[Fenced Code Blocks]: fenced_code_blocks.md
[Footnotes]: footnotes.md
[Tables]: tables.md
[Admonition]: admonition.md
[CodeHilite]: code_hilite.md
[Legacy Attributes]: legacy_attrs.md
[Legacy Emphasis]: legacy_em.md
[Meta-Data]: meta_data.md
[New Line to Break]: nl2br.md
[Markdown in HTML]: md_in_html.md
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
