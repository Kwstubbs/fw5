#!/usr/bin/env python3
"""Generate a seed corpus for fuzz_mistune.py.

The harness feeds bytes through atheris.FuzzedDataProvider.ConsumeUnicode(),
which reads the first byte as an encoding selector: an odd value makes the
remaining bytes pass through as ASCII. Every seed is therefore prefixed with
\\x01 so the file contents are the markdown the parser actually sees.
"""

import os
import sys

# Constructs that make mistune emit tags carrying attributes (href/src/alt/
# title/class/style), plus the recursion-heavy block forms.
SEEDS = [
    '[a](http://x "t")',
    '![a](http://x "t")',
    '[a][r]\n\n[r]: http://x "t"',
    '![a][r]\n\n[r]: http://x "t"',
    '![]: x',
    '[![]: a\n[[]]("""]![]:',
    '[a](javascript:alert(x))',
    '<a href="x">y</a>',
    '<img src="x" alt="y">',
    '<http://autolink>',
    '```py\ncode\n```',
    '| a | b |\n|---|---|\n| 1 | 2 |',
    '>' * 200,
    '[' * 100,
    '![' * 100,
]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else 'corpus'
    os.makedirs(out, exist_ok=True)
    for i, seed in enumerate(SEEDS):
        path = os.path.join(out, f'seed{i:02d}')
        with open(path, 'wb') as fh:
            fh.write(b'\x01' + seed.encode())
    print(f'wrote {len(SEEDS)} seeds to {out}/')


if __name__ == '__main__':
    main()
