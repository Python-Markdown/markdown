title: Abbreviations Extension

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

Usage
-----

See [Extensions](index.md) for general extension usage. Use `abbr` as the name
of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['abbr'])
```
