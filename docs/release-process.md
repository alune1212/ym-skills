# 发布流程

## 原则

- 按 Skill 独立发布
- 发布元数据以 `registry/index.yaml` 为准
- 打包产物输出到 `dist/`

## 步骤

1. 确认 Skill 文档、评测、变更记录已更新
2. 运行 `uv run validate`
3. 运行 `uv run package-skill <skill-name>`
4. 检查 `dist/<skill-name>/` 内容
5. 按内部流程分发或上传产物

