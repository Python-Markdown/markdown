# Add x/html serialization to `Elementree`
# Taken from ElementTree 1.3 preview with slight modifications
#
# Copyright (c) 1999-2007 by Fredrik Lundh.  All rights reserved.
#
# fredrik@pythonware.com
# https://www.pythonware.com/
#
# --------------------------------------------------------------------
# The ElementTree toolkit is
#
# Copyright (c) 1999-2007 by Fredrik Lundh
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Secret Labs AB or the author not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD
# TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANT-
# ABILITY AND FITNESS.  IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR
# BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY
# DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
# OF THIS SOFTWARE.
# --------------------------------------------------------------------

"""
Python-Markdown provides two serializers which render [`ElementTree.Element`][xml.etree.ElementTree.Element]
objects to a string of HTML. Both functions wrap the same underlying code with only a few minor
differences as outlined below:

1. Empty (self-closing) tags are rendered as `<tag>` for HTML and as `<tag />` for XHTML.
2. Boolean attributes are rendered as `attrname` for HTML and as `attrname="attrname"` for XHTML.
"""

from __future__ import annotations

from xml.etree.ElementTree import ProcessingInstruction
from xml.etree.ElementTree import Comment, ElementTree, Element, QName, HTML_EMPTY
import re
from typing import Callable, Literal, NoReturn

__all__ = ['to_html_string', 'to_xhtml_string']

RE_AMP = re.compile(r'&(?!(?:\#[0-9]+|\#x[0-9a-f]+|[0-9a-z]+);)', re.I)
_RAW_TEXT_TAGS = frozenset(('script', 'style'))

# Known boolean attributes, whose presence alone carries the meaning and
# which may therefore be rendered in the minimized (valueless) form. The
# list of recognized attributes differs per output format: `xhtml` only
# recognizes the attributes declared boolean by the XHTML 1.0 spec, while
# `html` recognizes the boolean attributes of the HTML spec. Note that
# `download` is deliberately absent from both lists: it is only boolean
# when no value is assigned and a value changes its meaning.
BOOLEAN_ATTRIBUTES: dict[str, frozenset[str]] = {
    'html': frozenset([
        'allowfullscreen', 'async', 'autofocus', 'autoplay', 'checked',
        'controls', 'default', 'defer', 'disabled', 'formnovalidate',
        'hidden', 'inert', 'ismap', 'itemscope', 'loop', 'multiple', 'muted',
        'nomodule', 'novalidate', 'open', 'playsinline', 'readonly',
        'required', 'reversed', 'selected',
    ]),
    'xhtml': frozenset([
        'checked', 'compact', 'declare', 'defer', 'disabled', 'ismap',
        'multiple', 'noresize', 'noshade', 'nowrap', 'readonly', 'selected',
    ]),
}


def _raise_serialization_error(text: str) -> NoReturn:  # pragma: no cover
    raise TypeError(
        "cannot serialize {!r} (type {})".format(text, type(text).__name__)
        )


def _escape_cdata(text) -> str:
    # escape character data
    try:
        # it's worth avoiding do-nothing calls for strings that are
        # shorter than 500 character, or so.  assume that's, by far,
        # the most common case in most applications.
        if "&" in text:
            # Only replace & when not part of an entity
            text = RE_AMP.sub('&amp;', text)
        if "<" in text:
            text = text.replace("<", "&lt;")
        if ">" in text:
            text = text.replace(">", "&gt;")
        return text
    except (TypeError, AttributeError):  # pragma: no cover
        _raise_serialization_error(text)


def _escape_attrib(text: str) -> str:
    # escape attribute value
    try:
        if "&" in text:
            # Only replace & when not part of an entity
            text = RE_AMP.sub('&amp;', text)
        if "<" in text:
            text = text.replace("<", "&lt;")
        if ">" in text:
            text = text.replace(">", "&gt;")
        if "\"" in text:
            text = text.replace("\"", "&quot;")
        if "\n" in text:
            text = text.replace("\n", "&#10;")
        return text
    except (TypeError, AttributeError):  # pragma: no cover
        _raise_serialization_error(text)


