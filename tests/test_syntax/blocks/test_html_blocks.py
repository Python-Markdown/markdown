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

    # TODO: Fix this. Capitalization should be preserved on all tags.
    def test_raw_uppercase(self):
        self.assertMarkdownRenders(
            '<DIV>foo</DIV>',
            '<DIV>foo</DIV>'
        )

    # TODO: fix this. The blank line is optional but matches previous behavior and reference implementation.
    def test_multiple_raw_single__line(self):
        self.assertMarkdownRenders(
            '<p>*foo*</p><div>*bar*</div>',
            self.dedent(
                """
                <p>*foo*</p>

                <div>*bar*</div>
                """
            )
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

    def test_raw_surrounded_by_text_without_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Some *Markdown* text.
                <p>*Raw* HTML.</p>
                More *Markdown* text.
                """
            ),
            # TODO: Work out a way to eliminate the extra blank line.
            self.dedent(
                """
                <p>Some <em>Markdown</em> text.</p>
                <p>*Raw* HTML.</p>

                <p>More <em>Markdown</em> text.</p>
                """
            )
        )

    # TODO: fix this. A blank line between the tags is optional but would be a change in behavior.
    def test_raw_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            '<p>*foo*</p>*bar*',
            self.dedent(
                """
                <p>*foo*</p>
                <p><em>bar</em></p>
                """
            )
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

    def test_adjacent_raw_blocks(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <p>A raw paragraph.</p>
                <p>A second raw paragraph.</p>
                """
            ),
            # TODO: Work out a way to eliminate the extra blank line.
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

    def test_nested_raw_one_line(self):
        self.assertMarkdownRenders(
            '<div><p>*foo*</p></div>',
            '<div><p>*foo*</p></div>'
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

    def test_nested_inline_one_line(self):
        self.assertMarkdownRenders(
            '<p><em>foo</em><br></p>',
            '<p><em>foo</em><br></p>'
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

    def test_raw_html5(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <section>
                    <header>
                        <hgroup>
                            <h1>Hello :-)</h1>
                        </hgroup>
                    </header>
                    <figure>
                        <img src="image.png" alt="" />
                        <figcaption>Caption</figcaption>
                    </figure>
                    <footer>
                        <p>Some footer</p>
                    </footer>
                </section>
                """
            ),
            self.dedent(
                """
                <section>
                    <header>
                        <hgroup>
                            <h1>Hello :-)</h1>
                        </hgroup>
                    </header>
                    <figure>
                        <img src="image.png" alt="" />
                        <figcaption>Caption</figcaption>
                    </figure>
                    <footer>
                        <p>Some footer</p>
                    </footer>
                </section>
                """
            )
        )

    def test_raw_pre_tag(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                Preserve whitespace in raw html

                <pre>
                class Foo():
                    bar = 'bar'

                    @property
                    def baz(self):
                        return self.bar
                </pre>
                """
            ),
            self.dedent(
                """
                <p>Preserve whitespace in raw html</p>
                <pre>
                class Foo():
                    bar = 'bar'

                    @property
                    def baz(self):
                        return self.bar
                </pre>
                """
            )
        )

    def test_raw_pre_tag_nested_escaped_html(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <pre>
                &lt;p&gt;foo&lt;/p&gt;
                </pre>
                """
            ),
            self.dedent(
                """
                <pre>
                &lt;p&gt;foo&lt;/p&gt;
                </pre>
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
                    <p id="baz", style="margin: 15px; line-height: 1.5; text-align: center;">
                        <img scr="../foo.jpg" title="with 'quoted' text." valueless_attr weirdness="<i>foo</i>" />
                    </p>
                </div>
                """
            ),
            self.dedent(
                """
                <div id="foo, class="bar", style="background: #ffe7e8; border: 2px solid #e66465;">
                    <p id="baz", style="margin: 15px; line-height: 1.5; text-align: center;">
                        <img scr="../foo.jpg" title="with 'quoted' text." valueless_attr weirdness="<i>foo</i>" />
                    </p>
                </div>
                """
            )
        )

    def test_raw_comment_one_line(self):
        self.assertMarkdownRenders(
            '<!-- *foo* -->',
            '<!-- *foo* -->'
        )

    def test_raw_comment_one_line_with_tag(self):
        self.assertMarkdownRenders(
            '<!-- <tag> -->',
            '<!-- <tag> -->'
        )

    # Note: this is a change in behavior for Python_markdown but matches the reference implementation.
    # Previous output was `<!-- *foo* -->\n<p><em>bar</em></p>`. Browsers render both the same.
    def test_raw_comment_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            '<!-- *foo* -->*bar*',
            '<p><!-- *foo* --><em>bar</em></p>'
        )

    # TODO: Fix this. This matches Python-Markdown's previous behavior but not the reference implementation,
    # which outputs `<p><!-- *foo* --><p><em>bar</em></p></p>` (which is also the pre-fixed behavior).
    def test_raw_comment_one_line_followed_by_html(self):
        self.assertMarkdownRenders(
            '<!-- *foo* --><p>*bar*</p>',
            self.dedent(
                """
                <!-- *foo* -->
                <p>*bar*</p>
                """
            )
        )

    # TODO: Fix this. The trailing space is triping up the postprocessor: `<p>{placeholder} </p>`.
    # Note: this reflects a slight change in behavior as the trailing spacer is preserved. This matches
    # the reference implementation. However, it should be ok if we did not preserve the trailing space.
    def test_raw_comment_trailing_whitespace(self):
        self.assertMarkdownRenders(
            '<!-- *foo* --> ',
            '<!-- *foo* --> '
        )

    # Note: this is a change in behavior for Python-Markdown, which does *not* match the reference
    # implementation. However, it does match the HTML5 spec. Declarations must start with either
    # `<!DOCTYPE` or `<![`. Anything else that starts with `<!` is a comment. According to the
    # HTML5 spec, a comment without the hyphens is a "bogus comment", but a comment nonetheless.
    # See https://www.w3.org/TR/html52/syntax.html#markup-declaration-open-state.
    # If we wanted to change this behavior, we could override `HTMLParser.parse_bogus_comment()`.
    def test_bogus_comment(self):
        self.assertMarkdownRenders(
            '<!*foo*>',
            '<!--*foo*-->'
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

    def test_raw_multiline_comment_with_tag(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!--
                <tag>
                -->
                """
            ),
            self.dedent(
                """
                <!--
                <tag>
                -->
                """
            )
        )

    def test_raw_multiline_comment_first_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!-- *foo*
                -->
                """
            ),
            self.dedent(
                """
                <!-- *foo*
                -->
                """
            )
        )

    def test_raw_multiline_comment_last_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!--
                *foo* -->
                """
            ),
            self.dedent(
                """
                <!--
                *foo* -->
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

    def test_raw_comment_with_blank_lines_with_tag(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!--

                <tag>

                -->
                """
            ),
            self.dedent(
                """
                <!--

                <tag>

                -->
                """
            )
        )

    def test_raw_comment_with_blank_lines_first_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!-- *foo*

                -->
                """
            ),
            self.dedent(
                """
                <!-- *foo*

                -->
                """
            )
        )

    def test_raw_comment_with_blank_lines_last_line(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!--

                *foo* -->
                """
            ),
            self.dedent(
                """
                <!--

                *foo* -->
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

    def test_raw_comment_indented_with_tag(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!--

                    <tag>

                -->
                """
            ),
            self.dedent(
                """
                <!--

                    <tag>

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

    def test_comment_in_code_block(self):
        self.assertMarkdownRenders(
            '    <!-- *foo* -->',
            self.dedent(
                """
                <pre><code>&lt;!-- *foo* --&gt;
                </code></pre>
                """
            )
        )

    # Note: This is a change in behavior. Previously, Python-Markdown interpreted this in the same manner
    # as browsers and all text after the opening comment tag was considered to be in a comment. However,
    # that did not match the reference implementation. The new behavior does.
    def test_unclosed_comment_(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <!-- unclosed comment

                *not* a comment
                """
            ),
            self.dedent(
                """
                <p>&lt;!-- unclosed comment</p>
                <p><em>not</em> a comment</p>
                """
            )
        )

    def test_raw_processing_instruction_one_line(self):
        self.assertMarkdownRenders(
            "<?php echo '>'; ?>",
            "<?php echo '>'; ?>"
        )

    # This is inline as it is not on a line by itself.
    def test_raw_processing_instruction_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            "<?php echo '>'; ?>*bar*",
            "<p><?php echo '>'; ?><em>bar</em></p>"
        )

    def test_raw_multiline_processing_instruction(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <?php
                echo '>';
                ?>
                """
            ),
            self.dedent(
                """
                <?php
                echo '>';
                ?>
                """
            )
        )

    def test_raw_processing_instruction_with_blank_lines(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <?php

                echo '>';

                ?>
                """
            ),
            self.dedent(
                """
                <?php

                echo '>';

                ?>
                """
            )
        )

    def test_raw_processing_instruction_indented(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <?php

                    echo '>';

                ?>
                """
            ),
            self.dedent(
                """
                <?php

                    echo '>';

                ?>
                """
            )
        )

    def test_raw_declaration_one_line(self):
        self.assertMarkdownRenders(
            '<!DOCTYPE html>',
            '<!DOCTYPE html>'
        )

    # Note: this is a change in behavior for Python_markdown but matches the reference implementation.
    # Previous output was `<!DOCTYPE html>*bar*`.
    def test_raw_declaration_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            '<!DOCTYPE html>*bar*',
            '<p><!DOCTYPE html><em>bar</em></p>'
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

    # Note: this is a change in behavior for Python_markdown but matches the reference implementation.
    # Previous output was `<![CDATA[ document.write(">"); ]]>*bar*`.
    def test_raw_cdata_one_line_followed_by_text(self):
        self.assertMarkdownRenders(
            '<![CDATA[ document.write(">"); ]]>*bar*',
            '<p><![CDATA[ document.write(">"); ]]><em>bar</em></p>'
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

    def test_charref(self):
        self.assertMarkdownRenders(
            '&sect;',
            '<p>&sect;</p>'
        )

    def test_nested_charref(self):
        self.assertMarkdownRenders(
            '<p>&sect;</p>',
            '<p>&sect;</p>'
        )

    def test_entityref(self):
        self.assertMarkdownRenders(
            '&#167;',
            '<p>&#167;</p>'
        )

    def test_nested_entityref(self):
        self.assertMarkdownRenders(
            '<p>&#167;</p>',
            '<p>&#167;</p>'
        )

    # TODO: Fix this. `&T;` is not a valid charref.
    def test_amperstand(self):
        self.assertMarkdownRenders(
            'AT&T & AT&amp;T',
            '<p>AT&amp;T &amp; AT&amp;T</p>'
        )

    def test_startendtag(self):
        self.assertMarkdownRenders(
            '<hr>',
            '<hr>'
        )

    def test_startendtag_with_attrs(self):
        self.assertMarkdownRenders(
            '<hr id="foo" class="bar">',
            '<hr id="foo" class="bar">'
        )

    def test_startendtag_with_space(self):
        self.assertMarkdownRenders(
            '<hr >',
            '<hr >'
        )

    def test_closed_startendtag(self):
        self.assertMarkdownRenders(
            '<hr />',
            '<hr />'
        )

    def test_closed_startendtag_without_space(self):
        self.assertMarkdownRenders(
            '<hr/>',
            '<hr/>'
        )

    def test_closed_startendtag_with_attrs(self):
        self.assertMarkdownRenders(
            '<hr id="foo" class="bar" />',
            '<hr id="foo" class="bar" />'
        )

    def test_nested_startendtag(self):
        self.assertMarkdownRenders(
            '<div><hr></div>',
            '<div><hr></div>'
        )

    def test_nested_closed_startendtag(self):
        self.assertMarkdownRenders(
            '<div><hr /></div>',
            '<div><hr /></div>'
        )

    def test_auto_links_dont_break_parser(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <https://example.com>

                <email@example.com>
                """
            ),
            '<p><a href="https://example.com">https://example.com</a></p>\n'
            '<p><a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#101;&#109;'
            '&#97;&#105;&#108;&#64;&#101;&#120;&#97;&#109;&#112;&#108;&#101;'
            '&#46;&#99;&#111;&#109;">&#101;&#109;&#97;&#105;&#108;&#64;&#101;'
            '&#120;&#97;&#109;&#112;&#108;&#101;&#46;&#99;&#111;&#109;</a></p>'
        )

    def test_text_links_ignored(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                https://example.com

                email@example.com
                """
            ),
            self.dedent(
                """
                <p>https://example.com</p>
                <p>email@example.com</p>
                """
            ),
        )

    # TODO: fix this
    def text_invalid_tags(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                <some [weird](http://example.com) stuff>

                <some>> <<unbalanced>> <<brackets>
                """
            ),
            self.dedent(
                """
                <p><some <a href="http://example.com">weird</a> stuff></p>
                <p><some>&gt; &lt;<unbalanced>&gt; &lt;<brackets></p>
                """
            )
        )
