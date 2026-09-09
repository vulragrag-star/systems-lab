"""Run ledger: per-run JSON files plus optional JSONL index."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def runs_dir(experiment_root: Path) -> Path:
    d = experiment_root / "runs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def ledger_jsonl(experiment_root: Path) -> Path:
    return experiment_root / "ledger.jsonl"


def write_run(experiment_root: Path, record: dict[str, Any]) -> Path:
    rid = record["run_id"]
    out = runs_dir(experiment_root) / f"{rid}.json"
    out.write_text(json.dumps(record, indent=2) + "\n")
    with ledger_jsonl(experiment_root).open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, separators=(",", ":")) + "\n")
    return out


def load_run(experiment_root: Path, run_id: str) -> tuple[dict[str, Any], Path]:
    path = runs_dir(experiment_root) / f"{run_id}.json"
    if not path.exists():
        alt = Path(run_id)
        if alt.exists():
            path = alt
    if not path.exists():
        raise FileNotFoundError(f"run not found: {run_id}")
    return json.loads(path.read_text()), path


def list_runs(experiment_root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    rd = experiment_root / "runs"
    if rd.is_dir():
        for path in sorted(rd.glob("*.json")):
            try:
                records.append(json.loads(path.read_text()))
            except json.JSONDecodeError:
                continue
    if records:
        return records
    jl = ledger_jsonl(experiment_root)
    if jl.is_file():
        for line in jl.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records
