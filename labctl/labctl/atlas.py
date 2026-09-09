"""Atlas proceed pins and hard-leave deny checks."""
from __future__ import annotations

import json
from pathlib import Path

from labctl.paths import data_path


DENY_POLICIES = frozenset({"hard_ban", "agentscan"})


def load_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array in {path}")
    return data


def load_proceed(start: Path | None = None) -> list[dict]:
    return load_json(data_path("atlas-proceed-sample.json", start))


def load_hard_leaves(start: Path | None = None) -> list[dict]:
    return load_json(data_path("atlas-hard-leaves.json", start))


def normalize_repo(owner_repo: str) -> str:
    name = owner_repo.strip().removeprefix("https://github.com/").removesuffix(".git")
    if name.count("/") != 1:
        raise ValueError(f"Expected owner/repo, got: {owner_repo!r}")
    return name


def lookup_leave(owner_repo: str, start: Path | None = None) -> dict | None:
    key = normalize_repo(owner_repo)
    for row in load_hard_leaves(start):
        if row.get("full_name") == key:
            return row
    return None


def is_denied(owner_repo: str, start: Path | None = None) -> tuple[bool, dict | None]:
    row = lookup_leave(owner_repo, start)
    if row and row.get("policy") in DENY_POLICIES:
        return True, row
    return False, row
