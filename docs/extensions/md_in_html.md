title: Markdown in HTML Extension

# Markdown in HTML

## Summary

An extension that parses Markdown inside of HTML tags.

## Syntax

By default, Markdown ignores any content within a raw HTML block-level element. With the `md-in-html` extension
enabled, the content of a raw HTML block-level element can be parsed as Markdown by including  a `markdown` attribute
on the opening tag. The `markdown` attribute will be stripped from the output, while all other attributes will be
preserved.

The `markdown` attribute can be assigned one of three values: [`"1"`](#1), [`"block"`](#block), or [`"span"`](#span).

!!! note

    The expressions "block-level" and "span-level" as used in this document refer to an element's designation
    according to the HTML specification. Whereas the `"span"` and `"block"` values assigned to the `markdown`
    attribute refer to the Markdown parser's behavior.

### `markdown="1"` { #1 }

When the `markdown` attribute is set to `"1"`, then the parser will use the default behavior for that specific tag.

The following tags have the `block` behavior by default: `article`, `aside`, `blockquote`, `body`, `colgroup`,
`details`, `div`, `dl`, `fieldset`, `figcaption`, `figure`, `footer`, `form`, `group`, `header`, `hgroup`, `hr`,
`iframe`,  `main`, `map`, `menu`, `nav`, `noscript`, `object`, `ol`, `output`, `progress`, `section`, `table`,
`tbody`, `tfoot`, `thead`, `tr`,  `ul` and `video`.

For example, the following:

```
<div markdown="1">
This is a *Markdown* Paragraph.
</div>
```

... is rendered as:

``` html
<div>
<p>This is a <em>Markdown</em> Paragraph.</p>
</div>
```

The following tags have the `span` behavior by default: `address`, `dd`, `dt`, `h[1-6]`, `legend`, `li`, `p`, `td`,
and `th`.

For example, the following:

```
<p markdown="1">
This is not a *Markdown* Paragraph.
</p>
```

... is rendered as:

``` html
<p>
This is not a <em>Markdown</em> Paragraph.
</p>
```

### `markdown="block"` { #block }

When the `markdown` attribute is set to `"block"`, then the parser will force the `block` behavior on the contents of
the element so long as it is one of the `block` or `span` tags.

The content of a `block` element is parsed into block-level content. In other words, the text is rendered as
paragraphs, headers, lists, blockquotes, etc. Any inline syntax within those elements is processed as well.

For example, the following:

```
<section markdown="block">
# A header.

A *Markdown* paragraph.

* A list item.
* A second list item.

</section>
```

... is rendered as:

``` html
<section>
<h1>A header.</h1>
<p>A <em>Markdown</em> paragraph.</p>
<ul>
<li>A list item.</li>
<li>A second list item.</li>
</ul>
</section>
```

!!! warning

    Forcing elements to be parsed as `block` elements when they are not by default could result in invalid HTML.
    For example, one could force a `<p>` element to be nested within another `<p>` element. In most cases it is
    recommended to use the default behavior of `markdown="1"`. Explicitly setting `markdown="block"` should be
    reserved for advanced users who understand the HTML specification and how browsers parse and render HTML.

### `markdown="span"` { #span }

When the `markdown` attribute is set to `"span"`, then the parser will force the `span` behavior on the contents
of the element so long as it is one of the `block` or `span` tags.

The content of a `span` element is not parsed into block-level content. In other words, the content will not be
rendered as paragraphs, headers, etc. Only inline syntax will be rendered, such as links, strong, emphasis, etc.

For example, the following:

```
<div markdown="span">
# *Not* a header
</div>
```

... is rendered as:

``` html
<div>
# <em>Not</em> a header
</div>
```

### Ignored Elements

The following tags are always ignored, regardless of any `markdown` attribute: `canvas`, `math`, `option`, `pre`,
`script`, `style`, and `textarea`. All other raw HTML tags are treated as span-level tags and are not affected by this
extension.

### Nesting

When nesting multiple levels of raw HTML elements, a `markdown` attribute must be defined for each block-level
element. For any block-level element which does not have a `markdown` attribute, everything inside that element is
ignored, including child elements with `markdown` attributes.

For example, the following:

```
<article id="my-article" markdown="1">
# Article Title

A Markdown paragraph.

<section id="section-1" markdown="1">
## Section 1 Title

<p>Custom raw **HTML** which gets ignored.</p>

</section>

<section id="section-2" markdown="1">
## Section 2 Title

<p markdown="1">**Markdown** content.</p>

</section>

</article>
```

... is rendered as:

```html
<article id="my-article">
<h1>Article Title</h1>
<p>A Markdown paragraph.</p>
<section id="section-1">
<h2>Section 1 Title</h2>
<p>Custom raw **HTML** which gets ignored.</p>
</section>
<section id="section-2">
<h2>Section 2 Title</h2>
<p><strong>Markdown</strong> content.</p>
</section>
</article>
```

When the value of an element's `markdown` attribute is more permissive that its parent, then the parent's stricter
behavior is enforced. For example, a `block` element nested within a `span` element will be parsed using the `span`
behavior. However, if the value of an element's `markdown` attribute is the same as, or more restrictive than, its
parent, the the child element's behavior is observed. For example, a `block` element may contain either `block`
elements or `span` elements as children and each element will be parsed using the specified behavior.

### Tag Normalization

While the default behavior is for Markdown to not alter raw HTML, as this extension is parsing the content of raw HTML elements, it will do some normalization of the tags of block-level elements. For example, the following raw HTML:

```
<div markdown="1">
<p markdown="1">A Markdown paragraph with *no* closing tag.
<p>A raw paragraph with *no* closing tag.
</div>
```

... is rendered as:

``` html
<div>
<p>A Markdown paragraph with <em>no</em> closing tag.
</p>
<p>A raw paragraph with *no* closing tag.
</p>
</div>
```

Notice that the parser properly recognizes that an unclosed  `<p>` tag ends when another `<p>` tag begins or when the
parent element ends. In both cases, a closing `</p>` was added to the end of the element, regardless of whether a
`markdown` attribute was assigned to the element.

To avoid any normalization, an element must not be a descendant of any block-level element which has a `markdown`
attribute defined.

!!! warning

    The normalization behavior is only documented here so that document authors are not surprised when their carefully
    crafted raw HTML is altered by Markdown. This extension should not be relied on to normalize and generate valid
    HTML. For the best results, always include valid raw HTML (with both opening and closing tags) in your Markdown
    documents.

## Usage

From the Python interpreter:

``` pycon
>>> import markdown
>>> html = markdown.markdown(text, extensions=['md_in_html'])
```