def _escape_attrib_html(text: str) -> str:
    # escape attribute value
    try:
        if "&" in text:
            # Only replace & when not part of an entity
            text = RE_AMP.sub('&amp;', text)
        if "<" in text:
            text = text.replace("<", "&lt;")
        if ">" in text:
            text = text.replace(">", "&gt;")
        if "\"" in text:
            text = text.replace("\"", "&quot;")
        return text
    except (TypeError, AttributeError):  # pragma: no cover
        _raise_serialization_error(text)


def _serialize_html(write: Callable[[str], None], elem: Element, format: Literal["html", "xhtml"]) -> None:
    stack: list[Element | str] = [elem]
    is_html = format == "html"
    is_xhtml = format == "xhtml"
    html_bool_attrs = BOOLEAN_ATTRIBUTES['html']
    append = stack.append
    extend = stack.extend
    pop = stack.pop

    while stack:
        el = pop()

        if isinstance(el, str):
            write(el)
            continue

        tag = el.tag
        text = el.text

        if tag is Comment:
            write(f"<!--{_escape_cdata(text)}-->")
        elif tag is ProcessingInstruction:
            write(f"<?{_escape_cdata(text)}?>")
        elif tag is None:
            if text:
                write(_escape_cdata(text))
            # Add the children in reverse order so we process them in the right order.
            if el.tail:
                append(_escape_cdata(el.tail))
            if len(el):
                extend(reversed(el))
            continue
        else:
            namespace_uri = None
            if isinstance(tag, QName):
                # `QNAME` objects store their data as a string: `{uri}tag`
                if tag.text[:1] == "{":
                    namespace_uri, tag = tag.text[1:].split("}", 1)
                else:
                    raise ValueError('QName objects must define a tag.')
            tag_lower = tag.lower()
            is_empty = tag_lower in HTML_EMPTY
            attrib = el.attrib
            if attrib or namespace_uri:
                write(f"<{tag}")
                if attrib:
                    items = list(attrib.items())
                    if len(items) > 1:
                        items.sort()  # lexical order
                    for k, v in items:
                        if isinstance(k, QName):
                            # Assume a text only `QName`
                            k = k.text
                        if isinstance(v, QName):
                            # Assume a text only `QName`
                            v = v.text
                        if v is None:
                            # A valueless attribute is preserved exactly as it
                            # was provided: render the bare attribute name.
                            write(f" {k}")
                        else:
                            v = _escape_attrib_html(v)
                            if k == v and is_html and k in html_bool_attrs:
                                # handle boolean attributes
                                write(f" {v}")
                            else:
                                write(f' {k}="{v}"')
                if namespace_uri:
                    write(f' xmlns="{_escape_attrib(namespace_uri)}"')
                if is_xhtml and is_empty:
                    write(" />")
                    if el.tail:
                        write(_escape_cdata(el.tail))
                    continue
                write(">")
            elif is_xhtml and is_empty:
                write(f"<{tag} />")
                if el.tail:
                    write(_escape_cdata(el.tail))
                continue
            else:
                write(f"<{tag}>")

            if not len(el):
                if text:
                    escaped = text if tag_lower in _RAW_TEXT_TAGS else _escape_cdata(text)
                    write(escaped if is_empty else f"{escaped}</{tag}>")
                elif not is_empty:
                    write(f"</{tag}>")
                if el.tail:
                    write(_escape_cdata(el.tail))
                continue

            if text:
                if tag_lower in _RAW_TEXT_TAGS:
                    write(text)
                else:
                    write(_escape_cdata(text))
            # Push tail, end tag, and children in reverse order for LIFO traversal.
            if el.tail:
                append(_escape_cdata(el.tail))
            if not is_empty:
                append(f"</{tag}>")
            extend(reversed(el))
            continue
        if el.tail:
            write(_escape_cdata(el.tail))


def _write_html(root: Element, format: Literal["html", "xhtml"] = "html") -> str:
    assert root is not None
    data: list[str] = []
    write = data.append
    _serialize_html(write, root, format)
    return "".join(data)


# --------------------------------------------------------------------
# public functions


def to_html_string(element: Element) -> str:
    """ Serialize element and its children to a string of HTML5. """
    return _write_html(ElementTree(element).getroot(), format="html")


def to_xhtml_string(element: Element) -> str:
    """ Serialize element and its children to a string of XHTML. """
    return _write_html(ElementTree(element).getroot(), format="xhtml")
