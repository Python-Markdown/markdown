# -*- coding: utf-8 -*-
"""
Python Markdown

A Python implementation of John Gruber's Markdown.

Documentation: https://python-markdown.github.io/
GitHub: https://github.com/Python-Markdown/markdown/
PyPI: https://pypi.org/project/Markdown/

Started by Manfred Stienstra (http://www.dwerg.net/).
Maintained for a few years by Yuri Takhteyev (http://www.freewisdom.org).
Currently maintained by Waylan Limberg (https://github.com/waylan),
Dmitry Shachnev (https://github.com/mitya57) and Isaac Muse (https://github.com/facelessuser).

Copyright 2007-2023 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from markdown.test_tools import TestCase


class TestIndentedHTMLBlocks(TestCase):
    """
    Raw HTML blocks which start on a line indented by more than `tab_length` spaces.

    Within a containing block (a list item, an admonition, etc.) such a block is raw HTML. Where it can not be
    (an indented code block, or a paragraph which it cannot interrupt), the document must render as it always has.
    """

    def test_mdih_admonition_markdown_attr(self):
        """
        Under md_in_html the extractor stores an etree Element, not IndentedRawHtml, and the element text
        keeps the 4-space indent, so `**test**` becomes an indented code block. Intended change: a raw block
        in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''

                !!! note "Title"
                    <div markdown>
                    **test**
                    </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                <p><strong>test</strong></p>
                </div>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_admonition_markdown_1(self):
        """Same as above with markdown='1'. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div markdown="1">
                    **test**
                    </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                <p><strong>test</strong></p>
                </div>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_admonition_markdown_block_blank_lines(self):
        """markdown='block' with blank lines inside the element. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div markdown="block">

                    **test**

                    - a
                    - b

                    </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                <p><strong>test</strong></p>
                <ul>
                <li>a</li>
                <li>b</li>
                </ul>
                </div>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_admonition_markdown_span(self):
        """markdown='span' inside an admonition. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div markdown="span">
                    **test**
                    </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                <strong>test</strong>
                </div>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_admonition_nested_markdown(self):
        """
        Nested md_in_html elements: inner indentation relative to the outer start tag must survive. Intended
        change: a raw block in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div markdown>
                    <div markdown>
                    **test**
                    </div>
                    </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                <div>
                <p><strong>test</strong></p>
                </div>
                </div>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_admonition_markdown_deeper_content(self):
        """
        Content indented deeper than the start tag: that part is a real indented code block. Intended
        change: a raw block in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div markdown>
                        code

                    **test**
                    </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                <pre><code>code
                </code></pre>
                <p><strong>test</strong></p>
                </div>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_list_item_markdown(self):
        """md_in_html element inside a list item. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item

                    <div markdown>
                    **test**
                    </div>
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>
                <p>item</p>
                <div>
                <p><strong>test</strong></p>
                </div>
                </li>
                </ul>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_admonition_raw_div(self):
        """
        No `markdown` attribute: raw, content must stay literal. Intended change: a raw block in a
        container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div>
                    **test**
                    </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                **test**
                </div>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_code_block_root(self):
        """
        an indented code block containing `<div markdown>` must stay escaped code. Regression: renders as it
        always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                text

                    <div markdown>
                    **x**
                    </div>
                '''
            ),
            self.dedent(
                '''
                <p>text</p>
                <pre><code>&lt;div markdown&gt;
                **x**
                &lt;/div&gt;
                </code></pre>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_code_block_root_blank_lines(self):
        """Same with blank lines inside the element. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                text

                    <div markdown>

                    **x**

                    </div>
                '''
            ),
            self.dedent(
                '''
                <p>text</p>
                <pre><code>&lt;div markdown&gt;

                **x**

                &lt;/div&gt;
                </code></pre>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_code_block_in_list(self):
        """
        Code block (8 spaces) in a list item containing `<div markdown>`. Regression: renders as it always
        has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item

                        <div markdown>
                        **x**
                        </div>
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>item<pre><code>&lt;div markdown&gt;
                **x**
                &lt;/div&gt;
                </code></pre>
                </li>
                </ul>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_code_block_in_admonition(self):
        """
        Code block (8 spaces) in an admonition containing `<div markdown>`. Regression: renders as it always
        has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                        <div markdown>
                        **x**
                        </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <pre><code>&lt;div markdown&gt;
                **x**
                &lt;/div&gt;
                </code></pre>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_code_block_with_more_code(self):
        """
        Code after the element in the same code block must not gain blank lines. Regression: renders as it
        always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                text

                    <div markdown>
                    **x**
                    </div>
                    more code
                '''
            ),
            self.dedent(
                '''
                <p>text</p>
                <pre><code>&lt;div markdown&gt;
                **x**
                &lt;/div&gt;
                more code
                </code></pre>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_unclosed(self):
        """
        Unclosed `markdown` element in a container (source no longer available at close()). Intended change:
        a raw block in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div markdown>
                    **test**
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                <p><strong>test</strong></p>
                </div>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_unclosed_in_code_block(self):
        """
        Unclosed `markdown` element inside an indented code block must show its source as written (no
        `markdown='block'`, no double escaping, no invented </div>). Regression: renders as it always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                text

                    <div markdown>
                    **x** & <b>y</b>
                '''
            ),
            self.dedent(
                '''
                <p>text</p>
                <pre><code>&lt;div markdown&gt;
                **x** &amp; &lt;b&gt;y&lt;/b&gt;
                </code></pre>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_unclosed_nested_in_code_block(self):
        """Same with an unclosed nested element. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                text

                    <div markdown>
                    <p markdown>
                    **x**
                '''
            ),
            self.dedent(
                '''
                <p>text</p>
                <pre><code>&lt;div markdown&gt;
                &lt;p markdown&gt;
                **x**
                </code></pre>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_unclosed_in_admonition_code_block(self):
        """Same inside an admonition (8 spaces). Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note
                        <div markdown>
                        **x**
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Note</p>
                <pre><code>&lt;div markdown&gt;
                **x**
                </code></pre>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_mdih_tail_text(self):
        """Text after the closing tag on the same line. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div markdown>
                    **test**
                    </div> tail

                    after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                <p><strong>test</strong></p>
                </div>
                <p>tail</p>
                <p>after</p>
                </div>
                '''
            ),
            extensions=['admonition', 'md_in_html']
        )

    def test_admonition_div(self):
        """ Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div>
                    **test**
                    </div>
                    after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                **test**
                </div>
                <p>after</p>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_admonition_div_blank_lines(self):
        """ Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div>

                    **test**

                    </div>

                    after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>

                **test**

                </div>
                <p>after</p>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_list_item_div(self):
        """
        raw block in a list item should not be split at blank lines. Intended change: a raw block in a
        container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item

                    <div>

                    **test**

                    </div>

                    after
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>
                <p>item</p>
                <div>

                **test**

                </div>
                <p>after</p>
                </li>
                </ul>
                '''
            )
        )

    def test_nested_admonition_div(self):
        """Two levels of containers; indent of the tag is 8. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Outer"
                    !!! note "Inner"
                        <div>
                        **test**
                        </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Outer</p>
                <div class="admonition note">
                <p class="admonition-title">Inner</p>
                <div>
                **test**
                </div>
                </div>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_admonition_div_deeper_lines(self):
        """
        Lines inside the raw block indented deeper than the start tag must keep the extra indent. Intended
        change: a raw block in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div>
                        <p>deeper</p>
                    </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                    <p>deeper</p>
                </div>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_admonition_pre(self):
        """Whitespace-sensitive <pre> in a container. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <pre>
                      keep
                        this
                    </pre>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <pre>
                  keep
                    this
                </pre>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_admonition_script(self):
        """<script> in a container. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <script>
                    var x = "**no**";
                    </script>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <script>
                var x = "**no**";
                </script>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_admonition_comment(self):
        """
        Indented HTML comment (handled by handle_empty_tag / parse_comment path). Regression: renders as it
        always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <!-- a **comment** -->

                    after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <!-- a **comment** -->
                <p>after</p>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_admonition_unclosed_div(self):
        """
        Unclosed raw block at end of document (flush in close()). Intended change: a raw block in a
        container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div>
                    **test**
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                **test**
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_paragraph_continuation_div(self):
        """
        An indented line directly after paragraph text is a paragraph continuation, not code. Regression:
        renders as it always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                some text
                    <div>x</div>
                '''
            ),
            self.dedent(
                '''
                <p>some text
                    <div>x</div></p>
                '''
            )
        )

    def test_paragraph_continuation_div_multiline(self):
        """Same, multi-line raw block. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                some text
                    <div>
                    **x**
                    </div>
                more text
                '''
            ),
            self.dedent(
                '''
                <p>some text
                    <div>
                    <strong>x</strong>
                    </div>
                more text</p>
                '''
            )
        )

    def test_paragraph_chain_with_text(self):
        """
        Blocks that start where the last one ended, mid-paragraph, then text. Must stay one inline run.
        Regression: renders as it always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                some text
                    <div>a</div><div>b</div> trailing
                '''
            ),
            self.dedent(
                '''
                <p>some text
                    <div>a</div><div>b</div> trailing</p>
                '''
            )
        )

    def test_paragraph_chain_with_more_lines(self):
        """
        Same with an indented continuation line and a following paragraph. Regression: renders as it always
        has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                some text
                    <div>a</div><div>b</div> trailing
                    more

                after
                '''
            ),
            self.dedent(
                '''
                <p>some text
                    <div>a</div><div>b</div> trailing
                    more</p>
                <p>after</p>
                '''
            )
        )

    def test_paragraph_chain_of_three(self):
        """Three blocks in a row. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                some text
                    <div>a</div><div>b</div><div>c</div>
                '''
            ),
            self.dedent(
                '''
                <p>some text
                    <div>a</div><div>b</div><div>c</div></p>
                '''
            )
        )

    def test_paragraph_chain_multiline(self):
        """ Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                some text
                    <div>
                    a
                    </div><div>
                    b
                    </div> trailing
                more
                '''
            ),
            self.dedent(
                '''
                <p>some text
                    <div>
                    a
                    </div><div>
                    b
                    </div> trailing
                more</p>
                '''
            )
        )

    def test_paragraph_chain_multiline_indented(self):
        """Same with the continuation line indented. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                some text
                    <div>
                    a
                    </div><div>
                    b
                    </div> trailing
                    more
                '''
            ),
            self.dedent(
                '''
                <p>some text
                    <div>
                    a
                    </div><div>
                    b
                    </div> trailing
                    more</p>
                '''
            )
        )

    def test_code_chain_blocks(self):
        """ Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                text

                    <div>a</div><div>b</div><div>c</div> trailing
                    more
                '''
            ),
            self.dedent(
                '''
                <p>text</p>
                <pre><code>&lt;div&gt;a&lt;/div&gt;&lt;div&gt;b&lt;/div&gt;&lt;div&gt;c&lt;/div&gt; trailing
                more
                </code></pre>
                '''
            )
        )

    def test_code_chain_multiline(self):
        """Same, multi-line blocks. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                text

                    <div>
                    a
                    </div><div>
                    b
                    </div> trailing
                    more
                '''
            ),
            self.dedent(
                '''
                <p>text</p>
                <pre><code>&lt;div&gt;
                a
                &lt;/div&gt;&lt;div&gt;
                b
                &lt;/div&gt; trailing
                more
                </code></pre>
                '''
            )
        )

    def test_list_lazy_chain(self):
        """ Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item
                    <div>a</div><div>b</div> trailing
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>item
                    <div>a</div><div>b</div> trailing</li>
                </ul>
                '''
            )
        )

    def test_list_lazy_div_next_item(self):
        """
        Indented div on a lazy line of a list item, followed by another item. Both items must stay tight (no
        <p>): nothing may be inserted between the placeholder and the next item. Regression: renders as it
        always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item
                    <div>x</div>
                - b
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>item
                    <div>x</div></li>
                <li>b</li>
                </ul>
                '''
            )
        )

    def test_list_lazy_tail_next_item(self):
        """
        Same with text after the closing tag. The next item must not be swallowed into the paragraph.
        Regression: renders as it always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item
                    <div>x</div> trailing
                - b
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>item
                    <div>x</div> trailing</li>
                <li>b</li>
                </ul>
                '''
            )
        )

    def test_list_lazy_tail_next_item_ordered(self):
        """Same in an ordered list. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                1. item
                    <div>x</div> trailing
                2. b
                '''
            ),
            self.dedent(
                '''
                <ol>
                <li>item
                    <div>x</div> trailing</li>
                <li>b</li>
                </ol>
                '''
            )
        )

    def test_paragraph_tail_then_code(self):
        """
        Text after the closing tag in a paragraph, then a blank line and an indented code block. The code
        block must stay a code block. Regression: renders as it always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                some text
                    <div>x</div> trailing

                    code
                '''
            ),
            self.dedent(
                '''
                <p>some text
                    <div>x</div> trailing</p>
                <pre><code>code
                </code></pre>
                '''
            )
        )

    def test_fn_div_blank_lines(self):
        """Raw HTML with blank lines in a footnote. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Text[^1]

                [^1]:
                    <div>

                    **x**

                    </div>

                    after
                '''
            ),
            '<p>Text<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<div>\n'
            '\n'
            '**x**\n'
            '\n'
            '</div>\n'
            '<p>after&#160;<a class="footnote-backref" href="#fnref:1" title="Jump'
            ' back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extensions=['footnotes']
        )

    def test_fn_text_then_div(self):
        """Raw HTML after the text of a footnote. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Text[^1]

                [^1]: Note text.

                    <div>
                    **x**
                    </div>

                    after
                '''
            ),
            '<p>Text<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>Note text.</p>\n'
            '<div>\n'
            '**x**\n'
            '</div>\n'
            '<p>after&#160;<a class="footnote-backref" href="#fnref:1" title="Jump'
            ' back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extensions=['footnotes']
        )

    def test_fn_lazy_div(self):
        """
        Indented HTML on a lazy line of a footnote is part of the paragraph. Regression: renders as it
        always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Text[^1]

                [^1]: Note text.
                    <div>x</div>
                '''
            ),
            '<p>Text<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>Note text.\n'
            '<div>x</div>&#160;<a class="footnote-backref" href="#fnref:1"'
            ' title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extensions=['footnotes']
        )

    def test_fn_code_with_html(self):
        """Indented code with HTML in a footnote. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Text[^1]

                [^1]: Note.

                        <div>

                        code
                        </div>
                '''
            ),
            '<p>Text<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<p>Note.</p>\n'
            '<pre><code>&lt;div&gt;\n'
            '\n'
            'code\n'
            '&lt;/div&gt;\n'
            '</code></pre>\n'
            '<p><a class="footnote-backref" href="#fnref:1" title="Jump back to'
            ' footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extensions=['footnotes']
        )

    def test_fn_mdhtml(self):
        """A `markdown` element with blank lines in a footnote. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Text[^1]

                [^1]:
                    <div markdown>

                    **x**

                    </div>
                '''
            ),
            '<p>Text<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<div>\n'
            '<p><strong>x</strong></p>\n'
            '</div>\n'
            '<p><a class="footnote-backref" href="#fnref:1" title="Jump back to'
            ' footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extensions=['footnotes', 'md_in_html']
        )

    def test_fn_unclosed(self):
        """An unclosed raw block in a footnote. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Text[^1]

                [^1]:
                    <div>

                    **x**
                '''
            ),
            self.dedent(
                '''
                <p>Text<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>
                <div class="footnote">
                <hr />
                <ol>
                <li id="fn:1"></li>
                </ol>
                </div>
                '''
            ),
            extensions=['footnotes']
        )

    def test_dl_div_blank_lines(self):
        """Raw HTML with blank lines in a definition. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Term
                :   para

                    <div>

                    **x**

                    </div>

                    after
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>
                <p>para</p>
                <div>

                **x**

                </div>
                <p>after</p>
                </dd>
                </dl>
                '''
            ),
            extensions=['def_list']
        )

    def test_dl_div_after_definition(self):
        """Raw HTML after the text of a definition. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Term
                :   definition

                    <div>
                    **x**
                    </div>
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>
                <p>definition</p>
                <div>
                **x**
                </div>
                </dd>
                </dl>
                '''
            ),
            extensions=['def_list']
        )

    def test_dl_lazy_div(self):
        """
        Indented HTML on a lazy line of a definition is part of the paragraph. Regression: renders as it
        always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Term
                :   definition
                    <div>x</div>
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>definition
                <div>x</div></dd>
                </dl>
                '''
            ),
            extensions=['def_list']
        )

    def test_dl_code_with_html(self):
        """Indented code with HTML in a definition. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Term
                :   definition

                        <div>

                        code
                        </div>
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>definition<pre><code>&lt;div&gt;

                code
                &lt;/div&gt;
                </code></pre>
                </dd>
                </dl>
                '''
            ),
            extensions=['def_list']
        )

    def test_dl_mdhtml(self):
        """A `markdown` element with blank lines in a definition. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Term
                :   para

                    <div markdown>

                    **x**

                    </div>
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>
                <p>para</p>
                <div>
                <p><strong>x</strong></p>
                </div>
                </dd>
                </dl>
                '''
            ),
            extensions=['def_list', 'md_in_html']
        )

    def test_dl_unclosed(self):
        """An unclosed raw block in a definition. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Term
                :   para

                    <div>

                    **x**
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>
                <p>para</p>
                <div>

                **x**
                </dd>
                </dl>
                '''
            ),
            extensions=['def_list']
        )

    def test_adm_in_footnote(self):
        """Raw HTML in an admonition in a footnote. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Text[^1]

                [^1]:
                    !!! note
                        <div>

                        **x**

                        </div>
                '''
            ),
            '<p>Text<sup id="fnref:1"><a class="footnote-ref" href="#fn:1">1</a></sup></p>\n'
            '<div class="footnote">\n'
            '<hr />\n'
            '<ol>\n'
            '<li id="fn:1">\n'
            '<div class="admonition note">\n'
            '<p class="admonition-title">Note</p>\n'
            '<div>\n'
            '\n'
            '**x**\n'
            '\n'
            '</div>\n'
            '</div>\n'
            '<p><a class="footnote-backref" href="#fnref:1" title="Jump back to'
            ' footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n'
            '</ol>\n'
            '</div>',
            extensions=['footnotes', 'admonition']
        )

    def test_list_in_admonition(self):
        """Raw HTML with blank lines in a list in an admonition. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note
                    - item

                        <div>

                        **x**

                        </div>

                        after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Note</p>
                <ul>
                <li>
                <p>item</p>
                <div>

                **x**

                </div>
                <p>after</p>
                </li>
                </ul>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_admonition_in_list_in_definition(self):
        """Three levels of containers. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                Term
                :   - item

                        !!! note
                            <div>

                            **x**

                            </div>
                '''
            ),
            self.dedent(
                '''
                <dl>
                <dt>Term</dt>
                <dd>
                <ul>
                <li>
                <p>item</p>
                <div class="admonition note">
                <p class="admonition-title">Note</p>
                <div>

                **x**

                </div>
                </div>
                </li>
                </ul>
                </dd>
                </dl>
                '''
            ),
            extensions=['def_list', 'admonition']
        )

    def test_admonition_in_blockquote(self):
        """
        An admonition in a blockquote is a container, so its indented HTML is raw. Intended change: a raw
        block in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                > !!! note
                >     <div>
                >     **x**
                >     </div>
                '''
            ),
            self.dedent(
                '''
                <blockquote>
                <div class="admonition note">
                <p class="admonition-title">Note</p>
                <div>
                **x**
                </div>
                </div>
                </blockquote>
                '''
            ),
            extensions=['admonition']
        )

    def test_list_lazy_continuation_div(self):
        """Indented div right after a list item line (no blank line). Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item
                    <div>x</div>
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>item
                    <div>x</div></li>
                </ul>
                '''
            )
        )

    def test_code_block_in_list(self):
        """
        Code block (8 spaces) inside a list item containing HTML with blank lines. Regression: renders as it
        always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item

                        <div>

                        code
                        </div>
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>item<pre><code>&lt;div&gt;

                code
                &lt;/div&gt;
                </code></pre>
                </li>
                </ul>
                '''
            )
        )

    def test_code_block_in_admonition(self):
        """Code block (8 spaces) inside an admonition containing HTML. Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                        <div>
                        code
                        </div>
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <pre><code>&lt;div&gt;
                code
                &lt;/div&gt;
                </code></pre>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_trailing_text_after_close(self):
        """
        Text on the same line after the closing tag. Text after a block starts its own paragraph (as at the
        root). Intended change: a raw block in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div>x</div> trailing

                    after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>x</div>
                <p>trailing</p>
                <p>after</p>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_trailing_text_multiline_block(self):
        """
        Multi-line block followed by text on the closing line, then a lazy continuation line. Intended
        change: a raw block in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div>
                    **x**
                    </div> trailing
                    more

                    after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>
                **x**
                </div>
                <p>trailing
                more</p>
                <p>after</p>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_trailing_text_chained_blocks(self):
        """
        A second block starts on the closing line of the first, followed by text. Intended change: a raw
        block in a container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <div>a</div><div>b</div> trailing

                    after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <div>a</div>
                <div>b</div>
                <p>trailing</p>
                <p>after</p>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_trailing_text_after_comment(self):
        """
        Text after an indented comment on the same line (empty-tag path). Intended change: a raw block in a
        container.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                    <!-- c --> trailing

                    after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <!-- c -->
                <p>trailing</p>
                <p>after</p>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_trailing_text_in_list(self):
        """Text after the closing tag inside a list item. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                - item

                    <div>x</div> trailing

                    after
                '''
            ),
            self.dedent(
                '''
                <ul>
                <li>
                <p>item</p>
                <div>x</div>
                <p>trailing</p>
                <p>after</p>
                </li>
                </ul>
                '''
            )
        )

    def test_trailing_text_in_code_block(self):
        """
        Indented CODE with HTML followed by text on the same line must stay one code line. Regression:
        renders as it always has.
        """

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                text

                    <div>x</div> trailing
                    more code
                '''
            ),
            self.dedent(
                '''
                <p>text</p>
                <pre><code>&lt;div&gt;x&lt;/div&gt; trailing
                more code
                </code></pre>
                '''
            )
        )

    def test_trailing_text_in_code_block_in_admonition(self):
        """Same inside an admonition (8 spaces). Regression: renders as it always has."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Title"
                        <p>x</p> trailing
                        more code
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Title</p>
                <pre><code>&lt;p&gt;x&lt;/p&gt; trailing
                more code
                </code></pre>
                </div>
                '''
            ),
            extensions=['admonition']
        )

    def test_trailing_text_nested_admonition(self):
        """Two container levels. Intended change: a raw block in a container."""

        self.assertMarkdownRenders(
            self.dedent(
                R'''
                !!! note "Outer"
                    !!! note "Inner"
                        <div>x</div> trailing

                        after
                '''
            ),
            self.dedent(
                '''
                <div class="admonition note">
                <p class="admonition-title">Outer</p>
                <div class="admonition note">
                <p class="admonition-title">Inner</p>
                <div>x</div>
                <p>trailing</p>
                <p>after</p>
                </div>
                </div>
                '''
            ),
            extensions=['admonition']
        )
