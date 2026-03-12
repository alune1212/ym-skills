from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def run_command(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def test_validate_script_passes() -> None:
    result = run_command("shared/scripts/validate_repo.py")
    assert result.returncode == 0, result.stderr


def test_package_example_skill(tmp_path: Path) -> None:
    dist_dir = REPO_ROOT / "dist" / "example-skill"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    result = run_command("shared/scripts/package_skill.py", "example-skill")
    assert result.returncode == 0, result.stderr
    assert (dist_dir / "SKILL.md").exists()


def test_new_skill_updates_registry() -> None:
    skill_name = "demo-generated-skill"
    target_dir = REPO_ROOT / "skills" / skill_name
    dist_dir = REPO_ROOT / "dist" / skill_name
    registry_path = REPO_ROOT / "registry" / "index.yaml"
    original_registry = registry_path.read_text(encoding="utf-8")

    if target_dir.exists():
        shutil.rmtree(target_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    try:
        result = run_command("shared/scripts/new_skill.py", skill_name)
        assert result.returncode == 0, result.stderr
        assert (target_dir / "SKILL.md").exists()

        validate_result = run_command("shared/scripts/validate_repo.py")
        assert validate_result.returncode == 0, validate_result.stderr
    finally:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        registry_path.write_text(original_registry, encoding="utf-8")

