CodeHilite
==========

Summary
-------

The CodeHilite Extension adds code/syntax highlighting to standard 
Python-Markdown code blocks using [Pygments][].

[Python-Markdown]: http://www.freewisdom.org/projects/python-markdown/
[Pygments]: http://pygments.org/

This extension is included in the  Markdown library.

Setup
-----

You will also need to [download][dl] and install the Pygments package on your 
`PYTHONPATH`. You will need to determine the appropriate CSS classes and create
appropriate rules for them, which are either defined in or linked from the 
header of your HTML templates. See the excellent [documentation][] for more 
details. If no language is defined, Pygments will attempt to guess the 
language. When that fails, the code block will display as un-highlighted code.

[dl]: http://pygments.org/download/
[documentation]: http://pygments.org/docs

**Note:** The css and/or javascript is not included as part of this extension 
but shall always be provided by the end user.

Syntax
------

The CodeHilite Extension follows the same [syntax][] as regular Markdown code 
blocks, with one exception. The hiliter needs to know what language to use for 
the code block. There are three ways to tell the hiliter what language the code 
block contains and each one has a different result.

[syntax]: http://daringfireball.net/projects/markdown/syntax#precode

###SheBang (with path)

If the first line of the codeblock contains a shebang, the language is derived 
from that and line numbers are used.

        #!/usr/bin/python
        # Code goes here ...

Will result in:

    #!/usr/bin/python
    # Code goes here ...


###SheBang (no path)

If the first line contains a shebang, but the shebang line does not contain a 
path (a single `/` or even a space), then that line is removed from the code 
block before processing. Line numbers are used.

        #!python
        # Code goes here ...

Will result in:

    # Code goes here ...

####Colons

If the first line begins with three or more colons, the text following the 
colons identifies the language. The first line is removed from the code block 
before processing and line numbers are not used.

        :::python
        # Code goes here ...

Will result in:

    # Code goes here ...

###When No Language is Defined

CodeHilite is completely backward compatible so that if a code block is 
encountered that does not define a language, the block is simple wrapped in 
`<pre>` tags and output. Note: one exception would be that the Pygments 
highlighting engine will try to guess the language. Upon failure, the same 
behavior will happen as described here.

        # Code goes here ...

Will result in:

    # Code goes here ...

Lets see the source for that:

    <div class="codehilite" ><pre><code># Code goes here ...
    </code></pre></div>

Usage
-----

From the Python interpreter:

    >>> html = markdown.markdown(text, ['codehilite'])

If you want every code block to have line numbers, even when using colons 
(`:::`) for language identification, the setting `force_linenos` is available 
to do so.

    >>> html = markdown.markdown(text, 
    ...     ['codehilite(force_linenos=True)']
    ... )

If you want to prevent Pygments from guessing the language, only highlighting
blocks when you explicitly request it, set the `guess_lang` setting to 'False'.

    >>> html = markdown.markdown(text,
    ...     ['codehilite(guess_lang=False)']
    ... )
