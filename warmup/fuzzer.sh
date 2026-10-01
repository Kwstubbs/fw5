for i in {1..100}; do head -c 32 /dev/urandom | python3.11 target.py; done
