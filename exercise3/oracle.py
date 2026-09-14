#!/usr/bin/env python3
"""Attribute-injection oracle: targets bypass 2 only.

Bypass 2 is an escaping failure. An unescaped " in an interpolated value ends
the attribute early, so the rest of the payload is parsed as *new markup*. The
signature is therefore structural: a tag or attribute appears that mistune's
renderers cannot produce.

Do not look for the " itself. A successful breakout consumes the quote as a
delimiter, so it never reaches the parsed value, while a correctly escaped
&quot; decodes back into one -- the character is present exactly when the bug
is absent.
"""

from bs4 import BeautifulSoup

# Every attribute mistune 0.7.4 can emit, per tag. Taken from the renderer
# format strings and confirmed by rendering the seed corpus.
# Names only: an injected attribute whose name is already listed for that tag
# (e.g. title on <a>) is a breakout this oracle will not report.
ALLOWED_ATTRS = {
    "a": {"href", "title", "rel", "rev"},
    "img": {"src", "alt", "title"},
    "code": {"class"},
    "div": {"class"},
    "sup": {"class", "id"},
    "li": {"id"},
    "th": {"style"},
    "td": {"style"},
}

ALLOWED_TAGS = frozenset({
    "html", "head", "body",  # html5lib wraps every fragment in these
    "p", "a", "img", "pre", "code", "blockquote", "ul", "ol", "li", "hr", "br",
    "em", "strong", "del", "table", "thead", "tbody", "tr", "th", "td", "div",
    "sup", "h1", "h2", "h3", "h4", "h5", "h6",
})


def find_injection(html):
    """Return a description of the first injected construct, else None."""
    soup = BeautifulSoup(html, "html5lib")

    for tag in soup.find_all(True):
        if tag.name not in ALLOWED_TAGS:

        allowed = ALLOWED_ATTRS.get(tag.name, frozenset())
        for attr in tag.attrs:

    return None
