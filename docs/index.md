---
title: Python-Markdown
hide:
  - navigation
  - path
---

Python-Markdown
===============

This is a Python implementation of John Gruber's
[Markdown](https://daringfireball.net/projects/markdown/).
It is almost completely compliant with the reference implementation,
though there are a few very minor [differences](#differences). See John's
[Syntax Documentation](https://daringfireball.net/projects/markdown/syntax)
for the syntax rules.

To get started, see the [installation instructions](install.md), the [library
reference](library.md), and the [command line interface](cli.md).

Goals
-----

The Python-Markdown project is developed with the following goals in mind:

* Maintain a Python library (with an optional CLI wrapper) suited to use in web
  server environments (never raise an exception, never write to stdout, etc.) as
  an implementation of the markdown parser that follows the
  [syntax rules][] and the behavior of the original (markdown.pl)
  implementation as reasonably as possible (see [differences](#differences) for
  a few exceptions).

* Provide an [Extension API](extensions/api.md) which makes it possible
  to change and/or extend the behavior of the parser.

!!! info "Note"

    *This is not a CommonMark implementation*; nor is it trying to be!
    Python-Markdown was developed long before the CommonMark specification was
    released and has always (mostly) followed the [syntax rules][] and behavior
    of the original reference implementation. No accommodations have been made
    to address the changes which CommonMark has suggested. It is recommended
    that you look elsewhere if you want an implementation which follows the
    CommonMark specification.

Features
--------

In addition to the basic markdown syntax, Python-Markdown supports the following
features:

* __International Input__

    Python-Markdown will accept [input](library.md#the-basics) in any language
    supported by Unicode including bi-directional text. In fact the test suite
    includes documents written in Russian and Arabic.

* __Extensions__

    Various [extensions](extensions/index.md) are provided (including
    [extra](extensions/extra.md)) to change and/or extend the base syntax.
    Additionally, a public [Extension API](extensions/api.md) is available
    to write your own extensions.

* __Output Formats__

    Python-Markdown can output documents with either HTML or XHTML style tags.
    See the [Library Reference](library.md#output_format) for details.

* __Command Line Interface__

    In addition to being a Python Library, a
    [command line script](cli.md) is available for your convenience.

Differences
-----------

While Python-Markdown strives to fully implement markdown as described in the
[syntax rules](https://daringfireball.net/projects/markdown/syntax), the rules
can be interpreted in different ways and different implementations
occasionally vary in their behavior (see the
[Babelmark FAQ](https://johnmacfarlane.net/babelmark2/faq.html#what-are-some-examples-of-interesting-divergences-between-implementations)
for some examples). Known and intentional differences found in Python-Markdown
are summarized below:

* __Middle-Word Emphasis__

    Python-Markdown defaults to ignoring middle-word emphasis (and strong
    emphasis). In other words, `some_long_filename.txt` will not become
    `some<em>long</em>filename.txt`. This can be switched off if desired. See
    the [Legacy EM Extension](extensions/legacy_em.md) for details.

* __Indentation/Tab Length__

    The [syntax rules](https://daringfireball.net/projects/markdown/syntax#list)
    clearly state that when a list item consists of multiple paragraphs, "each
    subsequent paragraph in a list item **must** be indented by either 4 spaces
    or one tab" (emphasis added). However, many implementations do not enforce
    this rule and allow less than 4 spaces of indentation. The implementers of
    Python-Markdown consider it a bug to not enforce this rule.

    This applies to any block level elements nested in a list, including
    paragraphs, sub-lists, blockquotes, code blocks, etc. They **must** always
    be indented by at least four spaces (or one tab) for each level of nesting.

    In the event that one would prefer different behavior,
    [tab_length](library.md#tab_length) can be set to whatever length is
    desired. Be warned however, as this will affect indentation for all aspects
    of the syntax (including root level code blocks). Alternatively, a
    [third party extension] may offer a solution that meets your needs.

* __Consecutive Lists__

    While the syntax rules are not clear on this, many implementations (including
    the original) do not end one list and start a second list when the list marker
    (asterisks, pluses, hyphens, and numbers) changes. For consistency,
    Python-Markdown maintains the same behavior with no plans to change in the
    foreseeable future. That said, the [Sane List Extension](extensions/sane_lists.md)
    is available to provide a less surprising behavior.

* __Raw HTML Blocks__

    The [syntax rules](https://daringfireball.net/projects/markdown/syntax#html)
    state that a block-level HTML element must be separated from surrounding
    content by blank lines, and that its start and end tags should not be
    indented. At the top level of a document, Python-Markdown is more lenient: a
    line which starts with a block-level tag, or with a comment, processing
    instruction, `CDATA` section or declaration, indented by no more than three
    spaces, starts a raw HTML block, even when it directly follows a line of a
    paragraph. The block continues, across blank lines, until its tags are closed,
    and a tag which is never closed runs to the end of the document. Markdown is
    not parsed within a raw HTML block (the
    [Markdown in HTML Extension](extensions/md_in_html.md) can change that).

    Nested in a list item, definition, blockquote, admonition or footnote, a raw
    HTML block follows the same rules once the indentation of the nesting (or the
    `>` of a blockquote) is removed, with two differences:

    1. A raw HTML block must start a block of its own: after a blank line, right
       after a list marker or the `:` of a definition, or on the first line of
       the nested content. A block-level tag on a later line of a paragraph,
       including a lazy continuation line, remains part of that paragraph. A
       fenced code block is not recognized in nested content by the
       [Fenced Code Blocks Extension](extensions/fenced_code_blocks.md), so
       without this rule, the HTML of a code example in a list item would be
       rendered rather than shown.
    2. A tag which is never closed runs to the end of the list item (or other
       nesting block) rather than to the end of the document.

* __Automatic Links__

    Automatic links recognize URL schemes followed by `://`, including schemes
    other than HTTP and FTP, such as `<ssh://example.org>` and
    `<git+ssh://example.org/repo>`. URI forms without `://`, such as
    `<urn:foo>`, continue to be treated as raw HTML.

Support
-------

You may report bugs, ask for help, and discuss various other issues on the [bug tracker][].

[third party extension]: https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions
[syntax rules]: https://daringfireball.net/projects/markdown/syntax
[bug tracker]: https://github.com/Python-Markdown/markdown/issues
