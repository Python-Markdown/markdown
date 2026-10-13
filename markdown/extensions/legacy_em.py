# Legacy Em Extension for Python-Markdown
# =======================================

# This extension provides legacy behavior for _connected_words_.

# Copyright 2015-2018 The Python Markdown Project

# License: [BSD](https://opensource.org/licenses/bsd-license.php)

"""
This extension provides legacy behavior for _connected_words_.
"""

from __future__ import annotations

from . import Extension
from ..inlinepatterns import DelimiterProcessor


class LegacyEmExtension(Extension):
    """ Add legacy_em extension to Markdown class."""

    def extendMarkdown(self, md):
        """ Register the processor.

        | Class Instance                                                     | Registry                                                         | Name         | Priority |
        | ------------------------------------------------------------------ | ---------------------------------------------------------------- | ------------ | :------: |
        | [`DelimiterProcessor`][markdown.inlinepatterns.DelimiterProcessor] | [`inlinepatterns`][markdown.inlinepatterns.build_inlinepatterns] | `em_strong`  | `60`     |

        """
        # flake8: noqa: E501 27-29

        if md.delimiters is not None:
            md.delimiters.add('_', 'strong,em')
        else:
            md.inlinePatterns.register(DelimiterProcessor('_', 'strong,em', md), 'em_strong', 60)

def makeExtension(**kwargs):  # pragma: no cover
    """ Return an instance of the `LegacyEmExtension` """
    return LegacyEmExtension(**kwargs)
