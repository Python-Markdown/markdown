title: Extra Extension

# Python-Markdown Extra

## Summary

A compilation of various Python-Markdown extensions that (mostly) imitates
[PHP Markdown Extra](http://michelf.com/projects/php-markdown/extra/).

The supported extensions include:

* [Abbreviations](abbreviations.md)
* [Attribute Lists](attr_list.md)
* [Definition Lists](definition_lists.md)
* [Fenced Code Blocks](fenced_code_blocks.md)
* [Footnotes](footnotes.md)
* [Tables](tables.md)
* [Markdown in HTML](md_in_html.md)

See each individual extension for syntax documentation. Extra and all its
supported extensions are included in the standard Markdown library.

## Usage

From the Python interpreter:

```pycon
>>> import markdown
>>> html = markdown.markdown(text, extensions=['extra'])
```

There may be [additional extensions](index.md) that are distributed with
Python-Markdown that are not included here in Extra. The features
of those extensions are not part of PHP Markdown Extra, and
therefore, not part of Python-Markdown Extra. If you really would
like Extra to include additional extensions, we suggest creating
your own clone of Extra under a different name
(see the [Extension API](api.md)).
