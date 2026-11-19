#!/usr/bin/env python3
"""Write the bundled broadsheet image to /output/entry.png.

This entry's program is deliberately small: the artwork itself is the
bundled file ``entry.png`` that sits next to this script, and this program's
job is to place an exact copy of it at ``/output/entry.png`` and prove the
copy is byte-for-byte identical to the original. If anything differs, the
program fails loudly instead of silently producing a wrong file.

Usage:
    python3 main.py

Exit code is 0 only when the output file exists and matches the source
byte for byte. Any problem (missing source, unreadable file, failed
write, or a byte mismatch) prints a clear error and exits non-zero.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Name of the bundled image shipped with this entry.
SOURCE_NAME = "entry.png"

# Where the finished image must end up.
DESTINATION = Path("/output") / "entry.png"

# Largest image this entry is willing to handle. The bundled broadsheet is
# well under this; anything bigger means the wrong file got bundled.
MAX_IMAGE_BYTES = 1 * 1024 * 1024


def locate_source() -> Path:
    """Find ``entry.png`` next to this script, or in the working directory.

    The script is normally run from the repository root, so the image sits
    beside it. Resolving relative to ``__file__`` first keeps the program
    working no matter which directory it is launched from.
    """
    beside_script = Path(__file__).resolve().parent / SOURCE_NAME
    if beside_script.is_file():
        return beside_script

    in_working_dir = Path.cwd() / SOURCE_NAME
    if in_working_dir.is_file():
        return in_working_dir

    raise FileNotFoundError(
        f"could not find {SOURCE_NAME!r} next to main.py "
        f"({beside_script}) or in the working directory ({in_working_dir})"
    )


def read_source(path: Path) -> bytes:
    """Read the bundled image, refusing anything implausibly large."""
    payload = path.read_bytes()
    if len(payload) > MAX_IMAGE_BYTES:
        raise ValueError(
            f"{path} is {len(payload)} bytes, over the "
            f"{MAX_IMAGE_BYTES}-byte limit for this entry"
        )
    if not payload:
        raise ValueError(f"{path} is empty; refusing to write an empty image")
    # A real PNG always starts with these 8 signature bytes. Checking them
    # here catches a corrupt or swapped bundle before anything is written.
    png_signature = b"\x89PNG\r\n\x1a\n"
    if payload[:8] != png_signature:
        raise ValueError(
            f"{path} does not start with a PNG signature; "
            "the bundled image looks corrupt or is not a PNG file"
        )
    return payload


def write_and_verify(payload: bytes) -> None:
    """Write the image to /output and check the copy matches exactly."""
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(payload)

    written_back = DESTINATION.read_bytes()
    if written_back != payload:
        raise RuntimeError(
            f"verification failed: {DESTINATION} does not match the source "
            f"({len(written_back)} bytes written vs {len(payload)} expected)"
        )


def main() -> int:
    try:
        source_path = locate_source()
        payload = read_source(source_path)
        write_and_verify(payload)
    except (FileNotFoundError, ValueError, RuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {DESTINATION} ({len(payload)} bytes, verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
