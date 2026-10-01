import os, random, subprocess

TARGET = ["python3.11", "target.py"]
CHARSET = b"abcXYZ019 =-_.:;,\"'\\/\t\n\x00\xff"
SEEDS = [b"color=blue", b"color", b"=", b"a=b=c", b""]

def mutate(data):
    data = bytearray(data)
    for _ in range(random.randint(1, 5)):
        op = random.choice(["insert", "delete", "flip", "dup", "byte"])
        pos = random.randint(0, len(data))
        if op == "insert":
            data[pos:pos] = bytes([random.choice(CHARSET)])
        elif op == "delete" and data:
            del data[min(pos, len(data) - 1)]
        elif op == "flip" and data:
            i = min(pos, len(data) - 1)
            data[i] ^= 1 << random.randint(0, 7)
        elif op == "dup":
            data[pos:pos] = data[: random.randint(0, len(data))]
        elif op == "byte":
            data[pos:pos] = os.urandom(random.randint(1, 4))
    return bytes(data[:256])

def run(data):
    try:
        p = subprocess.run(TARGET, input=data, capture_output=True, timeout=2)
    except subprocess.TimeoutExpired:
        return ""
    return p.stderr.decode(errors="replace")

def main():
    os.makedirs("crashes", exist_ok=True)
    for i in range(1, 100000):
        data = mutate(random.choice(SEEDS))
        err = run(data)
        if "ValueError" in err:
            path = f"crashes/crash-{i}.bin"
            open(path, "wb").write(data)
            print("[!] ValueError found:", data, path)
            print(err)
            return
        if i % 200 == 0:
            print(i, "runs...")
    print("No crash found")

main()