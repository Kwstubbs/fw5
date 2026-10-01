#!/usr/bin/env python3

import argparse
import hashlib
import random
import string
import subprocess
import sys
from pathlib import Path
from typing import Final


def _main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Fuzz warmup target stdin"
    )
    parser.add_argument("--runs", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=0)
    arguments: argparse.Namespace = parser.parse_args()
    if arguments.runs < 1:
        parser.error("--runs must be at least 1")
    return _fuzz(arguments.runs, arguments.seed)


def _fuzz(runs: int, seed: int) -> int:
    seeds: Final[tuple[bytes, ...]] = (
        b"color",
        b"",
        b"=blue",
        b"color=",
        b"color=blue=green",
    )
    generator: random.Random = random.Random(seed)
    attempt: int
    for attempt in range(runs):
        data: bytes
        if attempt < len(seeds):
            data = seeds[attempt]
        else:
            data = bytes(
                generator.choices(
                    (string.ascii_letters + string.digits + " =-:").encode("ascii"),
                    k=generator.randint(1, 64),
                )
            )

        completed: subprocess.CompletedProcess[bytes] = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent / "target.py")],
            input=data,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
            timeout=2.0,
        )
        if completed.returncode == 0:
            continue

        if b"ValueError" in completed.stderr:
            print(
                f"ValueError after {attempt + 1} runs; "
                f"input saved to {_save_crash(data)}"
            )
            print(f"Input: {data!r}")
            return 0

        print(f"Target exited with status {completed.returncode} on input {data!r}")
        sys.stderr.write(completed.stderr.decode("utf-8", errors="replace"))
        return 1

    print(f"No ValueError found in {runs} runs (seed {seed})")
    return 1


def _save_crash(data: bytes) -> Path:
    crash_directory: Final[Path] = Path(__file__).resolve().parent / "crashes"
    crash_directory.mkdir(exist_ok=True)
    digest: str = hashlib.sha256(data).hexdigest()[:12]
    path: Path = crash_directory / f"crash-{digest}.bin"
    suffix: int = 1
    while path.exists():
        path = crash_directory / f"crash-{digest}-{suffix}.bin"
        suffix += 1
    path.write_bytes(data)
    return path


if __name__ == "__main__":
    raise SystemExit(_main())