# Exercise 3: Fuzzing mistune for XSS

The target is mistune 0.7.4, a Python library that converts Markdown to HTML.
It has a real XSS vulnerability. Your job is to write the check that detects it.

## Step 1: Install the dependencies

Everything the exercise needs is listed in `requirements.txt`. From the
`exercise3` directory:

```
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

That installs `atheris` (the fuzzing engine), `mistune==0.7.4` (the target),
and `beautifulsoup4` + `html5lib` (to parse the HTML that mistune produces).

Check it worked:

```
python -c "import atheris, mistune, bs4; print(mistune.__version__)"
```

## Step 2: What is an oracle?

A fuzzer has two halves.

The first half is **input generation**: Atheris mutates bytes, watches which
lines of mistune each input reaches, and keeps the inputs that reach new code.
That part is already written for you in `fuzz_mistune.py`.

The second half is the **oracle**: the code that looks at the result and
decides whether it is a bug. This is the half you have to write, and it is the
half that matters. Atheris only notices uncaught exceptions. Converting
Markdown to HTML does not throw, so if you do not define what "wrong" means,
the fuzzer will happily run for hours and report nothing.

For this target, "wrong" means mistune emitted HTML that lets an attacker run
JavaScript. mistune builds tags with string formatting, like this:

```python
'<a href="%s">' % link
```

If the text it substitutes contains a `"`, that quote ends the attribute early
and whatever follows is parsed by the browser as **new markup** rather than as
data. An attacker can use that to add an attribute such as `onclick`, or to
close the tag entirely and start a new one.

Ask a structural question instead: *did a tag or an attribute appear that
mistune's renderers could not have produced?* If so, something injected it.

## Step 3: Fill in oracle.py

Open `oracle.py`. Two lists are already provided:

- `ALLOWED_TAGS` — every tag mistune 0.7.4 can emit
- `ALLOWED_ATTRS` — every attribute it can emit, per tag

Complete `find_injection(html)`. The function receives the HTML string that
mistune produced and must return:

- a short string describing the first injected tag or attribute it finds, or
- `None` if the HTML only contains things mistune is allowed to emit

The two blank spots in the loop are where you decide that a tag, or an
attribute on a tag, does not belong.

## Step 4: Run the fuzzer

```
python fuzz_mistune.py -dict=bypass2.dict -artifact_prefix=crashes/
```

- `-dict=` gives the fuzzer Markdown syntax fragments to build inputs from
- `-artifact_prefix=` is where crash files are written; the trailing `/` is
  required, otherwise it is treated as a filename prefix

When your oracle fires, Atheris prints the payload and saves it under
`crashes/`. Replay any saved crash with:

```
python fuzz_mistune.py crashes/<crash-file>
```

## Step 5: Triage what you found

A crash file is a candidate, not a conclusion. For each one, print the raw HTML
and decide for yourself whether a browser would actually execute anything. Ask
which attribute or tag appeared, and where the attacker's text ended up in the
output.
