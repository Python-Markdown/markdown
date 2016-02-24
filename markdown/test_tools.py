import unittest
import textwrap
from markdown import markdown


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
