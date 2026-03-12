from __future__ import annotations

import argparse
import shutil
import sys

from shared.scripts.common import (
    DIST_DIR,
    SKILLS_DIR,
    ensure_within_directory,
    find_symlinks,
    validate_skill_name,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="将单个 Skill 打包到 dist 目录。")
    parser.add_argument("name", help="Skill 名称")
    args = parser.parse_args()

    try:
        skill_name = validate_skill_name(args.name)
        source_dir = ensure_within_directory(SKILLS_DIR, SKILLS_DIR / skill_name, "source path")
        target_dir = ensure_within_directory(DIST_DIR, DIST_DIR / skill_name, "target path")
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not source_dir.exists():
        print(f"Skill 不存在：{skill_name}", file=sys.stderr)
        return 1

    symlinks = find_symlinks(source_dir)
    if symlinks:
        print(f"Skill 包含符号链接，拒绝打包：{symlinks[0]}", file=sys.stderr)
        return 1

    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir)
    print(f"已打包到：{target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
