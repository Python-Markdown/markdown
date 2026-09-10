---
title: Admonition Extension
---

Admonition
==========

Summary
-------

The Admonition extension adds [rST-style][rST] admonitions to Markdown documents.

This extension is included in the standard Markdown library.

[rST]: http://docutils.sourceforge.net/docs/ref/rst/directives.html#specific-admonitions

!!! info "Note"

    This extension is in __maintenance mode__.  We will continue to fix bugs
    and keep it up-to-date with the core parser, but no new features or
    changes in behavior will be made. If you need a feature that this
    extension does not offer, then you have three options (1) find an
    existing [third-party extension] which meets your needs, (2) [build your
    own extension], or (3) fork this extension (pursuant to its licensing
    requirements) and maintain it as a third-party extension.

    We recommend [PyMdown Admonition] as an actively developed alternative. 

[third-party extension]: index.md#third-party-extensions
[build your own extension]: api.md
[PyMdown Admonition]: https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/admonition/

Syntax
------

Admonitions are created using the following syntax:

``` md-render
---
extensions: [admonition]
---
!!! type "optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph.
```

`type` will be used as the CSS class name and as default title. It must be a
single word.

``` md-render
---
extensions: [admonition]
---
!!! note
    You should note that the title will be automatically capitalized.
```

Optionally, you can use custom titles.

``` md-render
---
extensions: [admonition]
---
!!! danger "Don't try this at home"
    ...
```

If you don't want a title, use a blank string `""`.

``` md-render
---
extensions: [admonition]
---
!!! important ""
    This is an admonition box without a title.
```

You can also provide additional CSS class names separated by spaces. The first
class should be the "type."

``` md-render
---
extensions: [admonition]
---
!!! danger highlight blink "Don't try this at home"
    ...
```

rST suggests the following "types": `attention`, `caution`, `danger`, `error`,
`hint`, `important`, `note`, `tip`, and `warning`; however, you're free to use
whatever you want.

Styling
-------

There is no CSS included as part of this extension. Check out the default
[Sphinx][sphinx] theme for inspiration.

[sphinx]: https://www.sphinx-doc.org/en/master/

## Usage

See [Extensions](index.md) for general extension usage. Use `admonition` as the
name of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['admonition'])
```
