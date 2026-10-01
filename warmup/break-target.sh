#!/usr/bin/env bash

set -o pipefail

while true; do
    input=$(mktemp)
    output=$(mktemp)

    python3.11 ./fuzzer.py \
        | tee "$input" \
        | python3.11 target.py >"$output" 2>&1

    status=${PIPESTATUS[2]}

    if [ "$status" -ne 0 ]; then
        echo "=== CRASH INPUT ==="
        cat "$input"

        echo
        echo "=== ERROR ==="
        cat "$output"

        rm -f "$input" "$output"
        exit "$status"
    fi

    rm -f "$input" "$output"
done
