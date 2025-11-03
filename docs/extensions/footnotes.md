title: Footnotes Extension

Footnotes
=========

Summary
-------

The Footnotes extension adds syntax for defining footnotes in Markdown
documents.

This extension is included in the standard Markdown library.

Syntax
------

Python-Markdown's Footnote syntax follows the generally accepted syntax of the
Markdown community at large and almost exactly matches [PHP Markdown Extra][]'s
implementation of footnotes. The only differences involve a few subtleties in
the output.

[PHP Markdown Extra]: http://michelf.com/projects/php-markdown/extra/#footnotes

Example:

```md
Footnotes have a name, a reference[^1], and a definition[^word].

[^1]: This is a footnote definition.
[^word]: A footnote with the name "word".
```

A **footnote name** is a string that uniquely identifies a footnote within the
document. It may contain any character which is valid for an HTML id attribute
(including spaces). Examples: `1` in `[^1]`, `word` in `[^word]`,
and `@#$%` in `[^@#$%]`.

A **footnote reference** is a link within the text body to a footnote definition.
A footnote reference contains the footnote name prefixed by a caret `^` and enclosed
in square brackets `[]`. Examples: `[^1]` and `[^@#$%]`. In the output, footnote
references are replaced by a superscript number that links to the footnote definition.

A **footnote definition** must start with the corresponding footnote reference
followed by a colon and at least one space. The reference must exactly match
the reference used in the body (including capitalization and white space).
The content of the definition would then follow either on the same line
(`[^1]: This is a footnote definition.`) or on the next line.
Footnote definitions may contain multiple lines, paragraphs, code blocks,
blockquotes and most any other markdown syntax. The additional lines must be
indented one level (four spaces or one tab).

When working with multiple blocks, it may be helpful to start the definition on a
separate line from the reference which defines the content. This way the entire block
is indented consistently and any errors are more easily discernible by the author.

```md
[^1]:
    The first paragraph of the definition.

    Paragraph two of the definition.

    > A blockquote with
    > multiple lines.

        a code block

    A final paragraph.
```

Usage
-----

See [Extensions](index.md) for general extension usage. Use `footnotes` as the
name of the extension.

See the [Library Reference](../reference.md#extensions) for information about
configuring extensions.

The following options are provided to configure the output:

* **`PLACE_MARKER`**:
    A text string used to mark the position where the footnotes are rendered.
    Defaults to `///Footnotes Go Here///`.

    If the place marker text is not found in the document, the footnote
    definitions are placed at the end of the resulting HTML document.

* **`UNIQUE_IDS`**:
    Whether to avoid collisions across multiple calls to `reset()`. Defaults to
    `False`.

* **`BACKLINK_TEXT`**:
    The text string that links from the footnote definition back to the position
    in the document. Defaults to `&#8617;`.

* **`SUPERSCRIPT_TEXT`**:
    The text string that links from the position in the document to the footnote
    definition. Defaults to `{}`, i.e. only the footnote's number.

* **`BACKLINK_TITLE`**:
    The text string for the `title` HTML attribute of the footnote definition link.
    The placeholder `{}` will be replaced by the footnote number. Defaults to
    `Jump back to footnote {} in the text`.

* **`SEPARATOR`**:
    The text string used to set the footnote separator. Defaults to `:`.

* **`USE_DEFINITION_ORDER`**:
    Order footnotes by definition order (`True`) or by document order (`False`).
    Defaults to `True`.

    The default behavior matches the behavior prior to this option being added. 
    Disabling this option (setting to `False`) is experimental and results may not
    be consistent.

A trivial example:

```python
markdown.markdown(some_text, extensions=['footnotes'])
```

Resetting Instance State
-----

Footnote definitions are stored within the  `markdown.Markdown` class instance between
multiple runs of the class.  This allows footnotes from all runs to be included in
output, with links and references that are unique, even though the class has been
called multiple times.

However, if needed, the definitions can be cleared between runs by calling `reset`.

For instance, the home page of a blog might include the content from multiple documents.
By not calling `reset`, all of the footnotes will be rendered, and they will all have
unique links and references.

On the other hand, individual blog post pages might need the content from only one
document, and should have footnotes pertaining only to that page. By calling `reset`
between runs, the footnote definitions from the first document will be cleared before
the second document is rendered.

An example of calling `reset`:

```python
md = markdown.Markdown(extensions=['footnotes'])
html1 = md.convert(text_with_footnote)
md.reset()
html2 = md.convert(text_without_footnote)
```
