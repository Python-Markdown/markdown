Meta-Data
=========

Summary
-------

An extension to Python-Markdown that adds a syntax for defining meta-data about
a document. The Meta-Data extension is inspired by and follows the syntax of 
[MultiMarkdown][]. Currently, this extension does not use the meta-data in any 
way, but simply provides it as a `Meta` attribute of a markdown instance for 
use by other extensions or directly by your python code.

[MultiMarkdown]: http://fletcherpenney.net/MultiMarkdown_Syntax_Guide#metadata

This extension has been a part of the Markdown library since 2.0.

Syntax
------

Meta-data consists of a series of keywords and values defined at the beginning 
of a markdown document like this:

    Title:   My Document
    Summary: A brief description of my document.
    Authors: Waylan Limberg
             John Doe
    Date:    October 2, 2007
    blank-value: 
    base_url: http://example.com

    This is the first paragraph of the document.

The keywords are case-insensitive and may consist of letters, numbers, 
underscores and dashes and must end with a colon. The values consist of 
anything following the colon on the line and may even be blank. If a line is 
indented 4 or more spaces, that line is assumed to be an additional line of the
value for the previous keyword. A keyword may have as many lines as desired. 
The first blank line ends all meta-data for the document. Therefore, the first 
line of a document must not be blank. All meta-data is stripped from the 
document prior to any further processing by markdown.

Accessing the Meta-Data
-----------------------

The meta-data is made available as a python Dict in the `Meta` attribute of an 
instance of the Markdown class. For example, using the above document:

    >>> md = markdown.Markdown(extensions = ['meta'])
    >>> html = md.convert(text)
    >>> # Meta-data has been stripped from output
    >>> print html
    <p>This is the first paragraph of the document.</p>

    >>> # View meta-data
    >>> print md.Meta
    {
    'title' : ['My Document'],
    'summary' : ['A brief description of my document.'],
    'authors' : ['Waylan Limberg', 'John Doe'],
    'date' : ['October 2, 2007'],
    'blank-value' : [''],
    'base_url' : ['http://example.com']
    }

Note that the keys are all lowercase and the values consist of a list of 
strings where each item is one line for that key. This way, one could preserve 
line breaks if desired. Or the items could be joined where appropriate. No 
assumptions are made regarding the data. It is simply passed as found to the 
`Meta` attribute.

Perhaps the meta-data could be passed into a template system, or used by 
various markdown extensions. The possibilities are left to the imagination of 
the developer.

Compatible Extensions
---------------------

The following are extensions currently known to work with the Meta-Data 
Extension and the keywords they are known to support:

* [[HeaderId]]
    * `header_level`
    * `header_forceid`
* [[WikiLinks]]
    * `wiki_base_url`
    * `wiki_end_url`
    * `wiki_html_class`

