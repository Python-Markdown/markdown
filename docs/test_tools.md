title: Test Tools

# Test Tools

Python-Markdown provides some testing tools which simplify testing actual
Markdown output against expected output. The tools are built on the Python
standard  library [`unittest`][unittest]. Therefore, no additional libraries are
required. While Python-Markdown uses the tools for its own tests, they were
designed and built so that third party extensions could use them as well.
Therefore, the tools are importable from `markdown.test_tools`.

The test tools include two different `unittest.TestCase` subclasses:
`markdown.test_tools.TestCase` and `markdown.test_tools.LegacyTestCase`.

## markdown.test_tools.TestCase

The `markdown.test_tools.TestCase` class is a `unittest.TestCase` subclass with
a few additional helpers to make testing Markdown output easier.

Properties
: `default_kwargs`: A `dict` of keywords to pass to Markdown for each
test. The defaults can be overridden on individual tests.

Methods
: `assertMarkdownRenders`: accepts the source text, the expected output, an optional
  dictionary of `expected_attrs`, and any keywords to pass to Markdown. The
  `default_kwargs` defined on the class are used except where overridden by
  keyword arguments. The output and expected output are passed to
  `TestCase.assertMultiLineEqual`. An `AssertionError` is raised with a diff
  if the actual output does not equal the expected output. The optional
  keyword `expected_attrs` accepts a dictionary of attribute names as keys with
  expected values. Each value is checked against the attribute of that
  name on the instance of the `Markdown` class using `TestCase.assertEqual`. An
  `AssertionError` is raised if any value does not match the expected value.

: `dedent`: Dedent triple-quoted strings.

In all other respects, `markdown.test_tools.TestCase` behaves as
`unittest.TestCase`. In fact, `assertMarkdownRenders` tests could be mixed with
other `unittest` style tests within the same test class.

An example Markdown test might look like this:

```python
from markdown.test_tools import TestCase

class TestHr(TestCase):
    def test_hr_before_paragraph(self):
        self.assertMarkdownRenders(
            # The Markdown source text used as input
            self.dedent(
                """
                ***
                An HR followed by a paragraph with no blank line.
                """
            ),
            # The expected HTML output
            self.dedent(
                """
                <hr>
                <p>An HR followed by a paragraph with no blank line.</p>
                """
            ),
            # Other keyword arguments to pass to `markdown.markdown`
            output_format='html'
        )
```

## markdown.test_tools.LegacyTestCase

In the past Python-Markdown exclusively used file-based tests. Many of those
tests still exist in Python-Markdown's test suite, including the test files from
the [reference implementation][perl] (`markdown.pl`) and [PHP Markdown][PHP].
Each test consists of a matching pair of text and HTML files. The text file
contains a snippet of Markdown source text formatted for a specific syntax
feature and the HTML file contains the expected HTML output of that snippet.
When the test suite is run, each text file is run through Markdown and the
output is compared with the HTML file as a separate unit test. When a test
fails, the error report includes a diff of the expected output compared to the
actual output to easily identify any problems.

A separate `markdown.test_tools.LegacyTestCase` subclass must be created for
each directory of test files. Various properties can be defined within the
subclass to point to a directory of text-based test files and define various
behaviors/defaults for those tests. The following properties are supported:

* `location`: A path to the directory of test files. An absolute path is
  preferred.
* `exclude`: A list of tests to skip. Each test name should comprise of a
  file name without an extension.
* `normalize`: A boolean value indicating if the HTML should be normalized.
  Default: `False`. Note: Normalization of HTML requires that [PyTidyLib] be
  installed on the system. If PyTidyLib is not installed and `normalize` is set
  to `True`, then the test will be skipped, regardless of any other settings.
* `input_ext`: A string containing the file extension of input files.
  Default: `.txt`.
* `output_ext`: A string containing the file extension of expected output files.
  Default: `html`.
* `default_kwargs`: A `markdown.test_tools.Kwargs` instance which stores the
  default set of keyword arguments for all test files in the directory.

In addition, properties can be defined for each individual set of test files
within the directory. The property should be given the name of the file without
the file extension. Any spaces and dashes in the file name should be replaced
with underscores. The value of the property should be a
`markdown.test_tools.Kwargs` instance which contains the keyword arguments that
should be passed to `markdown.markdown` for that test file. The keyword
arguments will "update" the `default_kwargs`.

When the class instance is created during a test run, it will walk the given
directory and create a separate unit test for each set of test files using the
naming scheme: `test_filename`. One unit test will be run for each set of input
and output files.

The definition of an example set of tests might look like this:

```python
from markdown.test_tools import LegacyTestCase, Kwargs
import os

# Get location of this file and use to find text file dirs.
parent_test_dir = os.path.abspath(os.path.dirname(__file__))


class TestFoo(LegacyTestCase):
    # Define location of text file directory. In this case, the directory is
    # named "foo" and is in the same parent directory as this file.
    location = os.path.join(parent_test_dir, 'foo')
    # Define default keyword arguments. In this case, unless specified
    # differently, all tests should use the output format "html".
    default_kwargs = Kwargs(output_format='html')

    # The "xhtml" test should override the output format and use "xhtml".
    xhtml = Kwargs(output_format='xhtml')

    # The "toc" test should use the "toc" extension with a custom permalink
    # setting.
    toc = Kwargs(
        extensions=['markdown.extensions.toc'],
        extension_configs={'markdown.extensions.toc': {'permalink': "[link]"}}
    )
```

Note that in the above example, the text file directory may contain many more
text-based test files than `xhtml` (`xhtml.txt` and `xhtml.html`) and `toc`
(`toc.txt` and `toc.html`). As long as each set of files exists as a pair, a
test will be created and run for each of them. Only the `xhtml` and `toc` tests
needed to be specifically identified as they had specific, non-default settings
which needed to be defined.

## Running Python-Markdown's Tests

As all of the tests for the `markdown` library are unit tests, standard
`unittest` methods of calling tests can be used. For example, to run all of
Python-Markdown's tests, from the root of the git repository, run the following
command:

```sh
python -m unittest discover tests
```

That simple command will search everything in the `tests` directory and it's
sub-directories and run all `unittest` tests that it finds, including
`unittest.TestCase`, `markdown.test_tools.TestCase`, and
`markdown.test_tools.LegacyTestCase` subclasses. Normal [unittest] discovery
rules apply.

!!! seealso "See Also"

    See the [Contributing Guide] for instructions on setting up a
    [development environment] for running the tests.

[unittest]: https://docs.python.org/3/library/unittest.html
[Perl]: https://daringfireball.net/projects/markdown/
[PHP]: http://michelf.com/projects/php-markdown/
[PyTidyLib]: http://countergram.github.io/pytidylib/
[Contributing Guide]: contributing.md
[development environment]: contributing.md#development-environment
