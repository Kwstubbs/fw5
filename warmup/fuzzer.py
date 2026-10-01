
import random

def fuzz_input():
    input_data = "=" * 100
    fuzzed_data = bytearray(input_data, 'utf-8')
    for i in range(len(fuzzed_data)):
        if random.random() < 0.1:  # 10% chance to mutate each byte
            fuzzed_data[i] = random.randint(0, 255)
    return fuzzed_data.decode('utf-8', errors='ignore')

if __name__ == "__main__":
    print(fuzz_input())


