# Fuzzing Workshop

This repository contains hands-on fuzzing exercises, from a simple stdin target to native, Java, and Python fuzzing. Some targets are intentionally vulnerable and use outdated dependencies; use them only in this workshop environment, not with real data or on production systems.

## Table of Contents

- [Get Started in GitHub Codespaces](#get-started-in-github-codespaces)
- [Get Started Locally](#get-started-locally)
- [Verify Your Toolchain](#verify-your-toolchain)
- [Repository Contents](#repository-contents)
- [Submit Your Work](#submit-your-work)

## Get Started in GitHub Codespaces

1. Open [Kwstubbs/fw5](https://github.com/Kwstubbs/fw5) in a GitHub Codespace.
2. Wait for the devcontainer setup to finish. It installs Java 21, clang and libFuzzer, LLVM symbolizer, `uv`, and Python 3.11.
3. Create a branch for your work:

   ```sh
   git switch -c <your-username>/workshop-solution
   ```

4. Run the checks in [Verify Your Toolchain](#verify-your-toolchain).
5. Choose an exercise from [Repository Contents](#repository-contents), change to its directory, and follow its guide. For example, to start the warmup:

   ```sh
   cd warmup
   ```

6. Commit your work. When Codespaces offers to create a fork, accept the prompt, then push your branch and open a pull request back to `Kwstubbs/fw5`.

All solutions must be submitted through a pull request from your fork. Codespaces can [create and configure a fork for you](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-source-control-in-your-codespace#about-automatic-forking) when you are ready to push.

## Get Started Locally

Before locally cloning, open [Kwstubbs/fw5](https://github.com/Kwstubbs/fw5), select **Fork**, and create a fork under your GitHub account. Clone your fork and create a branch for your work, replacing `<your-username>` with your GitHub username:

```sh
git clone https://github.com/<your-username>/fw5.git
cd fw5
git switch -c <your-username>/workshop-solution
git remote add upstream https://github.com/Kwstubbs/fw5.git
```

The Codespaces devcontainer is based on Ubuntu 24.04. Linux is the supported local environment; use Codespaces if you are on another operating system or do not want to install the fuzzing toolchains. For a similar Ubuntu setup, install:

- Git
- JDK 21 (`java` and `javac`)
- Python 3.11
- `uv` (used to manage Python and install exercise dependencies)
- clang, LLVM tools including `llvm-symbolizer`, and the libFuzzer runtime

For example, on Ubuntu 24.04, install the system packages with:

```sh
sudo apt-get update
sudo apt-get install -y openjdk-21-jdk clang llvm libclang-rt-18-dev curl ca-certificates
```

Install `uv`, then use it to install Python 3.11 if it is not already available:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv python install 3.11
```

See the [`uv` installation guide](https://docs.astral.sh/uv/getting-started/installation/) for other installation methods. Requirements differ by exercise; Exercise 3, for example, creates its own virtual environment and installs packages from `requirements.txt`.

## Verify Your Toolchain

Codespaces runs these checks when the container is created. Local users can run them before starting an exercise:

```sh
git --version
java -version
javac -version
clang --version
llvm-symbolizer --version
uv --version
python3.11 --version
```

If a Codespaces check fails, open the Command Palette and run **Codespaces: Rebuild Container**. Locally, install the missing tool before continuing.

## Repository Contents

| Directory | Target and goal | Tooling | Start here |
| --- | --- | --- | --- |
| `warmup/` | Discover a crash in a simple stdin parser without inspecting its implementation | Python 3.11 and a fuzzer you write | [Warmup instructions](warmup/INSTRUCTIONS.md) |
| `exercise1/` | Find a memory-safety bug in jhead's EXIF parser | C, clang, and libFuzzer | [Exercise 1 instructions](exercise1/INSTRUCTIONS.md) |
| `exercise2/` | Complete a harness and fuzz a booking parser | Java 21 and the bundled Jazzer executable | [Exercise 2 instructions](exercise2/INSTRUCTIONS.md) |
| `exercise3/` | Complete an HTML-injection oracle and find a mistune XSS vulnerability | Python 3.11, Atheris, and an oracle test script | [Exercise 3 instructions](exercise3/INSTRUCTIONS.md) |
| `Homework/pypng/` | Fuzz the vendored PyPNG reader using the provided images as starting material | Python 3.11 and Atheris | [PyPNG starter harness](Homework/pypng/code/fuzzer.py) |

The guided exercises contain detailed build, fuzzing, corpus-reset, and crash-reproduction steps. Run their commands from the exercise directory. `Homework/pypng/` does not currently include a separate instruction file; its target code, harness, and sample assets are included in that directory.

## Submit Your Work

Commit your solution on your branch:

```sh
git status
git add <files-you-changed>
git commit -m "Complete fuzzing exercise"
git push --set-upstream origin <your-username>/workshop-solution
```

In Codespaces, accept the create a fork prompt when it comes up. For local development, `origin` already points to the fork you cloned. Open the pull request link printed by `git push`, or open your fork on GitHub and select **Compare & pull request**.

Before submitting, confirm that the pull request's base repository is `Kwstubbs/fw5` and its source branch is `<your-username>/workshop-solution` on your fork. Do not commit generated corpora, build output, virtual environments, or crash artifacts unless an exercise explicitly asks for them.