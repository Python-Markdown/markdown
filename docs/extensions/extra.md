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

To pass configuration options to the extensions included with Extra, they must be passed to Extra, with the
underlying extension identified as well. In that way Extra will have access to the options and can pass them on to
the appropriate underlying extension.

```python
config = {
    'extra': {
        'footnotes': {
            'UNIQUE_IDS': True
        },
        'fenced_code': {
            'lang_prefix': 'lang-'
        }
    },
    'toc': {
        'permalink': True
    }
}

html = markdown.markdown(text, extensions=['extra', 'toc'], extension_configs=config)
```

Note that in the above example, `footnotes` and `fenced_code` are both nested under the `extra` key as those
extensions are included with Extra. However, the `toc` extension is not included with `extra` and therefore its
configuration options are not nested under the `extra` key.

See each individual extension for a list of supported configuration options.

There are many other [extensions](index.md) which are distributed with Python-Markdown that are not included here in
Extra. The features of those extensions are not part of PHP Markdown Extra, and therefore, not part of Python-Markdown
Extra.
