#!/usr/bin/env python3
"""news-image-20261119 entrypoint: copy the front-page image to the output dir.

The image (entry.png, 1024x1024, "THE WORLD — Thursday 19 November 2026")
sums up the day's world news in 30 verified stories across 7 continents.
The program is deterministic: it copies fixed bytes and verifies the
SHA-256 of the copy against the known hash, so two runs write identical files.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "453a4b5169e4697ed7579cbcbea944a51ff8edbcf85b2f7f270e72523cf44e4a"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    # Verify the bundled image itself before copying, so a corrupted repo
    # file fails loudly instead of producing a bad entry.
    if sha256_of(src) != EXPECTED_SHA256:
        print(f"source sha256 mismatch for {src}", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    got = sha256_of(dst)
    if got != EXPECTED_SHA256:
        print(f"sha256 mismatch: {got} != {EXPECTED_SHA256}", file=sys.stderr)
        return 1
    print(f"wrote {dst} sha256={got}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
