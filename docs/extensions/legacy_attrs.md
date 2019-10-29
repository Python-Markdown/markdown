title: Legacy Attributes Extension

# Legacy Attributes

## Summary

The Legacy Attributes extension restores Python-Markdown's original attribute
setting syntax. Older versions of Python Markdown (prior to 3.0) included
built-in and undocumented support for defining attributes on elements. Most
users have never made use of the syntax and it has been deprecated in favor of
[Attribute Lists](attr_list.md). This extension restores the legacy behavior for
users who have existing documents which use the syntax.

## Syntax

Attributes are defined by including the following within the element you wish to
assign the attributes to:

```md
{@key=value}
```

For example, to define a class to a paragraph:

```md
A paragraph with the attribute defined {@class=foo}anywhere within.
```

Which results in the following output:

```html
<p class="foo">A paragraph with the attribute defined anywhere within.</p>
```

The same applies for inline elements:

```md
Some *emphasized{@id=bar}* text.
```

```html
<p>Some <em id="bar">emphasized</em> text.</p>
```

You can also define attributes in images:

```md
![Alt text{@id=baz}](path/to/image.jpg)
```

```html
<p><img alt="Alt text" id="baz" src="path/to/image.jpg" /></p>
```

## Usage

See [Extensions](index.md) for general extension usage. Use `legacy_attrs` as the
name of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['legacy_attrs'])
```
