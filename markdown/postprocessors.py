"""
POST-PROCESSORS
=============================================================================

Markdown also allows post-processors, which are similar to preprocessors in
that they need to implement a "run" method. However, they are run after core
processing.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import util
from . import odict
import re


def build_postprocessors(md, **kwargs):
    """ Build the default postprocessors for Markdown. """
    postprocessors = odict.OrderedDict()
    postprocessors["raw_html"] = RawHtmlPostprocessor(md)
    postprocessors["amp_substitute"] = AndSubstitutePostprocessor()
    postprocessors["unescape"] = UnescapePostprocessor()
    return postprocessors


class Postprocessor(util.Processor):
    """
    Postprocessors are run after the ElementTree it converted back into text.

    Each Postprocessor implements a "run" method that takes a pointer to a
    text string, modifies it as necessary and returns a text string.

    Postprocessors must extend markdown.Postprocessor.

    """

    def run(self, text):
        """
        Subclasses of Postprocessor should implement a `run` method, which
        takes the html document as a single text string and returns a
        (possibly modified) string.

        """
        pass  # pragma: no cover


class RawHtmlPostprocessor(Postprocessor):
    """ Restore raw html to the document. """

    def run(self, text):
        """ Iterate over html stash and restore html. """
        for i in range(self.md.htmlStash.html_counter):
            html = self.md.htmlStash.rawHtmlBlocks[i]
            if self.isblocklevel(html):
                text = text.replace(
                    "<p>%s</p>" % (self.md.htmlStash.get_placeholder(i)),
                    html + "\n"
                )
            text = text.replace(
                self.md.htmlStash.get_placeholder(i), html
            )
        return text

    def isblocklevel(self, html):
        m = re.match(r'^\<\/?([^ >]+)', html)
        if m:
            if m.group(1)[0] in ('!', '?', '@', '%'):
                # Comment, php etc...
                return True
            return util.isBlockLevel(m.group(1))
        return False


class AndSubstitutePostprocessor(Postprocessor):
    """ Restore valid entities """

    def run(self, text):
        text = text.replace(util.AMP_SUBSTITUTE, "&")
        return text


class UnescapePostprocessor(Postprocessor):
    """ Restore escaped chars """

    RE = re.compile('%s(\d+)%s' % (util.STX, util.ETX))

    def unescape(self, m):
        return util.int2str(int(m.group(1)))

    def run(self, text):
        return self.RE.sub(self.unescape, text)
