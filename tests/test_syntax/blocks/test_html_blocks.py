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

Copyright 2007-2018 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from markdown.test_tools import TestCase


class TestHTMLBlocks(TestCase):

    def test_raw_paragraph(self):
        self.assertMarkdownRenders(
            '<p>A raw paragraph.</p>',
            '<p>A raw paragraph.</p>'
        )

    def test_raw_skip_inline_markdown(self):
        self.assertMarkdownRenders(
            '<p>A *raw* paragraph.</p>',
            '<p>A *raw* paragraph.</p>'
        )

    def test_raw_indent_one_space(self):
        self.assertMarkdownRenders(
            ' <p>A *raw* paragraph.</p>',
            '<p>A *raw* paragraph.</p>'
        )

    def test_raw_indent_two_spaces(self):
        self.assertMarkdownRenders(
            '  <p>A *raw* paragraph.</p>',
            '<p>A *raw* paragraph.</p>'
        )

    def test_raw_indent_three_spaces(self):
        self.assertMarkdownRenders(
            '   <p>A *raw* paragraph.</p>',
            '<p>A *raw* paragraph.</p>'
        )

    def test_raw_indent_four_spaces(self):
        self.assertMarkdownRenders(
            '    <p>code block</p>',
            self.dedent(
                """
                <pre><code>&lt;p&gt;code block&lt;/p&gt;
                </code></pre>
                """
            )
        )

    def test_raw_span(self):
        self.assertMarkdownRenders(
            '<span>*inline*</span>',
            '<p><span><em>inline</em></span></p>'
        )

    def test_code_span(self):
        self.assertMarkdownRenders(
            '`<em>code span</em>`',
            '<p><code>&lt;em&gt;code span&lt;/em&gt;</code></p>'
        )

    def test_raw_empty(self):
        self.assertMarkdownRenders(
            '<p></p>',
            '<p></p>'
        )

    def test_raw_empty_space(self):
        self.assertMarkdownRenders(
            '<p> </p>',
            '<p> </p>'
        )

    def test_raw_empty_newline(self):
        self.assertMarkdownRenders(
            '<p>\n</p>',
            '<p>\n</p>'
        )

    def test_raw_empty_blank_line(self):
        self.assertMarkdownRenders(
            '<p>\n\n</p>',
            '<p>\n\n</p>'
        )

    def test_multiline_raw(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>
                    A raw paragraph
                    with multiple lines.
                </p>
                """
            ),
            self.dedent(
                """
                <p>
                    A raw paragraph
                    with multiple lines.
                </p>
                """
            )
        )

    def test_blank_lines_in_raw(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>

                    A raw paragraph...

                    with many blank lines.

                </p>
                """
            ),
            self.dedent(
                """
                <p>

                    A raw paragraph...

                    with many blank lines.

                </p>
                """
            )
        )

    def test_raw_surrounded_by_Markdown(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Some *Markdown* text.

                <p>*Raw* HTML.</p>

                More *Markdown* text.
                """
            ),
            self.dedent(
                """
                <p>Some <em>Markdown</em> text.</p>
                <p>*Raw* HTML.</p>

                <p>More <em>Markdown</em> text.</p>
                """
            )
        )

    def test_raw_without_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Some *Markdown* text.
                <p>*Raw* HTML.</p>
                More *Markdown* text.
                """
            ),
            # The raw gets treated as inline HTML. This follows the rules and this lib's
            # previous behavior, but not the reference implementation. TODO: Reevaluate.
            self.dedent(
                """
                <p>Some <em>Markdown</em> text.
                <p><em>Raw</em> HTML.</p>
                More <em>Markdown</em> text.</p>
                """
            )
            # The reference implementation does this instead:
            # self.dedent(
            #     """
            #     <p>Some <em>Markdown</em> text.</p>
            #     <p>*Raw* HTML.</p>
            #     <p>More <em>Markdown</em> text.</p>
            #     """
            # )
        )

    def test_raw_with_markdown_blocks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                    Not a Markdown paragraph.

                    * Not a list item.
                    * Another non-list item.

                    Another non-Markdown paragraph.
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                    Not a Markdown paragraph.

                    * Not a list item.
                    * Another non-list item.

                    Another non-Markdown paragraph.
                </div>
                """
            )
        )

    # TODO: This fails. Fix it.
    # The HTML parser is mostly doing the correct thing here. The problem is that the
    # two placeholders are in one paragraph so the postprocessor is not properly
    # swaping then out. It checks for `<p>{ placeholder }</p>` but we have
    # `<p>{ placeholder2 }\n{ placeholder2 }</p>`. We would need to add a second
    # newline or use some other method than the current HTML stash.
    def test_adjacent_raw_blocks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                """
            ),
            self.dedent(
                """
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                """
            )
        )

    def test_adjacent_raw_blocks_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>A raw paragraph.</p>

                <p>A second raw paragraph.</p>
                """
            ),
            self.dedent(
                """
                <p>A raw paragraph.</p>

                <p>A second raw paragraph.</p>
                """
            )
        )

    def test_nested_raw_block(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                <p>A raw paragraph.</p>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p>A raw paragraph.</p>
                </div>
                """
            )
        )

    def test_nested_indented_raw_block(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                    <p>A raw paragraph.</p>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                    <p>A raw paragraph.</p>
                </div>
                """
            )
        )

    def test_nested_raw_blocks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                </div>
                """
            )
        )

    def test_nested_raw_blocks_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>

                <p>A raw paragraph.</p>

                <p>A second raw paragraph.</p>

                </div>
                """
            ),
            self.dedent(
                """
                <div>

                <p>A raw paragraph.</p>

                <p>A second raw paragraph.</p>

                </div>
                """
            )
        )

    def test_raw_nested_inline(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                    <p>
                        <span>*text*</span>
                    </p>
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                    <p>
                        <span>*text*</span>
                    </p>
                </div>
                """
            )
        )

    def test_raw_nested_inline_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>

                    <p>

                        <span>*text*</span>

                    </p>

                </div>
                """
            ),
            self.dedent(
                """
                <div>

                    <p>

                        <span>*text*</span>

                    </p>

                </div>
                """
            )
        )

    def test_raw_p_no_end_tag(self):
        self.assertMarkdownRenders(
            '<p>*text*',
            '<p>*text*'
        )

    def test_raw_multiple_p_no_end_tag(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>*text*'

                <p>more *text*
                """
            ),
            self.dedent(
                """
                <p>*text*'

                <p>more *text*
                """
            )
        )

    def test_raw_p_no_end_tag_followed_by_blank_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>*raw text*'

                Still part of *raw* text.
                """
            ),
            self.dedent(
                """
                <p>*raw text*'

                Still part of *raw* text.
                """
            )
        )

    def test_raw_nested_p_no_end_tag(self):
        self.assertMarkdownRenders(
            '<div><p>*text*</div>',
            '<div><p>*text*</div>'
        )

    def test_raw_open_bracket_only(self):
        self.assertMarkdownRenders(
            '<',
            '<p>&lt;</p>'
        )

    def test_raw_open_bracket_followed_by_space(self):
        self.assertMarkdownRenders(
            '< foo',
            '<p>&lt; foo</p>'
        )

    def test_raw_missing_close_bracket(self):
        self.assertMarkdownRenders(
            '<foo',
            '<p>&lt;foo</p>'
        )

    def test_raw_attributes(self):
        self.assertMarkdownRenders(
            '<p id="foo", class="bar baz", style="margin: 15px; line-height: 1.5; text-align: center;">text</p>',
            '<p id="foo", class="bar baz", style="margin: 15px; line-height: 1.5; text-align: center;">text</p>'
        )

    def test_raw_attributes_nested(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div id="foo, class="bar", style="background: #ffe7e8; border: 2px solid #e66465;">
                    <p id="baz", style="margin: 15px; line-height: 1.5; text-align: center;">text</p>
                </div>
                """
            ),
            self.dedent(
                """
                <div id="foo, class="bar", style="background: #ffe7e8; border: 2px solid #e66465;">
                    <p id="baz", style="margin: 15px; line-height: 1.5; text-align: center;">text</p>
                </div>
                """
            )
        )

    def test_raw_comment_one_line(self):
        self.assertMarkdownRenders(
            '<!-- *foo* -->',
            '<!-- *foo* -->'
        )

    # TODO: Decide behavior here. Python-Markdown current outputs:
    #
    #   <!-- *foo* -->
    #   <p><em>bar</em></p>
    #
    # But the reference implementation outputs:
    #
    #   <p><!-- *foo* --><em>bar</em></p>
    #
    # As the raw HTML is not alone on the line, the reference implementation
    # considers it inline rather than block level. The behavior defined in
    # the test below is from the CommonMark spec, which we don't follow.
    def test_raw_comment_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            '<!-- *foo* -->*bar*',
            '<!-- *foo* -->*bar*'
        )

    def test_raw_multiline_comment(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!--
                *foo*
                -->
                """
            ),
            self.dedent(
                """
                <!--
                *foo*
                -->
                """
            )
        )

    def test_raw_comment_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!--

                *foo*

                -->
                """
            ),
            self.dedent(
                """
                <!--

                *foo*

                -->
                """
            )
        )

    def test_raw_comment_indented(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!--

                    *foo*

                -->
                """
            ),
            self.dedent(
                """
                <!--

                    *foo*

                -->
                """
            )
        )

    def test_raw_comment_nested(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <div>
                <!-- *foo* -->
                </div>
                """
            ),
            self.dedent(
                """
                <div>
                <!-- *foo* -->
                </div>
                """
            )
        )

    def test_raw_processing_instruction_one_line(self):
        self.assertMarkdownRenders(
            "<?php echo '>';' ?>",
            "<?php echo '>';' ?>"
        )

    # This is inline as it is not on a line by itself.
    def test_raw_processing_instruction_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            "<?php echo '>';' ?>*bar*",
            "<p><?php echo '>'; ' ?><em>bar</em></p>"
        )

    def test_raw_multiline_processing_instruction(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <?php
                echo '>';'
                ?>
                """
            ),
            self.dedent(
                """
                <?php
                echo '>';'
                ?>
                """
            )
        )

    def test_raw_processing_instruction_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <?php

                echo '>';'

                ?>
                """
            ),
            self.dedent(
                """
                <?php

                echo '>';'

                ?>
                """
            )
        )

    def test_raw_processing_instruction_indented(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <?php

                    echo '>';'

                ?>
                """
            ),
            self.dedent(
                """
                <?php

                    echo '>';'

                ?>
                """
            )
        )

    def test_raw_declaration_one_line(self):
        self.assertMarkdownRenders(
            '<!DOCTYPE html>',
            '<!DOCTYPE html>'
        )

    # TODO: Decide correct behavior. This matches current behavior and Commonmark.
    # The reference implementation considers this inline not block level:
    #
    #   <p><!DOCTYPE html><em>bar</em></p>
    #
    # But most implementations do this instead:
    #
    #   <p>&lt;!DOCTYPE html&gt;<em>bar</em></p>
    #
    # Either makes sense, but the later seems more correct to me.
    def test_raw_declaration_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            '<!DOCTYPE html>*bar*',
            '<!DOCTYPE html>*bar*'
        )

    def test_raw_multiline_declaration(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!DOCTYPE html PUBLIC
                  "-//W3C//DTD XHTML 1.1//EN"
                  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
                """
            ),
            self.dedent(
                """
                <!DOCTYPE html PUBLIC
                  "-//W3C//DTD XHTML 1.1//EN"
                  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
                """
            )
        )

    def test_raw_cdata_one_line(self):
        self.assertMarkdownRenders(
            '<![CDATA[ document.write(">"); ]]>',
            '<![CDATA[ document.write(">"); ]]>'
        )

    # TODO: Decide correct behavior. This matches current behavior and Commonmark.
    # The reference implementation considers this inline not block level:
    #
    #   <p><![CDATA[ document.write(">"); ]]><em>bar</em></p>
    #
    # But most implementations do this instead:
    #
    #   <p>&lt;[CDATA[ document.write(“&gt;”); ]]&gt;<em>bar</em></p>
    #
    # Either makes sense, but the later seems more correct to me.
    def test_raw_cdata_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            '<![CDATA[ document.write(">"); ]]>*bar*',
            '<![CDATA[ document.write(">"); ]]>*bar*'
        )

    def test_raw_multiline_cdata(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <![CDATA[
                document.write(">");
                ]]>
                """
            ),
            self.dedent(
                """
                <![CDATA[
                document.write(">");
                ]]>
                """
            )
        )

    def test_raw_cdata_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <![CDATA[

                document.write(">");

                ]]>
                """
            ),
            self.dedent(
                """
                <![CDATA[

                document.write(">");

                ]]>
                """
            )
        )

    def test_raw_cdata_indented(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <![CDATA[

                    document.write(">");

                ]]>
                """
            ),
            self.dedent(
                """
                <![CDATA[

                    document.write(">");

                ]]>
                """
            )
        )
