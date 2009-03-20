HTML Tidy
=========

Runs [HTML Tidy][] on the output of Python-Markdown using the [uTidylib][]
Python wrapper. Both libtidy and uTidylib must be installed on your system.

This extension is available in the standard Markdown library since version 2.0.

[HTML Tidy]: http://tidy.sourceforge.net/
[uTidylib]: http://utidylib.berlios.de/

Note than any Tidy [options][] can be passed in as extension configs. So, 
for example, to output HTML rather than XHTML, set ``output_xhtml=0``. To
indent the output, set ``indent=auto`` and to have Tidy wrap the output in 
``<html>`` and ``<body>`` tags, set ``show_body_only=0``. See Tidy's 
[options][] for a full list of the available options. The defaults are set to 
most closely match Markdowns defaults with the exception that you get much
better pretty-printing.

[options]: http://tidy.sourceforge.net/docs/quickref.html

Note that options set in this extension will override most any other settings
passed on to Markdown (such as "output_format"). Unlike Markdown, this extension
will also treat raw HTML no different than that output by Markdown. In other 
words, it may munge a document authors carefully crafted HTML. Of course, it
may also transform poorly formed raw HTML into nice, valid HTML. Take these
things into consideration when electing to use this extension.
