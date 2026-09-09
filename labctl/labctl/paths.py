"""Resolve systems-lab repo root and atlas data files."""
from __future__ import annotations

import os
from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    """Locate repo root via SYSTEMS_LAB_ROOT or by walking up for data/."""
    env = os.environ.get("SYSTEMS_LAB_ROOT")
    if env:
        root = Path(env).expanduser().resolve()
        if (root / "data").is_dir():
            return root
        raise FileNotFoundError(
            f"SYSTEMS_LAB_ROOT={env} does not contain a data/ directory"
        )

    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "data" / "atlas-hard-leaves.json").is_file() or (
            candidate / "data" / "atlas-proceed-sample.json"
        ).is_file():
            return candidate
        if (candidate / "data").is_dir() and (
            (candidate / "labctl").is_dir() or (candidate / "docs").is_dir()
        ):
            return candidate
    raise FileNotFoundError(
        "Could not find systems-lab root (set SYSTEMS_LAB_ROOT or run from the repo)"
    )


def data_path(name: str, start: Path | None = None) -> Path:
    """Return path to a file under data/ relative to the repo root."""
    root = find_repo_root(start)
    path = root / "data" / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing atlas data file: {path}")
    return path
