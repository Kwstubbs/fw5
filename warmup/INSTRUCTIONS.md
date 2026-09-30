# Simple stdin fuzzer warmup

This is a behavior-based fuzzing exercise only. Do not open or inspect `target.py`
or other target source code to find the vulnerability. Discover it by generating
inputs and observing the program's outputs and crashes.

## Step 1: Open a Codespace and create a branch

Sign in to GitHub and open https://github.com/Kwstubbs/fw5. Do not fork the
repository first.

Click **Code**, open the **Codespaces** tab, and choose **... > New with options**
to create a Codespace with at least **4 cores**.

Once the Codespace is ready, open its terminal and run:

	git switch -c workshop-solution
	cd warmup

This creates a local branch in your Codespace; it does not require write access
to the instructor's repository. Run the exercise commands below from `warmup`.

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

Write a fuzzer. Try to trigger a ValueError within the python script, which will crash the program.

## Step 5: Submit your fuzzer

In the same Codespace, once your fuzzer is ready, run these commands from the
`warmup` directory. Replace `fuzzer.py` if you used a different filename:

	git add -f fuzzer.py
	git commit -m "warmup solution"

The repository ignores `fuzzer.py`, so `-f` is needed to stage your solution if you happened to use that name.

When the fork prompt appears after committing, choose **Yes** (or enter `y` if
prompted in the terminal). Codespaces creates a fork under your GitHub account,
or connects to your existing fork, and points `origin` to it. Stay in the same
Codespace; there is no need to open a new one.

Push your branch to your fork:

	git push --set-upstream origin workshop-solution

Open the pull request link printed by `git push`, or visit your fork on GitHub
and click **Compare & pull request**. Confirm that the base repository is
`Kwstubbs/fw5` on its default branch, and the source is your fork's
`workshop-solution` branch. Add a title and click **Create pull request**.

## Alert: 
Step 6 may reveal information that is not intended for the exercise. Please only reproduce crashes after your fuzzer is submitted, or once the exercise is complete.

## Step 6: Reproduce a crash

From the `warmup` directory, replay the saved crash input by replacing the
filename below with the reported filename:

	python3.11 target.py < ./crashes/crash-78.bin
