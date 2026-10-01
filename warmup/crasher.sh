random_value() {
    head -c 32 /dev/urandom | xxd -p -c 32
}

input="$(random_value)=$(random_value)"

while true; do
    output=$(printf '%s\n' "$input" | python3 2>&1)
    if [[ "$output" == *ValueError* ]]; then
        printf '%s\n' "$output"
        printf 'Input that caused ValueError: %s\n' "$input"
        break
    fi
    input="$(random_value)=$(random_value)"
done
