import os
from pathlib import Path
import subprocess


target = Path(__file__).with_name("target.py")

while True:
	data = os.urandom(32)
	result = subprocess.run(
		["python3.11", str(target)],
		input=data,
		capture_output=True,
		check=False,
	)
	if b"ValueError:" in result.stderr:
		print(f"ValueError input: {data!r}", flush=True)
		print(result.stderr.decode(errors="replace"), end="", flush=True)
		break