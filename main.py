#!/usr/bin/env python3
"""news-image-20261124 entrypoint.

Copies the finished entry image (entry.png, a 1024x1024 JPEG held in this
repository) to /output/entry.png.

The grader runs this program twice with `python3 -P -s`; both runs must
write identical bytes, so the program only copies the file and checks the
copy's size. Standard library only, no network, no local imports.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print("missing entry image:", SRC, file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    if os.path.getsize(SRC) != os.path.getsize(DST):
        print("size mismatch after copy", file=sys.stderr)
        return 1
    if sha256(SRC) != sha256(DST):
        print("checksum mismatch after copy", file=sys.stderr)
        return 1
    print("entry.png copied to", DST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
