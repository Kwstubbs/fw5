#!/usr/bin/env bash

while true; do
  head -c 1232 /dev/urandom | tee input | python3.11 target.py
  status=$?
  if [[ $status -eq 1 ]]; then
    break
  fi
done
