#!/bin/bash
for i in {2..100}
do
    head -c 32 /dev/urandom | python3.11 target.py
done
