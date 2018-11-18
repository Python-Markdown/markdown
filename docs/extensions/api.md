title:      Extensions API

# Writing Extensions for Python-Markdown

Python-Markdown includes an API for extension writers to plug their own
custom functionality and/or syntax into the parser. There are Preprocessors
which allow you to alter the source before it is passed to the parser,
inline patterns which allow you to add, remove or override the syntax of
any inline elements, and Postprocessors which allow munging of the
output of the parser before it is returned. If you really want to dive in,
there are also Blockprocessors which are part of the core BlockParser.

As the parser builds an [ElementTree][ElementTree] object which is later rendered
as Unicode text, there are also some helpers provided to ease manipulation of
the tree. Each part of the API is discussed in its respective section below.
Additionally, reading the source of some [Available Extensions][] may be
helpful. For example, the [Footnotes][] extension uses most of the features
documented here.

## Preprocessors {: #preprocessors }

Preprocessors munge the source text before it is passed into the Markdown
core. This is an excellent place to clean up bad syntax, extract things the
parser may otherwise choke on and perhaps even store it for later retrieval.

Preprocessors should inherit from `markdown.preprocessors.Preprocessor` and
implement a `run` method with one argument `lines`. The `run` method of
each Preprocessor will be passed the entire source text as a list of Unicode
strings. Each string will contain one line of text. The `run` method should
return either that list, or an altered list of Unicode strings.

A pseudo example:

```python
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
```

## Inline Patterns {: #inlinepatterns }

### Legacy

Inline Patterns implement the inline HTML element syntax for Markdown such as
`*emphasis*` or `[links](http://example.com)`. Pattern objects should be
instances of classes that inherit from `markdown.inlinepatterns.Pattern` or
one of its children. Each pattern object uses a single regular expression and
must have the following methods:

* **`getCompiledRegExp()`**:

    Returns a compiled regular expression.

* **`handleMatch(m)`**:

    Accepts a match object and returns an ElementTree element of a plain
    Unicode string.

Also, Inline Patterns can define the property `ANCESTOR_EXCLUDES` with either
a list or tuple of undesirable ancestors. The pattern should not match if it
would cause the content to be a descendant of one of the defined tag names.

Note that any regular expression returned by `getCompiledRegExp` must capture
the whole block. Therefore, they should all start with `r'^(.*?)'` and end
with `r'(.*?)!'`. When using the default `getCompiledRegExp()` method
provided in the `Pattern` you can pass in a regular expression without that
and `getCompiledRegExp` will wrap your expression for you and set the
`re.DOTALL` and `re.UNICODE` flags. This means that the first group of your
match will be `m.group(2)` as `m.group(1)` will match everything before the
pattern.

For an example, consider this simplified emphasis pattern:

```python
from markdown.inlinepatterns import Pattern
from markdown.util import etree

class EmphasisPattern(Pattern):
    def handleMatch(self, m):
        el = etree.Element('em')
        el.text = m.group(2)
        return el
```

As discussed in [Integrating Your Code Into Markdown][], an instance of this
class will need to be provided to Markdown. That instance would be created
like so:

```python
# an oversimplified regex
MYPATTERN = r'\*([^*]+)\*'
# pass in pattern and create instance
emphasis = EmphasisPattern(MYPATTERN)
```

Actually it would not be necessary to create that pattern (and not just because
a more sophisticated emphasis pattern already exists in Markdown). The fact is,
that example pattern is not very DRY. A pattern for `**strong**` text would
be almost identical, with the exception that it would create a 'strong' element.
Therefore, Markdown provides a number of generic pattern classes that can
provide some common functionality. For example, both emphasis and strong are
implemented with separate instances of the `SimpleTagPattern` listed below.
Feel free to use or extend any of the Pattern classes found at
`markdown.inlinepatterns`.

### Future

While users can still create plugins with the existing
`markdown.inlinepatterns.Pattern`, a new, more flexible inline processor has
been added which users are encouraged to migrate to. The new inline processor
is found at `markdown.inlinepatterns.InlineProcessor`.

The new processor is very similar to legacy with two major distinctions.

1. Patterns no longer need to match the entire block, so patterns no longer
    start with `r'^(.*?)'` and end with `r'(.*?)!'`. This was a huge
    performance sink and this requirement has been removed. The returned match
    object will only contain what is explicitly matched in the pattern, and
    extension pattern groups now start with `m.group(1)`.

