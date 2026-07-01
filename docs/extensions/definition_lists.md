title: Definition Lists Extension

Definition Lists
================

Summary
-------

The Definition Lists extension adds the ability to create definition lists in
Markdown documents.

This extension is included in the standard Markdown library.

!!! Note

    This extension is in __maintanence mode__.  We will continue to fix bugs
    and keep it up-to-date with the core parser, but no new features or
    changes in behavior will be made. If you need a feature that this
    extension does not offer, then you have three options (1) find an
    existing [third-party extension] which meets your needs, (2) [build your
    own extension], or (3) fork this extension (pursuant to its licensing
    requirements) and maintain it as a third-party extension.

    We recommend [PyMdown Definition] as an actively developed alternative. 

[third-party extension]: index.md#third-party-extensions
[build your own extension]: api.md
[PyMdown Definition]: https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/definition/

Syntax
------

Definition lists are defined using the syntax established in
[PHP Markdown Extra][php].

[php]: http://www.michelf.com/projects/php-markdown/extra/#def-list

Thus, the following text (taken from the above referenced PHP documentation):

```md
Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.
```

will be rendered as:

```html
<dl>
<dt>Apple</dt>
<dd>Pomaceous fruit of plants of the genus Malus in
the family Rosaceae.</dd>

<dt>Orange</dt>
<dd>The fruit of an evergreen tree of the genus Citrus.</dd>
</dl>
```

Usage
-----

See [Extensions](index.md) for general extension usage. Use `def_list` as the
name of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['def_list'])
```
