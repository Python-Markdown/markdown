title: Sane Lists Extension

Sane Lists
==========

Summary
-------

The Sane Lists extension alters the behavior of the Markdown List syntax
to be less surprising.

This extension is included in the standard Markdown library.

Syntax
------

Sane Lists do not allow the mixing of list types. In other words, an ordered
list will not continue when an unordered list item is encountered and
vice versa. For example:

```md
1. Ordered item 1
2. Ordered item 2

* Unordered item 1
* Unordered item 2
```

will result in the following output:

```html
<ol>
  <li>Ordered item 1</li>
  <li>Ordered item 2</li>
</ol>

<ul>
  <li>Unordered item 1</li>
  <li>Unordered item 2</li>
</ul>
```

Whereas the default Markdown behavior would be to generate an unordered list.

Note that, unlike the default Markdown behavior, if a blank line is not
included between list items, the different list type is ignored completely.
This corresponds to the behavior of paragraphs. For example:

```md
A Paragraph.
* Not a list item.

1. Ordered list item.
* Not a separate list item.
```

With this extension the above will result in the following output:

```html
<p>A Paragraph.
* Not a list item.</p>

<ol>
  <li>Ordered list item.
  * Not a separate list item.</li>
</ol>
```

Sane lists also recognize the number used in ordered lists. Given the following
list:

```md
4. Apples
5. Oranges
6. Pears
```

By default markdown will ignore the fact that the first line started
with item number "4" and the HTML list will start with a number "1".
This extension will result in the following HTML output:

```html
<ol start="4">
  <li>Apples</li>
  <li>Oranges</li>
  <li>Pears</li>
</ol>
```

In all other ways, Sane Lists should behave as normal Markdown lists.

Usage
-----

See [Extensions](index.md) for general extension usage. Use `sane_lists` as the
name of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['sane_lists'])
```
