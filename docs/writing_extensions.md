Writing Extensions for Python-Markdown
======================================

Overview
--------

Python-Markdown includes an API for extension writers to plug their own 
custom functionality and/or syntax into the parser. There are preprocessors
which allow you to alter the source before it is passed to the parser, 
inline patterns which allow you to add, remove or override the syntax of
any inline elements, and postprocessors which allow munging of the
output of the parser before it is returned. If you really want to dive in, 
there are also blockprocessors which are part of the core BlockParser.

As the parser builds an [ElementTree][] object which is later rendered 
as Unicode text, there are also some helpers provided to ease manipulation of 
the tree. Each part of the API is discussed in its respective section below. 
Additionally, reading the source of some [Available Extensions][] may be 
helpful. For example, the [Footnotes][] extension uses most of the features 
documented here.

* [Preprocessors][]
* [InlinePatterns][]
* [Treeprocessors][] 
* [Postprocessors][]
* [BlockParser][]
* [Working with the ElementTree][]
* [Integrating your code into Markdown][]
    * [extendMarkdown][]
    * [OrderedDict][]
    * [registerExtension][]
    * [Config Settings][]
    * [makeExtension][]

<h3 id="preprocessors">Preprocessors</h3>

Preprocessors munge the source text before it is passed into the Markdown 
core. This is an excellent place to clean up bad syntax, extract things the 
parser may otherwise choke on and perhaps even store it for later retrieval.

Preprocessors should inherit from ``markdown.preprocessors.Preprocessor`` and 
implement a ``run`` method with one argument ``lines``. The ``run`` method of 
each Preprocessor will be passed the entire source text as a list of Unicode 
strings. Each string will contain one line of text. The ``run`` method should 
return either that list, or an altered list of Unicode strings.

A pseudo example:

    from markdown.preprocessors import Preprocessor

    class MyPreprocessor(Preprocessor):
        def run(self, lines):
            new_lines = []
            for line in lines:
                m = MYREGEX.match(line)
                if m:
                    # do stuff
                else:
                    new_lines.append(line)
            return new_lines

<h3 id="inlinepatterns">Inline Patterns</h3>

