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


def test_package_skill_rejects_path_traversal_name() -> None:
    protected_dir = REPO_ROOT / "package-skill-protected"
    protected_file = protected_dir / "marker.txt"
    if protected_dir.exists():
        shutil.rmtree(protected_dir)
    protected_dir.mkdir()
    protected_file.write_text("keep", encoding="utf-8")

    try:
        result = run_command("shared/scripts/package_skill.py", "../../package-skill-protected")
        assert result.returncode == 2
        assert "skill 名称只能包含" in result.stderr
        assert protected_file.exists()
    finally:
        if protected_dir.exists():
            shutil.rmtree(protected_dir)


def test_package_skill_rejects_symlinked_files(tmp_path: Path) -> None:
    skill_name = "symlink-skill"
    skill_dir = REPO_ROOT / "skills" / skill_name
    dist_dir = REPO_ROOT / "dist" / skill_name
    secret_path = tmp_path / "secret.txt"
    secret_path.write_text("secret", encoding="utf-8")

    if skill_dir.exists():
        shutil.rmtree(skill_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    try:
        skill_dir.mkdir()
        (skill_dir / "data.txt").write_text("public", encoding="utf-8")
        (skill_dir / "linked.txt").symlink_to(secret_path)

        result = run_command("shared/scripts/package_skill.py", skill_name)
        assert result.returncode == 1
        assert "符号链接" in result.stderr
        assert not dist_dir.exists()
    finally:
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)


def test_validate_rejects_symlinked_files(tmp_path: Path) -> None:
    link_path = REPO_ROOT / "skills" / "example-skill" / "linked.txt"
    secret_path = tmp_path / "secret.txt"
    secret_path.write_text("secret", encoding="utf-8")

    if link_path.exists() or link_path.is_symlink():
        link_path.unlink()

    try:
        link_path.symlink_to(secret_path)
        result = run_command("shared/scripts/validate_repo.py")
        assert result.returncode == 1
        assert "包含符号链接" in result.stderr
    finally:
        if link_path.exists() or link_path.is_symlink():
            link_path.unlink()


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
