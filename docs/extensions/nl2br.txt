NL2BR Extension
===============

A Python-Markdown extension to treat newlines as hard breaks; like
StackOverflow and [GitHub][] flavored Markdown do.

Usage:

    >>> import markdown
    >>> text = """
    ... Line 1
    ... Line 2
    ... """
    >>> html = markdown.markdown(text, extensions=['nl2br'])
    >>> print html
    <p>Line 1<br />
    Line 2</p>

[Github]: http://github.github.com/github-flavored-markdown/
