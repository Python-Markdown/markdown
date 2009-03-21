WikiLinks
=========

Summary
-------

An extension to Python-Markdown that adds [WikiLinks][]. Specifically, any 
``[[bracketed]]`` word is converted to a link.

[WikiLinks]: http://en.wikipedia.org/wiki/Wikilink

This extension has been included in the Markdown library since 2.0.

Syntax
------

A ``[[bracketed]]`` word is any combination of  upper or lower case letters,
number, dashes, underscores and spaces surrounded by double brackets. Therefore 

    [[Bracketed]]

Would produce the following html:

    <a href="/Bracketed/" class="wikilink">Bracketed</a>

Note that wikilinks are automatically assigned `class="wikilink"` making it 
easy to style wikilinks differently from other links on a page if one so 
desires. See below for ways to alter the class.

You should also note that when a space is used, the space is converted to an
underscore in the link but left as-is in the label. Perhaps an example 
would illustrate this best:

    [[Wiki Link]]

Becomes

    <a href="/Wiki_Link/" class="wikilink">Wiki Link</a>

Usage
-----

From the Python interpreter:

    >>> text = "Some text with a [[WikiLink]]."
    >>> html = markdown.markdown(text, ['wikilink'])

The default behavior is to point each link to the document root of the current 
domain and close with a trailing slash. Additionally, each link is assigned to 
the html class `wikilink`. This may not always be desirable. Therefore, one can
customize that behavior within Python code. Three settings are provided to 
change the default behavior:

1. **base_url**: String to append to beginning of URL. 

    Default: `'/'`

2. **end_url**: String to append to end of URL.

    Default: `'/'`

3. **html_class**: CSS hook. Leave blank for none.

    Default: `'wikilink'`

4. **build_url**: Callable which formats the URL from it's parts.

For an example, let us suppose links should always point to the subdirectory 
`/wiki/` and end with `.html`

    >>> html = markdown.markdown(text, 
    ...     ['wikilink(base_url=/wiki/,end_url=.html)']
    ... )

The above would result in the following link for `[[WikiLink]]`.

    <a href="/wiki/WikiLink.html" class="wikilink">WikiLink</a>

If you want to do more that just alter the base and/or end of the URL, you 
could also pass in a callable which must accept three arguments (``label``, 
``base``, and ``end``). The callable must return the URL in it's entirety.

    def my_url_builder(label, base, end):
        # do stuff
        return url

    md = markdown.Markdown(
            extensions=['wikilinks],
            extension_configs={'wikilinks' : [('build_url', my_url_builder)]}
    )


The option is also provided to change or remove the class attribute.

    >>> html = markdown.markdown(text, 
    ...     ['wikilink(base_url=myclass)']
    ... )

Would cause all wikilinks to be assigned to the class `myclass`.

    <a href="/WikiLink/" class="myclass">WikiLink</a>

The same options can be used on the command line as well:

    python markdown.py -x wikilink(base_url=http://example.com/,end_url=.html,html_class=foo) src.txt

Some may prefer the more complex format when calling the `Markdown` class directly:

    >>> md = markdown.Markdown( 
    ...     extensions = ['wikilink'], 
    ...     extension_configs = {'wikilink': [
    ...                                 ('base_url', 'http://example.com/'), 
    ...                                 ('end_url', '.html'),
    ...                                 ('html_class', '') ]},
    ...     safe_mode = True
    ... )
    >>> html = md.convert(text)

Using with Meta-Data
--------------------

The WikiLink Extension also supports the [[Meta-Data]] Extension. Please see 
the documentation for that extension for specifics. The supported meta-data 
keywords are:

* `wiki_base_url`
* `wiki_end_url`
* `wiki_html_class`

When used, the meta-data will override the settings provided through the  
`extension_configs` interface. 

This document:

    wiki_base_url: http://example.com/
    wiki_end_url:  .html
    wiki_html_class: 

    A [[WikiLink]] in the first paragraph.

would result in the following output (notice the blank `wiki_html_class`):

    <p>A <a href="http://example.com/WikiLink.html">WikiLink</a> in the first paragraph.</p>