2. The `handleMatch` method now takes an additional input called `data`,
    which is the entire block under analysis, not just what is matched with
    the specified pattern. The method also returns the element *and* the index
    boundaries relative to `data` that the return element is replacing
    (usually `m.start(0)` and `m.end(0)`).  If the boundaries are returned as
    `None`, it is assumed that the match did not take place, and nothing will
    be altered in `data`.

If all you need is the same functionality as the legacy processor, you can do
as shown below. Most of the time, simple regular expression processing is all
you'll need.

```python
from markdown.inlinepatterns import InlineProcessor
from markdown.util import etree

# an oversimplified regex
MYPATTERN = r'\*([^*]+)\*'

class EmphasisPattern(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element('em')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

# pass in pattern and create instance
emphasis = EmphasisPattern(MYPATTERN)
```

But, the new processor allows you handle much more complex patterns that are
too much for Python's Re to handle.  For instance, to handle nested brackets in
link patterns, the built-in link inline processor uses the following pattern to
find where a link *might* start:

```python
LINK_RE = NOIMG + r'\['
link = LinkInlineProcessor(LINK_RE, md_instance)
```

It then uses programmed logic to actually walk the string (`data`), starting at
where the match started (`m.start(0)`). If for whatever reason, the text
does not appear to be a link, it returns `None` for the start and end boundary
in order to communicate to the parser that no match was found.

```python
    # Just a snippet of the link's handleMatch
    # method to illustrate new logic
    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))

        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = util.etree.Element("a")
        el.text = text

        el.set("href", href)

        if title is not None:
            el.set("title", title)

        return el, m.start(0), index
```

### Generic Pattern Classes

Some example processors that are available.

* **`SimpleTextInlineProcessor(pattern)`**:

    Returns simple text of `group(2)` of a `pattern` and the start and end
    position of the match.

* **`SimpleTagInlineProcessor(pattern, tag)`**:

    Returns an element of type "`tag`" with a text attribute of `group(3)`
    of a `pattern`. `tag` should be a string of a HTML element (i.e.: 'em').
    It also returns the start and end position of the match.

* **`SubstituteTagInlineProcessor(pattern, tag)`**:

    Returns an element of type "`tag`" with no children or text (i.e.: `br`)
    and the start and end position of the match.

A very small number of the basic legacy processors are still available to
prevent breakage of 3rd party extensions during the transition period to the
new processors. Three of the available processors are listed below.

* **`SimpleTextPattern(pattern)`**:

    Returns simple text of `group(2)` of a `pattern`.

* **`SimpleTagPattern(pattern, tag)`**:

    Returns an element of type "`tag`" with a text attribute of `group(3)`
    of a `pattern`. `tag` should be a string of a HTML element (i.e.: 'em').

* **`SubstituteTagPattern(pattern, tag)`**:

    Returns an element of type "`tag`" with no children or text (i.e.: `br`).

There may be other Pattern classes in the Markdown source that you could extend
or use as well. Read through the source and see if there is anything you can
use. You might even get a few ideas for different approaches to your specific
situation.

## Treeprocessors {: #treeprocessors }

Treeprocessors manipulate an ElementTree object after it has passed through the
core BlockParser. This is where additional manipulation of the tree takes
place. Additionally, the InlineProcessor is a Treeprocessor which steps through
the tree and runs the Inline Patterns on the text of each Element in the tree.

A Treeprocessor should inherit from `markdown.treeprocessors.Treeprocessor`,
over-ride the `run` method which takes one argument `root` (an ElementTree
object) and either modifies that root element and returns `None` or returns a
new ElementTree object.

A pseudo example:

```python
from markdown.treeprocessors import Treeprocessor

class MyTreeprocessor(Treeprocessor):
    def run(self, root):
        root.text = 'modified content'
```

Note that Python class methods return `None` by default when no `return`
statement is defined.  Additionally all Python variables refer to objects by
reference.  Therefore, the above `run` method modifies the `root` element
in place and returns `None`. The changes made to the `root` element and its
children are retained.

Some may be inclined to return the modified `root` element. While that would
work, it would cause a copy of the entire ElementTree to be generated each
time the Treeprocessor is run. Therefore, it is generally expected that
the `run` method would only return `None` or a new ElementTree object.

For specifics on manipulating the ElementTree, see
[Working with the ElementTree][workingwithetree] below.

## Postprocessors {: #postprocessors }

Postprocessors manipulate the document after the ElementTree has been
serialized into a string. Postprocessors should be used to work with the
text just before output.

