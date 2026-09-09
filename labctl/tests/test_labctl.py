from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from labctl.cli import main
from labctl.paths import data_path, find_repo_root


@pytest.fixture
def repo_root() -> Path:
    root = find_repo_root(Path(__file__))
    os.environ["SYSTEMS_LAB_ROOT"] = str(root)
    return root


def test_find_repo_root(repo_root: Path) -> None:
    assert (repo_root / "data" / "atlas-hard-leaves.json").is_file()
    assert data_path("atlas-proceed-sample.json").is_file()


def test_init_run_ledger_replay(tmp_path: Path, repo_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exp = tmp_path / "demo"
    assert main(["init", str(exp)]) == 0
    (exp / "experiment.yaml").write_text(
        """apiVersion: systems-lab.io/v1alpha1
kind: Experiment
metadata:
  name: pytest-echo
spec:
  runtime: local
  command: ["echo", "hello-lab"]
"""
    )
    rc = main(["run", str(exp)])
    assert rc == 0
    out = capsys.readouterr().out.strip().splitlines()[-1]
    payload = json.loads(out)
    rid = payload["run_id"]
    record = json.loads((exp / "runs" / f"{rid}.json").read_text())
    assert record["stdout"].strip() == "hello-lab"
    assert record["exit_code"] == 0
    assert record["experiment_sha256"]
    assert record["duration_s"] >= 0
    assert record["runtime"] == "local"
    assert (exp / "ledger.jsonl").is_file()

    assert main(["ledger", "list", "--path", str(exp)]) == 0
    listed = capsys.readouterr().out
    assert rid in listed

    assert main(["replay", rid, "--path", str(exp)]) == 0
    replay_out = capsys.readouterr().out
    assert "hello-lab" in replay_out


def test_wasmtime_fallback(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    exp = tmp_path / "wasm"
    assert main(["init", str(exp)]) == 0
    (exp / "experiment.yaml").write_text(
        """apiVersion: systems-lab.io/v1alpha1
kind: Experiment
metadata:
  name: wasm-fallback
spec:
  runtime: wasmtime
  command: ["echo", "fallback-ok"]
"""
    )
    assert main(["run", str(exp)]) == 0
    err = capsys.readouterr().err
    assert "falling back to local" in err or "wasmtime" in err


def test_pins_and_deny(repo_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["pins", "--limit", "3", "--json"]) == 0
    pins = json.loads(capsys.readouterr().out)
    assert isinstance(pins, list) and len(pins) == 3
    assert "full_name" in pins[0]

    assert main(["deny-check", "sqlite/sqlite"]) == 1
    denied = json.loads(capsys.readouterr().out)
    assert denied["denied"] is True
    assert denied["entry"]["policy"] == "hard_ban"

    assert main(["deny-check", "neovim/neovim"]) == 0
    ok = json.loads(capsys.readouterr().out)
    assert ok["denied"] is False
