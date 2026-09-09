"""Experiment runtime execution helpers."""
from __future__ import annotations

import shutil
import subprocess
import sys
from typing import Any


SUPPORTED = ("local", "wasmtime", "kind", "gvisor")


def execute(command: list[str], runtime: str) -> subprocess.CompletedProcess[str]:
    runtime = runtime or "local"
    if runtime not in SUPPORTED:
        raise ValueError(f"unsupported runtime {runtime}")

    effective = runtime
    note: str | None = None

    if runtime == "wasmtime":
        if not shutil.which("wasmtime"):
            note = "wasmtime not on PATH; falling back to local execution"
            effective = "local"
        elif command and str(command[0]).endswith(".wasm"):
            command = ["wasmtime", "run", *command]
            effective = "wasmtime"
        else:
            note = (
                "wasmtime is on PATH but command is not a .wasm module; "
                "falling back to local execution"
            )
            effective = "local"
    elif runtime == "kind":
        if not shutil.which("kind"):
            note = "kind not on PATH; falling back to local execution"
            effective = "local"
        else:
            note = (
                "kind is on PATH but cluster pod exec is not fully wired; "
                "falling back to local execution"
            )
            effective = "local"
    elif runtime == "gvisor":
        if not shutil.which("runsc"):
            note = "gVisor runsc not on PATH; falling back to local execution"
            effective = "local"
        else:
            note = (
                "gVisor runsc is on PATH but sandbox profile is not fully wired; "
                "falling back to local execution"
            )
            effective = "local"

    if note:
        print(f"note: {note}", file=sys.stderr)

    proc = subprocess.run(command, capture_output=True, text=True)
    # Attach metadata for callers without changing CompletedProcess API
    setattr(proc, "runtime_effective", effective)
    setattr(proc, "runtime_note", note)
    return proc


def runtime_meta(proc: subprocess.CompletedProcess[str], requested: str) -> dict[str, Any]:
    return {
        "runtime_requested": requested,
        "runtime_effective": getattr(proc, "runtime_effective", requested),
        "runtime_note": getattr(proc, "runtime_note", None),
    }
