title: Release Notes for v3.2

# Python-Markdown 3.2 Release Notes

Python-Markdown version 3.2 supports Python versions 2.7, 3.5, 3.6, 3.7,
PyPy and PyPy3.

## Backwards-incompatible changes

## `em` and `strong` inline processor changes

In order to fix issue #792, `em`/`strong` inline processors were refactored. This
translated into removing many of the existing inline processors that handled this
logic:

* `em_strong`
* `strong`
* `emphasis`
* `strong2`
* `emphasis`

These processors were replaced with two new ones:

* `em_strong`
* `em_strong2`

The [`legacy_em`](../extensions/legacy_em.md) extension was also modified with new,
refactored logic and simply overrides the `em_strong2` inline processor.

## New features

The following new features have been included in the release:

* Markdown parsing in HTML has been exposed via a separate extension called
  [`md_in_html`](../extensions/md_in_html.md).

## Bug fixes

The following bug fixes are included in the 3.2 release:

* Refactor bold and italic logic in order to solve complex nesting issues (#792).