Inline Patterns implement the inline HTML element syntax for Markdown such as
``*emphasis*`` or ``[links](http://example.com)``. Pattern objects should be 
instances of classes that inherit from ``markdown.inlinepatterns.Pattern`` or 
one of its children. Each pattern object uses a single regular expression and 
must have the following methods:

* **``getCompiledRegExp()``**: 

    Returns a compiled regular expression.

* **``handleMatch(m)``**: 

    Accepts a match object and returns an ElementTree element of a plain 
    Unicode string.

Note that any regular expression returned by ``getCompiledRegExp`` must capture
the whole block. Therefore, they should all start with ``r'^(.*?)'`` and end
with ``r'(.*?)!'``. When using the default ``getCompiledRegExp()`` method 
provided in the ``Pattern`` you can pass in a regular expression without that 
and ``getCompiledRegExp`` will wrap your expression for you and set the 
`re.DOTALL` and `re.UNICODE` flags. This means that the first group of your 
match will be ``m.group(2)`` as ``m.group(1)`` will match everything before the
pattern.

For an example, consider this simplified emphasis pattern:

    from markdown.inlinepatterns import Pattern
    from markdown.util import etree

    class EmphasisPattern(Pattern):
        def handleMatch(self, m):
            el = etree.Element('em')
            el.text = m.group(3)
            return el

As discussed in [Integrating Your Code Into Markdown][], an instance of this
class will need to be provided to Markdown. That instance would be created
like so:

    # an oversimplified regex
    MYPATTERN = r'\*([^*]+)\*'
    # pass in pattern and create instance
    emphasis = EmphasisPattern(MYPATTERN)

Actually it would not be necessary to create that pattern (and not just because
a more sophisticated emphasis pattern already exists in Markdown). The fact is,
that example pattern is not very DRY. A pattern for `**strong**` text would
be almost identical, with the exception that it would create a 'strong' element.
Therefore, Markdown provides a number of generic pattern classes that can 
provide some common functionality. For example, both emphasis and strong are
implemented with separate instances of the ``SimpleTagPettern`` listed below. 
Feel free to use or extend any of the Pattern classes found at `markdown.inlinepatterns`.

**Generic Pattern Classes**

* **``SimpleTextPattern(pattern)``**:

    Returns simple text of ``group(2)`` of a ``pattern``.

* **``SimpleTagPattern(pattern, tag)``**:

    Returns an element of type "`tag`" with a text attribute of ``group(3)``
    of a ``pattern``. ``tag`` should be a string of a HTML element (i.e.: 'em').

* **``SubstituteTagPattern(pattern, tag)``**:

    Returns an element of type "`tag`" with no children or text (i.e.: 'br').

There may be other Pattern classes in the Markdown source that you could extend
or use as well. Read through the source and see if there is anything you can 
use. You might even get a few ideas for different approaches to your specific
situation.

<h3 id="treeprocessors">Treeprocessors</h3>

Treeprocessors manipulate an ElemenTree object after it has passed through the
core BlockParser. This is where additional manipulation of the tree takes
place. Additionally, the InlineProcessor is a Treeprocessor which steps through
the tree and runs the InlinePatterns on the text of each Element in the tree.

A Treeprocessor should inherit from ``markdown.treeprocessors.Treeprocessor``,
over-ride the ``run`` method which takes one argument ``root`` (an Elementree 
object) and returns either that root element or a modified root element.

A pseudo example:

    from markdown.treprocessors import Treeprocessor

    class MyTreeprocessor(Treeprocessor):
        def run(self, root):
            #do stuff
            return my_modified_root

For specifics on manipulating the ElementTree, see 
[Working with the ElementTree][] below.

<h3 id="postprocessors">Postprocessors</h3>

Postprocessors manipulate the document after the ElementTree has been 
serialized into a string. Postprocessors should be used to work with the
text just before output.

A Postprocessor should inherit from ``markdown.postprocessors.Postprocessor`` 
and over-ride the ``run`` method which takes one argument ``text`` and returns 
a Unicode string.

Postprocessors are run after the ElementTree has been serialized back into 
Unicode text.  For example, this may be an appropriate place to add a table of 
contents to a document:

    from markdown.postprocessors import Postprocessor

    class TocPostprocessor(Postprocessor):
        def run(self, text):
            return MYMARKERRE.sub(MyToc, text)

<h3 id="blockparser">BlockParser</h3>

Sometimes, pre/tree/postprocessors and Inline Patterns aren't going to do what 
you need. Perhaps you want a new type of block type that needs to be integrated 
into the core parsing. In such a situation, you can add/change/remove 
functionality of the core ``BlockParser``. The BlockParser is composed of a
number of Blockproccessors. The BlockParser steps through each block of text
(split by blank lines) and passes each block to the appropriate Blockprocessor.
That Blockprocessor parses the block and adds it to the ElementTree. The
[Definition Lists][] extension would be a good example of an extension that
adds/modifies Blockprocessors.

A Blockprocessor should inherit from ``markdown.blockprocessors.BlockProcessor``
and implement both the ``test`` and ``run`` methods.

The ``test`` method is used by BlockParser to identify the type of block.
Therefore the ``test`` method must return a boolean value. If the test returns
``True``, then the BlockParser will call that Blockprocessor's ``run`` method.
If it returns ``False``, the BlockParser will move on to the next 
BlockProcessor.

The **``test``** method takes two arguments:

* **``parent``**: The parent etree Element of the block. This can be useful as
  the block may need to be treated differently if it is inside a list, for
  example.

* **``block``**: A string of the current block of text. The test may be a 
  simple string method (such as ``block.startswith(some_text)``) or a complex 
  regular expression.

The **``run``** method takes two arguments:

* **``parent``**: A pointer to the parent etree Element of the block. The run 
  method will most likely attach additional nodes to this parent. Note that
  nothing is returned by the method. The Elementree object is altered in place.

* **``blocks``**: A list of all remaining blocks of the document. Your run 
  method must remove (pop) the first block from the list (which it altered in
  place - not returned) and parse that block. You may find that a block of text
  legitimately contains multiple block types. Therefore, after processing the 
  first type, your processor can insert the remaining text into the beginning
  of the ``blocks`` list for future parsing.

Please be aware that a single block can span multiple text blocks. For example,
The official Markdown syntax rules state that a blank line does not end a
Code Block. If the next block of text is also indented, then it is part of
the previous block. Therefore, the BlockParser was specifically designed to 
address these types of situations. If you notice the ``CodeBlockProcessor``,
in the core, you will note that it checks the last child of the ``parent``.
If the last child is a code block (``<pre><code>...</code></pre>``), then it
appends that block to the previous code block rather than creating a new 
code block.

Each BlockProcessor has the following utility methods available:

* **``lastChild(parent)``**: 

    Returns the last child of the given etree Element or ``None`` if it had no 
    children.

* **``detab(text)``**: 

    Removes one level of indent (four spaces by default) from the front of each
    line of the given text string.

* **``looseDetab(text, level)``**: 

    Removes "level" levels of indent (defaults to 1) from the front of each line 
    of the given text string. However, this methods allows secondary lines to 
    not be indented as does some parts of the Markdown syntax.

Each BlockProcessor also has a pointer to the containing BlockParser instance at
``self.parser``, which can be used to check or alter the state of the parser.
The BlockParser tracks it's state in a stack at ``parser.state``. The state
stack is an instance of the ``State`` class.

**``State``** is a subclass of ``list`` and has the additional methods:

* **``set(state)``**: 

    Set a new state to string ``state``. The new state is appended to the end 
    of the stack.

* **``reset()``**: 

    Step back one step in the stack. The last state at the end is removed from 
    the stack.

* **``isstate(state)``**: 

    Test that the top (current) level of the stack is of the given string 
    ``state``.

Note that to ensure that the state stack doesn't become corrupted, each time a
state is set for a block, that state *must* be reset when the parser finishes
parsing that block.

An instance of the **``BlockParser``** is found at ``Markdown.parser``.
``BlockParser`` has the following methods:

* **``parseDocument(lines)``**: 

    Given a list of lines, an ElementTree object is returned. This should be 
    passed an entire document and is the only method the ``Markdown`` class 
    calls directly.

* **``parseChunk(parent, text)``**: 

    Parses a chunk of markdown text composed of multiple blocks and attaches 
    those blocks to the ``parent`` Element. The ``parent`` is altered in place 
    and nothing is returned. Extensions would most likely use this method for 
    block parsing.

* **``parseBlocks(parent, blocks)``**: 

    Parses a list of blocks of text and attaches those blocks to the ``parent``
    Element. The ``parent`` is altered in place and nothing is returned. This 
    method will generally only be used internally to recursively parse nested 
    blocks of text.

While is is not recommended, an extension could subclass or completely replace
the ``BlockParser``. The new class would have to provide the same public API.
However, be aware that other extensions may expect the core parser provided
and will not work with such a drastically different parser.

<h3 id="working_with_et">Working with the ElementTree</h3>

As mentioned, the Markdown parser converts a source document to an 
[ElementTree][] object before serializing that back to Unicode text. 
Markdown has provided some helpers to ease that manipulation within the context 
of the Markdown module.

First, to get access to the ElementTree module import ElementTree from 
``markdown`` rather than importing it directly. This will ensure you are using 
the same version of ElementTree as markdown. The module is found at 
``markdown.util.etree`` within Markdown.

    from markdown.util import etree
    
``markdown.util.etree`` tries to import ElementTree from any known location, 
first as a standard library module (from ``xml.etree`` in Python 2.5), then as 
a third party package (``Elementree``). In each instance, ``cElementTree`` is 
tried first, then ``ElementTree`` if the faster C implementation is not 
available on your system.

Sometimes you may want text inserted into an element to be parsed by 
[InlinePatterns][]. In such a situation, simply insert the text as you normally
would and the text will be automatically run through the InlinePatterns. 
However, if you do *not* want some text to be parsed by InlinePatterns,
then insert the text as an ``AtomicString``.

    from markdown.util import AtomicString
    some_element.text = AtomicString(some_text)

Here's a basic example which creates an HTML table (note that the contents of 
the second cell (``td2``) will be run through InlinePatterns latter):

    table = etree.Element("table") 
    table.set("cellpadding", "2")                      # Set cellpadding to 2
    tr = etree.SubElement(table, "tr")                 # Add child tr to table
    td1 = etree.SubElement(tr, "td")                   # Add child td1 to tr
    td1.text = markdown.AtomicString("Cell content")   # Add plain text content
    td2 = etree.SubElement(tr, "td")                   # Add second td to tr
    td2.text = "*text* with **inline** formatting."    # Add markup text
    table.tail = "Text after table"                    # Add text after table

