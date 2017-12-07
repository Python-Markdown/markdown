title: Release Notes for v2.0

Python-Markdown 2.0 Release Notes
=================================

We are happy to release Python-Markdown 2.0, which has been over a year in the
making. We have rewritten significant portions of the code, dramatically
extending the extension API, increased performance, and added numerous
extensions to the distribution (including an extension that mimics PHP Markdown
Extra), all while maintaining backward compatibility with the end user API in
version 1.7.

Python-Markdown supports Python versions 2.3, 2.4, 2.5, and 2.6. We have even
released a version converted to Python 3.0!

Backwards-incompatible Changes
------------------------------

While Python-Markdown has experienced numerous internal changes, those changes
should only affect extension authors. If you have not written your own
extensions, then you should not need to make any changes to your code.
However, you may want to ensure that any third party extensions you are using
are compatible with the new API.

The new extension API is fully [documented](../extensions/api.md) in the docs.
Below is a summary of the significant changes:

* The old home-grown NanoDOM has been replaced with ElementTree. Therefore all
  extensions must use ElementTree rather than the old NanoDOM.
* The various processors and patterns are now stored with OrderedDicts rather
  than lists. Any code adding processors and/or patterns into Python-Markdown
  will need to be adjusted to use the new API using OrderedDicts.
* The various types of processors available have been either combined, added,
  or removed. Ensure that your processors match the currently supported types.

What's New in Python-Markdown 2.0
---------------------------------

Thanks to the work of Artem Yunusov as part of GSoC 2008, Python-Markdown uses
ElementTree internally to build the (X)HTML document from markdown source text.
This has resolved various issues with the older home-grown NanoDOM and made
notable increases in performance.

Artem also refactored the Inline Patterns to better support nested patterns
which has resolved many inconsistencies in Python-Markdown's parsing of the
markdown syntax.

The core parser had been completely rewritten, increasing performance and, for
the first time, making it possible to override/add/change the way block level
content is parsed.

Python-Markdown now parses markdown source text more closely to the other
popular implementations (Perl, PHP, etc.) than it ever has before. With the
exception of a few minor insignificant differences, any difference should be
considered a bug, rather than a limitation of the parser.

The option to return HTML4 output as apposed to XHTML has been added. In
addition, extensions should be able to easily add additional output formats.

As part of implementing markdown in the Dr. Project project (a Trac fork), among
other things, David Wolever refactored the "extension" keyword so that it
accepts either the extension names as strings or instances of extensions. This
makes it possible to include multiple extensions in a single module.

Numerous extensions are included in the distribution by default. See
[available_extensions](../extensions/index.md) for a complete list.

See the [Change Log](index.md) for a full list of changes.

