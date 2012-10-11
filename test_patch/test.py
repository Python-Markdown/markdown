import os
import sys

# python-markdown Codehilite line numbers override
#
# © 2012 Noah K. Tilton <noahktilton@gmail.com>
# BSD License

# The following tests can be used to compare the new and old
# functionality side by side.

sys.path.insert(0, './test_patch/usr/lib/python3.2/site-packages')

import markdown

shebang1_code = """
    #!/usr/bin/env python
    # full shebanag first line
    print("Hello, world!")
    while True:
        awesome()
"""

shebang2_code = """
    #!python
    # mock shebang first line
    print("Hello, world!")
    while True:
        awesome()
"""

colons_code = """
    ::python
    # colons first line example
    print("Hello, world!")
    while True:
        awesome()
"""

with open("original_output.html", "w+b") as f:
#with open("output.html", "w+b") as f:

    w = lambda s: f.write(bytes("%s\n" % s, 'utf-8'))
    w("<link rel='stylesheet' href='css/code.css'/>")
    w("<h1>New <code>codehilite(linenos)</code> output</h1>")

    argtypes = [
            "codehilite",
            "codehilite(force_linenos=True)",
            "codehilite(force_linenos=False)",
            #"codehilite(linenos=True)",
            #"codehilite(linenos=False)",
    ]
    w("<pre>")
    for arg in argtypes:
        w(("*" * 72))
        w("")
        w("shebang 1 `%s`" % arg)
        w(markdown.markdown(shebang1_code, [arg]))
        w("")
        w("shebang 2 `%s`" % arg)
        w(markdown.markdown(shebang2_code, [arg]))
        w("")
        w("colons `%s`" % arg)
        w(markdown.markdown(colons_code, [arg]))
    w("</pre>")
