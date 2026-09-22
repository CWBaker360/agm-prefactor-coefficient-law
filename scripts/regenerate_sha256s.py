#!/usr/bin/env python3
"""Regenerate SHA256SUMS.txt from canonical Git blob bytes at HEAD.

Why this exists
---------------
Hashing a Windows working tree can produce CRLF-dependent checksums for text
files even though the repository stores canonical LF bytes.  This script hashes
the exact bytes stored by Git at HEAD, so the ledger is platform-independent.

Workflow
--------
1. Commit all content changes first.
2. Run this script from the repository root.
3. Review SHA256SUMS.txt.
4. Commit only the updated SHA256SUMS.txt.

SHA256SUMS.txt itself is excluded to avoid self-reference.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


LEDGER = Path("SHA256SUMS.txt")


def git(*args: str) -> bytes:
    proc = subprocess.run(
        ["git", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout


def main() -> int:
    root = git("rev-parse", "--show-toplevel").decode("utf-8").strip()
    if Path.cwd().resolve() != Path(root).resolve():
        raise SystemExit(
            f"Run this script from the repository root:\n  {root}"
        )

    # Canonical tracked paths at HEAD.
    tracked = [
        p
        for p in git("ls-tree", "-r", "--name-only", "HEAD")
        .decode("utf-8")
        .splitlines()
        if p and p != LEDGER.as_posix()
    ]

    lines: list[str] = []
    for path in tracked:
        blob = git("show", f"HEAD:{path}")
        digest = hashlib.sha256(blob).hexdigest()
        lines.append(f"{digest}  {path}")

    LEDGER.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {LEDGER} with {len(lines)} canonical Git-blob checksums.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
