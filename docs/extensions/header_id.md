HeaderId
========

Summary
-------

An extension to Python-Markdown that automatically generates 'id' attributes
for HTML header elements (h1-h6) in markdown's output.

This extension is included in the standard Markdown library.

Syntax
------

By default, all headers will automatically have unique "id" attributes 
generated based upon the text of the header (See below to turn this off). 
Note this example in which all three headers would have the same "id":

    #Header
    #Header
    #Header

Results in:

    <h1 id="header">Header</h1>
    <h1 id="header_1">Header</h1>
    <h1 id="header_2">Header</h1>

Configuring the Output
----------------------

The HeaderId extension has four configuration settings:

* **level**: Base level for headers.

    Default: `1`

    The `level` setting allows you to automatically adjust the header levels to
    fit within the hierarchy of your html templates. For example, suppose the 
    markdown text for a page should not contain any headers higher than level 3
    (`<h3>`). The following will accomplish that:

        >>>  text = '''
        ... #Some Header
        ... ## Next Level'''
        >>> html = markdown.markdown(text, extensions=['headerid(level=3)'])
        >>> print html
        <h3 id="some_header">Some Header</h3>
        <h4 id="next_level">Next Level</h4>'

* **forceid**: Force all headers to have an id.

    Default: `True`

    The `forceid` setting turns on or off the automatically generated ids for 
    headers that do not have one explicitly defined (using the attr_list 
    extension).

        >>> text = '''
        ... # Some Header
        ... # Header with ID # { #foo }'''
        >>> html = markdown.markdown(text, 
                        extensions=['attr_list', 'headerid(forceid=False)'])
        >>> print html
        <h1>Some Header</h1>
        <h1 id="foo">Header with ID</h1>

* **separator**: Word separator. Character which replaces whitespace in id.

    Default: `-`

* **slugify**: Callable to generate anchors.

    Default: `markdown.extensions.headerid.slugify`

    If you would like to use a different algorithm to define the ids, you can
    pass in a callable which takes two arguments:

    * `value`: The string to slugify.
    * `separator`: The Word Separator.

Using with Meta-Data
--------------------

The HeaderId Extension also supports the [Meta-Data](meta_data.html) Extension.
Please see the documentation for that extension for specifics. The supported 
meta-data keywords are:

* `header_level`
* `header_forceid`

When used, the meta-data will override the settings provided through the  
`extension_configs` interface. 

This document:

    header_level: 2
    header_forceid: Off

    # A Header


Will result in the following output:

    <h2>A Header</h2>
