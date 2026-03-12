# Security Best Practices Report

## Executive Summary

本次审查对象是一个以 Python 3.12 CLI 脚本为主的 Skill 仓库。仓库不包含 Web 服务框架，因此未命中 `security-best-practices` 技能 references 中的 Django/Flask/FastAPI 专项文档；以下结论基于 Python 文件系统工具的通用安全最佳实践。

本次审查确认了 2 个需要优先处理的问题：

- 1 个高危问题：打包脚本未校验 `skill name`，可被路径穿越利用为仓库外目录删除/覆盖原语。
- 1 个中危问题：打包流程会跟随符号链接复制文件，可能把打包机本地敏感文件带入发布产物。

当前 `uv run validate` 与 `uv run pytest` 均通过，但现有校验与测试没有覆盖恶意输入、路径逃逸或符号链接场景。

## High

### SBP-001: `package-skill` 存在路径穿越，可删除或覆盖 `dist/` 之外的目录

- 位置：
  - `shared/scripts/package_skill.py:16`
  - `shared/scripts/package_skill.py:21-24`
- 影响：攻击者只要控制 `uv run package-skill <name>` 中的 `name`，就能把目标路径逃逸到 `dist/` 之外，并触发 `shutil.rmtree()` 删除或 `shutil.copytree()` 覆盖仓库外目录。
- 细节：
  - `args.name` 没有经过与 `new_skill.py` 同等的名称校验。
  - `source_dir = SKILLS_DIR / args.name` 与 `target_dir = DIST_DIR / args.name` 都直接拼接用户输入。
  - 传入 `../../some-dir` 这类值时，`target_dir` 会落到 `dist/` 外部；若该路径存在，`shutil.rmtree(target_dir)` 会先删除它。
  - 这类问题在本仓库里风险较高，因为发布流程文档明确要求直接运行 `uv run package-skill <skill-name>`。
- 建议修复：
  - 复用 `new_skill.py` 的 `validate_skill_name()` 规则，只允许 `[a-z0-9][a-z0-9-]*`。
  - 在删除或复制前，对 `source_dir.resolve()` 和 `target_dir.resolve()` 做边界校验，确保它们分别位于 `SKILLS_DIR` 与 `DIST_DIR` 内。
  - 对异常路径直接失败，不做任何删除操作。

## Medium

### SBP-002: 打包时默认跟随符号链接，可能把本地敏感文件打进产物

- 位置：
  - `shared/scripts/package_skill.py:24`
- 影响：如果某个 Skill 目录内包含指向仓库外文件的符号链接，打包机会把链接目标内容复制进 `dist/<skill-name>/`，从而泄露打包机本地敏感文件。
- 细节：
  - `shutil.copytree(source_dir, target_dir)` 默认 `symlinks=False`，会解引用符号链接并复制其目标内容。
  - 这意味着一个被提交的恶意符号链接，或一个本地临时加入的符号链接，都可能在打包时被静默打包。
  - 当前仓库扫描未发现 `skills/` 下已有符号链接，但脚本本身没有任何拒绝或告警逻辑。
- 建议修复：
  - 在打包前显式扫描 `source_dir`，拒绝任何符号链接，或至少拒绝解析后落在 `source_dir` 之外的链接。
  - 将该校验加入 `validate_repo.py` 与测试用例，避免问题只在发布阶段暴露。

## Testing Gaps

- `tests/smoke/test_repo.py` 只覆盖正常输入，没有覆盖以下安全边界：
  - `package-skill ../../outside`
  - `skills/<name>` 内含符号链接
  - 删除目标目录前的路径归属校验

## Recommended Next Steps

1. 先修复 `shared/scripts/package_skill.py` 的名称校验和路径边界检查，消除高危删除/覆盖风险。
2. 再补充符号链接拒绝逻辑，并把恶意输入样例加入 `tests/smoke/test_repo.py`。
3. 如需，我可以按上述顺序直接提交修复。
