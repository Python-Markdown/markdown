from __future__ import absolute_import
import os
import io
import unittest
import textwrap
from . import markdown

try:
    import tidylib
except ImportError:
    tidylib = None

__all__ = ['TestCase', 'LegacyTestCase', 'Kwargs']


class TestCase(unittest.TestCase):
    """
    A unittest.TestCase subclass with helpers for testing Markdown output.

    Define `default_kwargs` as a dict of keywords to pass to Markdown for each
    test. The defaults can be overridden on individual tests.

    The `assertMarkdownRenders` method accepts the source text, the expected
    output, and any keywords to pass to Markdown. The `default_kwargs` are used
    except where overridden by `kwargs`. The ouput and expected ouput are passed
    to `TestCase.assertMultiLineEqual`. An AssertionError is raised with a diff
    if the actual output does not equal the expected output.

    The `dedent` method is available to dedent triple-quoted strings if
    necessary.

    In all other respects, behaves as unittest.TestCase.
    """

    default_kwargs = {}

    def assertMarkdownRenders(self, source, expected, **kwargs):
        """
        Test that source Markdown text renders to expected output with given keywords.
        """

        kws = self.default_kwargs.copy()
        kws.update(kwargs)
        output = markdown(source, **kws)
        self.assertMultiLineEqual(output, expected)

    def dedent(self, text):
        """
        Dedent text.
        """

        # TODO: If/when actual output ends with a newline, then use:
        # return textwrap.dedent(text.strip('/n'))
        return textwrap.dedent(text).strip()


#########################
# Legacy Test Framework #
#########################


class Kwargs(dict):
    """ A dict like class for holding keyword arguments. """
    pass


def _normalize_whitespace(text):
    """ Normalize whitespace for a string of html using tidylib. """
    output, errors = tidylib.tidy_fragment(text, options={
        'drop_empty_paras': 0,
        'fix_backslash': 0,
        'fix_bad_comments': 0,
        'fix_uri': 0,
        'join_styles': 0,
        'lower_literals': 0,
        'merge_divs': 0,
        'output_xhtml': 1,
        'quote_ampersand': 0,
        'newline': 'LF'
    })
    return output


class LegacyTestMeta(type):
    def __new__(cls, name, bases, dct):

        def generate_test(infile, outfile, normalize, kwargs):
            def test(self):
                with io.open(infile, encoding="utf-8") as f:
                    input = f.read()
                with io.open(outfile, encoding="utf-8") as f:
                    # Normalize line endings
                    # (on Windows, git may have altered line endings).
                    expected = f.read().replace("\r\n", "\n")
                output = markdown(input, **kwargs)
                if tidylib and normalize:
                    expected = _normalize_whitespace(expected)
                    output = _normalize_whitespace(output)
                elif normalize:
                    self.skipTest('Tidylib not available.')
                self.assertMultiLineEqual(output, expected)
            return test

        location = dct.get('location', '')
        exclude = dct.get('exclude', [])
        normalize = dct.get('normalize', False)
        input_ext = dct.get('input_ext', '.txt')
        output_ext = dct.get('output_ext', '.html')
        kwargs = dct.get('default_kwargs', Kwargs())

        if os.path.isdir(location):
            for file in os.listdir(location):
                infile = os.path.join(location, file)
                if os.path.isfile(infile):
                    tname, ext = os.path.splitext(file)
                    if ext == input_ext:
                        outfile = os.path.join(location, tname + output_ext)
                        tname = tname.replace(' ', '_').replace('-', '_')
                        kws = kwargs.copy()
                        if tname in dct:
                            kws.update(dct[tname])
                        test_name = 'test_%s' % tname
                        if tname not in exclude:
                            dct[test_name] = generate_test(infile, outfile, normalize, kws)
                        else:
                            dct[test_name] = unittest.skip('Excluded')(lambda: None)

        return type.__new__(cls, name, bases, dct)


# Define LegacyTestCase class with metaclass in Py2 & Py3 compatable way.
# See https://stackoverflow.com/a/38668373/866026
# TODO: If/when py2 support is dropped change to:
# class LegacyTestCase(unittest.Testcase, metaclass=LegacyTestMeta)


class LegacyTestCase(LegacyTestMeta('LegacyTestCase', (unittest.TestCase,), {'__slots__': ()})):
    """
    A `unittest.TestCase` subclass for running Markdown's legacy file-based tests.

    A subclass should define various properties which point to a directory of
    text-based test files and define various behaviors/defaults for those tests.
    The following properties are supported:

    location: A path to the directory fo test files. An absolute path is prefered.
    exclude: A list of tests to exclude. Each test name should comprise the filename
             without an extension.
    normalize: A boolean value indicating if the HTML should be normalized.
               Default: `False`.
    input_ext: A string containing the file extension of input files. Default: `.txt`.
    ouput_ext: A string containing the file extension of expected output files.
               Default: `html`.
    default_kwargs: A `Kwargs` instance which stores the default set of keyword
                    arguments for all test files in the directory.

    In addition, properties can be defined for each individual set of test files within
    the directory. The property should be given the name of the file wihtout the file
    extension. Any spaces and dashes in the filename should be replaced with
    underscores. The value of the property should be a `Kwargs` instance which
    contains the keyword arguments that should be passed to `Markdown` for that
    test file. The keyword arguments will "update" the `default_kwargs`.

    When the class instance is created, it will walk the given directory and create
    a seperate unitttest for each set of test files using the naming scheme:
    `test_filename`. One unittest will be run for each set of input and output files.
    """
    pass
