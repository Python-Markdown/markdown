title: Release Notes for v3.1

# Python-Markdown 3.1 Release Notes

Python-Markdown version 3.1 supports Python versions 2.7, 3.5, 3.6, 3.7,
PyPy and PyPy3.

## Backwards-incompatible changes

### `markdown.version` and `markdown.version_info` deprecated

Historically, version numbers were acquired via the attributes
`markdown.version` and `markdown.version_info`. As of 3.0, a more standardized
approach is being followed and versions are acquired via the
`markdown.__version__` and `markdown.__version_info__` attributes.  As of 3.1
the legacy attributes will raise a `DeprecationWarning` if they are accessed. In
a future release the legacy attributes will be removed.

## New features

The following new features have been included in the release:

* A [Contributing Guide](../contributing.md) has been added (#732).

* A new configuration option to set the footnote separator has been added. Also,
  the `rel` and `rev` attributes have been removed from footnotes as they are
  not valid in HTML5. The `refs` and `backrefs` classes already exist and
  serve the same purpose (#723).

* A new option for `toc_depth` to set not only the bottom section level,
  but also the top section level. A string consisting of two digits
  separated by a hyphen in between (`"2-5"`), defines the top (`t`) and the
  bottom (`b`) (`<ht>..<hb>`). A single integer still defines the bottom
  section level (`<h1>..<hb>`) only. (#787).

## Bug fixes

The following bug fixes are included in the 3.1 release:

* Update CLI to support PyYAML 5.1.
* Overlapping raw HTML matches no longer leave placeholders behind (#458).
* Emphasis patterns now recognize newline characters as whitespace (#783).
* Version format had been updated to be PEP 440 compliant (#736).
* Block level elements are defined per instance, not as class attributes
  (#731).
* Double escaping of block code has been eliminated (#725).
* Problems with newlines in references has been fixed (#742).
* Escaped `#` are now handled in header syntax (#762).
