title: New Line to Break Extension

New-Line-to-Break Extension
===========================

Summary
-------

The New-Line-to-Break (`nl2br`) Extension will cause newlines to be treated as
hard breaks; like StackOverflow and [GitHub][] flavored Markdown do.

[Github]: https://github.github.com/github-flavored-markdown/

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
