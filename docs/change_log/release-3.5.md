title: Release Notes for v3.5

# Python-Markdown 3.5 Release Notes

Python-Markdown version 3.5 supports Python versions 3.7, 3.8, 3.9, 3.10,
3.11 and PyPy3.

## New features

The following new features have been included in the 3.5 release:

* A new configuration option has been added to the
  [toc](../extensions/toc.md) extension (#1364):

    * A new boolean option `nested_anchor_ids` makes it possible to generate
      header anchor IDs as a concatenation of all of the parent header anchor
      IDs which precede it hierarchically. This feature can be useful when
      linking to specific subsections of the resultant document, as the anchor
      ID will more be more specific to the header and the headers above it.
