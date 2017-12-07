title: New Line to Break Extension

New-Line-to-Break Extension
===========================

Summary
-------

The New-Line-to-Break (`nl2b`) Extension will cause newlines to be treated as
hard breaks; like StackOverflow and [GitHub][] flavored Markdown do.

[Github]: http://github.github.com/github-flavored-markdown/

Example
-------

```pycon
>>> import markdown
>>> text = """
... Line 1
... Line 2
... """
>>> html = markdown.markdown(text, extensions=['markdown.extensions.nl2br'])
>>> print html
<p>Line 1<br />
Line 2</p>
```

Usage
-----

See [Extensions](index.md) for general extension usage, specify
`markdown.extensions.nl2br` as the name of the extension.

This extension does not accept any special configuration options.
