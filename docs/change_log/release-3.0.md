title: Release Notes for v3.0

# Python-Markdown 3.0 Release Notes

We are pleased to release Python-Markdown 3.0 which adds a few new features and
fixes various bugs and deprecates various old features. See the list of changes
below for details.

Python-Markdown version 3.0 supports Python versions 2.7, 3.4, 3.5, 3.6, 3.7,
PyPy and PyPy3.

## Backwards-incompatible changes

### `enable_attributes` keyword deprecated

The `enable_attributes` keyword is deprecated in version 3.0 and will be
ignored. Previously the keyword was `True` by default and enabled an
undocumented way to define attributes on document elements. The feature has been
removed from version 3.0. As most users did not use the undocumented feature, it
should not affect most users. For the few who did use the feature, it can be
enabled by using the [Legacy Attributes](../extensions/legacy_attrs.md)
extension.

### `smart_emphasis` keyword and `smart_strong` extension deprecated

The `smart_emphasis` keyword is deprecated in version 3.0 and will be ignored.
Previously the keyword was `True` by default and caused the parser to ignore
middle-word emphasis. Additionally, the optional `smart_strong` extension
provided the same behavior for strong emphasis. Both of those features are now
part of the default behavior, and the [Legacy
Emphasis](../extensions/legacy_em.md) extension is available to disable that
behavior.

### `output_formats` simplified to `html` and `xhtml`.

The `output_formats` keyword now only accepts two options: `html` and `xhtml`
Note that if `(x)html1`, `(x)html4` or `(x)html5` are passed in, the number is
stripped and ignored.

### `safe_mode` and `html_replacement_text` keywords deprecated

Both `safe_mode` and the associated `html_replacement_text` keywords are
deprecated in version 3.0 and will be ignored. The so-called "safe mode" was
never actually "safe" which has resulted in many people having a false sense of
security when using it. As an alternative, the developers of Python-Markdown
recommend that any untrusted content be passed through an HTML sanitizer (like
[Bleach]) after being converted to HTML by markdown. In fact, [Bleach Whitelist]
provides a curated list of tags, attributes, and styles suitable for filtering
user-provided HTML using bleach.

If your code previously looked like this:

```python
html = markdown.markdown(text, safe_mode=True)
```

Then it is recommended that you change your code to read something like this:

```python
import bleach
from bleach_whitelist import markdown_tags, markdown_attrs
html = bleach.clean(markdown.markdown(text), markdown_tags, markdown_attrs)
```

If you are not interested in sanitizing untrusted text, but simply desire to
escape raw HTML, then that can be accomplished through an extension which
removes HTML parsing:

```python
from markdown.extensions import Extension

class EscapeHtml(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')

html = markdown.markdown(text, extensions=[EscapeHtml()])
```

As the HTML would not be parsed with the above Extension, then the serializer
will escape the raw HTML, which is exactly what happened in previous versions
with `safe_mode="escape"`.

[Bleach]: https://bleach.readthedocs.io/
[Bleach Whitelist]: https://github.com/yourcelf/bleach-whitelist

### Positional arguments deprecated

Positional arguments on the `markdown.Markdown()` class are deprecated as are
all except the `text` argument on the `markdown.markdown()` wrapper function.
Using positional arguments will raise an error. Only keyword arguments should be
used. For example, if your code previously looked like this:

```python
html = markdown.markdown(text, [SomeExtension()])
```

Then it is recommended that you change it to read something like this:

```python
html = markdown.markdown(text, extensions=[SomeExtension()])
```

!!! Note
    This change is being made as a result of deprecating `"safe_mode"` as the
    `safe_mode` argument was one of the positional arguments. When that argument
    is removed, the two arguments following it will no longer be at the correct
    position. It is recommended that you always use keywords when they are
    supported for this reason.

### Extension name behavior has changed

In previous versions of Python-Markdown, the built-in extensions received
special status and did not require the full path to be provided. Additionally,
third party extensions whose name started with `"mdx_"` received the same
special treatment. This is no longer the case.

