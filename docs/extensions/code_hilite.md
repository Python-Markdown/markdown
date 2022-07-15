title: CodeHilite Extension

# CodeHilite

## Summary

The CodeHilite extension adds code/syntax highlighting to standard
Python-Markdown code blocks using [Pygments][].

[Pygments]: http://pygments.org/

This extension is included in the standard Markdown library.

## Setup

### Step 1: Download and Install Pygments

You will also need to [download][dl] and install the Pygments package on your
`PYTHONPATH`. The CodeHilite extension will produce HTML output without
Pygments, but it won't highlight anything (same behavior as setting
`use_pygments` to `False`).

[dl]: http://pygments.org/download/

### Step 2: Add CSS Classes

You will need to define the appropriate CSS classes with appropriate rules.
The CSS rules either need to be defined in or linked from the header of your
HTML templates. Pygments can generate CSS rules for you. Just run the following
command from the command line:

```bash
pygmentize -S default -f html -a .codehilite > styles.css
```

If you are using a different `css_class` (default: `.codehilite`), then
set the value of the `-a` option to that class name. The CSS rules will be
written to the `styles.css` file which you can copy to your site and link from
your HTML templates.

If you would like to use a different theme, swap out `default` for the desired
theme. For a list of themes installed on your system (additional themes can be
installed via Pygments plugins), run the following command:

```bash
pygmentize -L style
```

See Pygments' excellent [documentation] for more details. If no language is
defined, Pygments will attempt to guess the language. When that fails, the code
block will not be highlighted.

