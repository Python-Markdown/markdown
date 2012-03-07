title:      Sane Lists Extension
prev_title: RSS Extension
prev_url:   rss.html
next_title: Table of Contents Extension
next_url:   toc.html

Sane Lists
==========

Summary
-------

The Sane Lists Extension alters the behavior of the Markdown List syntax
to be less surprising.

This extension is included in the standard Markdown library.

Syntax
------

Sane Lists do not allow the mixing of list types. In other words, an ordered
list will not continue when an unordered list item is encountered and
vice versa. For example:

    1. Ordered item 1
    2. Ordered item 2

    * Unordered item 1
    * Unordered item 2

will result in the following output:

    <ol>
      <li>Ordered item 1</li>
      <li>Ordered item 2</li>
    </ol>

    <ul>
      <li>Unordered item 1</li>
      <li>Unordered item 2</li>
    </ul>

Whereas the default Markdown behavior would be to generate an unordered list.

Note that, unlike the default Markdown behavior, if a blank line is not
included between list items, the different list type is ignored completely. 
This corresponds to the behavior of paragraphs. For example:

    A Paragraph.
    * Not a list item.

    1. Ordered list item.
    * Not a separate list item.

With this extension the above will result in the following output:

    <p>A Paragraph.
    * Not a list item.</p>

    <ol>
      <li>Ordered list item.
      * Not a separate list item.</li>
    </ol>

In all other ways, Sane Lists should behave as normal Markdown lists.

Usage
-----

From the Python interpreter:

    >>> html = markdown.markdown(text, ['sane_lists'])

To use with other extensions, just add them to the list, like this:

    >>> html = markdown.markdown(text, ['def_list', 'sane_lists'])

The extension can also be called from the command line using Markdown's `-x` 
parameter:

    python -m markdown -x sane_lists source.txt > output.html
