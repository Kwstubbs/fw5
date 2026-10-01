import random
import subprocess

chars = b"abc= \n"

for i in range(1000):
    data = bytes(random.choice(chars) for _ in range(random.randint(1, 16)))
    p = subprocess.run(["python3", "target.py"], input=data, capture_output=True)
    if b"ValueError" in p.stderr:
        name = f"crashes/crash-{i}.bin"
        with open(name, "wb") as f:
            f.write(data)
        print(f"crash on {data!r}, saved {name}")
        break
