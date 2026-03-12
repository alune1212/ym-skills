# 仓库协作说明

始终使用简体中文。

## 仓库定位

这个仓库用于公司内部 Skill 的创建、维护、评测与分发。

## 基本规则

- 所有 Python 工具链统一使用 `uv`
- 统一 Python 版本为 `3.12`
- 所有依赖统一在根目录 `pyproject.toml` 管理
- 不允许在各个 Skill 目录中单独维护虚拟环境或额外依赖清单

## Skill 目录要求

每个 Skill 目录至少包含：

- `SKILL.md`
- `README.md`
- `CHANGELOG.md`
- `evals/evals.json`
- `scripts/`
- `references/`
- `assets/`

## 提交流程

在提交前至少完成：

1. `uv run validate`
2. `uv run pytest`
3. 如涉及发布，运行 `uv run package-skill <skill-name>`

## 文档约定

- `SKILL.md` 负责定义触发条件、工作流与输出要求
- `README.md` 负责面向维护者说明设计目标、限制与示例
- `CHANGELOG.md` 记录版本变化

