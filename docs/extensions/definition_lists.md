title: Definition Lists Extension

Definition Lists
================

Summary
-------

The Definition Lists extension adds the ability to create definition lists in
Markdown documents.

This extension is included in the standard Markdown library.

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
