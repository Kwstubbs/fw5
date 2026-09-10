# Simple stdin fuzzer warmup

## Step 1:

Open a codespace with at least 4 cores at https://github.com/Kwstubbs/fw5

## Step 2:

Run python3.11 target.py

The intentionally vulnerable target looks for a setting in the form key=value.
The target accepts input typed at a prompt or piped through standard input.

Try valid manual input:

	python3.11 target.py

Try piped input:

	printf 'color=blue' | python3.11 target.py
	printf 'color' | python3.11 target.py


## Step 3:

Try random bytes. The input must be bounded because /dev/urandom never ends:

	head -c 32 /dev/urandom | python3.11 target.py

## Step 4:

Try to trigger a ValueError within the python script, which will crash the program.
