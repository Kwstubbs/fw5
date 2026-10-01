#!/usr/bin/env python3

import secrets
import string

CHARS = (
    string.ascii_letters
    + string.digits
    + string.punctuation
    + " \t"
    + "áéíóúñÑüÜàèìòùç"
    + "[]{}()<>|\\/`~^"
)

def random_string():
    length = secrets.randbelow(33) + 8  # 8–40 chars
    return "".join(secrets.choice(CHARS) for _ in range(length))

print(f"{random_string()}={random_string()}", flush=True)
