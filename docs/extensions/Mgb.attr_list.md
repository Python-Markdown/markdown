title: Attribute Lists Extension

# Attribute Lists

## Summary

The Attribute Lists extension adds a syntax to define attributes on the various
HTML elements in markdown's output.

This extension is included in the standard Markdown library.

## Syntax

The basic syntax was inspired by Maruku's Attribute Lists feature (see [web archive][Maruku]).

[Maruku]: https://web.archive.org/web/20170324172643/http://maruku.rubyforge.org/proposal.html

### The List

An example attribute list might look like this:

```text
{: #someid .someclass somekey='some value' }
```

A word which starts with a hash (`#`) will set the id of an element.

A word which starts with a dot (`.`) will be added to the list of classes
assigned to an element.

A key/value pair (`somekey='some value'`) will assign that pair to the element.

Be aware that while the dot syntax will add to a class, using key/value pairs
will always override the previously defined attribute. Consider the following:

```text
{: #id1 .class1 id=id2 class="class2 class3" .class4 }
```

The above example would result in the following attributes being defined:

```text
id="id2" class="class2 class3 class4"
```

HTML includes support for some attributes to be a single term, like `checked`, for example. Therefore, the attribute
list `{: checked }` would result in `checked` if the [output format](../reference.md#output_format) is `html` or
`checked="checked"` if the output format is `xhtml`.

Curly braces can be backslash escaped to avoid being identified as an attribute list.

```text
\{ not an attribute list }
```

Opening and closing curly braces which are empty or only contain whitespace are ignored whether they are escaped or
not. Additionally, any attribute lists which are not located in the specific locations documented below are ignored.

The colon after the opening brace is optional, but is supported to maintain consistency with other implementations.
Therefore, the following is also a valid attribute list:

```text
{ #someid .someclass somekey='some value' }
```

In addition, the spaces after the opening brace and before the closing brace are optional. They are recommended as
they improve readability, but they are not required.

The Attribute List extension does not have any knowledge of which keys and/or values are valid in HTML. Therefore, it
is up to the document author to ensure that valid keys and values are used. However, the extension will escape any
characters in the key which are not valid by replacing them with an underscore. Multiple consecutive invalid
characters are reduced to a single underscore.

### Block Level

To define attributes for a block level element, the attribute list should
be defined on the last line of the block by itself.

```text
This is a paragraph.
{: #an_id .a_class }
```

The above results in the following output:

```html
<p id="an_id" class="a_class">This is a paragraph.</p>
```

An exception is headers, as they are only ever allowed on one line.

```text
A setext style header {: #setext}
=================================

### A hash style header ### {: #hash }
```

The above results in the following output:

```html
<h1 id="setext">A setext style header</h1>
<h3 id="hash">A hash style header</h3>
```

!!! seealso "See Also"
    By default, the [Fenced Code Blocks](./fenced_code_blocks.md#attributes) extension includes limited support for
    attribute lists. To get [full support](./fenced_code_blocks.md#keyvalue-pairs), both extensions must be enabled.

### Inline

To define attributes on inline elements, the attribute list should be defined
immediately after the inline element with no white space.

```text
[link](http://example.com){: class="foo bar" title="Some title!" }
```

The above results in the following output:

```html
<p><a href="http://example.com" class="foo bar" title="Some title!">link</a></p>
```

If the [tables](./tables.md) extension is enabled, attribute lists can be defined on table cells. To differentiate
attributes for an inline element from attributes for the containing cell, the attribute list must be separated from
the content by at least one space and be defined at the end of the cell content. As table cells can only ever be on
a single line, the attribute list must remain on the same line as the content of the cell.

```text
| set on td    | set on em   |
|--------------|-------------|
| *a* { .foo } | *b*{ .foo } |
```

The above example results in the following output:

```html
<table>
  <thead>
    <tr>
      <th>set on td</th>
      <th>set on em</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="foo"><em>a</em></td>
      <td><em class="foo">b</em></td>
    </tr>
  </tbody>
</table>
```

Note that in the first column, the attribute list is preceded by a space; therefore, it is assigned to the table cell
(`<td>` element). However, in the second column, the attribute list is not preceded by a space; therefore, it is
assigned to the inline element (`<em>`) which immediately preceded it.

Attribute lists may also be defined on table header cells (`<th>` elements) in the same manner.

### Limitations

There are a few types of elements which attribute lists do not work with. As a reminder, Markdown is a subset of HTML
and anything which cannot be expressed in Markdown can always be expressed with raw HTML directly.

__Code Blocks:__

:   Code blocks are unique in that they must be able to display Markdown syntax. Therefore, there is no way to
    determine if an attribute list is intended to be part of the code block or intended to define attributes on the
    wrapping element. For that reason, the extension ignores code blocks. To define attributes on code blocks, the
    [codehilite] and [fenced code blocks] extensions provide some options.

[codehilite]: code_hilite.md
[fenced code blocks]: fenced_code_blocks.md

__Nested Elements:__

:   Markdown provides mechanisms for nesting various block level elements within other elements. However, attribute
    lists only ever get applied to the immediate parent. There is no way to specify that an attribute list should be
    applied some number of levels up the document tree. For example, when including an attribute list within a
    blockquote, the attribute list is only ever applied to the paragraph the list is defined in. There is no way to
    define attributes on the `blockquote` element itself.

__Implied Elements:__

:   There are various HTML elements which are not represented in Markdown text, but only implied. For example, the
    `ul` and `ol` elements do not exist in Markdown. They are only implied by the presence of list items (`li`). There
    is no way to use an attribute list to define attributes on implied elements, including but not limited to the
    following: `ul`, `ol`, `dl`, `table`, `thead`, `tbody`, and `tr`.

## Usage

See [Extensions](index.md) for general extension usage. Use `attr_list` as the
name of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['attr_list'])
```
