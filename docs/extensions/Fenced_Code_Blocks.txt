Fenced Code Blocks
==================

Summary
-------

This extension adds a secondary way to define code blocks which overcomes a few
limitations of the indented code blocks.

This extension is included in the standard Markdown library.

Syntax
------

Fenced Code Blocks are defined using the syntax established in 
[PHP Markdown Extra][php].

[php]: http://www.michelf.com/projects/php-markdown/extra/#fenced-code-blocks

Thus, the following text (taken from the above referenced PHP documentation):

    This is a paragraph introducing:

    ~~~~~~~~~~~~~~~~~~~~
    a one-line code block
    ~~~~~~~~~~~~~~~~~~~~

Fenced code blocks can have a blank line as the first  and/or last line of a 
code block and they can also come immediately after a list item without becoming
part of the list.

In addition to PHP Extra's syntax, you can define the language of the code 
block for use by syntax highlighters etc. The language will be assigned as a 
class attribute of the ``<code>`` element in the output. Therefore, you should 
define the language as you would a css class - ``.language``. For consistency 
with other markdown syntax, the language can *optionally* be wrapped in curly 
brackets:

    ~~~~{.python}
    # python code
    ~~~~

    ~~~~.html
    <p>HTML Document</p>
    ~~~~

The above will output:

    <pre><code class="python"># python code
    </code></pre>
    
    <pre><code class="html">&lt;p&gt;HTML Document&lt;/p&gt;
    </code></pre>

Usage
-----

From the Python interpreter:

    >>> html = markdown.markdown(text, ['fenced_code'])



