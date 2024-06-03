title: Abbreviations Extension

ABBR

*[ABBR]: Abbreviation
*[ABBR]: Override Ignored

Abbreviations
=============

Summary
-------

The Abbreviations extension adds the ability to define abbreviations.
Specifically, any defined abbreviation is wrapped in  an `<abbr>` tag.

The Abbreviations extension is included in the standard Markdown library.

Syntax
------

Abbreviations are defined using the syntax established in
[PHP Markdown Extra][php].

[php]: http://www.michelf.com/projects/php-markdown/extra/#abbr

Thus, the following text (taken from the above referenced PHP documentation):

```md
The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium
```

will be rendered as:

```html
<p>The <abbr title="Hyper Text Markup Language">HTML</abbr> specification
is maintained by the <abbr title="World Wide Web Consortium">W3C</abbr>.</p>
```

The backslash (`\`) is not permitted in an abbreviation. Any abbreviation
definitions which include one or more backslashes between the square brackets
will not be recognized as an abbreviation definition.

Usage
-----

See [Extensions](index.md) for general extension usage. Use `abbr` as the name
of the extension.

The following options are provided to configure the output:

* **`use_last_abbr`**:
    `True` to use the last instance of an abbreviation, rather than the first instance.

    This is useful when auto-appending glossary files to pages while still wanting the page's
    abbreviations to take precedence. Not recommended for use with the `glossary` option.

* **`glossary`**:
    Path to a Markdown file containing abbreviations to be applied to every page.

    The abbreviations from this file will be the default abbreviations applied to every page with
    abbreviations defined on the page taking precedence (unless also using `use_last_abbr`). The
    glossary syntax should use the same Markdown syntax described on this page.

A trivial example:

```python
markdown.markdown(some_text, extensions=['abbr'])
```
