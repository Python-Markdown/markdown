title: Release Notes for v3.5

# Python-Markdown 3.5 Release Notes

Python-Markdown version 3.5 supports Python versions 3.7, 3.8, 3.9, 3.10,
3.11 and PyPy3.

## New features

The following new features have been included in the 3.5 release:

* A new configuration option has been added to the
  [toc](../extensions/toc.md) extension (#1339):

    * A new boolean option `permalink_leading` controls the position of
      the permanent link anchors generated with `permalink`. Setting
      `permalink_leading` to `True` will cause the links to be inserted
      at the start of the header, before any other header content. The
      default behavior for `permalink` is to append permanent links to
      the header, placing them after all other header content.

* Updated the list of empty HTML tags (#1353). This prevents invalid HTML when using certain new tags such as `<source>`.
