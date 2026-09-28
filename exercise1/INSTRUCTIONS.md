# Exercise 1: Fuzzing jhead's EXIF parser

The target is [jhead](https://github.com/Matthias-Wandel/jhead) 3.00, a C tool
that reads EXIF metadata out of JPEG files. The build is pinned to the commit
just before the 2016 hardening changes, so the memory-safety bug is still
present. You will fuzz it with libFuzzer.

## Step 1: Build the target

`build.sh` clones jhead at the pinned commit and compiles it together with the
harness in `fuzz_exif.c`. From the `exercise1` directory:

```
./build.sh
```

This needs `clang`. If it is missing:

```
sudo apt-get install -y clang libclang-rt-18-dev
```

The script prints the path to the binary it produced, `./fuzz_exif`.

Note that only libFuzzer's coverage instrumentation is enabled, not
AddressSanitizer. The bug is reachable as a plain segmentation fault.

## Step 2: Run the fuzzer

```
./fuzz_exif corpus -artifact_prefix=crashes/
```

- `corpus` is the directory of starting inputs
- `-artifact_prefix=` is where crashing inputs are written; the trailing `/` is
  required, otherwise it is treated as a filename prefix rather than a
  directory

libFuzzer prints a line whenever it discovers new coverage. When it finds a
crash it prints the stack trace and saves the input to `crashes/`.

Useful flags while experimenting:

```
-runs=100000          stop after N executions
-max_total_time=60    stop after N seconds
-max_len=4096         cap the size of generated inputs
```

## Step 3: Reproduce a crash

Pass a saved crash file instead of the corpus directory. No other flags are
needed:

```
./fuzz_exif crashes/<crash-file>
```

The binary runs that one input and should fail the same way every time. A crash
you cannot reproduce on demand is not yet a finding.

