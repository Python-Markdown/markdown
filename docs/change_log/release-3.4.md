title: Release Notes for v3.4

# Python-Markdown 3.4 Release Notes

Python-Markdown version 3.4 supports Python versions 3.6, 3.7, 3.8, 3.9, 3.10 and
PyPy3.

## Backwards-incompatible changes

This release doesn't have any backwards-incompatible changes.

## New features

The following new features have been included in the 3.4 release:

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

## Bug fixes
