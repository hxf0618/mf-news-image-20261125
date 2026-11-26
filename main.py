#!/usr/bin/env python3
"""Entry point for the news-image-20261125 bounty.

Copies the pre-drawn front page (entry.png, in this repository) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Standard library only.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

MAX_BYTES = 1048576
MAX_DIMENSION = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def check_png(path):
    """Validate the copied file: real PNG, <=1024x1024, <=1 MiB."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit("entry.png too large: %d bytes" % size)
    with open(path, "rb") as f:
        header = f.read(33)
    if header[:8] != PNG_SIGNATURE:
        raise SystemExit("entry.png is not a PNG")
    # IHDR chunk: length 13, type "IHDR", then width/height as uint32.
    if header[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        raise SystemExit("entry.png too big: %dx%d" % (width, height))
    return width, height, size


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    width, height, size = check_png(dest)
    print("wrote %s (%dx%d, %d bytes)" % (dest, width, height, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
