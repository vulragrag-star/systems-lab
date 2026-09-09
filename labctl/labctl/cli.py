"""labctl — thin glue over mature OSS parts (Task/Dagger/kind/wasmtime/…)."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import yaml

from labctl import atlas
from labctl.ledger import list_runs, load_run, write_run
from labctl.runtime import execute, runtime_meta


def _run_id(payload: bytes) -> str:
    return hashlib.sha256(payload + str(time.time_ns()).encode()).hexdigest()[:16]


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.path)
    root.mkdir(parents=True, exist_ok=True)
    exp = root / "experiment.yaml"
    if not exp.exists():
        exp.write_text(
            """apiVersion: systems-lab.io/v1alpha1
kind: Experiment
metadata:
  name: untitled
spec:
  runtime: local
  command: ["echo", "edit me"]
  capture:
    stdout: true
    exitCode: true
"""
        )
    (root / "runs").mkdir(exist_ok=True)
    print(f"initialized {root.resolve()}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    root = Path(args.path)
    exp_path = root / "experiment.yaml"
    if not exp_path.exists():
        print(f"missing {exp_path}", file=sys.stderr)
        return 2
    raw = exp_path.read_bytes()
    doc = yaml.safe_load(raw)
    spec = (doc or {}).get("spec") or {}
    cmd = spec.get("command") or ["echo", "empty"]
    if not isinstance(cmd, list) or not all(isinstance(x, (str, int, float)) for x in cmd):
        print("spec.command must be a list of scalars", file=sys.stderr)
        return 2
    cmd = [str(x) for x in cmd]
    runtime = spec.get("runtime") or "local"
    started = time.time()
    try:
        proc = execute(cmd, runtime)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    rid = _run_id(raw)
    meta = runtime_meta(proc, runtime)
    record = {
        "run_id": rid,
        "experiment_sha256": hashlib.sha256(raw).hexdigest(),
        "command": cmd,
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "duration_s": round(time.time() - started, 3),
        "runtime": meta["runtime_effective"],
        "runtime_requested": meta["runtime_requested"],
        "runtime_effective": meta["runtime_effective"],
        "runtime_note": meta["runtime_note"],
    }
    out = write_run(root, record)
    print(
        json.dumps(
            {
                "run_id": rid,
                "exit_code": proc.returncode,
                "runtime": meta["runtime_effective"],
                "record": str(out),
            }
        )
    )
    return proc.returncode


def cmd_replay(args: argparse.Namespace) -> int:
    root = Path(args.path)
    try:
        record, record_path = load_run(root, args.run_id)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    exp_path = root / "experiment.yaml"
    if exp_path.exists():
        current = hashlib.sha256(exp_path.read_bytes()).hexdigest()
        expected = record.get("experiment_sha256")
        if expected and current != expected:
            print(
                f"experiment_sha256 mismatch: record={expected} current={current}",
                file=sys.stderr,
            )
            if not args.force:
                return 3
        else:
            print(f"experiment_sha256 ok: {current}", file=sys.stderr)

    if args.show_only:
        print(json.dumps(record, indent=2))
        return 0

    cmd = record.get("command") or ["echo", "empty"]
    runtime = record.get("runtime_requested") or record.get("runtime") or "local"
    print(f"replaying {record_path} runtime={runtime} command={cmd}", file=sys.stderr)
    started = time.time()
    try:
        proc = execute(list(cmd), str(runtime))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    result = {
        "replay_of": record.get("run_id"),
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "duration_s": round(time.time() - started, 3),
        **runtime_meta(proc, str(runtime)),
        "match_exit": proc.returncode == record.get("exit_code"),
        "match_stdout": proc.stdout == record.get("stdout"),
    }
    print(json.dumps(result, indent=2))
    return proc.returncode


def cmd_ledger_list(args: argparse.Namespace) -> int:
    root = Path(args.path)
    records = list_runs(root)
    if args.json:
        print(json.dumps(records, indent=2))
        return 0
    if not records:
        print("no runs recorded")
        return 0
    for rec in records:
        print(
            f"{rec.get('run_id')}\texit={rec.get('exit_code')}\t"
            f"runtime={rec.get('runtime') or rec.get('runtime_effective')}\t"
            f"duration_s={rec.get('duration_s')}\t"
            f"sha256={(rec.get('experiment_sha256') or '')[:12]}"
        )
    return 0


def cmd_pins(args: argparse.Namespace) -> int:
    try:
        rows = atlas.load_proceed()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    limit = args.limit
    if args.json:
        print(json.dumps(rows[:limit] if limit else rows, indent=2))
        return 0
    shown = rows[:limit] if limit else rows
    for row in shown:
        print(
            f"{row.get('full_name')}\tstars={row.get('stars')}\t"
            f"policy={row.get('policy')}\tsector={row.get('sector')}"
        )
    if limit and len(rows) > limit:
        print(f"... {len(rows) - limit} more (use --limit 0 for all)", file=sys.stderr)
    return 0


def cmd_deny_check(args: argparse.Namespace) -> int:
    try:
        denied, row = atlas.is_denied(args.repo)
    except (FileNotFoundError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    payload = {
        "repo": atlas.normalize_repo(args.repo),
        "denied": denied,
        "entry": row,
    }
    print(json.dumps(payload, indent=2))
    return 1 if denied else 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="labctl", description="systems-lab control CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create experiment directory")
    s.add_argument("path")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("run", help="execute experiment and write run ledger entry")
    s.add_argument("path")
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("replay", help="re-validate and re-exec a run record")
    s.add_argument("run_id")
    s.add_argument("--path", default=".")
    s.add_argument("--show-only", action="store_true", help="print record without re-exec")
    s.add_argument(
        "--force",
        action="store_true",
        help="re-exec even if experiment_sha256 mismatches",
    )
    s.set_defaults(func=cmd_replay)

    s = sub.add_parser("ledger", help="inspect the experiment run ledger")
    led = s.add_subparsers(dest="ledger_cmd", required=True)
    ls = led.add_parser("list", help="list recorded runs")
    ls.add_argument("--path", default=".")
    ls.add_argument("--json", action="store_true")
    ls.set_defaults(func=cmd_ledger_list)

    s = sub.add_parser("pins", help="list atlas proceed sample pins")
    s.add_argument("--json", action="store_true")
    s.add_argument("--limit", type=int, default=50, help="0 = all")
    s.set_defaults(func=cmd_pins)

    s = sub.add_parser("deny-check", help="check owner/repo against atlas hard leaves")
    s.add_argument("repo", help="owner/repo")
    s.set_defaults(func=cmd_deny_check)

    args = p.parse_args(argv)
    if getattr(args, "limit", None) == 0:
        args.limit = None
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
