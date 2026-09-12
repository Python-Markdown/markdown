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

Copyright 2007-2019 The Python Markdown Project (v. 1.7 and later)
Copyright 2004, 2005, 2006 Yuri Takhteyev (v. 0.2-1.6b)
Copyright 2004 Manfred Stienstra (the original version)

License: BSD (see LICENSE.md for details).
"""

from markdown.test_tools import TestCase


class TestNotEmphasis(TestCase):

    def test_standalone_asterisk(self):
        self.assertMarkdownRenders(
            '*',
            '<p>*</p>'
        )

    def test_standalone_understore(self):
        self.assertMarkdownRenders(
            '_',
            '<p>_</p>'
        )

    def test_standalone_asterisks_consecutive(self):
        self.assertMarkdownRenders(
            'Foo * * * *',
            '<p>Foo * * * *</p>'
        )

    def test_standalone_understore_consecutive(self):
        self.assertMarkdownRenders(
            'Foo _ _ _ _',
            '<p>Foo _ _ _ _</p>'
        )

    def test_standalone_asterisks_pairs(self):
        self.assertMarkdownRenders(
            'Foo ** ** ** **',
            '<p>Foo ** ** ** **</p>'
        )

    def test_standalone_understore_pairs(self):
        self.assertMarkdownRenders(
            'Foo __ __ __ __',
            '<p>Foo __ __ __ __</p>'
        )

    def test_standalone_asterisks_triples(self):
        self.assertMarkdownRenders(
            'Foo *** *** *** ***',
            '<p>Foo *** *** *** ***</p>'
        )

    def test_standalone_understore_triples(self):
        self.assertMarkdownRenders(
            'Foo ___ ___ ___ ___',
            '<p>Foo ___ ___ ___ ___</p>'
        )

    def test_standalone_asterisk_in_text(self):
        self.assertMarkdownRenders(
            'foo * bar',
            '<p>foo * bar</p>'
        )

    def test_standalone_understore_in_text(self):
        self.assertMarkdownRenders(
            'foo _ bar',
            '<p>foo _ bar</p>'
        )

    def test_standalone_asterisks_in_text(self):
        self.assertMarkdownRenders(
            'foo * bar * baz',
            '<p>foo * bar * baz</p>'
        )

    def test_standalone_understores_in_text(self):
        self.assertMarkdownRenders(
            'foo _ bar _ baz',
            '<p>foo _ bar _ baz</p>'
        )

    def test_standalone_asterisks_with_newlines(self):
        self.assertMarkdownRenders(
            'foo\n* bar *\nbaz',
            '<p>foo\n* bar *\nbaz</p>'
        )

    def test_standalone_understores_with_newlines(self):
        self.assertMarkdownRenders(
            'foo\n_ bar _\nbaz',
            '<p>foo\n_ bar _\nbaz</p>'
        )

    def test_standalone_underscore_at_begin(self):
        self.assertMarkdownRenders(
            '_ foo_ bar',
            '<p>_ foo_ bar</p>'
        )

    def test_standalone_asterisk_at_end(self):
        self.assertMarkdownRenders(
            'foo *bar *',
            '<p>foo *bar *</p>'
        )

    def test_standalone_understores_at_begin_end(self):
        self.assertMarkdownRenders(
            '_ bar _',
            '<p>_ bar _</p>'
        )

    def test_complex_emphasis_asterisk(self):
        self.assertMarkdownRenders(
            'This is text **bold *italic bold*** with more text',
            '<p>This is text <strong>bold <em>italic bold</em></strong> with more text</p>'
        )

    def test_complex_emphasis_asterisk_mid_word(self):
        self.assertMarkdownRenders(
            'This is text **bold*italic bold*** with more text',
            '<p>This is text <strong>bold<em>italic bold</em></strong> with more text</p>'
        )

    def test_complex_emphasis_smart_underscore(self):
        self.assertMarkdownRenders(
            'This is text __bold _italic bold___ with more text',
            '<p>This is text <strong>bold <em>italic bold</em></strong> with more text</p>'
        )

    def test_complex_emphasis_smart_underscore_mid_word(self):
        self.assertMarkdownRenders(
            'This is text __bold_italic bold___ with more text',
            '<p>This is text <strong>bold_italic bold</strong>_ with more text</p>'
        )

    def test_nested_emphasis(self):

        self.assertMarkdownRenders(
            'This text is **bold *italic* *italic* bold**',
            '<p>This text is <strong>bold <em>italic</em> <em>italic</em> bold</strong></p>'
        )

    def test_complex_multple_emphasis_type(self):

        self.assertMarkdownRenders(
            'traced ***along*** bla **blocked** if other ***or***',
            '<p>traced <strong><em>along</em></strong> bla <strong>blocked</strong> if other <strong><em>or</em></strong></p>'  # noqa: E501
        )

    def test_complex_multple_emphasis_type_variant2(self):

        self.assertMarkdownRenders(
            'on the **1-4 row** of the AP Combat Table ***and*** receive',
            '<p>on the <strong>1-4 row</strong> of the AP Combat Table <strong><em>and</em></strong> receive</p>'
        )

    def test_link_emphasis_outer(self):

        self.assertMarkdownRenders(
            '**[text](url)**',
            '<p><strong><a href="url">text</a></strong></p>'
        )

    def test_link_emphasis_inner(self):

        self.assertMarkdownRenders(
            '[**text**](url)',
            '<p><a href="url"><strong>text</strong></a></p>'
        )

    def test_link_emphasis_inner_outer(self):

        self.assertMarkdownRenders(
            '**[**text**](url)**',
            '<p><strong><a href="url"><strong>text</strong></a></strong></p>'
        )

    def test_underscore_legacy(self):

        self.assertMarkdownRenders(
            self.dedent(
                """
                THIS_SHOULD_STAY_AS_IS

                Here is some _emphasis_, ok?

                Ok, at least _this_ should work.

                THIS__SHOULD__STAY

                Here is some __strong__ stuff.

                THIS___SHOULD___STAY?
                """
            ),
            self.dedent(
                """
                <p>THIS_SHOULD_STAY_AS_IS</p>
                <p>Here is some <em>emphasis</em>, ok?</p>
                <p>Ok, at least <em>this</em> should work.</p>
                <p>THIS__SHOULD__STAY</p>
                <p>Here is some <strong>strong</strong> stuff.</p>
                <p>THIS___SHOULD___STAY?</p>
                """
            )
        )

    def test_nested_patterns(self):

        self.assertMarkdownRenders(
            self.dedent(
                """
                ___[link](http://example.com)___
                ***[link](http://example.com)***
                **[*link*](http://example.com)**
                __[_link_](http://example.com)__
                __[*link*](http://example.com)__
                **[_link_](http://example.com)**
                [***link***](http://example.com)

                ***I am ___italic_ and__ bold* I am `just` bold**

                Example __*bold italic*__ on the same line __*bold italic*__.

                Example **_bold italic_** on the same line **_bold italic_**.
                """
            ),
            self.dedent(
                """
                <p><strong><em><a href="http://example.com">link</a></em></strong>
                <strong><em><a href="http://example.com">link</a></em></strong>
                <strong><a href="http://example.com"><em>link</em></a></strong>
                <strong><a href="http://example.com"><em>link</em></a></strong>
                <strong><a href="http://example.com"><em>link</em></a></strong>
                <strong><a href="http://example.com"><em>link</em></a></strong>
                <a href="http://example.com"><strong><em>link</em></strong></a></p>
                <p><strong><em>I am <strong><em>italic</em> and</strong> bold</em> I am <code>just</code> bold</strong></p>
                <p>Example <strong><em>bold italic</em></strong> on the same line <strong><em>bold italic</em></strong>.</p>
                <p>Example <strong><em>bold italic</em></strong> on the same line <strong><em>bold italic</em></strong>.</p>
                """  # noqa: E501
            )
        )

    def test_em_strong_complex(self):

        self.assertMarkdownRenders(
            self.dedent(
                """
                ___test test__ test test_

                ___test test_ test test__

                ___test___

                __test__

                ___test_ test___

                ___test_ test__

                _test_test test_test_

                ***test test** test test*

                ***test test* test test**

                **test*

                ***test***

                **test***

                ***test* test**

                *test*test test*test*
                """
            ),
            self.dedent(
                """
                <p><em><strong>test test</strong> test test</em></p>
                <p><strong><em>test test</em> test test</strong></p>
                <p><strong><em>test</em></strong></p>
                <p><strong>test</strong></p>
                <p><strong><em>test</em> test</strong>_</p>
                <p><strong><em>test</em> test</strong></p>
                <p><em>test_test test_test</em></p>
                <p><em><strong>test test</strong> test test</em></p>
                <p><strong><em>test test</em> test test</strong></p>
                <p>*<em>test</em></p>
                <p><strong><em>test</em></strong></p>
                <p><strong>test</strong>*</p>
                <p><strong><em>test</em> test</strong></p>
                <p><em>test</em>test test<em>test</em></p>
                """
            )
        )

    def test_strong_and_em_together(self):

        self.assertMarkdownRenders(
            self.dedent(
                """
                ***This is strong and em.***

                So is ***this*** word.

                ___This is strong and em.___

                So is ___this___ word.
                """
            ),
            self.dedent(
                """
                <p><strong><em>This is strong and em.</em></strong></p>
                <p>So is <strong><em>this</em></strong> word.</p>
                <p><strong><em>This is strong and em.</em></strong></p>
                <p>So is <strong><em>this</em></strong> word.</p>
                """
            )
        )

    def test_advanced_nesting(self):

        self.assertMarkdownRenders(
            self.dedent(
                """
                **a*bc**

                *a**b**c**d**e**f*

                ***a**b*cd**e*f***

                ***a**b*cd*e**f***

                ***a**b*cd*e**f*g*h***

                ***a***bc**d*e***

                *a**b**c**d**e**f*

                *a**b***c**d***e**f*

                *a**b***c**d***e**f**

                __a _b c__

                _a __b __c __d __e __f_

                ___a __b _c d__ e_ f___

                ___a __b _c d_ e__ f___

                ___a __b _c d_ e__ f _g_ h___

                ___a ___b c__ d_ e___

                _a __b__ _c __d__ _e __f__
                """
            ),
            self.dedent(
                """
                <p>*<em>a<em>bc</em></em></p>
                <p><em>a<strong>b</strong>c<strong>d</strong>e**f</em></p>
                <p><em><strong>a</strong>b</em>cd<strong>e<em>f</em></strong></p>
                <p><em><strong>a</strong>b</em>cd<em>e<strong>f</strong></em></p>
                <p><em><strong>a</strong>b</em>cd<em>e<strong>f<em>g</em>h</strong></em></p>
                <p><strong><em>a</em></strong>bc<strong>d<em>e</em></strong></p>
                <p><em>a<strong>b</strong>c<strong>d</strong>e**f</em></p>
                <p><em>a<strong>b</strong></em>c<strong>d</strong><em>e**f</em></p>
                <p><em>a<strong>b</strong></em>c<strong>d</strong>*e<strong>f</strong></p>
                <p>_<em>a <em>b c</em></em></p>
                <p>_a __b __c __d __e _<em>f</em></p>
                <p><strong><em>a <em><em>b <em>c d</em></em> e</em> f</em></strong></p>
                <p><strong><em>a <strong>b <em>c d</em> e</strong> f</em></strong></p>
                <p><strong><em>a <strong>b <em>c d</em> e</strong> f <em>g</em> h</em></strong></p>
                <p><strong><em>a <em><strong>b c</strong> d</em> e</em></strong></p>
                <p>_a <strong>b</strong> _c <strong>d</strong> _e <strong>f</strong></p>
                """
            )
        )


class TestCommonMark(TestCase):
    """Test CommonMark."""

    def test_commonmark(self):
        """Test CommonMark."""

        self.maxDiff = None

        self.assertMarkdownRenders(
            self.dedent(
                R"""
                *foo bar*

                a * foo bar*

                <!-- a*"foo"* -->

                <!-- *$*alpha.

                *£*bravo.

                *€*charlie. -->

                <!-- Augment because Python Markdown parses lists first -->
                test * a *

                foo*bar*

                5*6*78

                _foo bar_

                _ foo bar_

                a_"foo"_

                foo_bar_

                5_6_78

                пристаням_стремятся_

                aa_"bb"_cc

                foo-_(bar)_

                _foo*

                *foo bar *

                *foo bar
                *

                <!-- *(*foo) -->

                *(*foo*)*

                *foo*bar

                _foo bar _

                _(_foo)

                _(_foo_)_

                _foo_bar

                _пристаням_стремятся

                _foo_bar_baz_

                _(bar)_.

                **foo bar**

                ** foo bar**

                <!-- a**"foo"** -->

                foo**bar**

                __foo bar__

                __ foo bar__

                __
                foo bar__

                a__"foo"__

                foo__bar__

                5__6__78

                пристаням__стремятся__

                __foo, __bar__, baz__

                foo-__(bar)__

                **foo bar **

                <!-- **(**foo) -->

                *(**foo**)*

                **Gomphocarpus (*Gomphocarpus physocarpus*, syn.
                *Asclepias physocarpa*)**

                **foo "*bar*" foo**

                **foo**bar

                __foo bar __

                __(__foo)

                _(__foo__)_

                __foo__bar

                __пристаням__стремятся

                __foo__bar__baz__

                __(bar)__.

                *foo [bar](/url)*

                *foo
                bar*

                _foo __bar__ baz_

                _foo _bar_ baz_

                __foo_ bar_

                *foo *bar**

                *foo **bar** baz*

                *foo**bar**baz*

                *foo**bar*

                ***foo** bar*

                *foo **bar***

                *foo**bar***

                <!-- Python Markdown prefers triple tokens as <strong><em> -->
                foo***bar***baz

                foo******bar*********baz

                *foo **bar *baz* bim** bop*

                *foo [*bar*](/url)*

                ** is not an empty emphasis

                **** is not an empty strong emphasis

                **foo [bar](/url)**

                **foo
                bar**

                __foo _bar_ baz__

                __foo __bar__ baz__

                ____foo__ bar__

                **foo **bar****

                **foo *bar* baz**

                **foo*bar*baz**

                ***foo* bar**

                **foo *bar***

                **foo *bar **baz**
                bim* bop**

                **foo [*bar*](/url)**

                __ is not an empty emphasis

                ____ is not an empty strong emphasis

                foo ***

                foo *\**

                foo *_*

                foo *****

                foo **\***

                foo **_**

                **foo*

                *foo**

                ***foo**

                ****foo*

                **foo***

                *foo****

                foo ___

                foo _\__

                foo _*_

                foo _____

                foo __\___

                foo __*__

                __foo_

                _foo__

                ___foo__

                ____foo_

                __foo___

                _foo____

                **foo**

                *_foo_*

                __foo__

                _*foo*_

                ****foo****

                ____foo____

                ******foo******

                <!-- Python Markdown prefers triple tokens as <strong><em> -->
                ***foo***

                _____foo_____

                *foo _bar* baz_

                <!-- we run * and _ in different passes, we cannot match CommonMark here currently>
                <!-- *foo __bar *baz bim__ bam* -->

                **foo **bar baz**

                *foo *bar baz*

                *[bar*](/url)

                _foo [bar_](/url)

                *<img src="foo" title="*"/>

                **<a href="**">

                __<a href="__">

                *a `*`*

                _a `_`_

                **a<https://foo.bar/?q=**>

                __a<https://foo.bar/?q=__>
                """
            ),
            self.dedent(
                """
                <p><em>foo bar</em></p>
                <p>a * foo bar*</p>
                <!-- a*"foo"* -->

                <!-- *$*alpha.

                *£*bravo.

                *€*charlie. -->

                <!-- Augment because Python Markdown parses lists first -->
                <p>test * a *</p>
                <p>foo<em>bar</em></p>
                <p>5<em>6</em>78</p>
                <p><em>foo bar</em></p>
                <p>_ foo bar_</p>
                <p>a_"foo"_</p>
                <p>foo_bar_</p>
                <p>5_6_78</p>
                <p>пристаням_стремятся_</p>
                <p>aa_"bb"_cc</p>
                <p>foo-<em>(bar)</em></p>
                <p>_foo*</p>
                <p>*foo bar *</p>
                <p>*foo bar
                *</p>
                <!-- *(*foo) -->

                <p><em>(</em>foo<em>)</em></p>
                <p><em>foo</em>bar</p>
                <p>_foo bar _</p>
                <p>_(_foo)</p>
                <p><em>(<em>foo</em>)</em></p>
                <p>_foo_bar</p>
                <p>_пристаням_стремятся</p>
                <p><em>foo_bar_baz</em></p>
                <p><em>(bar)</em>.</p>
                <p><strong>foo bar</strong></p>
                <p>** foo bar**</p>
                <!-- a**"foo"** -->

                <p>foo<strong>bar</strong></p>
                <p><strong>foo bar</strong></p>
                <p>__ foo bar__</p>
                <p>__
                foo bar__</p>
                <p>a__"foo"__</p>
                <p>foo__bar__</p>
                <p>5__6__78</p>
                <p>пристаням__стремятся__</p>
                <p><strong>foo, <strong>bar</strong>, baz</strong></p>
                <p>foo-<strong>(bar)</strong></p>
                <p>**foo bar **</p>
                <!-- **(**foo) -->

                <p><em>(<strong>foo</strong>)</em></p>
                <p><strong>Gomphocarpus (<em>Gomphocarpus physocarpus</em>, syn.
                <em>Asclepias physocarpa</em>)</strong></p>
                <p><strong>foo "<em>bar</em>" foo</strong></p>
                <p><strong>foo</strong>bar</p>
                <p>__foo bar __</p>
                <p>__(__foo)</p>
                <p><em>(<strong>foo</strong>)</em></p>
                <p>__foo__bar</p>
                <p>__пристаням__стремятся</p>
                <p><strong>foo__bar__baz</strong></p>
                <p><strong>(bar)</strong>.</p>
                <p><em>foo <a href="/url">bar</a></em></p>
                <p><em>foo
                bar</em></p>
                <p><em>foo <strong>bar</strong> baz</em></p>
                <p><em>foo <em>bar</em> baz</em></p>
                <p><em><em>foo</em> bar</em></p>
                <p><em>foo <em>bar</em></em></p>
                <p><em>foo <strong>bar</strong> baz</em></p>
                <p><em>foo<strong>bar</strong>baz</em></p>
                <p><em>foo**bar</em></p>
                <p><em><strong>foo</strong> bar</em></p>
                <p><em>foo <strong>bar</strong></em></p>
                <p><em>foo<strong>bar</strong></em></p>
                <!-- Python Markdown prefers triple tokens as <strong><em> -->
                <p>foo<strong><em>bar</em></strong>baz</p>
                <p>foo<strong><strong><strong>bar</strong></strong></strong>***baz</p>
                <p><em>foo <strong>bar <em>baz</em> bim</strong> bop</em></p>
                <p><em>foo <a href="/url"><em>bar</em></a></em></p>
                <p>** is not an empty emphasis</p>
                <p>**** is not an empty strong emphasis</p>
                <p><strong>foo <a href="/url">bar</a></strong></p>
                <p><strong>foo
                bar</strong></p>
                <p><strong>foo <em>bar</em> baz</strong></p>
                <p><strong>foo <strong>bar</strong> baz</strong></p>
                <p><strong><strong>foo</strong> bar</strong></p>
                <p><strong>foo <strong>bar</strong></strong></p>
                <p><strong>foo <em>bar</em> baz</strong></p>
                <p><strong>foo<em>bar</em>baz</strong></p>
                <p><strong><em>foo</em> bar</strong></p>
                <p><strong>foo <em>bar</em></strong></p>
                <p><strong>foo <em>bar <strong>baz</strong>
                bim</em> bop</strong></p>
                <p><strong>foo <a href="/url"><em>bar</em></a></strong></p>
                <p>__ is not an empty emphasis</p>
                <p>____ is not an empty strong emphasis</p>
                <p>foo ***</p>
                <p>foo <em>*</em></p>
                <p>foo <em>_</em></p>
                <p>foo *****</p>
                <p>foo <strong>*</strong></p>
                <p>foo <strong>_</strong></p>
                <p>*<em>foo</em></p>
                <p><em>foo</em>*</p>
                <p>*<strong>foo</strong></p>
                <p>***<em>foo</em></p>
                <p><strong>foo</strong>*</p>
                <p><em>foo</em>***</p>
                <p>foo ___</p>
                <p>foo <em>_</em></p>
                <p>foo <em>*</em></p>
                <p>foo _____</p>
                <p>foo <strong>_</strong></p>
                <p>foo <strong>*</strong></p>
                <p>_<em>foo</em></p>
                <p><em>foo</em>_</p>
                <p>_<strong>foo</strong></p>
                <p>___<em>foo</em></p>
                <p><strong>foo</strong>_</p>
                <p><em>foo</em>___</p>
                <p><strong>foo</strong></p>
                <p><em><em>foo</em></em></p>
                <p><strong>foo</strong></p>
                <p><em><em>foo</em></em></p>
                <p><strong><strong>foo</strong></strong></p>
                <p><strong><strong>foo</strong></strong></p>
                <p><strong><strong><strong>foo</strong></strong></strong></p>
                <!-- Python Markdown prefers triple tokens as <strong><em> -->
                <p><strong><em>foo</em></strong></p>
                <p><strong><em><strong>foo</strong></em></strong></p>
                <p><em>foo _bar</em> baz_</p>
                <!-- we run * and _ in different passes, we cannot match CommonMark here currently>
                <!-- *foo __bar *baz bim__ bam* -->

                <p>**foo <strong>bar baz</strong></p>
                <p>*foo <em>bar baz</em></p>
                <p>*<a href="/url">bar*</a></p>
                <p>_foo <a href="/url">bar_</a></p>
                <p>*<img src="foo" title="*"/></p>
                <p>**<a href="**"></p>
                <p>__<a href="__"></p>
                <p><em>a <code>*</code></em></p>
                <p><em>a <code>_</code></em></p>
                <p>**a<a href="https://foo.bar/?q=**">https://foo.bar/?q=**</a></p>
                <p>__a<a href="https://foo.bar/?q=__">https://foo.bar/?q=__</a></p>
                """
            )
        )


class TestProcessorRemoval(TestCase):

    def test_remove_processor(self):

        import markdown
        from markdown.inlinepatterns import DelimiterProcessor

        # Remove all delimiter processors
        md = markdown.Markdown()

        extensions = md.delimiters.values()
        self.assertEqual(len(extensions), 2)

        for ext in md.delimiters.values():
            self.assertTrue(isinstance(ext, DelimiterProcessor))

        md.inlinePatterns.deregister('em_strong')
        md.inlinePatterns.deregister('em_strong2')

        # Call reset which will cause them to remove themselves from being registered
        md.reset()

        extensions = md.delimiters.values()
        self.assertEqual(len(extensions), 0)
