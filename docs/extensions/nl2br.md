title: New Line to Break Extension

New-Line-to-Break Extension
===========================

Summary
-------

The New-Line-to-Break (`nl2br`) Extension will cause newlines to be treated as
hard breaks; like StackOverflow and [GitHub][] flavored Markdown do.

[Github]: https://github.github.com/github-flavored-markdown/

!!! Note

    This extension is in __maintanence mode__.  We will continue to fix bugs
    and keep it up-to-date with the core parser, but no new features or
    changes in behavior will be made. If you need a feature that this
    extension does not offer, then you have three options (1) find an
    existing [third-party extension] which meets your needs, (2) [build your
    own extension], or (3) fork this extension (pursuant to its licensing
    requirements) and maintain it as a third-party extension.

[third-party extension]: index.md#third-party-extensions
[build your own extension]: api.md

Example
-------

```pycon
>>> import markdown
>>> text = """
... Line 1
... Line 2
... """
>>> html = markdown.markdown(text, extensions=['nl2br'])
>>> print html
<p>Line 1<br />
Line 2</p>
```

Usage
-----

See [Extensions](index.md) for general extension usage. Use `nl2br` as the name
of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['nl2br'])
```
