title:      Release Notes for v2.5

Python-Markdown 2.5 Release Notes
=================================

We are pleased to release Python-Markdown 2.5 which adds a few new features
and fixes various bugs. See the list of changes below for details.

Python-Markdown version 2.5 supports Python versions 2.7, 3.2, 3.3, and 3.4.

Backwards-incompatible Changes
------------------------------

* Python-Markdown no longer supports Python version 2.6. You must be using Python
  versions 2.7, 3.2, 3.3, or 3.4.

[importlib]: https://pypi.org/project/importlib/

* The `force_linenos` configuration key on the [CodeHilite Extension] has been **deprecated**
  and will raise a `KeyError` if provided. In the previous release (2.4), it was
  issuing a `DeprecationWarning`. The [`linenums`][linenums] keyword should be used
  instead, which provides more control of the output.

[CodeHilite Extension]: ../extensions/code_hilite.md
[linenums]: ../extensions/code_hilite.md#usage

* Both `safe_mode` and the associated `html_replacement_text` keywords will be
  deprecated in version 2.6 and will raise a **`PendingDeprecationWarning`** in
  2.5. The so-called "safe mode" was never actually "safe" which has resulted in
  many people having a false sense of security when using it. As an alternative,
  the developers of Python-Markdown recommend that any untrusted content be
  passed through an HTML sanitizer (like [Bleach]) after being converted to HTML
  by markdown.

    If your code previously looked like this:

        html = markdown.markdown(text, same_mode=True)

    Then it is recommended that you change your code to read something like this:

        import bleach
        html = bleach.clean(markdown.markdown(text))

    If you are not interested in sanitizing untrusted text, but simply desire to
    escape raw HTML, then that can be accomplished through an extension which
    removes HTML parsing:

        from markdown.extensions import Extension

        class EscapeHtml(Extension):
            def extendMarkdown(self, md, md_globals):
                del md.preprocessors['html_block']
                del md.inlinePatterns['html']

        html = markdown.markdown(text, extensions=[EscapeHtml()])

    As the HTML would not be parsed with the above Extension, then the
    serializer will escape the raw HTML, which is exactly what happens now when
    `safe_mode="escape"`.

[Bleach]: https://bleach.readthedocs.io/

* Positional arguments on the `markdown.Markdown()` are pending deprecation as are
  all except the `text` argument on the `markdown.markdown()` wrapper function.
  Only keyword arguments should be used. For example, if your code previously
  looked like this:

         html = markdown.markdown(text, ['extra'])

    Then it is recommended that you change it to read something like this:

        html = markdown.markdown(text, extensions=['extra'])

    !!! Note
        This change is being made as a result of deprecating `"safe_mode"` as the
        `safe_mode` argument was one of the positional arguments. When that argument
        is removed, the two arguments following it will no longer be at the correct
        position. It is recommended that you always use keywords when they are supported
        for this reason.

* In previous versions of Python-Markdown, the built-in extensions received
  special status and did not require the full path to be provided. Additionally,
  third party extensions whose name started with `"mdx_"` received the same
  special treatment. This behavior will be deprecated in version 2.6 and will
  raise a **`PendingDeprecationWarning`** in 2.5. Ensure that you always use the
  full path to your extensions. For example, if you previously did the
  following:

        markdown.markdown(text, extensions=['extra'])

    You should change your code to the following:

        markdown.markdown(text, extensions=['markdown.extensions.extra'])

    The same applies to the command line:

        $ python -m markdown -x markdown.extensions.extra input.txt

    See the [documentation](../reference.md#extensions) for a full explanation
    of the current behavior.

* The previously documented method of appending the extension configuration as
  a string to the extension name will be deprecated in Python-Markdown
  version 2.6 and will raise a **`PendingDeprecationWarning`** in 2.5. The
  [`extension_configs`](../reference.md#extension_configs) keyword should
  be used instead. See the [documentation](../reference.md#extension-configs)
  for a full explanation of the current behavior.

What's New in Python-Markdown 2.5
---------------------------------

* The [Smarty Extension] has had a number of additional configuration settings
  added, which allows one to define their own substitutions to better support
  languages other than English. Thanks to [Martin Altmayer] for implementing this
  feature.

[Smarty Extension]: ../extensions/smarty.md
[Martin Altmayer]:https://github.com/MartinAltmayer

* Named Extensions (strings passed to the [`extensions`][ex] keyword of
  `markdown.Markdown`) can now point to any module and/or Class on your
  PYTHONPATH. While dot notation was previously supported, a module could not
  be at the root of your PYTHONPATH. The name had to contain at least one dot
  (requiring it to be a sub-module). This restriction no longer exists.

    Additionally, a Class may be specified in the name. The class must be at the
    end of the name (which uses dot notation from PYTHONPATH) and be separated
    by a colon from the module.

    Therefore, if you were to import the class like this:

        from path.to.module import SomeExtensionClass

    Then the named extension would comprise this string:

        "path.to.module:SomeExtensionClass"

    This allows multiple extensions to be implemented within the same module and
    still accessible when the user is not able to import the extension directly
    (perhaps from a template filter or the command line).

    This also means that extension modules are no longer required to include the
    `makeExtension` function which returns an instance of the extension class.
    However, if the user does not specify the class name (she only provides
    `"path.to.module"`) the extension will fail to load without the
    `makeExtension` function included in the module. Extension authors will want
    to document carefully what is required to load their extensions.

[ex]: ../reference.md#extensions

* The Extension Configuration code has been refactored to make it a little
  easier for extension authors to work with configuration settings. As a
  result, the [`extension_configs`][ec] keyword now accepts a dictionary
  rather than requiring a list of tuples. A list of tuples is still supported
  so no one needs to change their existing code. This should also simplify the
  learning curve for new users.

    Extension authors are encouraged to review the new methods available on the
    `markdown.extnesions.Extension` class for handling configuration and adjust
    their code going forward. The included extensions provide a model for best
    practices. See the [API] documentation for a full explanation.

[ec]: ../reference.md#extension_configs
[API]: ../extensions/api.md#configsettings

* The [Command Line Interface][cli] now accepts a `--extensions_config` (or
  `-c`) option which accepts a file name and passes the parsed content of a
  [YAML] or [JSON] file to the [`extension_configs`][ec] keyword of the
  `markdown.Markdown` class. The contents of the YAML or JSON must map to a
  Python Dictionary which matches the format required by the
  `extension_configs` keyword. Note that [PyYAML] is required to parse YAML
  files.

[cli]: ../cli.md#using-extensions
[YAML]: https://yaml.org/
[JSON]: https://json.org/
[PyYAML]: https://pyyaml.org/

* The [Admonition Extension][ae] is no longer considered "experimental."

[ae]: ../extensions/admonition.md

* There have been various refactors of the testing framework. While those
  changes will not directly effect end users, the code is being better tested
  which will benefit everyone.

* Various bug fixes have been made. See the [commit
  log](https://github.com/Python-Markdown/markdown/commits/master) for a
  complete history of the changes.
