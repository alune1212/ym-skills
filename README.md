# ym-skills

公司内部 Skill 的源码与发布仓库。

## 目标

- 统一管理 Skill 源码、评测、打包与发布元数据。
- 所有 Python 脚本统一通过 `uv` 管理和执行。
- 每个 Skill 独立维护文档、评测样例和私有脚本，但共享仓库级依赖与工具链。

## Python 与 `uv`

- 标准 Python 版本：`3.12`
- 安装运行时：`uv python install 3.12`
- 初始化环境：`uv sync`
- 执行仓库脚本：`uv run <command>`
- 新增依赖：`uv add <package>`
- 新增开发依赖：`uv add --dev <package>`

禁止直接使用裸 `python` 或 `pip` 维护仓库环境。

## 常用命令

```bash
uv sync
uv run new-skill demo-skill
uv run validate
uv run package-skill example-skill
uv run pytest
```

如果你更偏好 `make`，也可以使用：

```bash
make sync
make new-skill NAME=demo-skill
make validate
make test
make package NAME=example-skill
```

## 目录概览

```text
docs/           仓库规范、评审与发布文档
templates/      新 Skill 模板
skills/         Skill 源码目录
shared/         仓库级脚本、schema、提示模板
registry/       Skill 注册表与 owner 清单
tests/          冒烟测试与公共测试数据
dist/           打包产物目录（默认不提交产物）
```

## 新增一个 Skill

1. `uv sync`
2. `uv run new-skill <skill-name>`
3. 补充 `skills/<skill-name>/SKILL.md`、`README.md`、`evals/evals.json`
4. 在 `registry/index.yaml` 中确认元数据
5. 运行 `uv run validate`
6. 运行 `uv run package-skill <skill-name>`

## 仓库约束

- 仓库级 Python 工具放在 `shared/scripts/`
- Skill 私有脚本放在 `skills/<name>/scripts/`
- 所有依赖只在根目录 `pyproject.toml` 管理
- 每个 Skill 至少包含：
  - `SKILL.md`
  - `README.md`
  - `CHANGELOG.md`
  - `evals/evals.json`

