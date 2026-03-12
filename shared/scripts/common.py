from __future__ import annotations

import os
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO_ROOT / "skills"
TEMPLATE_DIR = REPO_ROOT / "templates" / "skill"
REGISTRY_PATH = REPO_ROOT / "registry" / "index.yaml"
OWNERS_PATH = REPO_ROOT / "registry" / "owners.yaml"
DIST_DIR = REPO_ROOT / "dist"

REQUIRED_SKILL_FILES = [
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "evals/evals.json",
]

SKILL_NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]*")


def validate_skill_name(name: str) -> str:
    if not SKILL_NAME_PATTERN.fullmatch(name):
        raise ValueError("skill 名称只能包含小写字母、数字和连字符，且必须以字母或数字开头。")
    return name


def ensure_within_directory(base_dir: Path, candidate: Path, label: str) -> Path:
    base_resolved = base_dir.resolve(strict=False)
    candidate_resolved = candidate.resolve(strict=False)
    try:
        candidate_resolved.relative_to(base_resolved)
    except ValueError as exc:
        raise ValueError(f"{label} 超出允许目录：{candidate}") from exc
    return candidate_resolved


def find_symlinks(base_dir: Path) -> list[Path]:
    if not base_dir.exists():
        return []
    if base_dir.is_symlink():
        return [base_dir]

    symlinks: list[Path] = []
    for root, dirnames, filenames in os.walk(base_dir, followlinks=False):
        root_path = Path(root)
        for name in [*dirnames, *filenames]:
            path = root_path / name
            if path.is_symlink():
                symlinks.append(path)

    return sorted(symlinks)
