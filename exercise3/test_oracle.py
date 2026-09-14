#!/usr/bin/env python3
"""Check the oracle before fuzzing.

MUST_PASS carries the legitimate constructs that define mistune's tag and
attribute vocabulary; if the allowlist drifts, these fail first.
"""

import sys

import mistune

from oracle import find_injection

MUST_FLAG = [
    ('<junorouse@gmail.com"\nonclick="alert(1);>', "mailto autolink injects onclick"),
    ('```"><script>alert(1)</script>\ncode\n```',
     "code lang: quote closes class, > closes the tag, script becomes a real element"),
    ('```py"onx="1\ncode\n```', "code lang: quote alone only reaches a new attribute"),
    ('text[^a"onx="1]\n\n[^a"onx="1]: note', "footnote id injects onx"),
]

MUST_PASS = [
    ('[x](EE"Z)', "quote escaped to &quot;, stays inside the attribute"),
    ('[a](u "t")', "href + title"),
    ('![a](u "t")', "src + alt + title"),
    ('```py\ncode\n```', "code class"),
    ('| a | b |\n|:--|--:|\n| 1 | 2 |', "table cell style"),
    ('text[^1]\n\n[^1]: note', "footnote sup/li ids and rel/rev"),
    ('<script>alert(1)</script>', "raw HTML escaped when escape=True"),
    # Out of scope on purpose: a real bug, but scheme filtering, not escaping.
    ('[aa](java\nscript:alert`1`;)', "bypass 1 is not this exercise's target"),
]


def main():
    md = mistune.Markdown(escape=True)
    failures = 0

    for src, why in MUST_FLAG:
        reason = find_injection(md(src))
        if reason is None:
            failures += 1
        print(f"[{'PASS' if reason else 'FAIL'}] expect finding ({why}): {reason}")

    for src, why in MUST_PASS:
        reason = find_injection(md(src))
        if reason is not None:
            failures += 1
        print(f"[{'FAIL' if reason else 'PASS'}] expect clean   ({why}): {reason}")

    print(f"\n{failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
