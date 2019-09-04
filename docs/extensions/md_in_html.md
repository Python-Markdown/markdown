title: Markdown in HTML Extension

# Markdown in HTML

## Summary

An extensions that parses Markdown inside of HTML tags.

## Usage

From the Python interpreter:

```pycon
>>> import markdown
>>> html = markdown.markdown(text, extensions=['md_in_html'])
```

Unlike the other Extra features, this feature is built into the markdown core and
is turned on when `markdown.extensions.extra` or `markdown.extensions.md_in_html`
is enabled.

The content of any raw HTML block element can be Markdown-formatted simply by
adding a `markdown` attribute to the opening tag. The markdown attribute will be
stripped from the output, but all other attributes will be preserved.

If the markdown value is set to `1` (recommended) or any value other than `span`
or `block`, the default behavior will be executed: `p`,`h[1-6]`,`li`,`dd`,`dt`,
`td`,`th`,`legend`, and `address` elements skip block parsing while others do not.
If the default is overridden by a value of `span`, *block parsing will be skipped*
regardless of tag. If the default is overridden by a value of `block`,
*block parsing will occur* regardless of tag.

#### Simple Example:

```md
This is *true* markdown text.

<div markdown="1">
This is *true* markdown text.
</div>
```

#### Result:

```html
<p>This is <em>true</em> markdown text.</p>
<div>
<p>This is <em>true</em> markdown text.</p>
</div>
```

### Nested Markdown Inside HTML Blocks

Nested elements are more sensitive and must be used cautiously. To avoid
unexpected results:

* Only nest elements within block mode elements.
* Follow the closing tag of inner elements with a blank line.
* Only have one level of nesting.

#### Complex Example:

```md
<div markdown="1" name="Example">

The text of the `Example` element.

<div markdown="1" name="DefaultBlockMode">
This text gets wrapped in `p` tags.
</div>

The tail of the `DefaultBlockMode` subelement.

<p markdown="1" name="DefaultSpanMode">
This text *is not* wrapped in additional `p` tags.
</p>

The tail of the `DefaultSpanMode` subelement.

<div markdown="span" name="SpanModeOverride">
This `div` block is not wrapped in paragraph tags.
Note: Subelements are not required to have tail text.
</div>

<p markdown="block" name="BlockModeOverride">
This `p` block *is* foolishly wrapped in further paragraph tags.
</p>

The tail of the `BlockModeOverride` subelement.

<div name="RawHtml">
Raw HTML blocks may also be nested.
</div>

</div>

This text is after the markdown in HTML.
```

#### Complex Result:

```html
<div name="Example">
<p>The text of the <code>Example</code> element.</p>
<div name="DefaultBlockMode">
<p>This text gets wrapped in <code>p</code> tags.</p>
</div>
<p>The tail of the <code>DefaultBlockMode</code> subelement.</p>
<p name="DefaultSpanMode">
This text <em>is not</em> wrapped in additional <code>p</code> tags.</p>
<p>The tail of the <code>DefaultSpanMode</code> subelement.</p>
<div name="SpanModeOverride">
This <code>div</code> block is not wrapped in paragraph tags.
Note: Subelements are not required to have tail text.</div>
<p name="BlockModeOverride">
<p>This <code>p</code> block <em>is</em> foolishly wrapped in further paragraph tags.</p>
</p>
<p>The tail of the <code>BlockModeOverride</code> subelement.</p>
<div name="RawHtml">
Raw HTML blocks may also be nested.
</div>

</div>
<p>This text is after the markdown in HTML.</p>
```
