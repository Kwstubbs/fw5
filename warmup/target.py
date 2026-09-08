import sys


def parse(data: bytes) -> None:
    if b"=" not in data:
        print("Ignored input without a setting")
        return

    key, value = data.strip().split(b"=")
    print(f"key={key!r}, value={value!r}")


if sys.stdin.isatty():
    input_data = input("Enter key=value: ").encode()
else:
    input_data = sys.stdin.buffer.read(64)

parse(input_data)