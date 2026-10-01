mkdir -p out
i=0
while true; do
  i=$((i+1))
  head -c 32 /dev/urandom > "out/input_$i.bin"
  python3.11 target.py < "out/input_$i.bin" > "out/run_$i.log" 2>&1
  if grep -q '^Traceback' "out/run_$i.log"; then
    echo "Run $i: Traceback. See out/run_$i.log and out/input_$i.bin"
    break
  fi
done
