title: WikiLinks Extension

# WikiLinks

## Summary

The WikiLinks extension adds support for [WikiLinks][]. Specifically, any
``[[bracketed]]`` word is converted to a link.

This extension is included in the standard Markdown library.

[WikiLinks]: https://en.wikipedia.org/wiki/Wikilink

## Syntax

A ``[[bracketed]]`` word is any combination of  upper or lower case letters,
number, dashes, underscores and spaces surrounded by double brackets. Therefore

```md
[[Bracketed]]
```

would produce the following HTML:

```html
<a href="/Bracketed/" class="wikilink">Bracketed</a>
```

Note that WikiLinks are automatically assigned `class="wikilink"` making it
easy to style WikiLinks differently from other links on a page if one so
desires. See below for ways to alter the class.

Also note that when a space is used, the space is converted to an underscore in
the link but left as-is in the label. Perhaps an example would illustrate this
best:

```md
[[Wiki Link]]
```

becomes

```html
<a href="/Wiki_Link/" class="wikilink">Wiki Link</a>
```

## Usage

See [Extensions](index.md) for general extension usage. Use `wikilinks` as the
name of the extension.

See the [Library Reference](../reference.md#extensions) for information about
configuring extensions.

The default behavior is to point each link to the document root of the current
domain and close with a trailing slash. Additionally, each link is assigned to
the HTML class `wikilink`.

The following options are provided to change the default behavior:

* **`base_url`**: String to append to beginning of URL.

    Default: `'/'`

* **`end_url`**: String to append to end of URL.

    Default: `'/'`

* **`html_class`**: CSS class. Leave blank for none.

    Default: `'wikilink'`

* **`build_url`**: Callable which formats the URL from its parts.

A trivial example:

```python
markdown.markdown(some_text, extensions=['wikilinks'])
```

### Examples

For an example, let us suppose links should always point to the sub-directory
`/wiki/` and end with `.html`

```pycon
>>> from markdown.extensions.wikilinks import WikiLinkExtension
>>> html = markdown.markdown(text,
...     extensions=[WikiLinkExtension(base_url='/wiki/', end_url='.html')]
... )
```

The above would result in the following link for `[[WikiLink]]`.

```html
<a href="/wiki/WikiLink.html" class="wikilink">WikiLink</a>
```

If you want to do more that just alter the base and/or end of the URL, you
could also pass in a callable which must accept three arguments (``label``,
``base``, and ``end``). The callable must return the URL in it's entirety.

```pycon
>>> def my_url_builder(label, base, end):
...    # do stuff
...    return url
...
>>> html = markdown.markdown(text,
...     extensions=[WikiLinkExtension(build_url=my_url_builder)],
... )
```

The option is also provided to change or remove the class attribute.

```pycon
>>> html = markdown.markdown(text,
...     extensions=[WikiLinkExtension(html_class='myclass')]
... )
```

Would cause all WikiLinks to be assigned to the class `myclass`.

```html
<a href="/WikiLink/" class="myclass">WikiLink</a>
```

## Using with Meta-Data extension

The WikiLink extension also supports the [Meta-Data](meta_data.md) extension.
Please see the documentation for that extension for specifics. The supported
meta-data keywords are:

* `wiki_base_url`
* `wiki_end_url`
* `wiki_html_class`

When used, the meta-data will override the settings provided through the
`extension_configs` interface.

This document:

```md
wiki_base_url: http://example.com/
wiki_end_url:  .html
wiki_html_class:

A [[WikiLink]] in the first paragraph.
```

would result in the following output (notice the blank `wiki_html_class`):

```html
<p>A <a href="http://example.com/WikiLink.html">WikiLink</a> in the first paragraph.</p>
```
