#!/usr/bin/env python3
"""Black-box stdin fuzzer for warmup/target.py.

The target is treated as an opaque subprocess.  Inputs are generated as
bounded byte strings, with a small amount of structure mixed into the random
data so delimiter-related parser bugs are reached quickly.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import subprocess
import sys
from pathlib import Path


DEFAULT_MAX_INPUT = 32
DEFAULT_ITERATIONS = 10_000
DEFAULT_TIMEOUT = 1.0


def generate_input(rng: random.Random, max_input: int) -> bytes:
    """Return one bounded input without relying on target implementation."""
    length = rng.randrange(max_input + 1)
    data = bytearray(rng.randbytes(length))

    # Bias a subset of cases toward printable settings and common separators.
    # The rest remain unrestricted random bytes.
    if rng.random() < 0.65:
        alphabet = b"abcdefghijklmnopqrstuvwxyz0123456789_=-"
        data = bytearray(rng.choice(alphabet) for _ in range(length))

    if max_input and rng.random() < 0.75:
        insert_at = rng.randrange(len(data) + 1)
        data[insert_at:insert_at] = b"="
    if max_input and rng.random() < 0.30:
        insert_at = rng.randrange(len(data) + 1)
        data[insert_at:insert_at] = b"="

    return bytes(data[:max_input])


def run_target(target: Path, payload: bytes, timeout: float) -> tuple[int, bytes, bytes]:
    """Run the target with one input and return its process result."""
    try:
        result = subprocess.run(
            [sys.executable, str(target)],
            cwd=target.parent,
            input=payload,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        return -1, stdout, stderr
    return result.returncode, result.stdout, result.stderr


def is_value_error(returncode: int, stderr: bytes) -> bool:
    """Recognize the requested crash from observable process behavior."""
    return returncode != 0 and b"ValueError" in stderr


def save_crash(crashes: Path, payload: bytes) -> Path:
    crashes.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(payload).hexdigest()[:12]
    path = crashes / f"crash-{digest}.bin"
    path.write_bytes(payload)
    return path


def fuzz(iterations: int, max_input: int, timeout: float, seed: int | None) -> int:
    target = Path(__file__).with_name("target.py")
    rng = random.Random(seed)

    for case in range(1, iterations + 1):
        payload = generate_input(rng, max_input)
        returncode, stdout, stderr = run_target(target, payload, timeout)
        if is_value_error(returncode, stderr):
            crash = save_crash(Path(__file__).with_name("crashes"), payload)
            print(f"ValueError found on case {case}")
            print(f"input: {payload!r}")
            print(f"saved: {crash}")
            return 0

    print(f"No ValueError found in {iterations} cases", file=sys.stderr)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", "--iterations", type=int, default=DEFAULT_ITERATIONS)
    parser.add_argument("--max-input", type=int, default=DEFAULT_MAX_INPUT)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.iterations < 1 or args.max_input < 0 or args.timeout <= 0:
        parser.error("iterations must be >= 1, max-input >= 0, and timeout > 0")
    return fuzz(args.iterations, args.max_input, args.timeout, args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
