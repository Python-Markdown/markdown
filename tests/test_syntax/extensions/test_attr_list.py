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


class TestAttrList(TestCase):
    maxDiff = None
    default_kwargs = {'extensions': ['attr_list']}

    # TODO: Move the rest of the `attr_list` tests here.

    def test_empty_attr_list(self):
        self.assertMarkdownRenders(
            '*foo*{ }',
            '<p><em>foo</em>{ }</p>'
        )

    def test_curly_after_inline(self):
        self.assertMarkdownRenders(
            '*inline*{.a} } *text*{.a }}',
            '<p><em class="a">inline</em> } <em class="a">text</em>}</p>'
        )

    def test_extra_eq_gets_ignored_inside_curly_inline(self):
        # Undesired behavior but kept for historic compatibility.
        self.assertMarkdownRenders(
            '*inline*{data-test="x" =a} *text*',
            '<p><em data-test="x">inline</em> <em>text</em></p>'
        )

    def test_curly_after_block(self):
        self.assertMarkdownRenders(
            '# Heading {.a} }',
            '<h1>Heading {.a} }</h1>'
        )

    def test_curly_in_single_quote(self):
        self.assertMarkdownRenders(
            "# Heading {data-test='{}'}",
            '<h1 data-test="{}">Heading</h1>'
        )

    def test_curly_in_double_quote(self):
        self.assertMarkdownRenders(
            '# Heading {data-test="{}"}',
            '<h1 data-test="{}">Heading</h1>'
        )

    def test_unclosed_quote_ignored(self):
        # Undesired behavior but kept for historic compatibility.
        self.assertMarkdownRenders(
            '# Heading {foo="bar}',
            '<h1 foo="&quot;bar">Heading</h1>'
        )

    def test_backslash_escape_value(self):
        self.assertMarkdownRenders(
            '# `*Foo*` { id="\\*Foo\\*" }',
            '<h1 id="*Foo*"><code>*Foo*</code></h1>'
        )

    def test_unclosed_curly_with_long_run_of_spaces(self):
        """
        An unclosed attribute list followed by a long run of spaces should be
        left as plain text, no matter how many trailing spaces there are.

        The content and the trailing spaces both match the same part of the
        pattern, so without care the regex backtracks over every way of
        splitting the spaces while failing to find the closing brace.
        """
        text = 'foo\n{a' + (' ' * 50000)
        self.assertMarkdownRenders(text, f'<p>{text}</p>')

    def test_table_td(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                | A { .foo }  | *B*{ .foo } | C { } | D{ .foo }     | E { .foo } F |
                |-------------|-------------|-------|---------------|--------------|
                | a { .foo }  | *b*{ .foo } | c { } | d{ .foo }     | e { .foo } f |
                | valid on td | inline      | empty | missing space | not at end   |
                """
            ),
            self.dedent(
                """
                <table>
                <thead>
                <tr>
                <th class="foo">A</th>
                <th><em class="foo">B</em></th>
                <th>C { }</th>
                <th>D{ .foo }</th>
                <th>E { .foo } F</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                <td class="foo">a</td>
                <td><em class="foo">b</em></td>
                <td>c { }</td>
                <td>d{ .foo }</td>
                <td>e { .foo } f</td>
                </tr>
                <tr>
                <td>valid on td</td>
                <td>inline</td>
                <td>empty</td>
                <td>missing space</td>
                <td>not at end</td>
                </tr>
                </tbody>
                </table>
                """
            ),
            extensions=['attr_list', 'tables']
        )


class TestAttrListValuelessAttributes(TestCase):
    """ Valueless (boolean-style) attributes are preserved as provided.

    Only known boolean attributes keep the historic `key="key"`
    representation, and the list of known attributes differs per
    output format. See issue #1501.
    """

    maxDiff = None
    default_kwargs = {'extensions': ['attr_list']}

    def test_valueless_non_boolean_preserved_xhtml(self):
        self.assertMarkdownRenders(
            '[download](file.txt){download}',
            '<p><a download href="file.txt">download</a></p>'
        )

    def test_valueless_non_boolean_preserved_html(self):
        self.assertMarkdownRenders(
            '[download](file.txt){download}',
            '<p><a download href="file.txt">download</a></p>',
            output_format='html'
        )

    def test_valueless_non_boolean_consistent_across_formats(self):
        # Previously `xhtml` rendered `download="download"` (which gives the
        # downloaded file a default name) while `html` rendered bare
        # `download` (which does not): the same source changed meaning with
        # the output format.
        for output_format in ['xhtml', 'html']:
            self.assertMarkdownRenders(
                '[download](file.txt){download}',
                '<p><a download href="file.txt">download</a></p>',
                output_format=output_format
            )

    def test_explicit_value_equal_to_name_preserved(self):
        # An explicitly assigned value must not be dropped, even when it is
        # equal to the attribute name and the attribute is not boolean.
        for output_format in ['xhtml', 'html']:
            self.assertMarkdownRenders(
                '[download](file.txt){download="download"}',
                '<p><a download="download" href="file.txt">download</a></p>',
                output_format=output_format
            )

    def test_known_boolean_attribute_xhtml(self):
        self.assertMarkdownRenders(
            '[x](y){checked}',
            '<p><a checked="checked" href="y">x</a></p>'
        )

    def test_known_boolean_attribute_html(self):
        self.assertMarkdownRenders(
            '[x](y){checked}',
            '<p><a checked href="y">x</a></p>',
            output_format='html'
        )

    def test_xhtml_only_boolean_attribute(self):
        # `compact` is a boolean attribute in XHTML 1.0 but not in HTML.
        self.assertMarkdownRenders(
            '# Heading {compact}',
            '<h1 compact="compact">Heading</h1>'
        )
        self.assertMarkdownRenders(
            '# Heading {compact}',
            '<h1 compact>Heading</h1>',
            output_format='html'
        )

    def test_html_only_boolean_attribute(self):
        # `open` is a boolean attribute in HTML but not in XHTML 1.0. It
        # renders bare in both formats: in HTML as a known boolean, and in
        # XHTML as a valueless attribute preserved as provided.
        for output_format in ['xhtml', 'html']:
            self.assertMarkdownRenders(
                '[x](y){open}',
                '<p><a href="y" open>x</a></p>',
                output_format=output_format
            )

    def test_generic_valueless_attribute(self):
        for output_format in ['xhtml', 'html']:
            self.assertMarkdownRenders(
                '[x](y){foo}',
                '<p><a foo href="y">x</a></p>',
                output_format=output_format
            )

    def test_valueless_attribute_on_block_element(self):
        self.assertMarkdownRenders(
            '# Heading {download}',
            '<h1 download>Heading</h1>'
        )

    def test_get_attrs_and_remainder_marks_valueless_as_none(self):
        from markdown.extensions.attr_list import get_attrs_and_remainder
        attrs, remainder = get_attrs_and_remainder('download checked key=value .cls #the-id')
        self.assertEqual(remainder, '')
        self.assertIn(('download', None), attrs)
        self.assertIn(('checked', None), attrs)
        self.assertIn(['key', 'value'], attrs)
        self.assertIn(('.', 'cls'), attrs)
        self.assertIn(('id', 'the-id'), attrs)

    def test_serializer_renders_none_value_as_bare_name(self):
        import xml.etree.ElementTree as etree

        from markdown.serializers import to_html_string, to_xhtml_string

        elem = etree.Element('a')
        elem.set('download', None)
        elem.set('checked', 'checked')
        elem.set('href', 'file.txt')
        elem.text = 'x'
        self.assertEqual(
            to_html_string(elem),
            '<a checked download href="file.txt">x</a>'
        )
        self.assertEqual(
            to_xhtml_string(elem),
            '<a checked="checked" download href="file.txt">x</a>'
        )

    def test_serializer_preserves_explicit_value_equal_to_name(self):
        import xml.etree.ElementTree as etree

        from markdown.serializers import to_html_string, to_xhtml_string

        elem = etree.Element('a')
        elem.set('download', 'download')
        elem.text = 'x'
        self.assertEqual(to_html_string(elem), '<a download="download">x</a>')
        self.assertEqual(to_xhtml_string(elem), '<a download="download">x</a>')

    def test_fenced_code_valueless_config_word(self):
        # `fenced_code` shares the attribute parser: a valueless config word
        # keeps its historic treatment there (key used as its own value).
        self.assertMarkdownRenders(
            '``` { .python linenos }\nx = 1\n```',
            '<pre><code class="language-python" linenos="linenos">x = 1\n</code></pre>',
            extensions=['fenced_code', 'attr_list']
        )
