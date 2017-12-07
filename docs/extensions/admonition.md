title: Admonition Extension

Admonition
==========

Summary
-------

The Admonition extension adds [rST-style][rST] admonitions to Markdown documents.

This extension is included in the standard Markdown library.

[rST]: http://docutils.sourceforge.net/docs/ref/rst/directives.html#specific-admonitions

Syntax
------

Admonitions are created using the following syntax:

```md
!!! type "optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph.
```

`type` will be used as the CSS class name and as default title. It must be a
single word. So, for instance:

```md
!!! note
    You should note that the title will be automatically capitalized.
```

will render:

```html
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>You should note that the title will be automatically capitalized.</p>
</div>
```

Optionally, you can use custom titles. For instance:

```md
!!! danger "Don't try this at home"
    ...
```

will render:

```html
<div class="admonition danger">
<p class="admonition-title">Don't try this at home</p>
<p>...</p>
</div>
```

If you don't want a title, use a blank string `""`:

```md
!!! important ""
    This is a admonition box without a title.
```

results in:

```html
<div class="admonition important">
<p>This is a admonition box without a title.</p>
</div>
```

rST suggests the following `types`, but you're free to use whatever you want:
    attention, caution, danger, error, hint, important, note, tip, warning.

Styling
-------

There is no CSS included as part of this extension. Look up the default
[Sphinx][sphinx] theme if you need inspiration.

[sphinx]: http://sphinx.pocoo.org/
