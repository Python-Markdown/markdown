title: Badge Extension

Badge
==========

Summary
-------

The Badge extension adds support for badges to Markdown documents.

Syntax
------

Badges are created using the following syntax:

```md
{{ type "optional explicit title within double quotes" }}
```

`type` will be used as the CSS class name and as default title. It must be a
single word. So, for instance:

```md
{{ note "Alpha" }}
```

will render:

```html
<span class="badge note">
<span class="badge-title">Alpha</span>
</span>
```

Optionally, you can use custom titles. For instance:

```md
{{ danger "Warning" }}
```

will render:

```html
<span class="badge danger">
<span class="badge-title">Warning</span>
</span>
```

If you don't want a title, use a blank string `""`:

```md
This is a badge without a title: {{ important "" }}
```

results in:

```html
<span class="badge danger"></span>
```

You can also provide additional CSS class names separated by spaces. The first
class should be the "type." For example:

```md
{{ danger highlight blink "Don't try this at home" }}
```

will render:

```html
<span class="badge danger highlight blink">
<span class="badge-title">Don't try this at home</span>
</span>
```

Styling
-------

There is no CSS included as part of this extension. Check out the default
[Sphinx][sphinx] theme for inspiration.

[sphinx]: https://www.sphinx-doc.org/en/master/

## Usage

See [Extensions](index.md) for general extension usage. Use `badge` as the
name of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['badge'])
```
