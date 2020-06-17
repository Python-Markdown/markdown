title: Release Notes for v3.3

# Python-Markdown 3.3 Release Notes

Python-Markdown version 3.3 supports Python versions 3.5, 3.6, 3.7, 3.8, and
PyPy3.

## Backwards-incompatible changes

...

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

* Fix issues with complex emphasis (#979).
* Limitations of `attr_list` extension are Documented (#965).
