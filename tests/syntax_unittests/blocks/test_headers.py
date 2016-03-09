import unittest
from markdown.test_tools import TestCase


class TestSetextHeaders(TestCase):

    def test_setext_h1(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H1
                =============
                """
            ),
            
            '<h1>This is an H1</h1>'
        )

    def test_setext_h2(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H2
                -------------
                """
            ),
            
            '<h2>This is an H2</h2>'
        )

    def test_setext_h1_mismatched_length(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H1
                ===
                """
            ),
            
            '<h1>This is an H1</h1>'
        )
    
    def test_setext_h2_mismatched_length(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H2
                ---
                """
            ),
            
            '<h2>This is an H2</h2>'
        )

    def test_setext_h1_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H1
                =============
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h1>This is an H1</h1>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )
    
    def test_setext_h2_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is an H2
                -------------
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h2>This is an H2</h2>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )

    # TODO: fix this
    # see http://johnmacfarlane.net/babelmark2/?normalize=1&text=Paragraph%0AAn+H1%0A%3D%3D%3D%3D%3D
    @unittest.skip('This is broken in Python-Markdown')
    def test_p_followed_by_setext_h1(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is a Paragraph.
                Followed by an H1 with no blank line.
                =====================================
                """
            ),
            self.dedent(
                """
                <p>This is a Paragraph.</p>
                <h1>Followed by an H1 with no blank line.</h1>
                """
            )
        )

    # TODO: fix this
    # see http://johnmacfarlane.net/babelmark2/?normalize=1&text=Paragraph%0AAn+H2%0A-----
    @unittest.skip('This is broken in Python-Markdown')
    def test_p_followed_by_setext_h2(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                This is a Paragraph.
                Followed by an H2 with no blank line.
                -------------------------------------
                """
            ),
            self.dedent(
                """
                <p>This is a Paragraph.</p>
                <h2>Followed by an H2 with no blank line.</h2>
                """
            )
        )

