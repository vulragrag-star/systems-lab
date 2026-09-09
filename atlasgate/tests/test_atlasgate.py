from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from atlasgate.cli import main
from atlasgate.paths import find_repo_root


@pytest.fixture
def repo_root() -> Path:
    # Walk from this file up into the monorepo
    here = Path(__file__).resolve()
    root = here.parents[2]  # atlasgate/tests -> atlasgate -> systems-lab
    if not (root / "data").is_dir():
        root = find_repo_root(here)
    os.environ["SYSTEMS_LAB_ROOT"] = str(root)
    return root


def test_check_repo_denied(repo_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check-repo", "yt-dlp/yt-dlp"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["denied"] is True
    assert payload["entry"]["policy"] == "hard_ban"


def test_check_repo_agentscan(repo_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check-repo", "sveltejs/svelte"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["entry"]["policy"] == "agentscan"


def test_check_repo_ok(repo_root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["check-repo", "neovim/neovim"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["denied"] is False


def test_trailer(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["trailer"]) == 0
    text = capsys.readouterr().out
    assert "Assisted-by: AI" in text
    assert "AI-Assisted: true" in text


def test_scan_ci_skip(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["scan-ci"]) == 0
    out = capsys.readouterr().out
    assert "zizmor" in out.lower()
