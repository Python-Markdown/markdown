title: Release Notes for v3.3

# Python-Markdown 3.3 Release Notes

Python-Markdown version 3.3 supports Python versions 3.5, 3.6, 3.7, 3.8, and
PyPy3.

## Backwards-incompatible changes

### The prefix `language-` is now prepended to all language classes by default on code blocks.

The [HTML5 spec][spec] recommends that the class defining the language of a code block be prefixed with `language-`.
Therefore, by default, both the [fenced_code] and [codehilite] extensions now prepend the prefix when code
highlighting is disabled.

If you have previously been including the prefix manually in your fenced code blocks, then you will not want a second
instance of the prefix. Similarly, if you are using a third party syntax highlighting tool which does not recognize
the prefix, or requires a different prefix, then you will want to redefine the prefix globally using the `lang_prefix`
configuration option of either the `fenced_code` or `codehilite` extensions.

For example, to configure `fenced_code` to not apply any prefix (the previous behavior), set the option to an empty string:

```python
from markdown.extensions.fenced_code import FencedCodeExtension

markdown.markdown(src, extensions=[FencedCodeExtension(lang_prefix='')])
```

!!! note
    When code highlighting is [enabled], the output from Pygments is used unaltered. Currently, Pygments does not
    provide an option to include the language class in the output, let alone prefix it. Therefore, any language prefix
    is only applied when syntax highlighting is disabled.

## New features

The following new features have been included in the 3.3 release:

* All Pygments' options are now available for syntax highlighting (#816).
    - The [Codehilite](../extensions/code_hilite.md) extension now accepts any options
      which Pygments supports as global configuration settings on the extension.
    - [Fenced Code Blocks](../extensions/fenced_code_blocks.md) will accept any of the
      same options on individual code blocks.
    - Any of the previously supported aliases to Pygments' options continue to be
      supported at this time. However, it is recommended that the Pygments option names
      be used directly to ensure continued compatibility in the future.

* [Fenced Code Blocks](../extensions/fenced_code_blocks.md) now work with
  [Attribute Lists](../extensions/attr_list.md) when syntax highlighting is disabled.
  Any random HTML attribute can be defined and set on the `<code>` tag of fenced code
  blocks when the `attr_list` extension is enabled (#816).

## Bug fixes

The following bug fixes are included in the 3.3 release:

* Avoid a `RecursionError` from deeply nested blockquotes (#799).
* Fix issues with complex emphasis (#979).
* Limitations of `attr_list` extension are Documented (#965).
* Fix unescaping of HTML characters `<>` in CodeHilite (#990).

[spec]: https://www.w3.org/TR/html5/text-level-semantics.html#the-code-element
[fenced_code]: ../extensions/fenced_code_blocks.md
[codehilite]: ../extensions/code_hilite.md
[enabled]: ../extensions/fenced_code_blocks.md#enabling-syntax-highlighting
