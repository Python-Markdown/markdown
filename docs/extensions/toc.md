title: Table of Contents Extension

Table of Contents
=================

Summary
-------

The Table of Contents extension generates a Table of Contents from a Markdown
document and adds it into the resulting HTML document.

This extension is included in the standard Markdown library.

Syntax
------

By default, all headers will automatically have unique `id` attributes
generated based upon the text of the header. Note this example, in which all
three headers would have the same `id`:

```md
#Header
#Header
#Header
```

Results in:

```html
<h1 id="header">Header</h1>
<h1 id="header_1">Header</h1>
<h1 id="header_2">Header</h1>
```

Place a marker in the document where you would like the Table of Contents to
appear. Then, a nested list of all the headers in the document will replace the
marker. The marker defaults to `[TOC]` so the following document:

```md
[TOC]

# Header 1

## Header 2
```

would generate the following output:

```html
<div class="toc">
  <ul>
    <li><a href="#header-1">Header 1</a></li>
      <ul>
        <li><a href="#header-2">Header 2</a></li>
      </ul>
  </ul>
</div>
<h1 id="header-1">Header 1</h1>
<h2 id="header-2">Header 2</h2>
```

Regardless of whether a `marker` is found in the document (or disabled), the
Table of Contents is available as an attribute (`toc`) on the Markdown class.
This allows one to insert the Table of Contents elsewhere in their page
template. For example:

```pycon
>>> md = markdown.Markdown(extensions=['toc'])
>>> html = md.convert(text)
>>> page = render_some_template(context={'body': html, 'toc': md.toc})
```

The `toc_tokens` attribute is also available on the Markdown class and contains
a nested list of dict objects. For example, the above document would result in
the following object at `md.toc_tokens`:

```python
[
    {
        'level': 1,
        'id': 'header-1',
        'name': 'Header 1',
        'children': [
            {'level': 2, 'id': 'header-2', 'name': 'Header 2', 'children':[]}
        ]
    }
]
```

Note that the `level` refers to the `hn` level. In other words, `<h1>` is level
`1` and `<h2>` is level `2`, etc. Be aware that improperly nested levels in the
input may result in odd nesting of the output.

### Custom Labels

In most cases, the text label in the Table of Contents should match the text of
the header. However, occasionally that is not desirable. In that case, if this
extension is used in conjunction with the [Attribute Lists Extension] and a
`data-toc-label` attribute is defined on the header, then the contents of that
attribute will be used as the text label for the item in the Table of Contents.
For example, the following Markdown:

[Attribute Lists Extension]: attr_list.md

```md
[TOC]

# Functions

## `markdown.markdown(text [, **kwargs])` { #markdown data-toc-label='markdown.markdown' }
```
would generate the following output:

```html
<div class="toc">
  <ul>
    <li><a href="#functions">Functions</a></li>
      <ul>
        <li><a href="#markdown">markdown.markdown</a></li>
      </ul>
  </ul>
</div>
<h1 id="functions">Functions</h1>
<h2 id="markdown"><code>markdown.markdown(text [, **kwargs])</code></h2>
```

Notice that the text in the Table of Contents is much cleaner and easier to read
in the context of a Table of Contents. The `data-toc-label` is not included in
the HTML header element. Also note that the ID was manually defined in the
attribute list to provide a cleaner URL when linking to the header. If the ID is
not manually defined, it is always derived from the text of the header, never
from the `data-toc-label` attribute.

Usage
-----

See [Extensions](index.md) for general extension usage. Use `toc` as the name
of the extension.

See the [Library Reference](../reference.md#extensions) for information about
configuring extensions.

The following options are provided to configure the output:

* **`marker`**:
    Text to find and replace with the Table of Contents. Defaults to `[TOC]`.

    Set to an empty string to disable searching for a marker, which may save
    some time, especially on long documents.

* **`title`**:
    Title to insert in the Table of Contents' `<div>`. Defaults to `None`.

* **`anchorlink`**:
    Set to `True` to cause all headers to link to themselves. Default is `False`.

* **`permalink`**:
    Set to `True` or a string to generate permanent links at the end of each header.
    Useful with Sphinx style sheets.

    When set to `True` the paragraph symbol (&para; or "`&para;`") is used as
    the link text. When set to a string, the provided string is used as the link
    text.

* **`baselevel`**:
    Base level for headers. Defaults to `1`.

    The `baselevel` setting allows the header levels to be automatically
    adjusted to fit within the hierarchy of your HTML templates. For example,
    suppose the Markdown text for a page should not contain any headers higher
    than level 3 (`<h3>`). The following will accomplish that:

        :::pycon
        >>>  text = '''
        ... #Some Header
        ... ## Next Level'''
        >>> from markdown.extensions.toc import TocExtension
        >>> html = markdown.markdown(text, extensions=[TocExtension(baselevel=3)])
        >>> print html
        <h3 id="some_header">Some Header</h3>
        <h4 id="next_level">Next Level</h4>'

* **`slugify`**:
    Callable to generate anchors.

    Default: `markdown.extensions.headerid.slugify`

    In order to use a different algorithm to define the id attributes, define  and
    pass in a callable which takes the following two arguments:

    * `value`: The string to slugify.
    * `separator`: The Word Separator.

    The callable must return a string appropriate for use in HTML `id` attributes.

* **`separator`**:
    Word separator. Character which replaces white space in id. Defaults to "`-`".

* **`toc_depth`**
    Define the range of section levels to include in the Table of Contents.
    A single integer (`b`) defines the bottom section level (`<h1>..<hb>`) only.
    A string consisting of two digits separated by a hyphen in between (`"2-5"`),
    define the top (`t`) and the bottom (`b`) (`<ht>..<hb>`). Defaults to `6` (bottom).

    When used with conjunction with `baselevel`, this parameter will not
    take the fitted hierarchy from `baselevel` into account. That is, if
    both `toc_depth` and `baselevel` are `3`, then only the highest level
    will be present in the table. If you set `baselevel` to `3` and
    `toc_depth` to `"2-6"`, the *first* headline will be `<h3>` and so still
    included in the Table of Contents. To exclude this first level, you
    have to set `toc_depth` to `"4-6"`.