A Postprocessor should inherit from `markdown.postprocessors.Postprocessor`
and over-ride the `run` method which takes one argument `text` and returns
a Unicode string.

Postprocessors are run after the ElementTree has been serialized back into
Unicode text.  For example, this may be an appropriate place to add a table of
contents to a document:

```python
from markdown.postprocessors import Postprocessor

class TocPostprocessor(Postprocessor):
    def run(self, text):
        return MYMARKERRE.sub(MyToc, text)
```

## BlockParser {: #blockparser }

Sometimes, Preprocessors, Treeprocessors, Postprocessors, and Inline Patterns
are not going to do what you need. Perhaps you want a new type of block type
that needs to be integrated into the core parsing. In such a situation, you can
add/change/remove functionality of the core `BlockParser`. The BlockParser is
composed of a number of Blockprocessors. The BlockParser steps through each
block of text (split by blank lines) and passes each block to the appropriate
Blockprocessor. That Blockprocessor parses the block and adds it to the
ElementTree. The
[Definition Lists][] extension would be a good example of an extension that
adds/modifies Blockprocessors.

A Blockprocessor should inherit from `markdown.blockprocessors.BlockProcessor`
and implement both the `test` and `run` methods.

The `test` method is used by BlockParser to identify the type of block.
Therefore the `test` method must return a Boolean value. If the test returns
`True`, then the BlockParser will call that Blockprocessor's `run` method.
If it returns `False`, the BlockParser will move on to the next
Blockprocessor.

The **`test`** method takes two arguments:

* **`parent`**: The parent ElementTree Element of the block. This can be useful
  as the block may need to be treated differently if it is inside a list, for
  example.

* **`block`**: A string of the current block of text. The test may be a
  simple string method (such as `block.startswith(some_text)`) or a complex
  regular expression.

The **`run`** method takes two arguments:

* **`parent`**: A pointer to the parent ElementTree Element of the block. The run
  method will most likely attach additional nodes to this parent. Note that
  nothing is returned by the method. The ElementTree object is altered in place.

* **`blocks`**: A list of all remaining blocks of the document. Your run
  method must remove (pop) the first block from the list (which it altered in
  place - not returned) and parse that block. You may find that a block of text
  legitimately contains multiple block types. Therefore, after processing the
  first type, your processor can insert the remaining text into the beginning
  of the `blocks` list for future parsing.

Please be aware that a single block can span multiple text blocks. For example,
The official Markdown syntax rules state that a blank line does not end a
Code Block. If the next block of text is also indented, then it is part of
the previous block. Therefore, the BlockParser was specifically designed to
address these types of situations. If you notice the `CodeBlockProcessor`,
in the core, you will note that it checks the last child of the `parent`.
If the last child is a code block (`<pre><code>...</code></pre>`), then it
appends that block to the previous code block rather than creating a new
code block.

Each Blockprocessor has the following utility methods available:

* **`lastChild(parent)`**:

    Returns the last child of the given ElementTree Element or `None` if it
    had no children.

* **`detab(text)`**:

    Removes one level of indent (four spaces by default) from the front of each
    line of the given text string.

* **`looseDetab(text, level)`**:

    Removes "level" levels of indent (defaults to 1) from the front of each line
    of the given text string. However, this methods allows secondary lines to
    not be indented as does some parts of the Markdown syntax.

Each Blockprocessor also has a pointer to the containing BlockParser instance at
`self.parser`, which can be used to check or alter the state of the parser.
The BlockParser tracks it's state in a stack at `parser.state`. The state
stack is an instance of the `State` class.

**`State`** is a subclass of `list` and has the additional methods:

* **`set(state)`**:

    Set a new state to string `state`. The new state is appended to the end
    of the stack.

* **`reset()`**:

    Step back one step in the stack. The last state at the end is removed from
    the stack.

* **`isstate(state)`**:

    Test that the top (current) level of the stack is of the given string
    `state`.

Note that to ensure that the state stack does not become corrupted, each time a
state is set for a block, that state *must* be reset when the parser finishes
parsing that block.

An instance of the **`BlockParser`** is found at `Markdown.parser`.
`BlockParser` has the following methods:

* **`parseDocument(lines)`**:

    Given a list of lines, an ElementTree object is returned. This should be
    passed an entire document and is the only method the `Markdown` class
    calls directly.

* **`parseChunk(parent, text)`**:

    Parses a chunk of markdown text composed of multiple blocks and attaches
    those blocks to the `parent` Element. The `parent` is altered in place
    and nothing is returned. Extensions would most likely use this method for
    block parsing.

