---
title: Playground
hide:
  - navigation
  - path
  - toc
---

<div class="pyodide" data-install="markdown,pymdown-extensions,pygments" data-session="playground" data-minlines="10" data-maxlines="30">
<div class="pyodide-editor-bar">
<span class="pyodide-bar-item">Editor (session: playground)</span><span id="exec-1--run" title="Run: press Ctrl-Enter" class="pyodide-bar-item pyodide-clickable"><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M8 5.14v14l11-7-11-7Z"></path></svg></span> Run</span>
</div>
<div><pre id="exec-1--editor" class="pyodide-editor">import markdown
from markdown.extensions.toc import TocExtension

source = '''
# Heading

A paragraph of **Markdown** text.
'''
html = markdown.markdown(source, extensions=[TocExtension(permalink=True)])
print(html)
</pre></div>
<div class="pyodide-editor-bar">
<span class="pyodide-bar-item">Output</span><span id="exec-1--clear" class="pyodide-bar-item pyodide-clickable"><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.14 3c-.51 0-1.02.2-1.41.59L2.59 14.73c-.78.77-.78 2.04 0 2.83L5.03 20h7.66l8.72-8.73c.79-.77.79-2.04 0-2.83l-4.85-4.85c-.39-.39-.91-.59-1.42-.59M17 18l-2 2h7v-2"></path></svg></span> Clear</span>
</div>
<pre><code id="exec-1--output" class="pyodide-output"></code></pre>
</div>

!!! tip ""
    Feel free to edit the Python code above. You may use and configure any of the
    [built-in extensions], as well as any of the [PyMdown Extensions]. 

    To run the code, click the **:material-play: Run** button in the top-right
    corner or, if the editor is active (cursor is blinking), you may press
    ++ctrl+enter++ on your keyboard.

    This interactive Python editor is made possible by [Pyodide], [Ace] and
    [Highlight.js].

[Pyodide]: https://pyodide.org
[Ace]: https://ace.c9.io/
[Highlight.js]: https://highlightjs.org/
[built-in extensions]: extensions/index.md
[PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/
