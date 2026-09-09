"""atlasgate — atlas-aware disclosure + release governance gate."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from atlasgate.paths import data_path

DENY_POLICIES = frozenset({"hard_ban", "agentscan"})

AI_DISCLOSURE_TRAILER = """\
Assisted-by: AI
AI-Assisted: true

This change was produced or reviewed with AI assistance. Maintainers:
verify intent, license compatibility, and security before merging.
"""


def _normalize_repo(owner_repo: str) -> str:
    name = owner_repo.strip().removeprefix("https://github.com/").removesuffix(".git")
    if name.count("/") != 1:
        raise ValueError(f"Expected owner/repo, got: {owner_repo!r}")
    return name


def _load_hard_leaves() -> list[dict]:
    path = data_path("atlas-hard-leaves.json")
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        raise ValueError(f"Expected JSON array in {path}")
    return data


def cmd_check_repo(args: argparse.Namespace) -> int:
    try:
        key = _normalize_repo(args.repo)
        leaves = _load_hard_leaves()
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    match = next((row for row in leaves if row.get("full_name") == key), None)
    denied = bool(match and match.get("policy") in DENY_POLICIES)
    payload = {"repo": key, "denied": denied, "entry": match}
    print(json.dumps(payload, indent=2))
    if denied:
        policy = match.get("policy")
        print(
            f"atlasgate: {key} is denied by atlas hard leaves (policy={policy})",
            file=sys.stderr,
        )
        return 1
    return 0


def cmd_trailer(_args: argparse.Namespace) -> int:
    sys.stdout.write(AI_DISCLOSURE_TRAILER)
    if not AI_DISCLOSURE_TRAILER.endswith("\n"):
        sys.stdout.write("\n")
    return 0


def cmd_scan_ci(args: argparse.Namespace) -> int:
    zizmor = shutil.which("zizmor")
    if not zizmor:
        print(
            "atlasgate scan-ci: zizmor not on PATH; skipping CI workflow scan "
            "(install https://github.com/zizmorcore/zizmor to enable)"
        )
        return 0
    target = Path(args.path)
    cmd = [zizmor, str(target)]
    print(f"atlasgate scan-ci: running {' '.join(cmd)}", file=sys.stderr)
    proc = subprocess.run(cmd)
    return proc.returncode


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="atlasgate",
        description="Atlas-aware disclosure + release governance gate",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser(
        "check-repo",
        help="fail if owner/repo is hard_ban or agentscan in atlas-hard-leaves.json",
    )
    s.add_argument("repo", help="owner/repo")
    s.set_defaults(func=cmd_check_repo)

    s = sub.add_parser("trailer", help="print AI disclosure trailer text")
    s.set_defaults(func=cmd_trailer)

    s = sub.add_parser(
        "scan-ci",
        help="run zizmor on workflows if available, else note skip",
    )
    s.add_argument(
        "--path",
        default=".",
        help="path for zizmor to scan (default: .)",
    )
    s.set_defaults(func=cmd_scan_ci)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