* **`parseBlocks(parent, blocks)`**:

    Parses a list of blocks of text and attaches those blocks to the `parent`
    Element. The `parent` is altered in place and nothing is returned. This
    method will generally only be used internally to recursively parse nested
    blocks of text.

While it is not recommended, an extension could subclass or completely replace
the `BlockParser`. The new class would have to provide the same public API.
However, be aware that other extensions may expect the core parser provided
and will not work with such a drastically different parser.

## Working with the ElementTree {: #working_with_et }

As mentioned, the Markdown parser converts a source document to an
[ElementTree][ElementTree] object before serializing that back to Unicode text.
Markdown has provided some helpers to ease that manipulation within the context
of the Markdown module.

First, to get access to the ElementTree module import ElementTree from
`markdown` rather than importing it directly. This will ensure you are using
the same version of ElementTree as markdown. The module is found at
`markdown.util.etree` within Markdown.

```python
from markdown.util import etree
```

`markdown.util.etree` tries to import ElementTree from any known location,
first as a standard library module (from `xml.etree` in Python 2.5), then as
a third party package (ElementTree). In each instance, `cElementTree` is
tried first, then ElementTree if the faster C implementation is not
available on your system.

Sometimes you may want text inserted into an element to be parsed by
[Inline Patterns][]. In such a situation, simply insert the text as you normally
would and the text will be automatically run through the Inline Patterns.
However, if you do *not* want some text to be parsed by Inline Patterns,
then insert the text as an `AtomicString`.

```python
from markdown.util import AtomicString
some_element.text = AtomicString(some_text)
```

Here's a basic example which creates an HTML table (note that the contents of
the second cell (`td2`) will be run through Inline Patterns latter):

```python
table = etree.Element("table")
table.set("cellpadding", "2")                      # Set cellpadding to 2
tr = etree.SubElement(table, "tr")                 # Add child tr to table
td1 = etree.SubElement(tr, "td")                   # Add child td1 to tr
td1.text = markdown.util.AtomicString("Cell content") # Add plain text content
td2 = etree.SubElement(tr, "td")                   # Add second td to tr
td2.text = "*text* with **inline** formatting."    # Add markup text
table.tail = "Text after table"                    # Add text after table
```

You can also manipulate an existing tree. Consider the following example which
adds a `class` attribute to `<a>` elements:

```python
def set_link_class(self, element):
    for child in element:
        if child.tag == "a":
              child.set("class", "myclass") #set the class attribute
          set_link_class(child) # run recursively on children
```

