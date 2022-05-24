title: Release Notes for v3.4

# Python-Markdown 3.4 Release Notes

Python-Markdown version 3.4 supports Python versions 3.6, 3.7, 3.8, 3.9, 3.10 and
PyPy3.

## Backwards-incompatible changes

### The `table` extension now uses a `style` attribute instead of `align` attribute for alignment.

The [HTML4 spec][spec4] specifically
deprecates the use of the `align` attribute and it does not appear at all in the
[HTML5 spec][spec5]. Therefore, by default, the [table] extension will now use the `style`
attribute (setting just the `text-align` property) in `td` and `th` blocks.

[spec4]: https://www.w3.org/TR/html4/present/graphics.html#h-15.1.2
[spec5]: https://www.w3.org/TR/html53/tabular-data.html#attributes-common-to-td-and-th-elements

The former behavior is available by setting the setting `use_align_attribute` configuration
option to `True` when adding the extension.

For example, to configure the old `align` behavior:

```python
from markdown.extensions.tables import TableExtension

markdown.markdown(src, extensions=[TableExtension(use_align_attribute=True)])
```

In addition, tests were moved to the modern test environment.

## New features

The following new features have been included in the 3.4 release:

* Use `style` attribute in tables for alignment instead of `align` for better CSS
  inter-operation. The old behavior is available by setting `use_align_attribute=True` when
  adding the extension.

* Some new configuration options have been added to the [footnotes](../extensions/footnotes.md)
  extension (#1218):

    * Small refactor of the `BACKLINK_TITLE` option; The use of `format()` instead
      of "old" `%d` formatter allows to specify text without the need to have the
      number of the footnote in it (like footnotes on Wikipedia for example).
      The modification is backward compatible so no configuration change is required.

    * Addition of a new option `SUPERSCRIPT_TEXT` that allows to specify a custom
      placeholder for the footnote itself in the text.
      Ex: `[{}]` will give <sup>[1]</sup>, `({})` will give <sup>(1)</sup>,
      or just by default, the current behavior: <sup>1</sup>.

* The [Table of Contents](../extensions/toc.md) extension now accepts a `toc_class`
  parameter which can be used to set the CSS class(es) on the `<div>` that contains the
  Table of Contents (#1224).

* The CodeHilite extension now supports a `pygments_formatter` option that can be set to
    use a custom formatter class with Pygments (#1187). Additionally, the specified
    Pygments formatter is passed an extra option `lang_str` to denote the language of
    the code block (#1258).
    - If set to a string like `'html'`, we get the default formatter by that name.
    - If set to a class (or any callable), it is called with all the options to get a
      formatter instance.

## Bug fixes

The following bug fixes are included in the 3.4 release:

* Extension entry-points are only loaded if needed (#1216).
