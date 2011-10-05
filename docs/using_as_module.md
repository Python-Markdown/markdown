Using Markdown as a Python Library
==================================

First and foremost, Python-Markdown is intended to be a python library module
used by various projects to convert Markdown syntax into HTML.

The Basics
----------

To use markdown as a module:

    import markdown
    html = markdown.markdown(your_text_string)

The Details
-----------

Python-Markdown provides two public functions (`markdown.markdown` and 
`markdown.markdownFromFile`) both of which wrap the public class
`markdown.Markdown`. If you're processing one document at a time, the
functions will serve your needs. However, if you need to process 
multiple documents, it may be advantageous to create a single instance 
of the `markdown.Markdown` class and pass multiple documents through it.

### `markdown.markdown(text [, **kwargs])`

The following options are available on the `markdown.markdown` function:

* `text` (required): The source text string.

    Note that Python-Markdown expects **Unicode** as input (although
    a simple ASCII string may work) and returns output as Unicode.  
    Do not pass encoded strings to it! If your input is encoded, (e.g. as 
    UTF-8), it is your responsibility to decode it.  For example:

        input_file = codecs.open("some_file.txt", mode="r", encoding="utf-8")
        text = input_file.read()
        html = markdown.markdown(text)

    If you want to write the output to disk, you must encode it yourself:

        output_file = codecs.open("some_file.html", "w", 
                                  encoding="utf-8", 
                                  errors="xmlcharrefreplace"
        )
        output_file.write(html)

* `extensions`: A list of extensions.

    Python-Markdown provides an API for third parties to write extensions to
    the parser adding their own additions or changes to the syntax. A few
    commonly used extensions are shipped with the markdown library. See
    the [extension documentation](extensions) for a list of available extensions.

    The list of extensions may contain instances of extensions or stings of
    extension names. If an extension name is provided as a string, the
    extension must be importable as a python module either within the 
    `markdown.extensions` package or on your PYTHONPATH with a name starting 
    with `mdx_`, followed by the name of the extension.  Thus, 
    `extensions=['extra']` will first look for the module 
    `markdown.extensions.extra`, then a module named `mdx_extra`. 

* `extension-configs`: A dictionary of configuration settings for extensions.

    The dictionary must be of the following format:

        extension-configs = {'extension_name_1': 
                               [
                                  ('option_1', 'value_1'),
                                  ('option_2', 'value_2')
                               ],
                             'extension_name_2':
                               [
                                  ('option_1', 'value_1')
                               ]
                            }
    See the documentation specific to the extension you are using for help in 
    specifying configuration settings for that extension.

* `output_format`: Format of output. 

    Supported formats are:

    * `"xhtml1"`: Outputs XHTML 1.x. **Default**.
    * `"xhtml5"`: Outputs XHTML style tags of HTML 5
    * `"xhtml"`: Outputs latest supported version of XHTML (currently XHTML 1.1).
    * `"html4"`: Outputs HTML 4
    * `"html5"`: Outputs HTML style tags of HTML 5
    * `"html"`: Outputs latest supported version of HTML (currently HTML 4).

    Note that it is suggested that the more specific formats ("xhtml1",
    "html5", & "html4") be used as "xhtml" or "html" may change in the future
    if it makes sense at that time. The values can either be lowercase or 
    uppercase.

* `safe_mode`: Disallow raw html.

    If you are using Markdown on a web system which will transform text 
    provided by untrusted users, you may want to use the "safe_mode" 
    option which ensures that the user's HTML tags are either replaced, 
    removed or escaped. (They can still create links using Markdown syntax.)

    The following values are accepted:

    * `False` (Default): Raw HTML is passed through unaltered.

    * `replace`: Replace all HTML blocks with the text assigned to 
      `html_replacement_text` To maintain backward compatibility, setting 
      `safe_mode=True` will have the same effect as `safe_mode='replace'`.   

        To replace raw HTML with something other than the default, do:

            md = markdown.Markdown(safe_mode='replace', 
                               html_replacement_text='--RAW HTML NOT ALLOWED--')

    * `remove`: All raw HTML will be completely stripped from the text with
      no warning to the author.

    * `escape`: All raw HTML will be escaped and included in the document.

        For example, the following source:

            Foo <b>bar</b>.

        Will result in the following HTML:

            <p>Foo &lt;b&gt;bar&lt;/b&gt;.</p>

    Note that "safe_mode" does not alter the `enable_attributes` option, which 
    could allow someone to inject javascript (i.e., `{@onclick=alert(1)}`). You 
    may also want to set `enable_attributes=False` when using "safe_mode".

* `html_replacement_text`: Text used when safe_mode is set to `replace`.
  Defaults to `[HTML_REMOVED]`.

* `tab_length`: Length of tabs in the source. Default: 4

* `enable_attributes`: Enable the conversion of attributes. Default: True

* `smart_emphasis`: Treat `_connected_words_` intelligently Default: True

* `lazy_ol`: Ignore number of first item of ordered lists. Default: True

    Given the following list:

        4. Apples
        5. Oranges
        6. Pears

    By default markdown will ignore the fact the the first line started 
    with item number "4" and the HTML list will start with a number "1".
    If `lazy_ol` is set to `True`, then markdown will output the following
    HTML:

        <ol>
          <li start="4">Apples</li>
          <li>Oranges</li>
          <li>Pears</li>
        </ol>


### `markdown.markdownFromFile(**kwargs)`

With a few exceptions, `markdown.markdownFromFile` accepts the same options as 
`markdown.markdown`. It does **not** accept a `text` (or Unicode) string. 
Instead, it accepts the following required options:

* `input` (required): The source text file.

    `input` may be set to one of three options:

    * a string which contains a path to a readable file on the file system,
    * a readable file-like object,
    * or `None` (default) which will read from `stdin`.

* `output`: The target which output is written to.

    `output` may be set to one of three options:

    * a string which contains a path to a writable file on the file system,
    * a writable file-like object,
    * or `None` (default) which will write to `stdout`.

* `encoding`: The encoding of the source text file. Defaults to 
  "utf-8". The same encoding will always be used for input and output. 
  The 'xmlcharrefreplace' error handler is used when encoding the output.

    **Note:** This is the only place that decoding and encoding of unicode
    takes place in Python-Markdown. If this rather naive solution does not
    meet your specific needs, it is suggested that you write your own code
    to handle your encoding/decoding needs.

### `markdown.Markdown([**kwargs])`

The same options are available when initializing the `markdown.Markdown` class
as on the `markdown.markdown` function, except that the class does **not**
accept a source text string on initialization. Rather, the source text string
must be passed to one of two instance methods:

* `Markdown.convert(source)`

    The `source` text must meet the same requirements as the `text` argument
    of the `markdown.markdown` function.

    You should also use this method if you want to process multiple strings
    without creating a new instance of the class for each string.

        md = markdown.Markdown()
        html1 = md.convert(text1)
        html2 = md.convert(text2)

    Note that depending on which options and/or extensions are being used,
    the parser may need its state reset between each call to `convert`.

        html1 = md.convert(text1)
        md.reset()
        html2 = md.convert(text2)
    
    You can also change calls to `reset` togeather:
    
        html3 = md.reset().convert(text3)

* `Markdown.convertFile(**kwargs)`

    The arguments of this method are identical to the arguments of the same
    name on the `markdown.markdownFromFile` function (`input`, `output`, and 
    `encoding`). As with the `convert` method, this method should be used to 
    process multiple files without creating a new instance of the class for 
    each document. State may need to be `reset` between each call to 
    `convertFile` as is the case with `convert`.
