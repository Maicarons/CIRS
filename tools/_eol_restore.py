#!/usr/bin/env python3
"""Restore the original line-ending style of the modified src/docs/lang/*.toml files.

The DOC_CC_* fix rewrote whole files through Python text I/O, which normalised
CRLF to LF on Windows.  The blobs committed in git use CRLF for most of these
files, so the diff showed every line as changed.  This script restores the
committed EOL style so the diff only contains the real label changes.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "src" / "docs" / "lang"


def head_blob(path: Path) -> bytes | None:
    try:
        out = subprocess.run(
            ["git", "show", "HEAD:" + path.relative_to(ROOT).as_posix()],
            cwd=str(ROOT), capture_output=True,
        )
    except OSError:
        return None
    return out.stdout if out.returncode == 0 else None


def main() -> int:
    changed = 0
    checked = 0
    for path in sorted(LANG_DIR.glob("*.toml")):
        rel = path.relative_to(ROOT).as_posix()
        blob = head_blob(path)
        if blob is None:
            continue
        checked += 1
        head_crlf = b"\r\n" in blob
        cur = path.read_bytes()
        cur_crlf = b"\r\n" in cur
        if head_crlf == cur_crlf:
            continue
        if head_crlf:
            body = cur.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
        else:
            body = cur.replace(b"\r\n", b"\n")
        path.write_bytes(body)
        changed += 1
        print(f"eol-restored {rel} -> {'CRLF' if head_crlf else 'LF'}")
    print(f"checked={checked} changed={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
