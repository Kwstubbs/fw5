import os
from pathlib import Path
import subprocess
import sys


target = Path(__file__).with_name("target.py")

for iteration in range(2_000):
    candidate = os.urandom(32)
    result = subprocess.run(
        [sys.executable, str(target)],
        input=candidate,
        capture_output=True,
    )

    if result.returncode != 0:
        crash_file = Path(__file__).with_name(f"crash-{iteration}.bin")
        crash_file.write_bytes(candidate)
        print(f"Crash found: {crash_file.name}")
        print(result.stderr.decode(errors="replace"))
        break
else:
    print("No crash found after 2,000 attempts")