Support has been added for extensions to define an [entry
point](../extensions/api.md#entry_point). An entry point is a string name which
can be used to point to an `Extension` class. The built-in extensions now have
entry points which match the old short names. And any third-party extensions
which define entry points can now get the same behavior. See the documentation
for each specific extension to find the assigned name.

If an extension does not define an entry point, then the full path to the
extension must be used. See the [documentation](../reference.md#extensions) for
a full explanation of the current behavior.

### Extension configuration as part of extension name deprecated

The previously documented method of appending the extension configuration
options as a string to the extension name is deprecated and will raise an error.
The [`extension_configs`](../reference.md#extension_configs) keyword should be
used instead. See the [documentation](../reference.md#extension_configs) for a
full explanation of the current behavior.

### HeaderId extension deprecated

The HeaderId Extension is deprecated and will raise an error if specified. Use
the [Table of Contents](../extensions/toc.md) Extension instead, which offers
most of the features of the HeaderId Extension and more (support for meta data
is missing).

Extension authors who have been using the `slugify` and `unique` functions
defined in the HeaderId Extension should note that those functions are now
defined in the Table of Contents extension and should adjust their import
statements accordingly (`from markdown.extensions.toc import slugify, unique`).

###  Homegrown `OrderedDict` has been replaced with a purpose-built `Registry`

All processors and patterns now get "registered" to a
[Registry](../extensions/api.md#registry). A backwards compatible shim is
included so that existing simple extensions should continue to work.
A `DeprecationWarning` will be raised for any code which calls the old API.

### Markdown class instance references.

Previously, instances of the `Markdown` class were represented as any one of
`md`, `md_instance`, or `markdown`. This inconsistency made it difficult when
developing extensions, or just maintaining the existing code. Now, all instances
are consistently represented as `md`.

The old attributes on class instances still exist, but raise a
`DeprecationWarning` when accessed. Also on classes where the instance was
optional, the attribute always exists now and is simply `None` if no instance
was provided (previously the attribute would not exist).

### `markdown.util.isBlockLevel` deprecated

The `markdown.util.isBlockLevel` function is deprecated and will raise a
`DeprecationWarning`. Instead, extensions should use the `isBlockLevel` method
of the `Markdown` class instance. Additionally, a list of block level elements
is defined in the `block_level_elements` attribute of the `Markdown` class which
extensions can access to alter the list of elements which are treated as block
level elements.

### `md_globals` keyword deprecated from extension API

Previously, the `extendMarkdown` method of a `markdown.extensions.Extension`
subclasses accepted an `md_globals` keyword, which contained the value returned
by Python's `globals()` built-in function. As all of the configuration is now
held within the `Markdown` class instance, access to the globals is no longer
necessary and any extensions which expect the keyword will raise a
`DeprecationWarning`. A future release will raise an error.

### `markdown.version` and `markdown.version_info` deprecated

Historically, version numbers were acquired via the attributes
`markdown.version` and `markdown.version_info`. Moving forward, a more
standardized approach is being followed and versions are acquired via the
`markdown.__version__` and `markdown.__version_info__` attributes.  The legacy
attributes are still available to allow distinguishing versions between the
legacy Markdown 2.0 series and the Markdown 3.0 series, but in the future the
legacy attributes will be removed.

### Added new, more flexible `InlineProcessor` class

A new `InlineProcessor` class handles inline processing much better and allows
for more flexibility. The new `InlineProcessor` classes no longer utilize
unnecessary pretext and post-text captures. New class can accept the buffer that
is being worked on and manually process the text without regular expressions and
return new replacement bounds. This helps us to handle links in a better way and
handle nested brackets and logic that is too much for regular expression.

## New features

The following new features have been included in the release:

* A new [testing framework](../test_tools.md) is included as a part of the
  Markdown library, which can also be used by third party extensions.

* A new `toc_depth` parameter has been added to the
  [Table of Contents Extension](../extensions/toc.md).

* A new `toc_tokens` attribute has been added to the Markdown class by the
  [Table of Contents Extension](../extensions/toc.md), which contains the raw
  tokens used to build the Table of Contents. Users can use this to build their
  own custom Table of Contents rather than needing to parse the HTML available
  on the `toc` attribute of the Markdown class.

* When the [Table of Contents Extension](../extensions/toc.md) is used in
  conjunction with the [Attribute Lists Extension](../extensions/attr_list.md)
  and a `data-toc-label` attribute is defined on a header, the content of the
  `data-toc-label` attribute is now used as the content of the Table of Contents
  item for that header.

* Additional CSS class names can be appended to
  [Admonitions](../extensions/admonition.md).
