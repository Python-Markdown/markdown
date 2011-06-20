Attribute Lists
===============

Summary
-------

An extension to Python-Markdown that adds a syntax to define attributes on
the various HTML elements in markdown's output.

This extension is included in the standard Markdown library.

Syntax
------

The basic syntax was inspired by [Maruku][]'s Attribute List feature.

[Maruku]: http://maruku.rubyforge.org/proposal.html#attribute_lists

### The List ###

An example attribute list might look like this:

    {: #someid .someclass somekey='some values' }

A word which starts with a hash `#` will set the id of an element.

A word which starts with a dot `.` will add to the list of classes assigned to
an element.

A key/value pair will assign that pair to the element.

Be aware that while the dot syntax will add to a class, using key/value pairs
will always override the previously defined attribute. Consider the following:

    {: #id1 .class1 id=id2 class="class2 class3" .class4 }

The above example would result in the following attributes being defined:

    id="id2 class="class2 class3 class4"

### Block Level ###

To define attributes for a block level element, the attribute list should
be defined on the last line of the block by itself.

    This is a paragraph.
    {: #an_id .a_class }

The above results in the following output:

    <p id="an_id" class="a_class">This is a paragraph.</p>

The one exception is headers, as they are only ever allowed on one line.

    A setext style header {: #setext}
    =================================

    ### A hash style header ### {: #hash }

The above results in the following output:

    <h1 id="setext">A setext style header</h1>
    <h3 id="hash">A hash style header</h3>

### Inline ###

To define attributes on inline elements, the attribute list should be defined 
immediately after the inline element with no whitespace.

    [link](http://example.com){: class="foo bar" title="Some title! }

The above results in the following output:

    <p><a href="http://example.com" class="foo bar" title="Some title!">link</a></p>
