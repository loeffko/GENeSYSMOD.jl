# -*- coding: utf-8 -*-
"""script_dataload.py

Runs the North-America conversion scripts in series and copies the resulting
Excel files into the Julia model's InputData folder.

Configuration is read from script_dataload_settings.conf located next to this
script. Run from anywhere:

    python C:\\path\\to\\script_dataload.py

Steps:
  1. Read paths + script list + copy patterns from the .conf file.
  2. Run each conversion script with cwd = conversion_script_dir
     (the scripts rely on relative paths and local imports, so the working
     directory must be the Conversion Script folder).
  3. Copy all files matching the configured glob pattern(s) from the output
     folder to the model InputData folder (overwriting existing files).
"""

import configparser
import glob
import os
import shutil
import subprocess
import sys

CONF_NAME = "script_dataload_settings.conf"


def die(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.join(here, CONF_NAME)
    if not os.path.isfile(conf_path):
        die(f"Config file not found: {conf_path}")

    cfg = configparser.ConfigParser()
    cfg.read(conf_path, encoding="utf-8")

    try:
        conv_dir = cfg.get("paths", "conversion_script_dir").strip()
        output_dir = cfg.get("paths", "output_dir").strip()
        input_dir = cfg.get("paths", "model_inputdata_dir").strip()
        scripts = [s.strip() for s in cfg.get("run", "scripts").split(",") if s.strip()]
        patterns = [p.strip() for p in cfg.get("run", "copy_patterns").split(",") if p.strip()]
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        die(f"Config file incomplete: {e}")

    python_exe = cfg.get("run", "python_exe", fallback="").strip() or sys.executable

    # --- sanity checks ---
    if not os.path.isdir(conv_dir):
        die(f"Conversion script dir not found: {conv_dir}")
    if not os.path.isdir(input_dir):
        die(f"Model InputData dir not found: {input_dir}")
    for s in scripts:
        if not os.path.isfile(os.path.join(conv_dir, s)):
            die(f"Script not found in conversion dir: {s}")

    # --- 1) run conversion scripts in series ---
    for s in scripts:
        print(f"\n=== Running {s} ===")
        result = subprocess.run([python_exe, s], cwd=conv_dir)
        if result.returncode != 0:
            die(f"{s} failed with exit code {result.returncode}. Aborting (no files copied).")

    # --- 2) copy resulting Excel files ---
    if not os.path.isdir(output_dir):
        die(f"Output dir not found after conversion: {output_dir}")

    copied = []
    for pattern in patterns:
        for src in sorted(glob.glob(os.path.join(output_dir, pattern))):
            dst = os.path.join(input_dir, os.path.basename(src))
            shutil.copy2(src, dst)
            copied.append(os.path.basename(src))
            print(f"Copied: {os.path.basename(src)} -> {input_dir}")

    if not copied:
        die(f"No files matched pattern(s) {patterns} in {output_dir}")

    print(f"\nDone. {len(copied)} file(s) copied to {input_dir}")


if __name__ == "__main__":
    main()
