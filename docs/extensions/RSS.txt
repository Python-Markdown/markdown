RSS
===

Summary
-------

An extension to Python-Markdown that outputs a markdown document as RSS. This 
extension has been included with Python-Markdown since 1.7 and should be 
available to anyone who has a typical install of Python-Markdown.

Usage
-----

From the Python interpreter:

    >>> import markdown
    >>> text = "Some markdown document."
    >>> rss = markdown.markdown(text, ['rss'])

Configuring the Output
----------------------

An RSS document includes some data about the document (URI, author, title) that
will likely need to be configured for your needs. Therefore, three configuration
options are available:

* **URL** : The Main URL for the document.
* **CREATOR** : The Feed creator's name.
* **TITLE** : The title for the feed.

An example:

    >>> rss = markdown.markdown(text, extensions = \
    ...        ['rss(URL=http://example.com,CREATOR=JOHN DOE,TITLE=My Document)']
    ... )
