title: Fenced Code Blocks Extension

# Fenced Code Blocks

## Summary

The Fenced Code Blocks extension adds a secondary way to define code blocks,
which overcomes a few limitations of the indented code blocks.

This extension is included in the standard Markdown library.

## Syntax

Fenced Code Blocks are defined using the syntax established in
[PHP Markdown Extra][php].

[php]: http://www.michelf.com/projects/php-markdown/extra/#fenced-code-blocks

Thus, the following text (taken from the above referenced PHP documentation):

```md
This is a paragraph introducing:

~~~~~~~~~~~~~~~~~~~~~
a one-line code block
~~~~~~~~~~~~~~~~~~~~~
```

Fenced code blocks can have a blank line as the first  and/or last line of a
code block and they can also come immediately after a list item without becoming
part of the list.

!!! warning

    Fenced Code Blocks are only supported at the document root level.
    Therefore, they cannot be nested inside lists or blockquotes.
    If you need to nest fenced code blocks, you may want to try the
    the third party extension [SuperFences] instead.

[SuperFences]: https://facelessuser.github.io/pymdown-extensions/extensions/superfences/

### Language

In addition to PHP Extra's syntax, you can define the language of the code
block for use by syntax highlighters etc. The language will be assigned as a
class attribute of the ``<code>`` element in the output. Therefore, you should
define the language as you would a CSS class - ``.language``. For consistency
with other markdown syntax, the language can *optionally* be wrapped in curly
brackets:

```md
~~~~{.python}
# python code
~~~~

~~~~.html
<p>HTML Document</p>
~~~~
```

The above will output:

```html
<pre><code class="python"># python code
</code></pre>

<pre><code class="html">&lt;p&gt;HTML Document&lt;/p&gt;
</code></pre>
```

[GitHub][]'s backtick (`\``) syntax is also supported in this extension:

````md
```python
# more python code
```
````

[GitHub]: https://github.github.com/github-flavored-markdown/

### Emphasized Lines

If you would like to have your fenced code blocks highlighted with the
[CodeHilite][] extension, simply enable that extension (remember that
[Pygments][] is its dependency) and the language of your fenced code blocks
will be passed in and highlighted appropriately.

Similar to the [colon][] syntax of the CodeHilite extension, fenced code blocks
can also have emphasized certain lines of code.

The lines can be specified with PHP Extra's syntax:

```md
~~~~{.python hl_lines="1 3"}
# This line is emphasized
# This line isn't
# This line is emphasized
~~~~
```

... or with GitHub's:

````md
```python hl_lines="1 3"
# This line is emphasized
# This line isn't
# This line is emphasized
```
````

[CodeHilite]: code_hilite.md
[Pygments]: http://pygments.org/
[colon]: code_hilite.md#colons

## Usage

See [Extensions](index.md) for general extension usage. Use `fenced_code` as
the name of the extension.

This extension does not accept any special configuration options.

A trivial example:

```python
markdown.markdown(some_text, extensions=['fenced_code'])
```
