title: SmartyPants Extension

SmartyPants
===========

Summary
-------

The SmartyPants extension converts ASCII dashes, quotes and ellipses to
their HTML entity equivalents.

ASCII symbol | Replacements    | HTML Entities       | Substitution Keys
------------ | --------------- | ------------------- | ----------------------------------------
`'`          | &lsquo; &rsquo; | `&lsquo;` `&rsquo;` | `'left-single-quote'`, `'right-single-quote'`
`"`          | &ldquo; &rdquo; | `&ldquo;` `&rdquo;` | `'left-double-quote'`, `'right-double-quote'`
`<< >>`      | &laquo; &raquo; | `&laquo;` `&raquo;` | `'left-angle-quote'`, `'right-angle-quote'`
`...`        | &hellip;        | `&hellip;`          | `'ellipsis'`
`--`         | &ndash;         | `&ndash;`           | `'ndash'`
`---`        | &mdash;         | `&mdash;`           | `'mdash'`

Using the configuration option 'substitutions' you can overwrite the
default substitutions. Just pass a dict mapping (a subset of) the
keys to the substitution strings.

For example, one might use the following configuration to get correct quotes for
the German language:

```python
extension_configs = {
    'smarty': {
        'substitutions': {
            'left-single-quote': '&sbquo;', # sb is not a typo!
            'right-single-quote': '&lsquo;',
            'left-double-quote': '&bdquo;',
            'right-double-quote': '&ldquo;'
        }
    }
}
```

!!! note
    This extension re-implements the Python [SmartyPants]
    library by integrating it into the markdown parser.
    While this does not provide any additional features,
    it does offer a few advantages. Notably, it will not
    try to work on highlighted code blocks (using the
    [CodeHilite] Extension) like the third party library
    has been known to do.

[SmartyPants]: https://pythonhosted.org/smartypants/
[CodeHilite]: code_hilite.md

!!! Note

    This extension is in __maintanence mode__.  We will continue to fix bugs
    and keep it up-to-date with the core parser, but no new features or
    changes in behavior will be made. If you need a feature that this
    extension does not offer, then you have three options (1) find an
    existing [third-party extension] which meets your needs, (2) [build your
    own extension], or (3) fork this extension (pursuant to its licensing
    requirements) and maintain it as a third-party extension.

[third-party extension]: index.md#third-party-extensions
[build your own extension]: api.md

Usage
-----

See [Extensions](index.md) for general extension usage. Use `smarty` as the
name of the extension.

See the [Library Reference](../reference.md#extensions) for information about
configuring extensions.

The following options are provided to configure the output:

Option                | Default value | Description
------                | ------------- | -----------
`smart_dashes`        | `True`        | whether to convert dashes
`smart_quotes`        | `True`        | whether to convert straight quotes
`smart_angled_quotes` | `False`       | whether to convert angled quotes
`smart_ellipses`      | `True`        | whether to convert ellipses
`substitutions`       | `{}`          | overwrite default substitutions

A trivial example:

```python
markdown.markdown(some_text, extensions=['smarty'])
```

Further reading
---------------

SmartyPants extension is based on the original SmartyPants implementation
by John Gruber. Please read its [documentation][1] for details.

[1]: https://daringfireball.net/projects/smartypants/