class TestHashHeaders(TestCase):

    def test_hash_h1_open(self):
        self.assertMarkdownRenders(
            '# This is an H1',
            
            '<h1>This is an H1</h1>'
        )

    def test_hash_h2_open(self):
        self.assertMarkdownRenders(
            '## This is an H2',
            
            '<h2>This is an H2</h2>'
        )
    
    def test_hash_h3_open(self):
        self.assertMarkdownRenders(
            '### This is an H3',
            
            '<h3>This is an H3</h3>'
        )

    def test_hash_h4_open(self):
        self.assertMarkdownRenders(
            '#### This is an H4',
            
            '<h4>This is an H4</h4>'
        )

    def test_hash_h5_open(self):
        self.assertMarkdownRenders(
            '##### This is an H5',
            
            '<h5>This is an H5</h5>'
        )
    
    def test_hash_h6_open(self):
        self.assertMarkdownRenders(
            '###### This is an H6',
            
            '<h6>This is an H6</h6>'
        )
    
    def test_hash_gt6_open(self):
        self.assertMarkdownRenders(
            '####### This is an H6',
            
            '<h6># This is an H6</h6>'
        )
    
    def test_hash_h1_open_missing_space(self):
        self.assertMarkdownRenders(
            '#This is an H1',
            
            '<h1>This is an H1</h1>'
        )

    def test_hash_h2_open_missing_space(self):
        self.assertMarkdownRenders(
            '##This is an H2',
            
            '<h2>This is an H2</h2>'
        )
    
    def test_hash_h3_open_missing_space(self):
        self.assertMarkdownRenders(
            '###This is an H3',
            
            '<h3>This is an H3</h3>'
        )

    def test_hash_h4_open_missing_space(self):
        self.assertMarkdownRenders(
            '####This is an H4',
            
            '<h4>This is an H4</h4>'
        )

    def test_hash_h5_open_missing_space(self):
        self.assertMarkdownRenders(
            '#####This is an H5',
            
            '<h5>This is an H5</h5>'
        )
    
    def test_hash_h6_open_missing_space(self):
        self.assertMarkdownRenders(
            '######This is an H6',
            
            '<h6>This is an H6</h6>'
        )
    
    def test_hash_gt6_open_missing_space(self):
        self.assertMarkdownRenders(
            '#######This is an H6',
            
            '<h6>#This is an H6</h6>'
        )
    
    def test_hash_h1_closed(self):
        self.assertMarkdownRenders(
            '# This is an H1 #',
            
            '<h1>This is an H1</h1>'
        )

    def test_hash_h2_closed(self):
        self.assertMarkdownRenders(
            '## This is an H2 ##',
            
            '<h2>This is an H2</h2>'
        )
    
    def test_hash_h3_closed(self):
        self.assertMarkdownRenders(
            '### This is an H3 ###',
            
            '<h3>This is an H3</h3>'
        )

    def test_hash_h4_closed(self):
        self.assertMarkdownRenders(
            '#### This is an H4 ####',
            
            '<h4>This is an H4</h4>'
        )

    def test_hash_h5_closed(self):
        self.assertMarkdownRenders(
            '##### This is an H5 #####',
            
            '<h5>This is an H5</h5>'
        )
    
    def test_hash_h6_closed(self):
        self.assertMarkdownRenders(
            '###### This is an H6 ######',
            
            '<h6>This is an H6</h6>'
        )
    
    def test_hash_gt6_closed(self):
        self.assertMarkdownRenders(
            '####### This is an H6 #######',
            
            '<h6># This is an H6</h6>'
        )
    
    def test_hash_h1_closed_missing_space(self):
        self.assertMarkdownRenders(
            '#This is an H1#',
            
            '<h1>This is an H1</h1>'
        )

    def test_hash_h2_closed_missing_space(self):
        self.assertMarkdownRenders(
            '##This is an H2##',
            
            '<h2>This is an H2</h2>'
        )
    
    def test_hash_h3_closed_missing_space(self):
        self.assertMarkdownRenders(
            '###This is an H3###',
            
            '<h3>This is an H3</h3>'
        )

    def test_hash_h4_closed_missing_space(self):
        self.assertMarkdownRenders(
            '####This is an H4####',
            
            '<h4>This is an H4</h4>'
        )

    def test_hash_h5_closed_missing_space(self):
        self.assertMarkdownRenders(
            '#####This is an H5#####',
            
            '<h5>This is an H5</h5>'
        )
    
    def test_hash_h6_closed_missing_space(self):
        self.assertMarkdownRenders(
            '######This is an H6######',
            
            '<h6>This is an H6</h6>'
        )
    
    def test_hash_gt6_closed_missing_space(self):
        self.assertMarkdownRenders(
            '#######This is an H6#######',
            
            '<h6>#This is an H6</h6>'
        )

    def test_hash_h1_closed_mismatch(self):
        self.assertMarkdownRenders(
            '# This is an H1 ##',
            
            '<h1>This is an H1</h1>'
        )

    def test_hash_h2_closed_mismatch(self):
        self.assertMarkdownRenders(
            '## This is an H2 #',
            
            '<h2>This is an H2</h2>'
        )
    
    def test_hash_h3_closed_mismatch(self):
        self.assertMarkdownRenders(
            '### This is an H3 #',
            
            '<h3>This is an H3</h3>'
        )

    def test_hash_h4_closed_mismatch(self):
        self.assertMarkdownRenders(
            '#### This is an H4 #',
            
            '<h4>This is an H4</h4>'
        )

    def test_hash_h5_closed_mismatch(self):
        self.assertMarkdownRenders(
            '##### This is an H5 #',
            
            '<h5>This is an H5</h5>'
        )
    
    def test_hash_h6_closed_mismatch(self):
        self.assertMarkdownRenders(
            '###### This is an H6 #',
            
            '<h6>This is an H6</h6>'
        )
    
    def test_hash_gt6_closed_mismatch(self):
        self.assertMarkdownRenders(
            '####### This is an H6 ##################',
            
            '<h6># This is an H6</h6>'
        )

    def test_hash_h1_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                # This is an H1
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h1>This is an H1</h1>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )
    
    def test_hash_h2_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ## This is an H2
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h2>This is an H2</h2>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )
    
    def test_hash_h3_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ### This is an H3
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h3>This is an H3</h3>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )
    
    def test_hash_h4_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                #### This is an H4
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h4>This is an H4</h4>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )
        
    def test_hash_h5_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ##### This is an H5
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h5>This is an H5</h5>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )
        
    def test_hash_h6_followed_by_p(self):
        self.assertMarkdownRenders(
            self.dedent(
                """
                ###### This is an H6
                Followed by a Paragraph with no blank line.
                """
            ),
            self.dedent(
                """
                <h6>This is an H6</h6>
                <p>Followed by a Paragraph with no blank line.</p>
                """
            )
        )
