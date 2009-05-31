import os, codecs
import markdown
from nose.tools import assert_equal
import difflib
from plugins import MdSyntaxError

class SyntaxBase:
    """
    Generator that steps through all files in a dir and runs each text file
    (*.txt) as a seperate unit test.

    Each subclass of SyntaxBase should define `dir` as a string containing the 
    name of the directory which holds the test files. For example:

        dir = "path/to/mytests"

    A subclass may redefine the `setUp` method to create a custom `Markdown`
    instance specific to that batch of tests.
    
    """
    
    dir = ""

    def __init__(self):
        self.files = [x.replace(".txt", "")
                      for x in os.listdir(self.dir) if x.endswith(".txt")]

    def setUp(self):
        """ 
        Create  Markdown instance. 
        
        Override this method to create a custom `Markdown` instance assigned to 
        `self.md`. For example:

            self.md = markdown.Markdown(extensions=["footnotes"], safe_mode="replace")

        """
        self.md = markdown.Markdown()

    def tearDown(self):
        """ tearDown is not implemented. """
        pass

    def test_syntax(self):
        for file in self.files:
            yield self.check_syntax, file

    def check_syntax(self, file):
        input_file = os.path.join(self.dir, file + ".txt")
        input = codecs.open(input_file, encoding="utf-8").read()
        output_file = os.path.join(self.dir, file + ".html")
        expected_output = codecs.open(output_file, encoding="utf-8").read()
        output = self.normalize(self.md.convert(input))
        diff = [l for l in difflib.unified_diff(self.normalize(expected_output),
                                                output, output_file, 
                                                'actual_output.html', n=3)]
        if diff:
            #assert False, 
            raise MdSyntaxError('Output from "%s" failed to match expected output.\n\n%s' % (input_file, ''.join(diff)))

    def normalize(self, text):
        return ['%s\n' % l for l in text.strip().split('\n')]
