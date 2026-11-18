#!/usr/bin/env python3
"""news-image-20261118 entry program (Python 3.13, standard library only).

Copies the finished front-page image shipped in this repository to
/output/entry.png. No network, no fonts, no third-party packages at
runtime, so both grading runs write byte-identical output.

The image itself was rendered offline at build time by render.py
(Pillow + Liberation fonts, all copy baked in) and saved as entry.png.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
