title: Release Notes for v3.4

# Python-Markdown 3.4 Release Notes

Python-Markdown version 3.4 supports Python versions 3.6, 3.7, 3.8, 3.9 and PyPy3.

## Backwards-incompatible changes

This release doesn't have any backwards-incompatible changes.

## New features

The following new features have been included in the 3.4 release:

* The Codehilite extension now supports a `pygments_formatter` option that can be set to
    use a custom formatter class with Pygments.
    - If set to a string like `'html'`, we get the default formatter by that name.
    - If set to a class (or any callable), it is called with all the options to get a
      formatter instance.

## Bug fixes
