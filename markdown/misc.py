# -*- coding: utf-8 -*-
import re
from misc_logging import CRITICAL

import etree_loader


"""
CONSTANTS
=============================================================================
"""

"""
Constants you might want to modify
-----------------------------------------------------------------------------
"""

# default logging level for command-line use
COMMAND_LINE_LOGGING_LEVEL = CRITICAL
TAB_LENGTH = 4               # expand tabs to this many spaces
ENABLE_ATTRIBUTES = True     # @id = xyz -> <... id="xyz">
SMART_EMPHASIS = True        # this_or_that does not become this<i>or</i>that
DEFAULT_OUTPUT_FORMAT = 'xhtml1'     # xhtml or html4 output
HTML_REMOVED_TEXT = "[HTML_REMOVED]" # text used instead of HTML in safe mode
BLOCK_LEVEL_ELEMENTS = re.compile("p|div|h[1-6]|blockquote|pre|table|dl|ol|ul"
                                  "|script|noscript|form|fieldset|iframe|math"
                                  "|ins|del|hr|hr/|style|li|dt|dd|thead|tbody"
                                  "|tr|th|td")
DOC_TAG = "div"     # Element used to wrap document - later removed

# Placeholders
STX = u'\u0002'  # Use STX ("Start of text") for start-of-placeholder
ETX = u'\u0003'  # Use ETX ("End of text") for end-of-placeholder
INLINE_PLACEHOLDER_PREFIX = STX+"klzzwxh:"
INLINE_PLACEHOLDER = INLINE_PLACEHOLDER_PREFIX + "%s" + ETX
AMP_SUBSTITUTE = STX+"amp"+ETX


"""
Constants you probably do not need to change
-----------------------------------------------------------------------------
"""

RTL_BIDI_RANGES = ( (u'\u0590', u'\u07FF'),
                     # Hebrew (0590-05FF), Arabic (0600-06FF),
                     # Syriac (0700-074F), Arabic supplement (0750-077F),
                     # Thaana (0780-07BF), Nko (07C0-07FF).
                    (u'\u2D30', u'\u2D7F'), # Tifinagh
                    )

# Extensions should use "markdown.misc.etree" instead of "etree" (or do `from
# markdown.misc import etree`).  Do not import it by yourself.

etree = etree_loader.importETree()

"""
AUXILIARY GLOBAL FUNCTIONS
=============================================================================
"""


def isBlockLevel(tag):
    """Check if the tag is a block level HTML tag."""
    return BLOCK_LEVEL_ELEMENTS.match(tag)

"""
MISC AUXILIARY CLASSES
=============================================================================
"""

class AtomicString(unicode):
    """A string which should not be further processed."""
    pass
