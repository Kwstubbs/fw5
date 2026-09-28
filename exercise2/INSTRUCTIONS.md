# Exercise 2: Fuzzing a Java booking parser

The target is `BookingForm.parseBooking`, which turns a block of text into a
`Booking` object. You will fuzz it with
[Jazzer](https://github.com/CodeIntelligenceTesting/jazzer), the JVM equivalent
of libFuzzer. Jazzer is already included in the `jazzer/` directory.

## Step 1: Finish the harness

Open `fuzzer.java`. Jazzer calls `fuzzerTestOneInput(byte[] data)` once per
input, and the harness has a gap in it:

```java
// Convert the input byte array into the appropriate format for parsing
BookingForm.parseBooking();
```

`parseBooking` takes a `String`, so you need to turn the `byte[]` Jazzer hands
you into one and pass it in. The file will not compile until you do.

The `try`/`catch` around the call ignores `IllegalArgumentException`, because
rejecting malformed input is what the parser is *supposed* to do. Any other
exception escaping the call is what Jazzer reports as a finding.

## Step 2: Compile

From the `exercise2` directory:

```
javac -d out BookingForm.java fuzzer.java
```

This needs a JDK. Check you have one:

```
javac -version
```

The compiled classes land in `out/`.

## Step 3: Run the fuzzer

```
./jazzer/jazzer --cp=out --target_class=fuzzer -artifact_prefix=crashes/ corpus
```

- `--cp=out` is the classpath holding your compiled classes
- `--target_class=fuzzer` is the class containing `fuzzerTestOneInput`
- `-artifact_prefix=` is where crashing inputs are written; the trailing `/` is
  required, otherwise it is treated as a filename prefix
- `corpus` is the directory of starting inputs

Jazzer flags use `--`, while the libFuzzer flags underneath it use a single
`-`. Mixing the two up is the most common reason a flag appears to be ignored.

Useful libFuzzer flags while experimenting:

```
-runs=100000          stop after N executions
-max_total_time=60    stop after N seconds
```

## Step 4: Reproduce a crash

When Jazzer finds a crash it prints the stack trace, writes the input to
`crashes/`, and also writes a `Crash_<hash>.java` reproducer in the current
directory. Replay a saved input with:

```
./jazzer/jazzer --cp=out --target_class=fuzzer crashes/<crash-file>
```

