title: Fenced Code Blocks Extension

# Fenced Code Blocks

## Summary

The Fenced Code Blocks extension adds a secondary way to define code blocks, which overcomes a few limitations of
indented code blocks.

This extension is included in the standard Markdown library.

## Syntax

Fenced Code Blocks are defined using the syntax originally established in [PHP Markdown Extra][php] and popularized by
[GitHub Flavored Markdown][gfm].

Fenced code blocks begin with three or more backticks (` ``` `) or tildes (`~~~`) on a line by themselves and end with
a matching set of backticks or tildes on a line by themselves. The closing set must contain the same number and type
of characters as the opening set. It is recommended that a blank line be placed before and after the code block.

````md
A paragraph before the code block.

```
a one-line code block
```

A paragraph after the code block.
````

While backticks seem to be more popular among users, tildes may be used as well.

````md
~~~
a one-line code block
~~~
````

To include a set of backticks (or tildes) within a code block, use a different number of backticks for the
deliminators.

`````md
````
```
````
`````

Fenced code blocks can have a blank line as the first and/or last line of the code block and those lines will be
preserved.

````md
```

a three-line code block

```
````

Unlike indented code blocks, a fenced code block can immediately follow a list item without becoming
part of the list.

````md
* A list item.

```
not part of the list
```
````

!!! warning

    Fenced Code Blocks are only supported at the document root level. Therefore, they cannot be nested inside lists or
    blockquotes. If you need to nest fenced code blocks, you may want to try the third party extension [SuperFences]
    instead.

### Attributes

Various attributes may be defined on a per-code-block basis by defining them immediately following the opening
deliminator. The attributes should be wrapped in curly braces `{}` and be on the same line as the deliminator. It is
generally best to separate the attribute list from the deliminator with a space. Attributes within the list must be
separated by a space.

````md
``` { attributes go here }
a code block with attributes
```
````

How those attributes will affect the output will depend on various factors as described below.

#### Language

The language of the code within a code block can be specified for use by syntax highlighters, etc. The language should
be prefixed with a dot and not contain any whitespace (`.language-name`).

````md
``` { .html }
<p>HTML Document</p>
```
````

So long as the language is the only option specified, the curly brackets and/or the dot may be excluded:

````md
``` html
<p>HTML Document</p>
```
````

Either of the above examples will output the following HTML:

```html
<pre><code class="language-html">&lt;p&gt;HTML Document&lt;/p&gt;
</code></pre>
```

Note that the language name has been prefixed with `language-` and it has been assigned to the `class` attribute on
the `<code>` tag, which is the format suggested by the [HTML 5 Specification][html5] (see the second "example" in the
Specification). While `language` is the default prefix, the prefix may be overridden using the
[`lang_prefix`](#lang_prefix) configuration option.

#### Classes

In addition to the language, additional classes may be defined by prefixing them with a dot, just like the language.

````md
``` { .html .foo .bar }
<p>HTML Document</p>
```
````

When defining multiple classes, only the first class will be used as the "language" for the code block. All others are
assigned to the `<pre>` tag unaltered. Additionally, the curly braces and dot are required for all classes, including
the language class if more than one class is defined.

The above example will output the following HTML:

```html
<pre class="foo bar"><code class="language-html">&lt;p&gt;HTML Document&lt;/p&gt;
</code></pre>
```

#### ID

An `id` can be defined for a code block, which would allow a link to point directly to the code block using a URL
hash. IDs must be prefixed with a hash character (`#`) and only contain characters permitted in HTML `id` attributes.

````md
``` { #example }
A linkable code block
```
````

The `id` attribute is assigned to the `<pre>` tag of the output. The above example will output the following HTML:

```html
<pre id="example"><code>A linkable code block
</code></pre>
```

From elsewhere within the same document, one could link to the code block with `[link](#example)`.

IDs may be defined along with the language, other classes, or any other supported attributes. The order of items does
not matter.

````md
``` { #example .lang .foo .bar }
A linkable code block
```
````

#### Key/Value Pairs

If the `fenced_code` and [`attr_list`][attr_list] extensions are both enabled, then key/value pairs can be defined in
the attribute list. So long as code highlighting is not enabled (see below), the key/value pairs will be assigned as
attributes on the `<code>` tag in the output. Key/value pairs must be defined using the syntax documented for the
`attr_list` extension (for example, values with whitespace must be wrapped in quotes).

````md
``` { .lang #example style="color: #333; background: #f8f8f8;" }
A code block with inline styles. Fancy!
```
````

The above example will output the following HTML:

```html
<pre id="example"><code class="language-lang"  style="color: #333; background: #f8f8f8;">A code block with inline styles. Fancy!
</code></pre>
```

If the `attr_list` extension is not enabled, then the key/value pairs will be ignored.

#### Syntax Highlighting

If the `fenced_code` extension and syntax highlighting are both enabled, then the [`codehilite`][codehilite]
extension will be used for syntax highlighting the contents of the code block. The language defined in the attribute
list will be passed to `codehilite` to ensure that the correct language is used. If no language is specified and
language guessing is not disabled for the `codehilite` extension, then the language will be guessed.

The `codehilite` extension uses the [Pygments] engine to do syntax highlighting. Any valid Pygments options can be
defined as key/value pairs in the attribute list and will be passed on to Pygments.

````md
``` { .lang linenos=true linenostart=42 hl_lines="43-44 50" title="An Example Code Block" }`
A truncated code block...
```
````

Valid options include any option accepted by Pygments' [`HTMLFormatter`][HTMLFormatter] except for the `full` option,
as well as any options accepted by the relevant [lexer][lexer] (each language has its own lexer). While most lexers
don't have options that are all that useful in this context, there are a few important exceptions. For example, the
[PHP lexer's] `startinline` option eliminates the need to start each code fragment with `<?php`.

!!! note

    The `fenced_code` extension does not alter the output provided by Pygments. Therefore, only options which Pygments
    provides can be utilized. As Pygments does not currently provide a way to define an ID, any ID defined in an
    attribute list will be ignored when syntax highlighting is enabled. Additionally, any key/value pairs which are not Pygments options will be ignored, regardless of whether the `attr_list` extension is enabled.

##### Enabling Syntax Highlighting

To enable syntax highlighting, the [`codehilite`][codehilite] extension must be enabled and the `codehilite`
extension's `use_pygments` option must be set to `True` (the default).

Alternatively, so long as the `codehilite` extension is enabled, you can override a global `use_pygments=False`
option for an individual code block by including `use_pygments=true` in the attribute list. While the `use_pygments`
key/value pair will not be included in the output, all other attributes will behave as they would if syntax
highlighting was enabled only for that code block.

Conversely, to disable syntax highlighting on an individual code block, include `use_pygments=false` in the attribute
list. While the `use_pygments` key/value pair will not be included in the output, all other attributes will behave as
they would if syntax highlighting was disabled for that code block regardless of any global setting.

!!! seealso "See Also"

    You will need to properly install and setup Pygments for syntax highlighting to work. See the `codehilite`
    extension's [documentation][setup] for details.

## Usage

See [Extensions] for general extension usage. Use `fenced_code` as the name of the extension.

See the [Library Reference] for information about configuring extensions.

The following option is provided to configure the output:

* **`lang_prefix`**{#lang_prefix}:
    The prefix prepended to the language class assigned to the HTML `<code>` tag. Default: `language-`.

A trivial example:

```python
markdown.markdown(some_text, extensions=['fenced_code'])
```

[php]: http://www.michelf.com/projects/php-markdown/extra/#fenced-code-blocks
[gfm]: https://help.github.com/en/github/writing-on-github/creating-and-highlighting-code-blocks
[SuperFences]: https://facelessuser.github.io/pymdown-extensions/extensions/superfences/
[html5]: https://html.spec.whatwg.org/#the-code-element
[attr_list]: ./attr_list.md
[codehilite]: ./code_hilite.md
[Pygments]: http://pygments.org/
[HTMLFormatter]: https://pygments.org/docs/formatters/#HtmlFormatter
[lexer]: https://pygments.org/docs/lexers/
[PHP lexer's]: https://pygments.org/docs/lexers/#lexers-for-php-and-related-languages
[setup]: ./code_hilite.md#setup
[Extensions]: ./index.md
[Library Reference]: ../reference.md#extensions
