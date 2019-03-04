title: Python-Markdown

Python-Markdown
===============

This is a Python implementation of John Gruber's
[Markdown](http://daringfireball.net/projects/markdown/).
It is almost completely compliant with the reference implementation,
though there are a few very minor [differences](#differences). See John's
[Syntax Documentation](http://daringfireball.net/projects/markdown/syntax)
for the syntax rules.

To get started, see the [installation instructions](install.md), the [library
reference](reference.md), and the [command line interface](cli.md).

Goals
-----

The Python-Markdown project is developed with the following goals in mind:

* Maintain a Python 2 *and* Python 3 library (with an optional CLI wrapper)
  suited to use in web server environments (never raise an exception, never
  write to stdout, etc.) as an implementation of the markdown parser that
  follows the [syntax rules](http://daringfireball.net/projects/markdown/syntax)
  and the behavior of the original (markdown.pl) implementation as reasonably as
  possible (see [differences](#differences) for a few exceptions).

* Provide an [Extension API](extensions/api.md) which makes it possible
  to change and/or extend the behavior of the parser.

Features
--------

In addition to the basic markdown syntax, Python-Markdown supports the following
features:

* __International Input__

    Python-Markdown will accept [input](reference.md#text) in any language
    supported by Unicode including bi-directional text. In fact the test suite
    includes documents written in Russian and Arabic.

* __Extensions__

    Various [extensions](extensions/index.md) are provided (including
    [extra](extensions/extra.md)) to change and/or extend the base syntax.
    Additionally, a public [Extension API](extensions/api.md) is available
    to write your own extensions.

* __Output Formats__

    Python-Markdown can output documents with either HTML or XHTML style tags.
    See the [Library Reference](reference.md#output_format) for details.

* __Command Line Interface__

    In addition to being a Python Library, a
    [command line script](cli.md) is available for your convenience.

Differences
-----------

While Python-Markdown strives to fully implement markdown as described in the
[syntax rules](http://daringfireball.net/projects/markdown/syntax), the rules
can be interpreted in different ways and different implementations
occasionally vary in their behavior (see the
[Babelmark FAQ](http://johnmacfarlane.net/babelmark2/faq.html#what-are-some-examples-of-interesting-divergences-between-implementations)
for some examples). Known and intentional differences found in Python-Markdown
are summarized below:

* __Middle-Word Emphasis__

    Python-Markdown defaults to ignoring middle-word emphasis (and strong
    emphasis). In other words, `some_long_filename.txt` will not become
    `some<em>long</em>filename.txt`. This can be switched off if desired. See
    the [Legacy EM Extension](extensions/legacy_em.md) for details.

* __Indentation/Tab Length__

    The [syntax rules](http://daringfireball.net/projects/markdown/syntax#list)
    clearly state that when a list item consists of multiple paragraphs, "each
    subsequent paragraph in a list item **must** be indented by either 4 spaces
    or one tab" (emphasis added). However, many implementations do not enforce
    this rule and allow less than 4 spaces of indentation. The implementers of
    Python-Markdown consider it a bug to not enforce this rule.

    This applies to any block level elements nested in a list, including
    paragraphs, sub-lists, blockquotes, code blocks, etc. They **must** always
    be indented by at least four spaces (or one tab) for each level of nesting.

    In the event that one would prefer different behavior,
    [tab_length](reference.md#tab_length) can be set to whatever length is
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

Support
-------

You may report bugs, ask for help, and discuss various other issues on the [bug tracker][].

[third party extension]: https://github.com/Python-Markdown/markdown/wiki/Third-Party-Extensions
[bug tracker]: http://github.com/Python-Markdown/markdown/issues
