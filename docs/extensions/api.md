title:      Extensions API

# Writing Extensions for Python-Markdown

Python-Markdown includes an API for extension writers to plug their own custom functionality and syntax into the
parser. An extension will patch into one or more stages of the parser:

* [*Preprocessors*](#preprocessors) alter the source before it is passed to the parser. 
* [*Block Processors*](#blockprocessors) work with blocks of text separated by blank lines.
* [*Tree Processors*](#treeprocessors) modify the constructed ElementTree
* [*Inline Processors*](#inlineprocessors) are common tree processors for inline elements, such as `*strong*`. 
* [*Postprocessors*](#postprocessors) munge of the output of the parser just before it is returned. 

The parser loads text, applies the preprocessors, creates and builds an [ElementTree][ElementTree] object from the
block processors and inline processors, renders the ElementTree object as Unicode text, and then then applies the
postprocessors.

There are classes and helpers provided to ease writing your extension. Each part of the API is discussed in its
respective section below. Additionally, you can walk through the [Tutorial on Writing Extensions][tutorial]; look at
some of the [Available Extensions][] and their [source code][extension source]. As always, you may report bugs, ask
for help, and discuss various other issues on the [bug tracker].

## Phases of processing {: #stages }

### Preprocessors {: #preprocessors }

Preprocessors munge the source text before it is passed to the Markdown parser. This is an excellent place to clean up
bad characters or to extract portions for later processing that the parser may otherwise choke on.

Preprocessors inherit from `markdown.preprocessors.Preprocessor` and implement a `run` method, which takes a single
parameter `lines`. This parameter is the entire source text stored as a list of Unicode strings, one per line.  `run`
should return its processed list of Unicode strings, one per line.

#### Example

This simple example removes any lines with 'NO RENDER' before processing:

```python
from markdown.preprocessors import Preprocessor
import re

class NoRender(Preprocessor):
    """ Skip any line with words 'NO RENDER' in it. """
    def run(self, lines):
        new_lines = []
        for line in lines:
            m = re.search("NO RENDER", line)
            if not m:    
                # any line without NO RENDER is passed through
                new_lines.append(line)  
        return new_lines
```

#### Usages

Some preprocessors in the Markdown source tree include:

| Class                         | Kind      | Description |
| ------------------------------|-----------|------------------------------------------------- |
| [`NormalizeWhiteSpace`][c1]   | built-in  | Normalizes whitespace by expanding tabs, fixing `\r` line endings, etc. |
| [`HtmlBlockPreprocessor`][c2] | built-in  | Removes html blocks from the text and stores them for later processing |
| [`ReferencePreprocessor`][c3] | built-in  | Removes reference definitions from text and stores for later processing |
| [`MetaPreprocessor`][c4]      | extension | Strips and records meta data at top of documents |
| [`FootnotesPreprocessor`][c5] | extension | Removes footnote blocks from the text and stores them for later processing |

[c1]: https://github.com/Python-Markdown/markdown/blob/master/markdown/preprocessors.py
[c2]: https://github.com/Python-Markdown/markdown/blob/master/markdown/preprocessors.py
[c3]: https://github.com/Python-Markdown/markdown/blob/master/markdown/preprocessors.py
[c4]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/meta.py
[c5]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/footnotes.py

### Block Processors {: #blockprocessors }

A block processor parses blocks of text and adds new elements to the `ElementTree`. Blocks of text, separated from
other text by blank lines, may have a different syntax and produce a differently structured tree than other Markdown. 
Block processors excel at code formatting, equation layouts, and tables.

Block processors inherit from `markdown.blockprocessors.BlockProcessor`, are passed `md.parser` on initialization, and
implement both the `test` and `run` methods:  

* `test(self, parent, block)` takes two parameters: `parent` is the parent `ElementTree` element and `block` is a
  single, multi-line, Unicode string of the current block. `test`, often a regular expression match, returns a true
  value if the block processor's `run` method should be called to process starting at that block.  
* `run(self, parent, blocks)` has the same `parent` parameter as `test`; and `blocks` is the list of all remaining
  blocks in the document, starting with the `block` passed to `test`. `run` may return `False` (not `None`) to signal
  failure, meaning that it did not process the blocks after all. On success, `run` is expected to `pop` one or more
  blocks from the front of `blocks` and attach new nodes to `parent`.  

Crafting block processors is more involved and flexible than the other processors, involving controlling recursive
parsing of the block's contents and managing state across invocations. For example, a blank line is allowed in
indented code, so the second invocation of the inline code processor appends to the element tree generated by the
previous call.  Other block processors may insert new text into the `blocks` list, signal to future calls of itself,
and more.

To make writing these complex beasts more tractable, three convenience functions have been provided by the
`BlockProcessor` parent class:

* `lastChild(parent)` returns the last child of the given element or `None` if it has no children.
* `detab(text)` removes one level of indent (four spaces by default) from the front of each line of the given
  multi-line, text string, until a non-blank line is indented less. 
* `looseDetab(text, level)` removes multiple levels
  of indent from the front of each line of `text` but does not affect lines indented less.  

Also, `BlockProcessor` provides the fields `self.tab_length`, the tab length (default 4), and `self.parser`, the
current `BlockParser` instance.  

#### BlockParser

`BlockParser`, not to be confused with `BlockProcessor`, is the class used by Markdown to cycle through all the
registered block processors.  You should never need to create your own instance; use `self.parser` instead.

The `BlockParser` instance provides a stack of strings for its current state, which your processor can push with
`self.parser.set(state)`,  pop with `self.parser.reset()`, or check the the top state with
`self.parser.isstate(state)`. Be sure your code pops the states it pushes.

The `BlockParser` instance can also be called recursively, that is, to process blocks from within your block
processor.  There are three methods:

* `parseDocument(lines)` parses a list of lines, each a single-line Unicode string, returning a complete
  `ElementTree`.
* `parseChunk(parent, text)` parses a single, multi-line, possibly multi-block, Unicode string `text` and attaches the
  resulting tree to `parent`.  
* `parseBlocks(parent, blocks)` takes a list of `blocks`, each a multi-line Unicode string without blank lines, and
  attaches the resulting tree to `parent`.   

For perspective, Markdown calls `parseDocument` which calls `parseChunk` which calls `parseBlocks` which calls your
block processor, which, in turn, might call one of these routines.

#### Example

This example calls out important paragraphs by giving them a border.  It looks for a fence line of exclamation points
before and after and renders the fenced blocks into a new, styled `div`.  If it does not find the ending fence line,
it does nothing.  

Our code, like most block processors, is longer than other examples:

```python
def test_block_processor():
    class BoxBlockProcessor(BlockProcessor):
        RE_FENCE_START = r'^ *!{3,} *\n' # start line, e.g., `   !!!! `
        RE_FENCE_END = r'\n *!{3,}\s*$'  # last non-blank line, e.g, '!!!\n  \n\n'

        def test(self, parent, block):
            return re.match(self.RE_FENCE_START, block)

        def run(self, parent, blocks):
            original_block = blocks[0]
            blocks[0] = re.sub(self.RE_FENCE_START, '', blocks[0])

            # Find block with ending fence
            for block_num, block in enumerate(blocks):
                if re.search(self.RE_FENCE_END, block):
                    # remove fence
                    blocks[block_num] = re.sub(self.RE_FENCE_END, '', block)
                    # render fenced area inside a new div
                    e = etree.SubElement(parent, 'div')
                    e.set('style', 'display: inline-block; border: 1px solid red;')
                    self.parser.parseBlocks(e, blocks[0:block_num + 1])
                    # remove used blocks
                    for i in range(0, block_num + 1):
                        blocks.pop(0)
                    return True  # or could have had no return statement
            # No closing marker!  Restore and do nothing
            blocks[0] = original_block
            return False  # equivalent to our test() routine returning False

    class BoxExtension(Extension):
        def extendMarkdown(self, md):
            md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), 'box', 175)
```

Start with this example input:

``` text
A regular paragraph of text.

!!!!!
First paragraph of wrapped text.

Second Paragraph of **wrapped** text.
!!!!!

Another regular paragraph of text.
```

The fenced text adds one node with two children to the tree:

* `div`, with a `style` attribute.  It renders as 
  `<div style="display: inline-block; border: 1px solid red;">...</div>`
    * `p` with text `First paragraph of wrapped text.`
    * `p` with text `Second Paragraph of **wrapped** text`.  The conversion to a `<strong>` tag will happen when
      running the inline processors, which will happen after all of the block processors have completed.

The example output might display as follows:

!!! note ""
    <p>A regular paragraph of text.</p>
    <div style="display: inline-block; border: 1px solid red;">
    <p>First paragraph of wrapped text.</p>
    <p>Second Paragraph of **wrapped** text.</p>
    </div>
    <p>Another regular paragraph of text.</p>

#### Usages

Some block processors in the Markdown source tree include:

| Class                       | Kind      |  Description                                |
| ----------------------------|-----------|---------------------------------------------|
| [`HashHeaderProcessor`][b1] | built-in  |  Title hashes (`#`), which may split blocks |
| [`HRProcessor`][b2]         | built-in  |  Horizontal lines, e.g., `---`              |
| [`OListProcessor`][b3]      | built-in  |  Ordered lists; complex and using `state`   |
| [`Admonition`][b4]          | extension |  Render each [Admonition][] in a new `div`  |

[b1]: https://github.com/Python-Markdown/markdown/blob/master/markdown/blockprocessors.py
[b2]: https://github.com/Python-Markdown/markdown/blob/master/markdown/blockprocessors.py
[b3]: https://github.com/Python-Markdown/markdown/blob/master/markdown/blockprocessors.py
[Admonition]: https://python-markdown.github.io/extensions/admonition/
[b4]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/admonition.py

### Tree processors {: #treeprocessors }

Tree processors manipulate the tree created by block processors.  They can even create an entirely new ElementTree
object. This is an excellent place for creating summaries, adding collected references, or last minute adjustments.

A tree processor must inherit from `markdown.treeprocessors.Treeprocessor` (note the capitalization). A tree processor
must implement a `run` method which takes a single argument `root`. In most cases `root` would be an
`xml.etree.ElementTree.Element` instance; however, in rare cases it could be some other type of ElementTree object.
The `run` method may return `None`, in which case the (possibly modified) original `root` object is used, or it may
return an entirely new `Element` object, which will replace the existing `root` object and all of its children.  It is
generally preferred to modify `root` in place and return `None`, which avoids creating multiple copies of the entire
document tree in memory.

For specifics on manipulating the ElementTree, see [Working with the ElementTree][workingwithetree] below.

#### Example

A pseudo example:

```python
from markdown.treeprocessors import Treeprocessor

class MyTreeprocessor(Treeprocessor):
    def run(self, root):
        root.text = 'modified content'
        # No return statement is same as `return None`
```

#### Usages

The  core `InlineProcessor` class is a tree processor.  It walks the tree, matches patterns, and splits and creates
nodes on matches.

Additional tree processors in the Markdown source tree include:

| Class                             | Kind      | Description                                                   |
| ----------------------------------|-----------|---------------------------------------------------------------|
| [`PrettifyTreeprocessor`][e1]     | built-in  |  Add line breaks to the html document                         |
| [`TocTreeprocessor`][e2]          | extension |  Builds a [table of contents][] from the finished tree        |
| [`FootnoteTreeprocessor`][e3]     | extension |  Create [footnote][] div at end of document                   |
| [`FootnotePostTreeprocessor`][e4] | extension |  Amend div created by `FootnoteTreeprocessor` with duplicates |

[e1]: https://github.com/Python-Markdown/markdown/blob/master/markdown/treeprocessors.py
[e2]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/toc.py
[e3]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/footnotes.py
[e4]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/footnotes.py
[table of contents]: https://python-markdown.github.io/extensions/toc/
[footnote]: https://python-markdown.github.io/extensions/footnotes/

### Inline Processors {: #inlineprocessors }

Inline processors, previously called inline patterns, are used to add formatting, such as `**emphasis**`, by replacing
a matched pattern with a new element tree node. It is an excellent for adding new syntax for inline tags.  Inline
processor code is often quite short.

Inline processors inherit from `InlineProcessor`, are initialized, and implement `handleMatch`:

*   `__init__(self, pattern, md=None)` is the inherited constructor.  You do not need to implement your own.
    * `pattern` is the regular expression string that must match the code block in order for the `handleMatch` method
      to be called.   
    * `md`, an optional parameter, is a pointer to the instance of `markdown.Markdown` and is available as `self.md`
      on the `InlineProcessor` instance.

*   `handleMatch(self, m, data)` must be implemented in all `InlineProcessor` subclasses.
    * `m` is the regular expression [match object][] found by the `pattern` passed to `__init__`.   
    * `data` is a single, multi-line, Unicode string containing the entire block of text around the pattern.  A block
      is text set apart by blank lines.  
    * Returns either `(None, None, None)`, indicating the provided match was rejected or `(el, start, end)`, if the
      match was successfully processed.  On success, `el` is the element being added the tree, `start` and `end` are
      indexes in `data` that were "consumed" by the pattern.  The "consumed" span will be replaced by a placeholder.
      The same inline processor may be called several times on the same block.

Inline Processors can define the property `ANCESTOR_EXCLUDES` which is either a list or tuple of undesirable ancestors.
The processor will be skipped if it would cause the content to be a descendant of one of the listed tag names.

##### Convenience Classes

Convenience subclasses of `InlineProcessor` are provide for common operations:

* [`SimpleTextInlineProcessor`][i1] returns the text of `group(1)` of the match.
* [`SubstituteTagInlineProcessor`][i4] is initialized as `SubstituteTagInlineProcessor(pattern, tag)`. It returns a
  new element `tag` whenever `pattern` is matched.
* [`SimpleTagInlineProcessor`][i3] is initialized as `SimpleTagInlineProcessor(pattern, tag)`. It returns an element
  `tag` with a text field of `group(2)` of the match.

##### Example

This example changes `--strike--` to `<del>strike</del>`.

```python
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension
import xml.etree.ElementTree as etree


class DelInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        el = etree.Element('del')
        el.text = m.group(1)
        return el, m.start(0), m.end(0)

class DelExtension(Extension):
    def extendMarkdown(self, md):
        DEL_PATTERN = r'--(.*?)--'  # like --del--
        md.inlinePatterns.register(DelInlineProcessor(DEL_PATTERN, md), 'del', 175)
```

Use this input example:

``` text
First line of the block.
This is --strike one--.
This is --strike two--.
End of the block.
```

The example output might display as follows:

!!! note ""
    <p>First line of the block.
    This is <del>strike one</del>.
    This is <del>strike two</del>.
    End of the block.</p>

* On the first call to `handleMatch`
    * `m` will be the match for `--strike one--`
    * `data` will be the string:
      `First line of the block.\nThis is --strike one--.\nThis is --strike two--.\nEnd of the block.`

    Because the match was successful, the region between the returned `start` and `end` are replaced with a
    placeholder token and the new element is added to the tree.    

* On the second call to `handleMatch`
    * `m` will be the match for `--strike two--` 
    * `data` will be the string
      `First line of the block.\nThis is klzzwxh:0000.\nThis is --strike two--.\nEnd of the block.`

Note the placeholder token `klzzwxh:0000`. This allows the regular expression to be run against the entire block,
not just the the text contained in an individual element. The placeholders will later be swapped back out for the
actual elements by the parser.

Actually it would not be necessary to create the above inline processor. The fact is, that example is not very DRY
(Don't Repeat Yourself). A pattern for `**strong**` text would be almost identical, with the exception that it would
create a `strong` element. Therefore, Markdown provides a number of generic `InlineProcessor` subclasses that can
provide some common functionality. For example, strike could be implemented with an instance of the
`SimpleTagInlineProcessor` class as demonstrated below. Feel free to use or extend any of the `InlineProcessor`
subclasses found at `markdown.inlinepatterns`.

```python
from markdown.inlinepatterns import SimpleTagInlineProcessor
from markdown.extensions import Extension

class DelExtension(Extension):
    def extendMarkdown(self, md):
        md.inlinePatterns.register(SimpleTagInlineProcessor(r'()--(.*?)--', 'del'), 'del', 175)
```


##### Usages

Here are some convenience functions and other examples:

| Class                            | Kind      | Description                                                   |
| ---------------------------------|-----------|---------------------------------------------------------------|
| [`AsteriskProcessor`][i5]        | built-in  | Emphasis processor for handling strong and em matches inside asterisks |
| [`AbbrInlineProcessor`][i6]      | extension | Apply tag to abbreviation registered by preprocessor          |
| [`WikiLinksInlineProcessor`][i7] | extension | Link `[[article names]]` to wiki given in metadata            |
| [`FootnoteInlineProcessor`][i8]  | extension | Replaces footnote in text with link to footnote div at bottom |

[i1]: https://github.com/Python-Markdown/markdown/blob/master/markdown/inlinepatterns.py
[i2]: https://github.com/Python-Markdown/markdown/blob/master/markdown/inlinepatterns.py
[i3]: https://github.com/Python-Markdown/markdown/blob/master/markdown/inlinepatterns.py
[i4]: https://github.com/Python-Markdown/markdown/blob/master/markdown/inlinepatterns.py
[i5]: https://github.com/Python-Markdown/markdown/blob/master/markdown/inlinepatterns.py
[i6]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/abbr.py
[i7]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/wikilinks.py
[i8]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/footnotes.py

### Patterns

In version 3.0, a new, more flexible inline processor was added, `markdown.inlinepatterns.InlineProcessor`.   The
original inline patterns, which inherit from `markdown.inlinepatterns.Pattern` or one of its children are still
supported, though users are encouraged to migrate.

#### Comparison with new `InlineProcessor`

The new `InlineProcessor` provides two major enhancements to `Patterns`:

1. Inline Processors no longer need to match the entire block, so regular expressions no longer need to start with
   `r'^(.*?)'` and end with `r'(.*?)%'`. This runs faster. The returned [match object][] will only contain what is
   explicitly matched in the pattern, and extension pattern groups now start with `m.group(1)`.

2.  The `handleMatch` method now takes an additional input called `data`, which is the entire block under analysis,
    not just what is matched with the specified pattern. The method now returns the element *and* the indexes relative
    to `data` that the return element is replacing (usually `m.start(0)` and `m.end(0)`).  If the boundaries are
    returned as `None`, it is assumed that the match did not take place, and nothing will be altered in `data`.

    This allows handling of more complex constructs than regular expressions can handle, e.g., matching nested
    brackets, and explicit control of the span "consumed" by the processor.
    
#### Inline Patterns

Inline Patterns can implement inline HTML element syntax for Markdown such as `*emphasis*` or
`[links](http://example.com)`. Pattern objects should be instances of classes that inherit from
`markdown.inlinepatterns.Pattern` or one of its children. Each pattern object uses a single regular expression and
must have the following methods:

* **`getCompiledRegExp()`**:

    Returns a compiled regular expression.

* **`handleMatch(m)`**:

    Accepts a match object and returns an ElementTree element of a plain Unicode string.

Inline Patterns can define the property `ANCESTOR_EXCLUDES` with is either a list or tuple of undesirable ancestors.
The pattern will be skipped if it would cause the content to be a descendant of one of the listed tag names.

Note that any regular expression returned by `getCompiledRegExp` must capture the whole block. Therefore, they should
all start with `r'^(.*?)'` and end with `r'(.*?)!'`. When using the default `getCompiledRegExp()` method provided in
the `Pattern` you can pass in a regular expression without that and `getCompiledRegExp` will wrap your expression for
you and set the `re.DOTALL` and `re.UNICODE` flags. This means that the first group of your match will be `m.group(2)`
as `m.group(1)` will match everything before the pattern.

For an example, consider this simplified emphasis pattern:

```python
from markdown.inlinepatterns import Pattern
import xml.etree.ElementTree as etree

class EmphasisPattern(Pattern):
    def handleMatch(self, m):
        el = etree.Element('em')
        el.text = m.group(2)
        return el
```

As discussed in [Integrating Your Code Into Markdown][], an instance of this class will need to be provided to
Markdown. That instance would be created like so:

```python
# an oversimplified regex
MYPATTERN = r'\*([^*]+)\*'
# pass in pattern and create instance
emphasis = EmphasisPattern(MYPATTERN)
```

### Postprocessors {: #postprocessors }

Postprocessors munge the document after the ElementTree has been serialized into a string. Postprocessors should be
used to work with the text just before output.  Usually, they are used add back sections that were extracted in a
preprocessor, fix up outgoing encodings, or wrap the whole document.

Postprocessors inherit from `markdown.postprocessors.Postprocessor` and implement a `run` method which takes a single
parameter `text`, the entire HTML document as a single Unicode string.  `run` should return a single Unicode string
ready for output.  Note that preprocessors use a list of lines while postprocessors use a single multi-line string.

#### Example

Here is a simple example that changes the output to one big page showing the raw html.

```python
from markdown.postprocessors import Postprocessor
import re

class ShowActualHtmlPostprocesor(Postprocessor):
    """ Wrap entire output in <pre> tags as a diagnostic. """
    def run(self, text):
        return '<pre>\n' + re.sub('<', '&lt;', text) + '</pre>\n'
```

#### Usages

Some postprocessors in the Markdown source tree include:

| Class                         | Kind      |  Description                                       |
| ------------------------------|-----------|----------------------------------------------------|
| [`raw_html`][p1]              | built-in  | Restore raw html from `htmlStash`, stored by `HTMLBlockPreprocessor`, and code highlighters |
| [`amp_substitute`][p2]        | built-in  | Convert ampersand substitutes to `&`; used in links |
| [`unescape`][p3]              | built-in  | Convert some escaped characters back from integers; used in links |
| [`FootnotePostProcessor`][p4] | extension | Replace footnote placeholders with html entities; as set by other stages |
 
 [p1]: https://github.com/Python-Markdown/markdown/blob/master/markdown/postprocessors.py
 [p2]: https://github.com/Python-Markdown/markdown/blob/master/markdown/postprocessors.py
 [p3]: https://github.com/Python-Markdown/markdown/blob/master/markdown/postprocessors.py
 [p4]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/footnotes.py
 

## Working with the ElementTree {: #working_with_et }

As mentioned, the Markdown parser converts a source document to an [ElementTree][ElementTree] object before
serializing that back to Unicode text. Markdown has provided some helpers to ease that manipulation within the context
of the Markdown module.

First, import the ElementTree module:

```python
import xml.etree.ElementTree as etree
```
Sometimes you may want text inserted into an element to be parsed by [Inline Patterns][]. In such a situation, simply
insert the text as you normally would and the text will be automatically run through the Inline Patterns. However, if
you do *not* want some text to be parsed by Inline Patterns, then insert the text as an `AtomicString`.

```python
from markdown.util import AtomicString
some_element.text = AtomicString(some_text)
```

Here's a basic example which creates an HTML table (note that the contents of the second cell (`td2`) will be run
through Inline Patterns latter):

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

You can also manipulate an existing tree. Consider the following example which adds a `class` attribute to `<a>`
elements:

```python
def set_link_class(self, element):
    for child in element:
        if child.tag == "a":
              child.set("class", "myclass") #set the class attribute
        set_link_class(child) # run recursively on children
```

For more information about working with ElementTree see the [ElementTree
Documentation][ElementTree].

## Working with Raw HTML {: #working_with_raw_html }

Occasionally an extension may need to call out to a third party library which returns a pre-made string
of raw HTML that needs to be inserted into the document unmodified. Raw strings can be stashed for later
retrieval using an `htmlStash` instance, rather than converting them into `ElementTree` objects. A raw string
(which may or may not be raw HTML) passed to `self.md.htmlStash.store()` will be saved to the stash and a
placeholder string will be returned which should be inserted into the tree instead. After the tree is
serialized, a postprocessor will replace the placeholder with the raw string. This prevents subsequent
processing steps from modifying the HTML data. For example,

```python
html = "<p>This is some <em>raw</em> HTML data</p>"
el = etree.Element("div")
el.text = self.md.htmlStash.store(html)
```

For the global `htmlStash` instance to be available from a processor, the `markdown.Markdown` instance must
be passed to the processor from [extendMarkdown](#extendmarkdown) and will be available as `self.md.htmlStash`.

## Integrating Your Code Into Markdown {: #integrating_into_markdown }

Once you have the various pieces of your extension built, you need to tell Markdown about them and ensure that they
are run in the proper sequence. Markdown accepts an `Extension` instance for each extension. Therefore, you will need
to define a class that extends `markdown.extensions.Extension` and over-rides the `extendMarkdown` method. Within this
class you will manage configuration options for your extension and attach the various processors and patterns to the
Markdown instance.

It is important to note that the order of the various processors and patterns matters. For example, if we replace
`http://...` links with `<a>` elements, and *then* try to deal with  inline HTML, we will end up with a mess.
Therefore, the various types of processors and patterns are stored within an instance of the `markdown.Markdown` class
in a [Registry][]. Your `Extension` class will need to manipulate those registries appropriately. You may `register`
instances of your processors and patterns with an appropriate priority, `deregister` built-in instances, or replace a
built-in instance with your own.

### `extendMarkdown` {: #extendmarkdown }

The `extendMarkdown` method of a `markdown.extensions.Extension` class accepts one argument:

* **`md`**:

    A pointer to the instance of the `markdown.Markdown` class. You should use this to access the
    [Registries][Registry] of processors and patterns. They are found under the following attributes:

    * `md.preprocessors`
    * `md.inlinePatterns`
    * `md.parser.blockprocessors`
    * `md.treeprocessors`
    * `md.postprocessors`

    Some other things you may want to access on the `markdown.Markdown` instance are:

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
    With access to the above items, theoretically you have the option to change anything through various
    [monkey_patching][] techniques. However, you should be aware that the various undocumented parts of Markdown may
    change without notice and your monkey_patches may break with a new release. Therefore, what you really should be
    doing is inserting processors and patterns into the Markdown pipeline. Consider yourself warned!

[monkey_patching]: https://en.wikipedia.org/wiki/Monkey_patch

A simple example:

```python
from markdown.extensions import Extension

class MyExtension(Extension):
    def extendMarkdown(self, md):
        # Register instance of 'mypattern' with a priority of 175
        md.inlinePatterns.register(MyPattern(md), 'mypattern', 175)
```

### registerExtension {: #registerextension }

Some extensions may need to have their state reset between multiple runs of the `markdown.Markdown` class. For
example, consider the following use of the [Footnotes][] extension:

```python
md = markdown.Markdown(extensions=['footnotes'])
html1 = md.convert(text_with_footnote)
md.reset()
html2 = md.convert(text_without_footnote)
```

Without calling `reset`, the footnote definitions from the first document will be inserted into the second document as
they are still stored within the class instance. Therefore the `Extension` class needs to define a `reset` method that
will reset the state of the extension (i.e.: `self.footnotes = {}`). However, as many extensions do not have a need
for `reset`, `reset` is only called on extensions that are registered.

To register an extension, call `md.registerExtension` from within your `extendMarkdown` method:

```python
def extendMarkdown(self, md):
    md.registerExtension(self)
    # insert processors and patterns here
```

Then, each time `reset` is called on the `markdown.Markdown` instance, the `reset` method of each registered extension
will be called as well. You should also note that `reset` will be called on each registered extension after it is
initialized the first time. Keep that in mind when over-riding the extension's `reset` method.

### Configuration Settings {: #configsettings }

If an extension uses any parameters that the user may want to change, those parameters should be stored in
`self.config` of your `markdown.extensions.Extension` class in the following format:

```python
class MyExtension(markdown.extensions.Extension):
    def __init__(self, **kwargs):
        self.config = {
            'option1' : ['value1', 'description1'],
            'option2' : ['value2', 'description2']
        }
        super(MyExtension, self).__init__(**kwargs)
```

When implemented this way the configuration parameters can be over-ridden at run time (thus the call to `super`). For
example:

```python
markdown.Markdown(extensions=[MyExtension(option1='other value')])
```

Note that if a keyword is passed in that is not already defined in `self.config`, then a `KeyError` is raised.

The `markdown.extensions.Extension` class and its subclasses have the following methods available to assist in working
with configuration settings:

* **`getConfig(key [, default])`**:

    Returns the stored value for the given `key` or `default` if the `key` does not exist. If not set, `default`
    returns an empty string.

* **`getConfigs()`**:

    Returns a dict of all key/value pairs.

* **`getConfigInfo()`**:

    Returns all configuration descriptions as a list of tuples.

* **`setConfig(key, value)`**:

    Sets a configuration setting for `key` with the given `value`. If `key` is unknown, a `KeyError` is raised. If the
    previous value of `key` was a Boolean value, then `value` is converted to a Boolean value. If the previous value
    of `key` is `None`, then `value` is converted to a Boolean value except when it is `None`. No conversion takes
    place when the previous value of `key` is a string.

* **`setConfigs(items)`**:

    Sets multiple configuration settings given a dict of key/value pairs.

### Naming an Extension { #naming_an_extension }

As noted in the [library reference] an instance of an extension can be passed directly to `markdown.Markdown`. In
fact, this is the preferred way to use third-party extensions.

For example:

```python
import markdown
from path.to.module import MyExtension
md = markdown.Markdown(extensions=[MyExtension(option='value')])
```

However, Markdown also accepts "named" third party extensions for those occasions when it is impractical to import an
extension directly (from the command line or from within templates). A "name" can either be a registered [entry
point](#entry_point) or a string using Python's [dot notation](#dot_notation).

#### Entry Point { #entry_point }

[Entry points] are defined in a Python package's `setup.py` script. The script must use [setuptools] to support entry
points. Python-Markdown extensions must be assigned to the `markdown.extensions` group. An entry point definition
might look like this:

```python
from setuptools import setup

setup(
    # ...
    entry_points={
        'markdown.extensions': ['myextension = path.to.module:MyExtension']
    }
)
```

After a user installs your extension using the above script, they could then call the extension using the
`myextension` string name like this:

```python
markdown.markdown(text, extensions=['myextension'])
```

Note that if two or more entry points within the same group are assigned the same name, Python-Markdown will only ever
use the first one found and ignore all others. Therefore, be sure to give your extension a unique name.

For more information on writing `setup.py` scripts, see the Python documentation on [Packaging and Distributing
Projects].

#### Dot Notation { #dot_notation }

If an extension does not have a registered entry point, Python's dot notation may be used instead. The extension must
be installed as a Python module on your PYTHONPATH. Generally, a class should be specified in the name. The class must
be at the end of the name and be separated by a colon from the module.

Therefore, if you were to import the class like this:

```python
from path.to.module import MyExtension
```

Then the extension can be loaded as follows:

```python
markdown.markdown(text, extensions=['path.to.module:MyExtension'])
```

You do not need to do anything special to support this feature. As long as your extension class is able to be
imported, a user can include it with the above syntax.

The above two methods are especially useful if you need to implement a large number of extensions with more than one
residing in a module. However, if you do not want to require that your users include the class name in their string,
you must define only one extension per module and that module must contain a module-level function called
`makeExtension` that accepts `**kwargs` and returns an extension instance.

For example:

```python
class MyExtension(markdown.extensions.Extension)
    # Define extension here...

def makeExtension(**kwargs):
    return MyExtension(**kwargs)
```

When `markdown.Markdown` is passed the "name" of your extension as a dot notation string that does not include a class
(for example `path.to.module`), it will import the module and call the `makeExtension` function to initiate your
extension.

## Registries

The `markdown.util.Registry` class is a priority sorted registry which Markdown uses internally to determine the
processing order of its various processors and patterns.

A `Registry` instance provides two public methods to alter the data of the registry: `register` and `deregister`. Use
`register` to add items and `deregister` to remove items. See each method for specifics.

When registering an item, a "name" and a "priority" must be provided. All items are automatically sorted by the value
of the "priority" parameter such that the item with the highest value will be processed first. The "name" is used to
remove (`deregister`) and get items.

A `Registry` instance is like a list (which maintains order) when reading data. You may iterate over the items, get an
item and get a count (length) of all items. You may also check that the registry contains an item.

When getting an item you may use either the index of the item or the string-based "name". For example:

```python
registry = Registry()
registry.register(SomeItem(), 'itemname', 20)
# Get the item by index
item = registry[0]
# Get the item by name
item = registry['itemname']
```

When checking that the registry contains an item, you may use either the string-based "name", or a reference to the
actual item. For example:

```python
someitem = SomeItem()
registry.register(someitem, 'itemname', 20)
# Contains the name
assert 'itemname' in registry
# Contains the item instance
assert someitem in registry
```

`markdown.util.Registry` has the following methods:

### `Registry.register(self, item, name, priority)` {: #registry.register data-toc-label='Registry.register'}

:   Add an item to the registry with the given name and priority.

    Parameters:

    * `item`: The item being registered.
    * `name`: A string used to reference the item.
    * `priority`: An integer or float used to sort against all items.

    If an item is registered with a "name" which already exists, the existing item is replaced with the new item.
    Tread carefully as the old item is lost with no way to recover it. The new item will be sorted according to its
    priority and will **not** retain the position of the old item.

### `Registry.deregister(self, name, strict=True)`  {: #registry.deregister data-toc-label='Registry.deregister'}

:   Remove an item from the registry.

    Set `strict=False` to fail silently.

### `Registry.get_index_for_name(self, name)` {: #registry.get_index_for_name data-toc-label='Registry.get_index_for_name'}

:   Return the index of the given `name`.

[match object]: https://docs.python.org/3/library/re.html#match-objects
[bug tracker]: https://github.com/Python-Markdown/markdown/issues
[extension source]:  https://github.com/Python-Markdown/markdown/tree/master/markdown/extensions
[tutorial]: https://github.com/Python-Markdown/markdown/wiki/Tutorial:-Writing-Extensions-for-Python-Markdown
[workingwithetree]: #working_with_et
[Integrating your code into Markdown]: #integrating_into_markdown
[extendMarkdown]: #extendmarkdown
[Registry]: #registry
[registerExtension]: #registerextension
[Config Settings]: #configsettings
[makeExtension]: #makeextension
[ElementTree]: https://docs.python.org/3/library/xml.etree.elementtree.html
[Available Extensions]: index.md
[Footnotes]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/footnotes.py
[Definition Lists]: https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/definition_lists
[library reference]: ../reference.md
[setuptools]: https://packaging.python.org/key_projects/#setuptools
[Entry points]: https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins
[Packaging and Distributing Projects]: https://packaging.python.org/tutorials/distributing-packages/
