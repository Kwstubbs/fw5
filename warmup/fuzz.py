import os
import random
import subprocess

random.seed(0)
os.makedirs("crashes", exist_ok=True)

for i in range(2000):
    n = random.randint(0, 64)
    data = bytes(0x3D if random.random() < 0.25 else random.randrange(256) for _ in range(n))
    r = subprocess.run(["python3.11", "target.py"], input=data, capture_output=True)
    if r.returncode != 0 and b"Traceback" in r.stderr:
        with open(f"crashes/fuzz-crash-{i}.bin", "wb") as f:
            f.write(data)
        print(f"CRASH iter={i} input={data!r}")
        print(r.stderr.decode(errors="replace").strip().splitlines()[-1])
        break
