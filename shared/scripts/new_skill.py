from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

from shared.scripts.common import REGISTRY_PATH, SKILLS_DIR, TEMPLATE_DIR, validate_skill_name


def replace_placeholders(base_dir: Path, skill_name: str) -> None:
    for path in base_dir.rglob("*"):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        path.write_text(text.replace("{{SKILL_NAME}}", skill_name), encoding="utf-8")


def update_registry(skill_name: str) -> None:
    if REGISTRY_PATH.exists():
        data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    else:
        data = {"skills": []}

    skills = data.setdefault("skills", [])
    if any(item["name"] == skill_name for item in skills):
        return

    skills.append(
        {
            "name": skill_name,
            "version": "0.1.0",
            "status": "draft",
            "owner": "unassigned",
            "tags": [],
            "path": f"skills/{skill_name}",
            "description": f"{skill_name} 的说明待补充。",
        }
    )
    skills.sort(key=lambda item: item["name"])
    REGISTRY_PATH.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="从模板创建一个新的 Skill。")
    parser.add_argument("name", help="Skill 名称，例如 demo-skill")
    args = parser.parse_args()

    try:
        skill_name = validate_skill_name(args.name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    target_dir = SKILLS_DIR / skill_name
    if target_dir.exists():
        print(f"Skill 已存在：{target_dir}", file=sys.stderr)
        return 1

    shutil.copytree(TEMPLATE_DIR, target_dir)
    replace_placeholders(target_dir, skill_name)
    changelog = target_dir / "CHANGELOG.md"
    changelog.write_text("# Changelog\n\n## 0.1.0\n\n- 初始化 Skill\n", encoding="utf-8")
    update_registry(skill_name)
    print(f"已创建 Skill：{target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
