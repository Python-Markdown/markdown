title: Tables Extension

Tables
======

Summary
-------

The Tables extension adds the ability to create tables in Markdown documents.

This extension is included in the standard Markdown library.

Syntax
------

Tables are defined using the syntax established in [PHP Markdown Extra][php].

[php]: http://www.michelf.com/projects/php-markdown/extra/#table

Thus, the following text (taken from the above referenced PHP documentation):

```md
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
```

will be rendered as:

```html
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
```

!!! seealso "See Also"
    The [Attribute Lists](./attr_list.md) extension includes support for defining attributes on table cells.

Usage
-----

See [Extensions](index.md) for general extension usage. Use `tables` as the
name of the extension.

See the [Library Reference](../reference.md#extensions) for information about
configuring extensions.

The following options are provided to change the default behavior:

* **`use_align_attribute`**: Set to `True` to use `align` instead of an appropriate `style` attribute

    Default: `'False'`

* **`set_css_classes`**: Set to `True` to inject css classes for tr and td tags. 

    Default: `'False'`

CSS classes added: 
* **`tr`** : `row-#`, `row-even`, `row-odd`
* **`td`** : `col-#`, `col-even`, `col-odd`

This will allow some CSS stying, for example: 
```css
.col-1 {
    background-color:blue;
    color:white;
}
```


A trivial example:

```python
markdown.markdown(some_text, extensions=['tables'])
```

### Examples

For an example, let us suppose that alignment should be controlled by the legacy `align`
attribute.

```pycon
>>> from markdown.extensions.tables import TableExtension
>>> html = markdown.markdown(text,
...                 extensions=[TableExtension(use_align_attribute=True)]
... )
```





