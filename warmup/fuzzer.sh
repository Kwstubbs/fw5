#!/bin/bash

for i in {1..1000}; do
    input=$(head -c 32 /dev/urandom | tr -d '\0')
    out=$(echo "$input" | python3.11 target.py)
    if [[ $? -gt 0 ]]; then
        echo "Input: $input"
        echo "$out"
    fi
done
