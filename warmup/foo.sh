while true; do
  head -c 32 /dev/urandom | python3.11 target.py
done
