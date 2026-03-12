from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

from shared.scripts.common import (
    REGISTRY_PATH,
    REQUIRED_SKILL_FILES,
    SKILLS_DIR,
    find_symlinks,
    validate_skill_name,
)


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path} 缺少 frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError(f"{path} frontmatter 格式无效")
    data = yaml.safe_load(parts[1]) or {}
    return data


def validate_skill_dir(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    try:
        validate_skill_name(skill_dir.name)
    except ValueError as exc:
        errors.append(f"{skill_dir}: {exc}")

    symlinks = find_symlinks(skill_dir)
    for symlink in symlinks:
        errors.append(f"{skill_dir}: 包含符号链接 {symlink}")

    for relative in REQUIRED_SKILL_FILES:
        if not (skill_dir / relative).exists():
            errors.append(f"{skill_dir}: 缺少 {relative}")

    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        try:
            frontmatter = read_frontmatter(skill_md)
            for field in ("name", "description"):
                if not frontmatter.get(field):
                    errors.append(f"{skill_md}: frontmatter 缺少 {field}")
        except ValueError as exc:
            errors.append(str(exc))

    evals_path = skill_dir / "evals" / "evals.json"
    if evals_path.exists():
        try:
            data = json.loads(evals_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{evals_path}: JSON 无法解析: {exc}")
        else:
            if not data.get("skill_name"):
                errors.append(f"{evals_path}: 缺少 skill_name")
            evals = data.get("evals")
            if not isinstance(evals, list) or not evals:
                errors.append(f"{evals_path}: evals 必须是非空数组")

    return errors


def validate_registry(skill_dirs: list[Path]) -> list[str]:
    errors: list[str] = []
    if not REGISTRY_PATH.exists():
        return ["registry/index.yaml 不存在"]

    data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    skills = data.get("skills")
    if not isinstance(skills, list):
        return ["registry/index.yaml 中的 skills 必须是数组"]

    by_name = {item.get("name"): item for item in skills if isinstance(item, dict)}
    actual_names = {path.name for path in skill_dirs}

    for name in actual_names:
        item = by_name.get(name)
        if item is None:
            errors.append(f"registry/index.yaml: 缺少 {name} 的注册信息")
            continue
        expected_path = f"skills/{name}"
        if item.get("path") != expected_path:
            errors.append(f"registry/index.yaml: {name} 的 path 应为 {expected_path}")
        for field in ("version", "status", "owner", "description"):
            if not item.get(field):
                errors.append(f"registry/index.yaml: {name} 缺少 {field}")

    for name in by_name:
        if name not in actual_names:
            errors.append(f"registry/index.yaml: 存在未落地目录的 skill {name}")

    return errors


def main() -> int:
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    errors: list[str] = []
    for skill_dir in skill_dirs:
        errors.extend(validate_skill_dir(skill_dir))
    errors.extend(validate_registry(skill_dirs))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("仓库校验通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
