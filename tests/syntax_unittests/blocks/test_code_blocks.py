from markdown.test_tools import TestCase

class TestCodeBlocks(TestCase):

    def test_simple_codeblock(self):
        self.assertMarkdownRenders(
            '    # A code block.',

            self.dedent(
                """
                <pre><code># A code block.
                </code></pre>
                """
            )
        )

    def test_tabbed_codeblock(self):
        self.assertMarkdownRenders(
            '\t# A code block.',

            self.dedent(
                """
                <pre><code># A code block.
                </code></pre>
                """
            )
        )

    def test_multiline_codeblock(self):
        self.assertMarkdownRenders(
            '    # Line 1\n    # Line 2\n',
        
            self.dedent(
                """
                <pre><code># Line 1
                # Line 2
                </code></pre>
                """
            )
        )

    def test_codeblock_with_blankline(self):
        self.assertMarkdownRenders(
            '    # Line 1\n\n    # Line 2\n',

            self.dedent(
                """
                <pre><code># Line 1

                # Line 2
                </code></pre>
                """
            )
        )
