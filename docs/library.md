---
title: Library Reference
---

# Using Markdown as a Python Library

First and foremost, Python-Markdown is intended to be a Python library module
used by various projects to convert Markdown syntax into HTML.

## The Basics

To use markdown as a module, pass a string to the [`markdown.markdown`]
[markdown.markdown] function.

```python
import markdown
html = markdown.markdown(your_text_string)
```

The string must be a *Unicode* string (the default string type in Python).

``` python
src = 'Some **Markdown** text.'
html = markdown.markdown(src)
```

Python-Markdown only ever outputs an HTML fragment. Therefore, the value of
`html` above would be:

``` html
<p>Some <strong>Markdown</strong> text.</p>
```

If you need a complete HTML document, including `<html>`, `<head>` and
`<body>` tags, then you will need to pass the output of Python-Markdown into
some other tool. For a minimal complete document,
[JustHTML](https://emilstenstrom.github.io/justhtml/) can do that with a
single line of code:

``` python
from justhtml import JustHTML

doc = JustHTML(html)
```

Assuming the value of `html` from above, the value returned by 
`doc.to_html()` would be the following string:

``` html
<html>
  <head></head>
  <body>
    <p>Some <strong>Markdown</strong> text.</p>
  </body>
</html>
```

For more sophisticated output, you may need to explore the use of a templating
system or a static site generator.

!!! tip "Important"

    Python-Markdown expects a **Unicode** string as input (some simple ASCII
    binary strings *may* work only by coincidence) and returns output as a
    Unicode string. Do not pass binary strings to it! If your input is
    encoded, (e.g. as UTF-8), it is your responsibility to decode it.  For
    example:

    ``` python
    binary_string = b'Some **Markdown** text.'
    html = markdown.markdown(binary_string.decode('utf-8'))
    ```

    If you need binary output, you will need to encode the output yourself.

    ``` python
    binary_html = html.encode('utf-8')
    ```

!!! warning

    The Python-Markdown library does ***not*** sanitize its HTML output. If
    you are processing Markdown input from an untrusted source, it is your
    responsibility to ensure that it is properly sanitized. For more
    information see [Sanitizing HTML Output].

[Sanitizing HTML Output]: sanitization.md

### Extensions

The primary way to modify Python-Markdown's behavior is through extensions. 
Python-Markdown provides an [API](extensions/api.md) for third parties to
write extensions to the parser adding their own additions or changes to the
syntax. A few commonly used extensions are provided with the `markdown`
library. See the [extension documentation](extensions/index.md) for a
list of available extensions.

To enable extensions, they should be passed to the `extensions` keyword.

``` python
markdown.markdown(src, extensions=[MyExtClass()])
```

The list of extensions may contain instances of extensions and/or strings
of extension names.

``` python
extensions=[MyExtClass(), 'myext', 'path.to.my.ext:MyExtClass']
```

!!! tip
    The preferred method is to pass in an instance of an extension. Strings
    should only be used when it is impossible to import the Extension Class
    directly (from the command line or in a template).

When passing in extension instances, each class instance must be a subclass
of `markdown.extensions.Extension` and any configuration options should be
defined when initiating the class instance rather than using the
[`extension_configs`](#extension_configs) keyword. For example:

``` python
from markdown.extensions import Extension
class MyExtClass(Extension):
    # define your extension here...

markdown.markdown(text, extensions=[MyExtClass(option='value')])
```

If an extension name is provided as a string, the string must either be the
registered entry point of any installed extension or the importable path
using Python's dot notation.

See the documentation specific to an extension for the string name assigned
to an extension as an entry point.  Simply include the defined name as
a string in the list of extensions. For example, if an extension has the
name `myext` assigned to it and the extension is properly installed, then
do the following:

``` python
markdown.markdown(text, extensions=['myext'])
```

If an extension does not have a registered entry point, Python's dot
notation may be used instead. The extension must be installed as a
Python module on your PYTHONPATH. Generally, a class should be specified in
the name. The class must be at the end of the name and be separated by a
colon from the module.

Therefore, if you were to import the class like this:

``` python
from path.to.module import MyExtClass
```

Then load the extension as follows:

``` python
markdown.markdown(text, extensions=['path.to.module:MyExtClass'])
```

If only one extension is defined within a module and the module includes a
`makeExtension` function which returns an instance of the extension, then
the class name is not necessary. For example, in that case one could do
`extensions=['path.to.module']`. Check the documentation for a specific
extension to determine if it supports this feature.

When loading an extension by name (as a string), you can only pass in
configuration settings to the extension by using the
[`extension_configs`](#extension_configs) keyword.

!!! seealso "See Also"
    See the documentation of the [Extension API](extensions/api.md) for
    assistance in creating extensions.

### Extension Configuration Options { #extension_configs }

The keyword `extension_configs` accepts a dictionary of configuration settings
for extensions.

Any configuration settings will only be passed to extensions loaded by name
(as a string). When loading extensions as class instances, pass the
configuration settings directly to the class when initializing it.

!!! tip
    The preferred method is to pass in an instance of an extension, which
    does not require use of the `extension_configs` keyword at all.
    See the [extensions](#extensions) keyword for details.

The dictionary of configuration settings must be in the following format:

``` python
extension_configs = {
    'extension_name_1': {
        'option_1': 'value_1',
        'option_2': 'value_2'
    },
    'extension_name_2': {
        'option_1': 'value_1'
    }
}
```

When specifying the extension name, be sure to use the exact same
string as is used in the [extensions](#extensions) keyword to load the
extension. Otherwise, the configuration settings will not be applied to
the extension. In other words, you cannot use the entry point in on
place and Python dot notation in the other. While both may be valid for
a given extension, they will not be recognized as being the same
extension by Markdown.

See the documentation specific to the extension you are using for help in
specifying configuration settings for that extension.

### Output Format {: #output_format }

The `output_format` keyword accepts a string which specfies the format of the
output.

``` python
markdown.markdown(src, output_format='html')
```

The supported formats are `xhtml` (the default) and `html`.

The only notable difference between the options are how self-closing tags are
formatted in the output (for example `<br />` for `xhtml` and `<br>` for
`html`).

### Tab Length { #tab_length }

The `tab_length` keyword sets the length of tabs in the source as an integer.
The default value is `4`.

``` python
markdown.markdown(src, tab_length=2)
```

## Working with Files

The Python-Markdown library provides the function
[`markdown.markdownFromFile`][markdown.markdownFromFile] which reads Markdown
directly from a file on your filestyem and writes directly to a file.

!!! warning

    The Python-Markdown library does ***not*** sanitize its HTML output. As
    `markdown.markdownFromFile` writes directly to the file system, there is
    no easy way to sanitize the output from Python code. Therefore, it is
    recommended that the `markdown.markdownFromFile` function not be used on
    input from an untrusted source. For more information see [Sanitizing HTML
    Output].

With a few exceptions, `markdown.markdownFromFile` accepts the same options as
`markdown.markdown`. It does **not** accept a `text` (or Unicode) string.
Instead, it accepts the keywords `input`, `output` and `encoding`.

``` python
markdown.markdownFromFile(
    input='source_file.md',
    output='output_file.html',
    encoding='utf-8'
)
```

The `input` and `output` keywords may be set to one of three options:

* a string which contains a path to a readable or writable file on the file system,
* a readable or writable file-like object,
* or `None` (default) which will read from `stdin` or write to `stdout`.

The `encoding` keyword defaults to `"utf-8"`. The same encoding will always be
used for input and output. The `xmlcharrefreplace` error handler is used when
encoding the output.

!!! warning

    As Python-Markdown only outputs an (X)HTML fragment, the `output` file
    will not be useful by itself and will likely need additional
    modifications. Therefore, this function has little useful value for
    anything other than passing output to `stdout` for use on the command
    line.

!!! tip
    This is the only place that decoding and encoding of Unicode
    takes place in Python-Markdown. If this rather naive solution does not
    meet your specific needs, it is suggested that you write your own code
    to handle your encoding/decoding needs.

    ``` python
    with open("some_file.txt", "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)

    # Pass your output through a template system here to get a complete HTML document.

    with open("some_file.html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(html)
    ```

## The `markdown.Markdown` Class

The above-referenced functions (`markdown.markdown` and
`markdown.markdownFromFile`) wrap the [`markdown.Markdown`][markdown.Markdown]
class and generally provide all of the functionality that a user may need.
However, in a few rare cases, a user may benefit from direct access to the
class itself.

The same options are available when initializing the `markdown.Markdown` class
as on the `markdown.markdown` function, except that the class does
**not** accept a source text string on initialization. Rather, the source text
string must be passed to one of two instance methods
([`convert`][markdown.Markdown.convert] or [`convertFile`][markdown.Markdown.convertFile]).

``` Python
md = markdown.Markdown()
html = md.convert(source_text)
```

The `source` text must meet the same requirements as the `text` argument of
the `markdown.markdown` function.

!!! warning

    Instances of the `markdown.Markdown` class are only thread safe within
    the thread they were created in. A single instance should not be accessed
    from multiple threads.

!!! warning

    The Python-Markdown library does ***not*** sanitize its HTML output. If
    you are processing Markdown input from an untrusted source, it is your
    responsibility to ensure that it is properly sanitized. For more
    information see [Sanitizing HTML Output].


You may want to use the class directly if you want to process multiple strings
without creating a new instance of the class for each string.

```python
md = markdown.Markdown()
html1 = md.convert(text1)
html2 = md.convert(text2)
```

Depending on which options and/or extensions are being used, the parser may
need its state reset between each call to `convert`. The 
[`reset`][markdown.Markdown.reset] method is available for this purpose.

```python
html1 = md.convert(text1)
md.reset()
html2 = md.convert(text2)
```

To make this easier, you can also chain calls to `reset` together:

```python
html3 = md.reset().convert(text3)
```

On some occasions, you may not want to reset the state. For example, the home
page of a blog often includes multiple posts on one page. To ensure that
there are no conflicts among the various references generated by the `toc`
extension, you can pass each post through the same class, which will ensure
all references are unique.

``` python
posts = []
md = markdown.Markdown(extensions=['toc'])
for post in blog_posts:
    posts.append(md.convert(post))
```

The [`convertFile`][markdown.Markdown.convertFile] method accepts the same
arguments as the `markdown.markdownFromFile` function. There is little
benefit in accessing this method directly and it remains for backward
compatability puposes only.
