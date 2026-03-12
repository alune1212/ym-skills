# 仓库结构设计

## 设计目标

- 支持多个内部 Skill 在同一仓库协作开发
- 统一脚手架、校验、评测与发布流程
- 降低目录漂移和环境漂移

## 顶层目录

- `docs/`：仓库规范与流程文档
- `templates/`：新 Skill 模板
- `skills/`：Skill 源码
- `shared/`：仓库级脚本、schema 与共享资源
- `registry/`：Skill 注册表和 owner 数据
- `tests/`：仓库级测试
- `dist/`：构建产物

## Python 运行时

- Python 版本固定为 `3.12`
- 依赖统一由根目录 `pyproject.toml` 与 `uv.lock` 管理
- 所有脚本通过 `uv run` 执行

## Skill 组织方式

每个 Skill 必须有独立目录，且包含：

- `SKILL.md`
- `README.md`
- `CHANGELOG.md`
- `evals/evals.json`
- `scripts/`
- `references/`
- `assets/`

## 注册表

`registry/index.yaml` 是仓库的单一事实来源，记录：

- `name`
- `version`
- `status`
- `owner`
- `tags`
- `path`
- `description`