You can also manipulate an existing tree. Consider the following example which 
adds a ``class`` attribute to ``<a>`` elements:

	def set_link_class(self, element):
		for child in element: 
		    if child.tag == "a":
                child.set("class", "myclass") #set the class attribute
            set_link_class(child) # run recursively on children

For more information about working with ElementTree see the ElementTree
[Documentation](http://effbot.org/zone/element-index.htm) 
([Python Docs](http://docs.python.org/lib/module-xml.etree.ElementTree.html)).

<h3 id="integrating_into_markdown">Integrating Your Code Into Markdown</h3>

Once you have the various pieces of your extension built, you need to tell 
Markdown about them and ensure that they are run in the proper sequence. 
Markdown accepts a ``Extension`` instance for each extension. Therefore, you
will need to define a class that extends ``markdown.extensions.Extension`` and 
over-rides the ``extendMarkdown`` method. Within this class you will manage 
configuration options for your extension and attach the various processors and 
patterns to the Markdown instance. 

It is important to note that the order of the various processors and patterns 
matters. For example, if we replace ``http://...`` links with ``<a>`` elements, 
and *then* try to deal with  inline html, we will end up with a mess. 
Therefore, the various types of processors and patterns are stored within an 
instance of the Markdown class in [OrderedDict][]s. Your ``Extension`` class 
will need to manipulate those OrderedDicts appropriately. You may insert 
instances of your processors and patterns into the appropriate location in an 
OrderedDict, remove a built-in instance, or replace a built-in instance with 
your own.

<h4 id="extendmarkdown">extendMarkdown</h4>

The ``extendMarkdown`` method of a ``markdown.extensions.Extension`` class 
accepts two arguments:

* **``md``**:

    A pointer to the instance of the Markdown class. You should use this to 
    access the [OrderedDict][]s of processors and patterns. They are found 
    under the following attributes:

    * ``md.preprocessors``
    * ``md.inlinePatterns``
    * ``md.parser.blockprocessors``
    * ``md.treepreprocessors``
    * ``md.postprocessors``

    Some other things you may want to access in the markdown instance are:

    * ``md.htmlStash``
    * ``md.output_formats``
    * ``md.set_output_format()``
    * ``md.registerExtension()``
    * ``md.html_replacement_text``
    * ``md.tab_length``
    * ``md.enable_attributes``
    * ``md.smart_emphasis``

* **``md_globals``**:

    Contains all the various global variables within the markdown module.

Of course, with access to those items, theoretically you have the option to 
changing anything through various [monkey_patching][] techniques. However, you 
should be aware that the various undocumented or private parts of markdown 
may change without notice and your monkey_patches may break with a new release.
Therefore, what you really should be doing is inserting processors and patterns
into the markdown pipeline. Consider yourself warned.

[monkey_patching]: http://en.wikipedia.org/wiki/Monkey_patch

A simple example:

    from markdown.extensions import Extension

    class MyExtension(Extension):
        def extendMarkdown(self, md, md_globals):
            # Insert instance of 'mypattern' before 'references' pattern
            md.inlinePatterns.add('mypattern', MyPattern(md), '<references')

<h4 id="ordereddict">OrderedDict</h4>

An OrderedDict is a dictionary like object that retains the order of it's
items. The items are ordered in the order in which they were appended to
the OrderedDict. However, an item can also be inserted into the OrderedDict
in a specific location in relation to the existing items.

Think of OrderedDict as a combination of a list and a dictionary as it has 
methods common to both. For example, you can get and set items using the 
``od[key] = value`` syntax and the methods ``keys()``, ``values()``, and 
``items()`` work as expected with the keys, values and items returned in the 
proper order. At the same time, you can use ``insert()``, ``append()``, and 
``index()`` as you would with a list.

Generally speaking, within Markdown extensions you will be using the special 
helper method ``add()`` to add additional items to an existing OrderedDict. 

The ``add()`` method accepts three arguments:

* **``key``**: A string. The key is used for later reference to the item.

* **``value``**: The object instance stored in this item.

* **``location``**: Optional. The items location in relation to other items. 

    Note that the location can consist of a few different values:

    * The special strings ``"_begin"`` and ``"_end"`` insert that item at the 
      beginning or end of the OrderedDict respectively. 
    
    * A less-than sign (``<``) followed by an existing key (i.e.: 
      ``"<somekey"``) inserts that item before the existing key.
    
    * A greater-than sign (``>``) followed by an existing key (i.e.: 
      ``">somekey"``) inserts that item after the existing key. 

Consider the following example:

    >>> from markdown.odict import OrderedDict
    >>> od = OrderedDict()
    >>> od['one'] =  1           # The same as: od.add('one', 1, '_begin')
    >>> od['three'] = 3          # The same as: od.add('three', 3, '>one')
    >>> od['four'] = 4           # The same as: od.add('four', 4, '_end')
    >>> od.items()
    [("one", 1), ("three", 3), ("four", 4)]

Note that when building an OrderedDict in order, the extra features of the
``add`` method offer no real value and are not necessary. However, when 
manipulating an existing OrderedDict, ``add`` can be very helpful. So let's 
insert another item into the OrderedDict.

    >>> od.add('two', 2, '>one')         # Insert after 'one'
    >>> od.values()
    [1, 2, 3, 4]

Now let's insert another item.

    >>> od.add('twohalf', 2.5, '<three') # Insert before 'three'
    >>> od.keys()
    ["one", "two", "twohalf", "three", "four"]

Note that we also could have set the location of "twohalf" to be 'after two'
(i.e.: ``'>two'``). However, it's unlikely that you will have control over the 
order in which extensions will be loaded, and this could affect the final 
sorted order of an OrderedDict. For example, suppose an extension adding 
'twohalf' in the above examples was loaded before a separate  extension which 
adds 'two'. You may need to take this into consideration when adding your 
extension components to the various markdown OrderedDicts.

Once an OrderedDict is created, the items are available via key:

    MyNode = od['somekey']

Therefore, to delete an existing item:

    del od['somekey']

To change the value of an existing item (leaving location unchanged):

    od['somekey'] = MyNewObject()

To change the location of an existing item:

    t.link('somekey', '<otherkey')

<h4 id="registerextension">registerExtension</h4>

Some extensions may need to have their state reset between multiple runs of the
Markdown class. For example, consider the following use of the [Footnotes][] 
extension:

    md = markdown.Markdown(extensions=['footnotes'])
    html1 = md.convert(text_with_footnote)
    md.reset()
    html2 = md.convert(text_without_footnote)

Without calling ``reset``, the footnote definitions from the first document will
be inserted into the second document as they are still stored within the class
instance. Therefore the ``Extension`` class needs to define a ``reset`` method
that will reset the state of the extension (i.e.: ``self.footnotes = {}``).
However, as many extensions do not have a need for ``reset``, ``reset`` is only
called on extensions that are registered.

To register an extension, call ``md.registerExtension`` from within your 
``extendMarkdown`` method:


    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        # insert processors and patterns here

Then, each time ``reset`` is called on the Markdown instance, the ``reset`` 
method of each registered extension will be called as well. You should also
note that ``reset`` will be called on each registered extension after it is
initialized the first time. Keep that in mind when over-riding the extension's
``reset`` method.

<h4 id="configsettings">Config Settings</h4>

If an extension uses any parameters that the user may want to change,
those parameters should be stored in ``self.config`` of your 
``markdown.Extension`` class in the following format:

    self.config = {parameter_1_name : [value1, description1],
                   parameter_2_name : [value2, description2] }

When stored this way the config parameters can be over-ridden from the
command line or at the time Markdown is initiated:

    markdown.py -x myextension(SOME_PARAM=2) inputfile.txt > output.txt

Note that parameters should always be assumed to be set to string
values, and should be converted at run time. For example:

    i = int(self.getConfig("SOME_PARAM"))

<h4 id="makeextension">makeExtension</h4>

Each extension should ideally be placed in its own module starting
with the  ``mdx_`` prefix (e.g. ``mdx_footnotes.py``).  The module must
provide a module-level function called ``makeExtension`` that takes
an optional parameter consisting of a dictionary of configuration over-rides 
and returns an instance of the extension.  An example from the footnote 
extension:

    def makeExtension(configs=None) :
        return FootnoteExtension(configs=configs)

By following the above example, when Markdown is passed the name of your 
extension as a string (i.e.: ``'footnotes'``), it will automatically import
the module and call the ``makeExtension`` function initiating your extension.

You may have noted that the extensions packaged with Python-Markdown do not
use the ``mdx_`` prefix in their module names. This is because they are all
part of the ``markdown.extensions`` package. Markdown will first try to import
from ``markdown.extensions.extname`` and upon failure, ``mdx_extname``. If both
fail, Markdown will continue without the extension.

However, Markdown will also accept an already existing instance of an extension.
For example:

    import markdown
    import myextension
    configs = {...}
    myext = myextension.MyExtension(configs=configs)
    md = markdown.Markdown(extensions=[myext])

This is useful if you need to implement a large number of extensions with more
than one residing in a module.

[Preprocessors]: #preprocessors
[InlinePatterns]: #inlinepatterns
[Treeprocessors]: #treeprocessors
[Postprocessors]: #postprocessors
[BlockParser]: #blockparser
[Working with the ElementTree]: #working_with_et
[Integrating your code into Markdown]: #integrating_into_markdown
[extendMarkdown]: #extendmarkdown
[OrderedDict]: #ordereddict
[registerExtension]: #registerextension
[Config Settings]: #configsettings
[makeExtension]: #makeextension
[ElementTree]: http://effbot.org/zone/element-index.htm
[Available Extensions]: extensions/
[Footnotes]: extensions/footnotes.html
[Definition Lists]: extensions/definition_lists.html
