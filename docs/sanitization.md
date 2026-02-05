title: Sanitization and Security

# Sanitizing HTML Output

The Python-Markdown library does ***not*** sanitize its HTML output. If you
are processing Markdown input from an untrusted source, it is your
responsibility to ensure that it is properly sanitized. See _[Markdown and
XSS]_ for an overview of some of the dangers and _[Improper markup sanitization
in popular software]_ for notes on best practices to ensure HTML is properly
sanitized. With those concerns in mind, some recommendations are provided
below to ensure that any input from an untrusted source is properly
sanitized.

That said, if you fully trust the source of your input, you may choose to do
nothing. Conversely, you may find solutions other than those suggested here.
However, you do so at your own risk.

## Using JustHTML

[JustHTML] is recommended as a sanitizer on the output of `markdown.markdown`
or `Markdown.convert`. When you pass HTML output through JustHTML, it is
sanitized by default according to a strict [allow list policy]. The policy
can be [customized] if necessary.

``` python
import markdown
from justhtml import JustHTML

html =  markdown.markdown(text)
safe_html = JustHTML(html, fragment=True).to_html()
```

## Using nh3 or bleach

If you cannot use JustHTML for some reason, some alternatives include [nh3] or
[bleach][^1]. However, be aware that these libraries will not be sufficient
in themselves and will require customization. Some useful lists of allowed
tags and attributes can be found in the [`bleach-allowlist`]
[bleach-allowlist] library, which should work with both nh3 and bleach as nh3
mirrors bleach's API.

``` python
import markdown
import bleach
from bleach_allowlist import markdown_tags, markdown_attrs

html =  markdown.markdown(text)
safe_html = bleach.clean(html, markdown_tags, markdown_attrs)
```

[^1]: The [bleach] project has been [deprecated](https://github.com/mozilla/bleach/issues/698). 
However, it may be the only option for some users as [nh3] is a set of Python bindings to a Rust library.

## Sanitizing on the Command Line

Both Python-Markdown and JustHTML provide command line interfaces which read
from STDIN and write to STDOUT. Therefore, they can be used togeather to
ensure that the output from untrusted input is properly sanitized.

```sh
echo "Some **Markdown** text." | python -m markdown | justhtml - --fragment > safe_output.html
```

For more information on JustHTML's Command Line Interface, see the
[documentation][JustHTML_CLI]. Use the `--help` option for a list of all available
options and arguments to the `markdown` command.

[Markdown and XSS]: https://michelf.ca/blog/2010/markdown-and-xss/
[Improper markup sanitization in popular software]: https://github.com/ChALkeR/notes/blob/master/Improper-markup-sanitization.md
[JustHTML]: https://emilstenstrom.github.io/justhtml/
[allow list policy]: https://emilstenstrom.github.io/justhtml/html-cleaning.html#default-sanitization-policy
[customized]: https://emilstenstrom.github.io/justhtml/html-cleaning.html#use-a-custom-sanitization-policy
[nh3]: https://nh3.readthedocs.io/en/latest/
[bleach]: http://bleach.readthedocs.org/en/latest/
[bleach-allowlist]: https://github.com/yourcelf/bleach-allowlist
[JustHTML_CLI]: https://emilstenstrom.github.io/justhtml/cli.html
