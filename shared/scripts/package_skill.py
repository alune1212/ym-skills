from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from shared.scripts.common import DIST_DIR, SKILLS_DIR


def main() -> int:
    parser = argparse.ArgumentParser(description="将单个 Skill 打包到 dist 目录。")
    parser.add_argument("name", help="Skill 名称")
    args = parser.parse_args()

    source_dir = SKILLS_DIR / args.name
    if not source_dir.exists():
        print(f"Skill 不存在：{args.name}", file=sys.stderr)
        return 1

    target_dir = DIST_DIR / args.name
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir)
    print(f"已打包到：{target_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

