from __future__ import annotations

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