!!! seealso "See Also"

    GitHub user [richeland] has provided a number of different [CSS style
    sheets][rich] which work with Pygments along with a [preview] of each theme.
    The `css_class` used is `.highlight`. Therefore, one would need to override the
    [`css_class`](#css_class) option when using richeland's CSS styles. However, the
    Python-Markdown project makes no guarantee that richeland's CSS styles will
    work with the version of Pygments you are using. To ensure complete
    compatibility, you should generate the CSS rules from your own installation
    of Pygments.

[richeland]: https://github.com/richleland
[rich]: https://github.com/richleland/pygments-css
[preview]: https://richleland.github.io/pygments-css/
[documentation]: http://pygments.org/docs/

## Syntax

The CodeHilite extension follows the same [syntax][] as regular Markdown code
blocks, with one exception. The highlighter needs to know what language to use for
the code block. There are three ways to tell the highlighter what language the
code block contains and each one has a different result.

!!! Note
    The format of the language identifier only effects the display of line numbers
    if `linenums` is set to `None` (the default). If set to `True` or `False`
    (see [Usage](#usage) below) the format of the identifier has no effect on the
    display of line numbers -- it only serves as a means to define the language
    of the code block.

[syntax]: https://daringfireball.net/projects/markdown/syntax#precode

### Shebang (with path)

If the first line of the code block contains a shebang, the language is derived
from that and line numbers are used.

```md
    #!/usr/bin/python
    # Code goes here ...
```

Will result in:

    #!/usr/bin/python
    # Code goes here ...

### Shebang (no path)

If the first line contains a shebang, but the shebang line does not contain a
path (a single `/` or even a space), then that line is removed from the code
block before processing. Line numbers are used.

```md
    #!python
    # Code goes here ...
```

Will result in:

    #!python
    # Code goes here ...

### Colons

If the first line begins with three or more colons, the text following the
colons identifies the language. The first line is removed from the code block
before processing and line numbers are not used.

```md
    :::python
    # Code goes here ...
```

Will result in:

    :::python
    # Code goes here ...

Certain lines can be selected for emphasis with the colon syntax. When
using Pygments' default CSS styles, emphasized lines have a yellow background.
This is useful to direct the reader's attention to specific lines.

```md
    :::python hl_lines="1 3"
    # This line is emphasized
    # This line isn't
    # This line is emphasized
```

Will result in:

    :::python hl_lines="1 3"
    # This line is emphasized
    # This line isn't
    # This line is emphasized

!!! Note
    `hl_lines` is named for Pygments' option meaning "highlighted lines".

### When No Language is Defined

CodeHilite is completely backwards compatible so that if a code block is
encountered that does not define a language, the block is simply wrapped in
`<pre>` tags and output.

```md
    # Code goes here ...
```

Will result in:

    # Code goes here ...

Lets see the source for that:

```html
<div class="codehilite"><pre><code># Code goes here ...
</code></pre></div>
```

!!! Note
    When no language is defined, the Pygments highlighting engine will try to guess
    the language (unless `guess_lang` is set to `False`). Upon failure, the same
    behavior will happen as described above.

## Usage

See [Extensions](index.md) for general extension usage. Use `codehilite` as the
name of the extension.

See the [Library Reference](../reference.md#extensions) for information about
configuring extensions.

The following options are provided to configure the output:

* **`linenums`**{ #linenums }:
    An alias to Pygments' `linenos` formatter option. Possible values are `True` for yes, `False` for no and `None`
    for auto. Defaults to `None`.

    Using `True` will force every code block to have line numbers, even when
    using colons (`:::`) for language identification.

    Using `False` will turn off all line numbers, even when using shebangs
    (`#!`) for language identification.

* **`guess_lang`**{ #guess_lang }:
    Automatic language detection. Defaults to `True`.

    Using `False` will prevent Pygments from guessing the language, and thus
    highlighting blocks only when you explicitly set the language.

* **`css_class`**{ #css_class }:
    An alias to Pygments `cssclass` formatter option. Set CSS class name for the wrapper `<div>` tag. Defaults to
    `codehilite`.

* **`pygments_style`**{ #pygments_style }:
    Pygments HTML Formatter Style (`ColorScheme`). Defaults to `default`.

    !!! Note
        This is useful only when `noclasses` is set to `True`, otherwise the
        CSS styles must be provided by the end user.

* **`noclasses`**{ #noclasses }:
    Use inline styles instead of CSS classes. Defaults to `False`.

* **`use_pygments`**{ #use_pygments }:
    Specifies the use of Pygments in generating the output.

    If `True` (the default) and Pygments is available, CodeHilite will use
    Pygments to analyze and format the output. Additionally, if using Pygments
    &gt;= 2.4, the output will be wrapped in `<code>` tags, whereas earlier
    versions will not.

    Otherwise, Pygments will not be used. If a language is defined for a code block, it will be assigned to the
    `<code>` tag as a class in the manner suggested by the [HTML5 spec][spec] and may be used by a JavaScript library
    in the browser to highlight the code block. See the [`lang_prefix`](#lang_prefix) option to customize the prefix.

* **`lang_prefix`**{ #lang_prefix }:
    The prefix prepended to the language class assigned to the HTML `<code>` tag. Default: `language-`.

* **`pygments_formatter`**{ #pygments_formatter }:
    This option can be used to change the Pygments formatter used for highlighting code blocks. By default, this
    is set to the string `'html'`, which means it'll use the default `HtmlFormatter` provided by Pygments.

    This can be set to a string representing any of the other default formatters, or set to a formatter class (or
    any callable).

    The code's language is always passed to the formatter as an extra option `lang_str`, with the value formatted as
    `{lang_prefix}{lang}`. If the language is unspecified, the language guessed by Pygments will be used. While
    this option has no effect to the Pygments's builtin formatters, a user can make use of the language in their custom
    formatter. See an example below.

    To see what formatters are available and how to subclass an existing formatter, please visit [Pygments
    documentation on this topic][pygments formatters].

* Any other Pygments' options:

    All other options are accepted and passed on to Pygments' lexer and formatter. Therefore,
    valid options include any options which are accepted by the [html formatter] or
    whichever [lexer] the code's language uses. Invalid options are ignored without error.

A trivial example:

```python
markdown.markdown(some_text, extensions=['codehilite'])
```

To keep the code block's language in the Pygments generated HTML output, one can provide a custom Pygments formatter
that takes the `lang_str` option. For example,

```python
from pygments.formatters import HtmlFormatter
from markdown.extensions.codehilite import CodeHiliteExtension


class CustomHtmlFormatter(HtmlFormatter):
    def __init__(self, lang_str='', **options):
        super().__init__(**options)
        # lang_str has the value {lang_prefix}{lang}
        # specified by the CodeHilite's options
        self.lang_str = lang_str

    def _wrap_code(self, source):
        yield 0, f'<code class="{self.lang_str}">'
        yield from source
        yield 0, '</code>'


some_text = '''\
    :::python
    print('hellow world')
'''

markdown.markdown(
    some_text,
    extensions=[CodeHiliteExtension(pygments_formatter=CustomHtmlFormatter)],
)
```

The formatter above will output the following HTML structure for a code block:

```html
<div class="codehilite">
    <pre>
        <code class="language-python">
        ...
        </code>
    </pre>
</div>
```

[html formatter]: https://pygments.org/docs/formatters/#HtmlFormatter
[lexer]: https://pygments.org/docs/lexers/
[spec]: https://www.w3.org/TR/html5/text-level-semantics.html#the-code-element
[pygments formatters]: https://pygments.org/docs/formatters/
