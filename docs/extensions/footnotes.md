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
Footnotes[^1] have a label[^@#$%] and the footnote's content.

[^1]: This is a footnote content.
[^@#$%]: A footnote on the label: "@#$%".
```

A footnote label must start with a caret `^` and may contain any inline text
(including spaces) between a set of square brackets `[]`. Only the first
caret has any special meaning.

A footnote content must start with the label followed by a colon and at least
one space. The label used to define the content must exactly match the label used
in the body (including capitalization and white space). The content would then
follow the label either on the same line or on the next line. The content may
contain multiple lines, paragraphs, code blocks, blockquotes and most any other
markdown syntax. The additional lines must be indented one level (four spaces or
one tab).

When working with multiple blocks, it may be helpful to start the content on a
separate line from the label which defines the content. This way the entire block
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

* **`BACKLINK_TITLE`**:
    The text string for the `title` HTML attribute of the footnote definition link.
    `%d` will be replaced by the footnote number. Defaults to `Jump back to
    footnote %d in the text`

* **`SEPARATOR`**:
    The text string used to set the footnote separator. Defaults to `:`.
