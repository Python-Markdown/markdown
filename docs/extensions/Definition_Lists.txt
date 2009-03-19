Definition Lists
----------------

Summary
-------

The Definition List Extension adds the ability to create definition list in
Markdown documents.

This extension is included in the standard Markdown library.

Syntax
------

Definition lists are defined using the syntax established in 
[PHP Markdown Extra][php].

[php]: http://www.michelf.com/projects/php-markdown/extra/#def-list

Thus, the following text (taken from the above referenced PHP documentation):

    Apple
    :   Pomaceous fruit of plants of the genus Malus in 
        the family Rosaceae.

    Orange
    :   The fruit of an evergreen tree of the genus Citrus.

will be rendered like so:

    <dl>
    <dt>Apple</dt>
    <dd>Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.</dd>

    <dt>Orange</dt>
    <dd>The fruit of an evergreen tree of the genus Citrus.</dd>
    </dl>


Usage
-----

From the Python interpreter:

    >>> html = markdown.markdown(text, ['def_list'])

To use with other extensions, just add them to the list, like this:

    >>> html = markdown.markdown(text, ['def_list', 'footnotes'])

The extension can also be called from the command line using Markdown's `-x` 
parameter:

    markdown.py -x def_list source.txt > output.html
