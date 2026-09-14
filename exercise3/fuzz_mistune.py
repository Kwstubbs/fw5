#!/usr/bin/env python3

import sys

from oracle import find_injection

import atheris

with atheris.instrument_imports():
    import mistune

# escape=True is what makes the allowlist sound: with raw HTML escaped, every
# tag and attribute left in the output was emitted by mistune's own renderers,
# so anything outside the vocabulary got there through an attribute breakout.
_markdown = mistune.Markdown(escape=True)


def TestOneInput(data):
    s = atheris.FuzzedDataProvider(data).ConsumeUnicode(len(data))
    html = _markdown(s)

    reason = find_injection(html)
    if reason:
        raise AssertionError(f"{reason}\n  payload: {s!r}\n  html:    {html!r}")


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
