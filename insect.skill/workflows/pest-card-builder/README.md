# Pest Card Builder — 使用说明

`pest-card-builder` 是 `insect.skill` 的子工作流 Skill，用于将外部知识源文件自动转化为标准化害虫知识卡片。

## 触发方式

在 DeepSeek TUI 或其他支持 Skill 机制的 Agent 中，提供源文件并说明目标：

```
用 pest-card-builder 处理这篇论文，目标害虫是玉米螟
```

或直接粘贴源文件内容：

```
用 pest-card-builder 根据以下资料生成知识卡片：

[粘贴的文本内容]
```

如果源文件在工作区内：

```
用 pest-card-builder 处理 insect.skill/sources/staging/paper_2024.pdf
```

## 流水线阶段

| 阶段 | 说明 | 自动化 |
|------|------|--------|
| Stage 1 — 来源登记 | 提取源文件元信息，分配 source_id | 自动 |
| Stage 2 — 事实抽取 | 逐字段从源文件中抽取结构化事实 | 自动 |
| Stage 3 — 实体规范化 | 确定 pest_id，规范中/英/拉丁名 | 自动 |
| Stage 4 — 生成草稿 | 运行 create_pest_card_stub.py 并填入内容 | 自动 |
| Stage 5 — 自动校验 | 运行 validate_pest_card.py 检查 | 自动 |
| **Stage 6 — 审核** | **列出卡片摘要和待审核项，等待确认** | **暂停** |
| Stage 7 — 入库 | 移动卡片到正式目录，更新索引 | 手动确认后 |

## 依赖资源

此 Skill 依赖 `insect.skill` 内的以下文件：

- `protocols/source_quality_policy.md` — 来源可信度分级
- `protocols/entity_normalization_policy.md` — 实体命名规范
- `protocols/pesticide_safety_policy.md` — 农药安全策略
- `templates/pest_card.md` — 卡片模板
- `scripts/create_pest_card_stub.py` — 骨架生成
- `scripts/validate_pest_card.py` — 卡片校验
- `schemas/pest_ontology.schema.json` — 本体 Schema

## 输出文件

| 文件 | 位置 |
|------|------|
| 来源登记 | `sources/source_registry.json` |
| 事实抽取 | `data/staging/fact_extracts/{pest_id}.facts.json` |
| 草稿卡片 | `data/staging/pest_cards/{pest_id}.draft.md` |
| 正式卡片（审核后） | `data/pest_cards/{pest_id}.md` |

## 当前状态

- 框架已就绪
- 等待用户提供第一批源文件进行端到端测试
