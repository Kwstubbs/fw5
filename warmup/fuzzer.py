#!/usr/bin/env python3
"""Fuzzer for parse() in parser.py.

Usage:
    python fuzz_parse.py                  # built-in mutation fuzzer (no deps)
    python fuzz_parse.py -n 50000 -s 1    # 50k iterations, fixed seed
    python fuzz_parse.py --atheris        # coverage-guided, needs `pip install atheris`
    python fuzz_parse.py --repro crashes/crash-ValueError-9.bin

The target runs code at import time (it reads stdin), so instead of importing
it we pull just the function definitions out with `ast` and exec those.
"""
import argparse
import ast
import contextlib
import hashlib
import io
import os
import random
import sys
import traceback

MAX_LEN = 64  # the real program only reads 64 bytes from stdin

SEEDS = [b"key=value", b"a=b\n", b"no setting here", b"=", b"  k = v  ", b""]
TOKENS = [b"=", b"==", b"\n", b"\r\n", b" ", b"\t", b"\x00", b"\xff", b"key", b"value"]


def load_parse(path):
    with open(path, "rb") as f:
        tree = ast.parse(f.read(), path)
    keep = (ast.Import, ast.ImportFrom, ast.FunctionDef)
    tree.body = [node for node in tree.body if isinstance(node, keep)]
    namespace = {"__name__": "fuzz_target"}
    exec(compile(tree, path, "exec"), namespace)
    return namespace["parse"]


def run_one(parse, data):
    with contextlib.redirect_stdout(io.StringIO()):
        parse(data[:MAX_LEN])


def mutate(data, rng):
    buf = bytearray(data)
    for _ in range(rng.randint(1, 4)):
        op = rng.randrange(5)
        if op == 0 and buf:  # flip a bit
            i = rng.randrange(len(buf))
            buf[i] ^= 1 << rng.randrange(8)
        elif op == 1:  # insert a random byte
            buf.insert(rng.randint(0, len(buf)), rng.randrange(256))
        elif op == 2 and buf:  # delete a slice
            i = rng.randrange(len(buf))
            del buf[i:i + rng.randint(1, 4)]
        elif op == 3:  # insert an interesting token
            i = rng.randint(0, len(buf))
            buf[i:i] = rng.choice(TOKENS)
        elif buf:  # duplicate a chunk
            i = rng.randrange(len(buf))
            j = rng.randint(i, len(buf))
            buf[rng.randint(0, len(buf)):0] = buf[i:j]
    return bytes(buf[:MAX_LEN])


def crash_signature(exc):
    frame = traceback.extract_tb(exc.__traceback__)[-1]
    return f"{type(exc).__name__}-{frame.lineno}"


def builtin_fuzz(parse, iterations, seed, out_dir):
    rng = random.Random(seed)
    corpus = list(SEEDS)
    seen = {}
    os.makedirs(out_dir, exist_ok=True)

    for n in range(iterations):
        data = mutate(rng.choice(corpus), rng)
        try:
            run_one(parse, data)
        except Exception as exc:
            sig = crash_signature(exc)
            if sig not in seen:
                seen[sig] = data
                path = os.path.join(out_dir, f"crash-{sig}.bin")
                with open(path, "wb") as f:
                    f.write(data)
                print(f"[{n}] NEW CRASH {sig}: {exc!r}")
                print(f"      input={data!r}  saved to {path}")
            continue
        # keep a bounded, varied corpus of non-crashing inputs
        if len(corpus) < 500 and hashlib.sha1(data).digest()[0] < 16:
            corpus.append(data)

    print(f"\nDone: {iterations} runs, {len(seen)} unique crash(es).")
    return 1 if seen else 0


def atheris_fuzz(parse, extra_argv):
    import atheris

    parse = atheris.instrument_func(parse)

    def test_one_input(data):
        run_one(parse, data)

    atheris.Setup([sys.argv[0]] + extra_argv, test_one_input)
    atheris.Fuzz()


def repro(parse, path):
    with open(path, "rb") as f:
        data = f.read()
    print(f"input={data!r}")
    parse(data[:MAX_LEN])  # let the traceback surface
    print("No crash.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--target", default="parser.py", help="file defining parse()")
    ap.add_argument("-n", "--iterations", type=int, default=100_000)
    ap.add_argument("-s", "--seed", type=int, default=None)
    ap.add_argument("-o", "--out", default="crashes", help="crash output dir")
    ap.add_argument("--atheris", action="store_true", help="use atheris/libFuzzer")
    ap.add_argument("--repro", metavar="FILE", help="re-run one saved input")
    args, extra = ap.parse_known_args()

    parse = load_parse(args.target)
    if args.repro:
        repro(parse, args.repro)
    elif args.atheris:
        atheris_fuzz(parse, extra)
    else:
        sys.exit(builtin_fuzz(parse, args.iterations, args.seed, args.out))


if __name__ == "__main__":
    main()