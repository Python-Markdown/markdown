Tables
----------------

Summary
-------

The Table Extension adds the ability to create tables in Markdown documents.

This extension is included in the standard Markdown library.

Syntax
------

Tables are defined using the syntax established in [PHP Markdown Extra][php].

[php]: http://www.michelf.com/projects/php-markdown/extra/#table

Thus, the following text (taken from the above referenced PHP documentation):

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

will be rendered as:

<table>
<thead>
<tr>
<th>First Header</th>
<th>Second Header</th>
</tr>
</thead>
<tbody>
<tr>
<td>Content Cell</td>
<td>Content Cell</td>

</tr>
<tr>
<td>Content Cell</td>
<td>Content Cell</td>
</tr>
</tbody>
</table>

Usage
-----

From the Python interpreter:

    >>> html = markdown.markdown(text, ['tables'])

