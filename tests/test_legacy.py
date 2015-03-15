from markdown.test_tools import LegacyTestCase, Kwargs
import os
import warnings

# Warnings should cause tests to fail...
warnings.simplefilter('error')
# Except for the warnings that shouldn't
warnings.filterwarnings('default', category=PendingDeprecationWarning)
warnings.filterwarnings('default', category=DeprecationWarning, module='markdown')

parent_test_dir = os.path.abspath(os.path.dirname(__file__))


class TestBasic(LegacyTestCase):
    location = os.path.join(parent_test_dir, 'basic')


class TestMisc(LegacyTestCase):
    location = os.path.join(parent_test_dir, 'misc')


class TestOptions(LegacyTestCase):
    location = os.path.join(parent_test_dir, 'options')

    lazy_ol_off = Kwargs(lazy_ol=False)

    html4 = Kwargs(output_format='html4')

    no_attributes = Kwargs(enable_attributes=False)

    no_smart_emphasis = Kwargs(smart_emphasis=False)


class TestPhp(LegacyTestCase):
    """
    Notes on "excluded" tests:

    Quotes in attributes: attributes get output in differant order

    Inline HTML (Span): Backtick in raw HTML attribute TODO: fixme

    Backslash escapes: Weird whitespace issue in output

    Ins & del: Our behavior follows markdown.pl I think PHP is wrong here

    Auto Links: TODO: fix raw HTML so is doesn't match <hr@example.com> as a <hr>.

    Empty List Item: We match markdown.pl here. Maybe someday we'll support this

    Headers: TODO: fix headers to not require blank line before

    Mixed OLs and ULs: We match markdown.pl here. I think PHP is wrong here

    Emphasis: We have various minor differances in combined & incorrect em markup.
    Maybe fix a few of them - but most aren't too important

    Code block in a list item: We match markdown.pl - not sure how php gets that output??

    PHP-Specific Bugs: Not sure what to make of the escaping stuff here.
    Why is PHP not removing a blackslash?
    """
    location = os.path.join(parent_test_dir, 'php')
    normalize = True
    input_ext = '.text'
    output_ext = '.xhtml'
    exclude = [
        'Quotes_in_attributes',
        'Inline_HTML_(Span)',
        'Backslash_escapes',
        'Ins_&_del',
        'Auto_Links',
        'Empty_List_Item',
        'Headers',
        'Mixed_OLs_and_ULs',
        'Emphasis',
        'Code_block_in_a_list_item',
        'PHP_Specific_Bugs'
    ]


# class TestPhpExtra(LegacyTestCase):
#     location = os.path.join(parent_test_dir, 'php/extra')
#     normalize = True
#     input_ext = '.text'
#     output_ext = '.xhtml'
#     default_kwargs = Kwargs(extensions=['extra'])


class TestPl2004(LegacyTestCase):
    location = os.path.join(parent_test_dir, 'pl/Tests_2004')
    normalize = True
    input_ext = '.text'
    exclude = ['Yuri_Footnotes']


class TestPl2007(LegacyTestCase):
    """
    Notes on "excluded" tests:

    Images: the attributes don't get ordered the same so we skip this

    Code Blocks: some weird whitespace issue

    Links, reference style: weird issue with nested brackets TODO: fixme

    Backslash escapes: backticks in raw html attributes TODO: fixme

    Code Spans: more backticks in raw html attributes TODO: fixme
    """
    location = os.path.join(parent_test_dir, 'pl/Tests_2007')
    normalize = True
    input_ext = '.text'
    exclude = [
        'Images',
        'Code_Blocks',
        'Links,_reference_style',
        'Backslash_escapes',
        'Code_Spans'
    ]


class TestExtensions(LegacyTestCase):
    location = os.path.join(parent_test_dir, 'extensions')
    exclude = ['codehilite']

    attr_list = Kwargs(
        extensions=[
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.smarty'
        ]
    )

    codehilite = Kwargs(extensions=['markdown.extensions.codehilite'])

    toc = Kwargs(extensions=['markdown.extensions.toc'])

    toc_invalid = Kwargs(extensions=['markdown.extensions.toc'])

    toc_out_of_order = Kwargs(extensions=['markdown.extensions.toc'])

    toc_nested = Kwargs(
        extensions=['markdown.extensions.toc'],
        extension_configs={'markdown.extensions.toc': {'permalink': True}}
    )

    toc_nested2 = Kwargs(
        extensions=['markdown.extensions.toc'],
        extension_configs={'markdown.extensions.toc': {'permalink': "[link]"}}
    )

    toc_nested_list = Kwargs(extensions=['markdown.extensions.toc'])

    wikilinks = Kwargs(extensions=['markdown.extensions.wikilinks'])

    fenced_code = Kwargs(extensions=['markdown.extensions.fenced_code'])

    github_flavored = Kwargs(extensions=['markdown.extensions.fenced_code'])

    sane_lists = Kwargs(extensions=['markdown.extensions.sane_lists'])

    nl2br_w_attr_list = Kwargs(
        extensions=[
            'markdown.extensions.nl2br',
            'markdown.extensions.attr_list'
        ]
    )

    admonition = Kwargs(extensions=['markdown.extensions.admonition'])

    smarty = Kwargs(
        extensions=['markdown.extensions.smarty'],
        extension_configs={'markdown.extensions.smarty': {'smart_angled_quotes': True}}
    )


class TestExtensionsExtra(LegacyTestCase):
    location = os.path.join(parent_test_dir, 'extensions/extra')
    default_kwargs = Kwargs(extensions=['markdown.extensions.extra'])

    loose_def_list = Kwargs(extensions=['markdown.extensions.def_list'])

    simple_def_lists = Kwargs(extensions=['markdown.extensions.def_list'])

    abbr = Kwargs(extensions=['markdown.extensions.abbr'])

    footnotes = Kwargs(extensions=['markdown.extensions.footnotes'])

    tables = Kwargs(extensions=['markdown.extensions.tables'])

    tables_and_attr_list = Kwargs(
        extensions=['markdown.extensions.tables', 'markdown.extensions.attr_list']
    )

    extra_config = Kwargs(
        extensions=['markdown.extensions.extra'],
        extension_configs={
            'markdown.extensions.extra': {
                'markdown.extensions.footnotes': {
                    'PLACE_MARKER': '~~~placemarker~~~'
                }
            }
        }
    )
