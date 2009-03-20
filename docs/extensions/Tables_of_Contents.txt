Table of Contents
=================

Summary
-------

Adds a Table of Contents to a Markdown document.

This extension is included with the Markdown library since version 2.0.

Syntax
------

Place a marker in the document where you would like the table of contents to
appear. Then, a nested list of all the headers in the document will replace the
marker. The marker defaults to ``[TOC]`` so the following document:

    [TOC]

    # Header 1

    ## Header 2

would generate the following output:

    <div class="toc">
      <ul>
        <li><a href="#header-1">Header 1</a></li>
          <ul>
            <li><a href="#header-2">Header 2</a></li>
          </ul>
      </ul>
    </div>
    <h1 id="header-1">Header 1</h1>
    <h1 id="header-2">Header 2</h1>

Configuration Options
---------------------

The following options are provided to configure the output:

* **marker**: Text to find and replace with the Table of Contents. Defaults
  to ``[TOC]``.
* **slugify**: Callable to generate anchors based on header text. Defaults to a
  built in ``slugify`` method. The callable must accept one argument which 
  contains the text content of the header and return a string which will be 
  used as the anchor text.
* **title**: Title to insert in TOC ``<div>``. Defaults to ``None``.
* **anchorlink**: Set to ``True`` to have the headers link to themselves. 
  Default is ``False``.
