# Skill 编写指南

## 新建流程

1. 运行 `uv run new-skill <skill-name>`
2. 完成 `SKILL.md` frontmatter
3. 在 `README.md` 中写清楚用途、边界与示例
4. 在 `evals/evals.json` 中补充至少 2 个真实样例
5. 更新 `CHANGELOG.md`
6. 运行 `uv run validate`

## `SKILL.md` 最低要求

- `name`
- `description`
- 明确触发条件
- 明确输入/输出
- 明确限制或风险点

## 脚本放置规则

- 通用脚本放 `shared/scripts/`
- 仅某个 Skill 使用的辅助脚本放 `skills/<name>/scripts/`
- 不在 Skill 目录内定义单独依赖

## 评测要求

每个 Skill 的 `evals/evals.json` 至少包含：

- `skill_name`
- 至少一个 `evals` 数组项
- 每个样例包含 `id`、`prompt`、`expected_output`、`files`