For more information about working with ElementTree see the ElementTree
[Documentation](http://effbot.org/zone/element-index.htm)
([Python Docs](http://docs.python.org/lib/module-xml.etree.ElementTree.html)).

## Integrating Your Code Into Markdown {: #integrating_into_markdown }

Once you have the various pieces of your extension built, you need to tell
Markdown about them and ensure that they are run in the proper sequence.
Markdown accepts an `Extension` instance for each extension. Therefore, you
will need to define a class that extends `markdown.extensions.Extension` and
over-rides the `extendMarkdown` method. Within this class you will manage
configuration options for your extension and attach the various processors and
patterns to the Markdown instance.

It is important to note that the order of the various processors and patterns
matters. For example, if we replace `http://...` links with `<a>` elements, and
*then* try to deal with  inline HTML, we will end up with a mess. Therefore, the
various types of processors and patterns are stored within an instance of the
Markdown class in a [Registry][]. Your `Extension` class will need to manipulate
those registries appropriately. You may `register` instances of your processors
and patterns with an appropriate priority, `deregister` built-in instances, or
replace a built-in instance with your own.

### `extendMarkdown` {: #extendmarkdown }

The `extendMarkdown` method of a `markdown.extensions.Extension` class
accepts one argument:

* **`md`**:

    A pointer to the instance of the Markdown class. You should use this to
    access the [Registries][Registry] of processors and patterns. They are
    found under the following attributes:

    * `md.preprocessors`
    * `md.inlinePatterns`
    * `md.parser.blockprocessors`
    * `md.treeprocessors`
    * `md.postprocessors`

    Some other things you may want to access in the markdown instance are:

    * `md.htmlStash`
    * `md.output_formats`
    * `md.set_output_format()`
    * `md.output_format`
    * `md.serializer`
    * `md.registerExtension()`
    * `md.tab_length`
    * `md.block_level_elements`
    * `md.isBlockLevel()`

!!! Warning
    With access to the above items, theoretically you have the option to
    change anything through various [monkey_patching][] techniques. However,
    you should be aware that the various undocumented parts of markdown may
    change without notice and your monkey_patches may break with a new release.
    Therefore, what you really should be doing is inserting processors and
    patterns into the markdown pipeline. Consider yourself warned!

[monkey_patching]: http://en.wikipedia.org/wiki/Monkey_patch

A simple example:

```python
from markdown.extensions import Extension

class MyExtension(Extension):
    def extendMarkdown(self, md):
        # Register instance of 'mypattern' with a priority of 175
        md.inlinePatterns.register(MyPattern(md), 'mypattern', 175)
```

### Registry

The `markdown.util.Registry` class is a priority sorted registry which Markdown
uses internally to determine the processing order of its various processors and
patterns.

A `Registry` instance provides two public methods to alter the data of the
registry: `register` and `deregister`. Use `register` to add items and
`deregister` to remove items. See each method for specifics.

When registering an item, a "name" and a "priority" must be provided. All
items are automatically sorted by the value of the "priority" parameter such
that the item with the highest value will be processed first. The "name" is
used to remove (`deregister`) and get items.

A `Registry` instance is like a list (which maintains order) when reading
data. You may iterate over the items, get an item and get a count (length)
of all items. You may also check that the registry contains an item.

When getting an item you may use either the index of the item or the
string-based "name". For example:

    registry = Registry()
    registry.register(SomeItem(), 'itemname', 20)
    # Get the item by index
    item = registry[0]
    # Get the item by name
    item = registry['itemname']

When checking that the registry contains an item, you may use either the
string-based "name", or a reference to the actual item. For example:

    someitem = SomeItem()
    registry.register(someitem, 'itemname', 20)
    # Contains the name
    assert 'itemname' in registry
    # Contains the item instance
    assert someitem in registry

`markdown.util.Registry` has the following methods:

#### `Registry.register(self, item, name, priority)` {: #registry.register }

:   Add an item to the registry with the given name and priority.

    Parameters:

    * `item`: The item being registered.
    * `name`: A string used to reference the item.
    * `priority`: An integer or float used to sort against all items.

    If an item is registered with a "name" which already exists, the existing
    item is replaced with the new item. Tread carefully as the old item is lost
    with no way to recover it. The new item will be sorted according to its
    priority and will **not** retain the position of the old item.

#### `Registry.deregister(self, name, strict=True)`  {: #registry.deregister }

:   Remove an item from the registry.

    Set `strict=False` to fail silently.

#### `Registry.get_index_for_name(self, name)` {: #registry.get_index_for_name }

:   Return the index of the given `name`.

### registerExtension {: #registerextension }

Some extensions may need to have their state reset between multiple runs of the
Markdown class. For example, consider the following use of the [Footnotes][]
extension:

```python
md = markdown.Markdown(extensions=['footnotes'])
html1 = md.convert(text_with_footnote)
md.reset()
html2 = md.convert(text_without_footnote)
```

Without calling `reset`, the footnote definitions from the first document will
be inserted into the second document as they are still stored within the class
instance. Therefore the `Extension` class needs to define a `reset` method
that will reset the state of the extension (i.e.: `self.footnotes = {}`).
However, as many extensions do not have a need for `reset`, `reset` is only
called on extensions that are registered.

To register an extension, call `md.registerExtension` from within your
`extendMarkdown` method:

```python
def extendMarkdown(self, md):
    md.registerExtension(self)
    # insert processors and patterns here
```

Then, each time `reset` is called on the Markdown instance, the `reset`
method of each registered extension will be called as well. You should also
note that `reset` will be called on each registered extension after it is
initialized the first time. Keep that in mind when over-riding the extension's
`reset` method.

### Configuration Settings {: #configsettings }

If an extension uses any parameters that the user may want to change,
those parameters should be stored in `self.config` of your
`markdown.extensions.Extension` class in the following format:

```python
class MyExtension(markdown.extensions.Extension):
    def __init__(self, **kwargs):
        self.config = {'option1' : ['value1', 'description1'],
                       'option2' : ['value2', 'description2'] }
        super(MyExtension, self).__init__(**kwargs)
```

When implemented this way the configuration parameters can be over-ridden at
run time (thus the call to `super`). For example:

```python
markdown.Markdown(extensions=[MyExtension(option1='other value'])
```

Note that if a keyword is passed in that is not already defined in
`self.config`, then a `KeyError` is raised.

The `markdown.extensions.Extension` class and its subclasses have the
following methods available to assist in working with configuration settings:

* **`getConfig(key [, default])`**:

    Returns the stored value for the given `key` or `default` if the `key`
    does not exist. If not set, `default` returns an empty string.

* **`getConfigs()`**:

    Returns a dict of all key/value pairs.

* **`getConfigInfo()`**:

    Returns all configuration descriptions as a list of tuples.

* **`setConfig(key, value)`**:

    Sets a configuration setting for `key` with the given `value`. If `key` is
    unknown, a `KeyError` is raised. If the previous value of `key` was
    a Boolean value, then `value` is converted to a Boolean value. If
    the previous value of `key` is `None`, then `value` is converted to
    a Boolean value except when it is `None`. No conversion takes place
    when the previous value of `key` is a string.

* **`setConfigs(items)`**:

    Sets multiple configuration settings given a dict of key/value pairs.

### Naming an Extension { #naming_an_extension }

As noted in the [library reference] an instance of an extension can be passed
directly to Markdown. In fact, this is the preferred way to use third-party
extensions.

For example:

```python
import markdown
from path.to.module import MyExtension
md = markdown.Markdown(extensions=[MyExtension(option='value')])
```

However, Markdown also accepts "named" third party extensions for those
occasions when it is impractical to import an extension directly (from the
command line or from within templates). A "name" can either be a registered
[entry point](#entry_point) or a string using Python's [dot
notation](#dot_notation).

#### Entry Point { #entry_point }

[Entry points] are defined in a Python package's `setup.py` script. The script
must use [setuptools] to support entry points. Python-Markdown extensions must
be assigned to the `markdown.extensions` group. An entry point definition might
look like this:

```python
from setuptools import setup

setup(
    # ...
    entry_points={
        'markdown.extensions': ['myextension = path.to.module:MyExtension']
    }
)
```

After a user installs your extension using the above script, they could then
call the extension using the `myextension` string name like this:

```python
markdown.markdown(text, extensions=['myextension'])
```

Note that if two or more entry points within the same group are assigned the
same name, Python-Markdown will only ever use the first one found and ignore all
others. Therefore, be sure to give your extension a unique name.

For more information on writing `setup.py` scripts, see the Python documentation
on [Packaging and Distributing Projects].

#### Dot Notation { #dot_notation }

If an extension does not have a registered entry point, Python's dot notation
may be used instead. The extension must be installed as a Python module on your
PYTHONPATH. Generally, a class should be specified in the name. The class must
be at the end of the name and be separated by a colon from the module.

Therefore, if you were to import the class like this:

```python
from path.to.module import MyExtension
```

Then the extension can be loaded as follows:

```python
markdown.markdown(text, extensions=['path.to.module:MyExtension'])
```

You do not need to do anything special to support this feature. As long as your
extension class is able to be imported, a user can include it with the above
syntax.

The above two methods are especially useful if you need to implement a large
number of extensions with more than one residing in a module. However, if you do
not want to require that your users include the class name in their string, you
must define only one extension per module and that module must contain a
module-level function called `makeExtension` that accepts `**kwargs` and returns
an extension instance.

For example:

```python
class MyExtension(markdown.extensions.Extension)
    # Define extension here...

def makeExtension(**kwargs):
    return MyExtension(**kwargs)
```

When Markdown is passed the "name" of your extension as a dot notation string
that does not include a class (for example `path.to.module`), it will import the
module and call the `makeExtension` function to initiate your extension.

[Preprocessors]: #preprocessors
[Inline Patterns]: #inlinepatterns
[Treeprocessors]: #treeprocessors
[Postprocessors]: #postprocessors
[BlockParser]: #blockparser
[workingwithetree]: #working_with_et
[Integrating your code into Markdown]: #integrating_into_markdown
[extendMarkdown]: #extendmarkdown
[Registry]: #registry
[registerExtension]: #registerextension
[Config Settings]: #configsettings
[makeExtension]: #makeextension
[ElementTree]: http://effbot.org/zone/element-index.htm
[Available Extensions]: index.md
[Footnotes]: https://github.com/Python-Markdown/mdx_footnotes
[Definition Lists]: https://github.com/Python-Markdown/mdx_definition_lists
[library reference]: ../reference.md
[setuptools]: https://packaging.python.org/key_projects/#setuptools
[Entry points]: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins
[Packaging and Distributing Projects]: https://packaging.python.org/tutorials/distributing-packages/
