title:      Test Suite
prev_title: Extension API
prev_url:   extensions/api.html
next_title: Change Log
next_url:   change_log.html

# Test Suite

Python-Markdown comes with a test suite which uses the [Nose] testing
framework and [YAML]. The test suite primarily serves to ensure that new bugs 
are not introduced as existing bugs are patched or new features are added. It 
also allows Python-Markdown to be tested with the tests from other 
implementations such as John Gruber's [Perl] implementation or Michel 
Fortin's [PHP] implementation.

The test suite can be run by calling the `run_tests.py` command at the root of
the distribution tarball or by calling the `nosetests` command directly. Either
way, Nose will need to be installed on your system first (run `easy_install
nose`). Any standard nosetests configuration options can be passed in on the command
line (i.e.: verbosity level or use of a plugin like coverage).

Additionally, a nicely formatted HTML report of all output is written to a
temporary file in `test-output.html`. Open the file in a browser to view
the report.

A `tox.ini` file is also provided, so [tox] can be used to automatically create
virtual environments, install all testing dependencies and run the tests on 
each supported Python version. See the wiki for instructions on 
[setting up a testing environment] to use tox.

The test suite contains two kinds of tests: Markdown Syntax Tests and Unit
Tests.

## Markdown Syntax Tests

The Syntax Tests are in the various directories contained within the 'tests'
directory of the packaged tarball. Each test consists of a matching pair of text
and HTML files. The text file contains a snippet of Markdown source text
formatted for a specific syntax feature and the HTML file contains the expected
HTML output of that snippet. When the test suite is run, each text file is run
through Markdown and the output is compared with the HTML file as a separate
Unit Test.

In fact, this is the primary reason for using Nose, it gives us an easy way to
treat each of these tests as a separate unit test which is reported on
separately. Additionally, with the help of a couple custom Nose plugins which
are included with the Markdown Test Suite, we are able to get back an easy to
read diff of the actual output compared to expected output when a test fails.

Here is some sample output with a test that is failing because of some
insignificant white space differences:

    $ ./run-tests.py
    ..........................................................M...........
    ............................SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
    SSSSSSSSSS.................S..........................................
    .........
    ======================================================================
    MarkdownSyntaxError: TestSyntax: "misc/lists3"
    ----------------------------------------------------------------------
    MarkdownSyntaxError: Output from "/home/waylan/code/python-markdown/te
    sts/misc/lists3.txt" failed to match expected output.

    --- /home/waylan/code/python-markdown/tests/misc/lists3.html 
    +++ actual_output.html 
    @@ -1,5 +1,5 @@ 
     <ul> 
     <li>blah blah blah 
    -sdf asdf asdf asdf asdf 
    -asda asdf asdfasd</li> 
    +    sdf asdf asdf asdf asdf 
    +    asda asdf asdfasd</li> 
     </ul>

    ---------------------------------------------------------------------- 
    Ran 219 tests in 7.698s

    FAILED (MarkdownSyntaxError=1, SKIP=53)

Note that 219 tests were run, one of which failed with a `MarkdownSyntaxError`.
Only Markdown Syntax Tests should fail with a `MarkdownSyntaxError`. Nose then
formats the error reports for `MarkdownSyntaxError`s so that they only include
useful information. Namely the text file which failed and a unified diff showing
the failure. Without the plugin, you would also get a useless traceback showing
how the code stepped through the test framework, but nothing about how Markdown
actually ran.

If, on the other hand, a Syntax Test failed because some other exception gets
raised by either Markdown or the test suite, then that would be reported as per
a normal unit test failure with the appropriate traceback for debugging
purposes.

### Syntax Test Configuration Settings

The other thing to note about the above example is that 53 tests were skipped.
Those tests have been explicitly configured to be skipped as they are primarily
tests from either PHP or Perl which are known to fail for various reasons. In
fact, a number of different configuration settings can be set for any specific
test.

Each Syntax Test directory contains a `test.cfg` file in the [YAML] format. The
file may contain a separate section for each text file named exactly as the file
is named minus the file extension (i.e.; the section for a test in `foo.txt`
would be `foo`). All settings are optional. Default settings for the entire
directory can be set under the `DEFAULT` section (must be all caps). Any
settings under a specific file section will override anything in the
`DEFAULT` section for that specific test only.

Below are the configuration options available and the defaults used when they
are not explicitly set.

* `normalize`: Switches white space normalization of the test output on or off. 
  Defaults to `False` (off). Note: This requires that [PyTidyLib] be installed on 
  the system. Otherwise the test will be skipped, regardless of any other 
  settings.  
* `skip`: Switches skipping of the test on and off. Defaults to `False` (off).  
* `input_ext`: Extension of input file. Defaults to `.txt`. Useful for tests 
  from other implementations.
* `output_ext`: Extension of output file. Defaults to `.html`. Useful for tests
  from other implementations.
* Any keyword argument accepted by the Markdown class. If not set, Markdown's 
  defaults are used. 

## Unit Tests

Unit Tests are used as regression tests for Python-Markdown's API.
All Unit Tests shipped with Python-Markdown are standard Python Unit Tests and
are all contained in `tests/test_apis.py` and `tests/test_extensions.py`. 
Standard discovery methods are used to find and run the tests. Therefore, when 
writing new tests, those standards and naming conventions should be followed.

[Nose]: http://somethingaboutorange.com/mrl/projects/nose/ 
[Perl]: http://daringfireball.net/projects/markdown/ 
[PHP]: http://michelf.com/projects/php-markdown/ 
[PyTidyLib]: http://countergram.com/open-source/pytidylib/
[tox]: http://testrun.org/tox/latest/
[setting up a testing environment]: https://github.com/waylan/Python-Markdown/wiki/Test-Environment-Setup
[YAML]: http://yaml.org/
