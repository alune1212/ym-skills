# 评审检查清单

提交或评审 Skill 变更时，至少检查以下内容：

- 目录结构是否符合模板要求
- `SKILL.md` frontmatter 是否完整
- `README.md` 是否解释清楚触发条件和边界
- `CHANGELOG.md` 是否记录版本变化
- `evals/evals.json` 是否存在且可解析
- `registry/index.yaml` 是否与目录和版本保持一致
- `uv run validate` 是否通过
- `uv run pytest` 是否通过

