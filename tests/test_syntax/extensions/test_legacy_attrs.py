# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from markdown.test_tools import TestCase


class TestLegacyAtrributes(TestCase):

    maxDiff = None

    def testLegacyAttrs(self):
        self.assertMarkdownRenders(
            self.dedent("""
                # Header {@id=inthebeginning}

                Now, let's try something *inline{@class=special}*, to see if it works

                @id=TABLE.OF.CONTENTS}


                * {@id=TABLEOFCONTENTS}


                Or in the middle of the text {@id=TABLEOFCONTENTS}

                {@id=tableofcontents}

                [![{@style=float: left; margin: 10px; border:
                none;}](http://fourthought.com/images/ftlogo.png "Fourthought
                logo")](http://fourthought.com/)

                ![img{@id=foo}][img]

                [img]: http://example.com/i.jpg
            """),
            self.dedent("""
                <h1 id="inthebeginning">Header </h1>
                <p>Now, let's try something <em class="special">inline</em>, to see if it works</p>
                <p>@id=TABLE.OF.CONTENTS}</p>
                <ul>
                <li id="TABLEOFCONTENTS"></li>
                </ul>
                <p id="TABLEOFCONTENTS">Or in the middle of the text </p>
                <p id="tableofcontents"></p>
                <p><a href="http://fourthought.com/"><img alt="" src="http://fourthought.com/images/ftlogo.png" style="float: left; margin: 10px; border: none;" title="Fourthought logo" /></a></p>
                <p><img alt="img" id="foo" src="http://example.com/i.jpg" /></p>
            """),  # noqa: E501
            extensions=['legacy_attrs']
        )
