title: Library Reference

# Using Markdown as a Python Library

First and foremost, Python-Markdown is intended to be a python library module
used by various projects to convert Markdown syntax into HTML.

## The Basics

To use markdown as a module:

```python
import markdown
html = markdown.markdown(your_text_string)
```

## The Details

Python-Markdown provides two public functions ([`markdown.markdown`](#markdown)
and [`markdown.markdownFromFile`](#markdownFromFile)) both of which wrap the
public class [`markdown.Markdown`](#Markdown). If you're processing one
document at a time, these functions will serve your needs. However, if you need
to process multiple documents, it may be advantageous to create a single
instance of the `markdown.Markdown` class and pass multiple documents through
it. If you do use a single instance though, make sure to call the `reset`
method appropriately ([see below](#convert)).

### markdown.markdown(text [, **kwargs]) {: #markdown }

The following options are available on the `markdown.markdown` function:

__text__{: #text }

:   The source Unicode string. (required)

    !!! note "Important"
        Python-Markdown expects **Unicode** as input (although
        some simple ASCII strings *may* work) and returns output as Unicode.
        Do not pass encoded strings to it! If your input is encoded, (e.g. as
        UTF-8), it is your responsibility to decode it.  For example:

            :::python
            input_file = codecs.open("some_file.txt", mode="r", encoding="utf-8")
            text = input_file.read()
            html = markdown.markdown(text)

        If you want to write the output to disk, you *must* encode it yourself:

            :::python
            output_file = codecs.open("some_file.html", "w",
                                      encoding="utf-8",
                                      errors="xmlcharrefreplace"
            )
            output_file.write(html)

__extensions__{: #extensions }

:   A list of extensions.

    Python-Markdown provides an [API](extensions/api.md) for third parties to
    write extensions to the parser adding their own additions or changes to the
    syntax. A few commonly used extensions are shipped with the markdown
    library. See the [extension documentation](extensions/index.md) for a
    list of available extensions.

    The list of extensions may contain instances of extensions and/or strings
    of extension names.

        :::python
        extensions=[MyExtension(), 'path.to.my.ext']

    !!! note
        The preferred method is to pass in an instance of an extension. Strings
        should only be used when it is impossible to import the Extension Class
        directly (from the command line or in a template).

    When passing in extension instances, each class instance must be a subclass
    of `markdown.extensions.Extension` and any configuration options should be
    defined when initiating the class instance rather than using the
    [`extension_configs`](#extension_configs) keyword. For example:

        :::python
        from markdown.extensions import Extension
        class MyExtension(Extension):
            # define your extension here...

        markdown.markdown(text, extensions=[MyExtension(option='value')])

    If an extension name is provided as a string, the extension must be
    importable as a python module on your PYTHONPATH. Python's dot notation is
    required. Therefore, to import the 'extra' extension, one would do
    `extensions=['markdown.extensions.extra']`

    Additionally, a Class may be specified in the name. The class must be at the
    end of the name and be separated by a colon from the module.

    Therefore, if you were to import the class like this:

        :::python
        from path.to.module import SomeExtensionClass

    Then the named extension would comprise this string:

        :::python
        "path.to.module:SomeExtensionClass"

    !!! note
        You should only need to specify the class name if more than one extension
        is defined within the same module. The extensions that come with
        Python-Markdown do *not* need to have the class name specified. However,
        doing so will not effect the behavior of the parser.

    When loading an extension by name (as a string), you may pass in
    configuration settings to the extension using the
    [`extension_configs`](#extension_configs) keyword.

    !!! seealso "See Also"
        See the documentation of the [Extension API](extensions/api.md) for
        assistance in creating extensions.

__extension_configs__{: #extension_configs }

:   A dictionary of configuration settings for extensions.

    Any configuration settings will only be passed to extensions loaded by name
    (as a string). When loading extensions as class instances, pass the
    configuration settings directly to the class when initializing it.

    !!! Note
        The preferred method is to pass in an instance of an extension, which
        does not require use of the `extension_configs` keyword at all.
        See the [extensions](#extensions) keyword for details.

    The dictionary of configuration settings must be in the following format:

        :::python
        extension_configs = {
            'extension_name_1': {
                'option_1': 'value_1',
                'option_2': 'value_2'
            },
            'extension_name_2': {
                'option_1': 'value_1'
            }
        }

    See the documentation specific to the extension you are using for help in
    specifying configuration settings for that extension.

__output_format__{: #output_format }:

:   Format of output.

    Supported formats are:

    * `"xhtml1"`: Outputs XHTML 1.x. **Default**.
    * `"xhtml5"`: Outputs XHTML style tags of HTML 5
    * `"xhtml"`: Outputs latest supported version of XHTML (currently XHTML 1.1).
    * `"html4"`: Outputs HTML 4
    * `"html5"`: Outputs HTML style tags of HTML 5
    * `"html"`: Outputs latest supported version of HTML (currently HTML 4).

    The values can be in either lowercase or uppercase.

    !!! warning
        It is suggested that the more specific formats (`"xhtml1"`, `"html5"`, &
        `"html4"`) be used as the more general formats (`"xhtml"` or `"html"`) may
        change in the future if it makes sense at that time.

__tab_length__{: #tab_length }:

: Length of tabs in the source. Default: 4

__enable_attributes__{: #enable_attributes}:

: Enable the conversion of attributes. Defaults to `True`.

__smart_emphasis__{: #smart_emphasis }:

: Treat `_connected_words_` intelligently Default: True

__lazy_ol__{: #lazy_ol }:

: Ignore number of first item of ordered lists. Default: True

    Given the following list:

        :::md
        4. Apples
        5. Oranges
        6. Pears

    By default markdown will ignore the fact the the first line started
    with item number "4" and the HTML list will start with a number "1".
    If `lazy_ol` is set to `False`, then markdown will output the following
    HTML:

        :::html
        <ol start="4">
          <li>Apples</li>
          <li>Oranges</li>
          <li>Pears</li>
        </ol>

### `markdown.markdownFromFile (**kwargs)` {: #markdownFromFile }

With a few exceptions, `markdown.markdownFromFile` accepts the same options as
`markdown.markdown`. It does **not** accept a `text` (or Unicode) string.
Instead, it accepts the following required options:

__input__{: #input } (required)

:   The source text file.

    `input` may be set to one of three options:

    * a string which contains a path to a readable file on the file system,
    * a readable file-like object,
    * or `None` (default) which will read from `stdin`.

__output__{: #output }

:   The target which output is written to.

    `output` may be set to one of three options:

    * a string which contains a path to a writable file on the file system,
    * a writable file-like object,
    * or `None` (default) which will write to `stdout`.

__encoding__{: #encoding }

:   The encoding of the source text file.

    Defaults to `"utf-8"`. The same encoding will always be used for input and output.
    The `xmlcharrefreplace` error handler is used when encoding the output.

    !!! Note
        This is the only place that decoding and encoding of Unicode
        takes place in Python-Markdown. If this rather naive solution does not
        meet your specific needs, it is suggested that you write your own code
        to handle your encoding/decoding needs.

### markdown.Markdown([**kwargs]) {: #Markdown }

The same options are available when initializing the `markdown.Markdown` class
as on the [`markdown.markdown`](#markdown) function, except that the class does
**not** accept a source text string on initialization. Rather, the source text
string must be passed to one of two instance methods:

#### Markdown.convert(source) {: #convert }

The `source` text must meet the same requirements as the [`text`](#text)
argument of the [`markdown.markdown`](#markdown) function.

You should also use this method if you want to process multiple strings
without creating a new instance of the class for each string.

```python
md = markdown.Markdown()
html1 = md.convert(text1)
html2 = md.convert(text2)
```

Depending on which options and/or extensions are being used, the parser may
need its state reset between each call to `convert`, otherwise performance
can degrade drastically:

```python
html1 = md.convert(text1)
md.reset()
html2 = md.convert(text2)
```

To make this easier, you can also chain calls to `reset` together:

```python
html3 = md.reset().convert(text3)
```

#### Markdown.convertFile(**kwargs) {: #convertFile }

The arguments of this method are identical to the arguments of the same
name on the `markdown.markdownFromFile` function ([`input`](#input),
[`output`](#output), and [`encoding`](#encoding)). As with the
[`convert`](#convert) method, this method should be used to
process multiple files without creating a new instance of the class for
each document. State may need to be `reset` between each call to
`convertFile` as is the case with `convert`.
