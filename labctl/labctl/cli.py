"""labctl — thin glue over mature OSS parts (Task/Dagger/kind/wasmtime/…)."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import yaml


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
    print(f"initialized {root}")
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
    runtime = spec.get("runtime") or "local"
    # MVP: local subprocess only; kind/gvisor/wasmtime wired in later slices
    if runtime not in ("local", "wasmtime", "kind", "gvisor"):
        print(f"unsupported runtime {runtime}", file=sys.stderr)
        return 2
    if runtime != "local":
        print(
            f"note: runtime={runtime} not fully wired yet; executing locally as stub",
            file=sys.stderr,
        )
    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    rid = _run_id(raw)
    runs = root / "runs"
    runs.mkdir(exist_ok=True)
    record = {
        "run_id": rid,
        "runtime_requested": runtime,
        "command": cmd,
        "exit_code": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "duration_s": round(time.time() - started, 3),
        "experiment_sha256": hashlib.sha256(raw).hexdigest(),
    }
    out = runs / f"{rid}.json"
    out.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"run_id": rid, "exit_code": proc.returncode, "record": str(out)}))
    return proc.returncode


def cmd_replay(args: argparse.Namespace) -> int:
    root = Path(args.path)
    record_path = root / "runs" / f"{args.run_id}.json"
    if not record_path.exists():
        # allow bare run id or path
        alt = Path(args.run_id)
        record_path = alt if alt.exists() else record_path
    if not record_path.exists():
        print(f"run not found: {args.run_id}", file=sys.stderr)
        return 2
    record = json.loads(record_path.read_text())
    print(json.dumps(record, indent=2))
    print(
        "replay stub: re-validate experiment_sha256 and re-exec in pinned runtime (TODO)",
        file=sys.stderr,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="labctl", description="systems-lab control CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create experiment directory")
    s.add_argument("path")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("run", help="execute experiment and write run ledger entry")
    s.add_argument("path")
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("replay", help="show (and later re-exec) a run record")
    s.add_argument("run_id")
    s.add_argument("--path", default=".")
    s.set_defaults(func=cmd_replay)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
