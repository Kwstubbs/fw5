#!/usr/bin/env bash
# Builds the exercise 4 fuzz target: jhead's EXIF parser.
#
# jhead 3.00, pinned to the commit just before the 2016 EXIF hardening changes
# ("handle potential overflow" / "Changes ... relating to fuzz testing").
#
# Note: libFuzzer coverage only - no AddressSanitizer. The bug is reachable as
# a plain SIGSEGV.
set -euo pipefail

cd "$(dirname "$0")"

JHEAD_REPO=https://github.com/Matthias-Wandel/jhead.git
JHEAD_COMMIT=8e226ed49eeb4311222cebd10c20b32c4b29b0bf

if ! command -v clang >/dev/null; then
  echo "clang is required (sudo apt-get install -y clang)" >&2
  exit 1
fi

if [ ! -d jhead ]; then
  git clone --quiet "$JHEAD_REPO" jhead
fi

git -C jhead checkout --quiet "$JHEAD_COMMIT"

clang -g -O1 -fsanitize=fuzzer -w \
  jhead/exif.c jhead/gpsinfo.c jhead/makernote.c jhead/iptc.c \
  jhead/jpgfile.c jhead/jpgqguess.c \
  fuzz_exif.c -o fuzz_exif -lm

echo "built ./fuzz_exif  (jhead $(git -C jhead log --oneline -1))"
echo
echo "run it with:"
echo "  ./fuzz_exif corpus -artifact_prefix=./"
