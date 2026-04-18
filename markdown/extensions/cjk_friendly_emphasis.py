# CJK-Friendly Emphasis Extension for Python-Markdown
# ===================================================

# This extension enables underscore emphasis (`_em_`, `__strong__`) to work
# correctly adjacent to CJK (Chinese, Japanese, Korean) characters.
#
# By default, Python-Markdown's underscore emphasis uses `\w` word boundaries
# to prevent intraword emphasis (e.g., `foo_bar_baz`). However, CJK characters
# are classified as `\w` in Python's regex engine, which means `_`/`__` fails
# when directly adjacent to CJK text (e.g., `これは__重要__です`).
#
# This extension modifies the underscore patterns to allow CJK characters as
# valid emphasis boundaries while preserving intraword protection for ASCII text.
#
# Note: Asterisk emphasis (`*`/`**`) already works with CJK text in
# Python-Markdown and is not affected by this extension.

# Copyright The Python Markdown Project

# License: [BSD](https://opensource.org/licenses/bsd-license.php)

"""
An extension to enable CJK-friendly underscore emphasis.

Underscore emphasis (`_em_`, `__strong__`) normally fails adjacent to CJK
characters because Python's `\\w` matches CJK, triggering intraword protection.
This extension relaxes the boundary check so CJK characters are treated as
valid emphasis delimiters.

Usage:

    >>> import markdown
    >>> md = markdown.Markdown(extensions=['cjk_friendly_emphasis'])
    >>> md.convert('これは__重要__です')
    '<p>これは<strong>重要</strong>です</p>'

"""

from __future__ import annotations

from . import Extension
from ..inlinepatterns import UnderscoreProcessor, EmStrongItem, EM_STRONG2_RE, STRONG_EM2_RE
import re

# CJK character class covering the major ranges:
# - CJK Radicals Supplement through CJK Symbols and Punctuation (U+2E80-U+303F)
# - Hiragana, Katakana (U+3040-U+30FF)
# - Bopomofo, Hangul Compatibility Jamo, Kanbun, etc. (U+3100-U+31FF)
# - Enclosed CJK, CJK Compatibility (U+3200-U+33FF)
# - CJK Unified Ideographs Extension A + main block (U+3400-U+9FFF)
# - Hangul Syllables (U+AC00-U+D7A3)
# - CJK Compatibility Ideographs (U+F900-U+FAFF)
# - CJK Compatibility Forms (U+FE30-U+FE4F)
# - Fullwidth Forms (U+FF00-U+FFEF)
_CJK = (
    r'[\u2E80-\u303F\u3040-\u30FF\u3100-\u31FF\u3200-\u33FF'
    r'\u3400-\u9FFF\uAC00-\uD7A3\uF900-\uFAFF'
    r'\uFE30-\uFE4F\uFF00-\uFFEF]'
)

# CJK-friendly boundary: not preceded by ASCII word char, OR preceded by CJK
_NOT_WORD_OR_CJK_BEFORE = rf'(?:(?<!\w)|(?<={_CJK}))'

# CJK-friendly boundary: not followed by ASCII word char, OR followed by CJK
_NOT_WORD_OR_CJK_AFTER = rf'(?:(?!\w)|(?={_CJK}))'

# _emphasis_  (CJK-friendly)
CJK_SMART_EMPHASIS_RE = (
    _NOT_WORD_OR_CJK_BEFORE + r'(_)(?!_)(.+?)(?<!_)\1' + _NOT_WORD_OR_CJK_AFTER
)

# __strong__  (CJK-friendly)
CJK_SMART_STRONG_RE = (
    _NOT_WORD_OR_CJK_BEFORE + r'(_{2})(?!_)(.+?)(?<!_)\1' + _NOT_WORD_OR_CJK_AFTER
)

# __strong _em___  (CJK-friendly)
CJK_SMART_STRONG_EM_RE = (
    _NOT_WORD_OR_CJK_BEFORE
    + r'(\_)\1(?!\1)(.+?)(?<!\w)\1(?!\1)(.+?)\1{3}'
    + _NOT_WORD_OR_CJK_AFTER
)


class CJKUnderscoreProcessor(UnderscoreProcessor):
    """Emphasis processor with CJK-friendly underscore boundary handling."""

    PATTERNS = [
        EmStrongItem(re.compile(EM_STRONG2_RE, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(STRONG_EM2_RE, re.DOTALL | re.UNICODE), 'double', 'em,strong'),
        EmStrongItem(re.compile(CJK_SMART_STRONG_EM_RE, re.DOTALL | re.UNICODE), 'double2', 'strong,em'),
        EmStrongItem(re.compile(CJK_SMART_STRONG_RE, re.DOTALL | re.UNICODE), 'single', 'strong'),
        EmStrongItem(re.compile(CJK_SMART_EMPHASIS_RE, re.DOTALL | re.UNICODE), 'single', 'em'),
    ]


class CJKFriendlyEmphasisExtension(Extension):
    """Add CJK-friendly emphasis extension to Markdown class."""

    def extendMarkdown(self, md):
        """Modify inline patterns."""
        md.inlinePatterns.register(
            CJKUnderscoreProcessor(r'_'), 'em_strong2', 50
        )


def makeExtension(**kwargs):  # pragma: no cover
    """Return an instance of the [`CJKFriendlyEmphasisExtension`][]."""
    return CJKFriendlyEmphasisExtension(**kwargs)
