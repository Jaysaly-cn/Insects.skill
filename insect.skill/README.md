# Agricultural Insect Skill — README

## 概述

`insect.skill` 是一个面向农业昆虫领域的轻量 Skill 包，旨在为通用 AI Agent（如 Codex、Claude Code、Claude、DeepSeek Agent 等）提供专业、稳健、可扩展的害虫诊断与综合防控建议工作流程。

## 当前版本状态

- **Version**: 0.1.0
- **Status**: framework-only
- **数据内容**: 本版本**不包含真实害虫知识库**。所有数据文件均为空结构或占位文件。
- **适用场景**: 框架搭建、流程验证、模板测试、知识注入前的架构准备。

## 目录结构

```
insect.skill/
├── SKILL.md                  # Skill 入口文件（YAML frontmatter + 正文）
├── README.md                 # 本文件
├── VERSION                   # 版本号
├── manifest.json             # Skill 元信息清单
├── data/                     # 数据目录
│   ├── README.md             # 数据目录说明
│   ├── pest_ontology.json    # 害虫本体数据（当前为空数组）
│   ├── crop_pest_map.json    # 作物-害虫映射（当前为空数组）
│   ├── similar_pests.json    # 相似害虫鉴别表（当前为空数组）
│   └── pest_cards/           # 单个害虫知识卡片目录（空）
├── schemas/                  # JSON Schema 定义
│   ├── pest_ontology.schema.json
│   ├── crop_pest_map.schema.json
│   └── similar_pests.schema.json
├── protocols/                # 工作流程与策略文档
│   ├── diagnosis_workflow.md
│   ├── image_observation_checklist.md
│   ├── uncertainty_policy.md
│   └── pesticide_safety_policy.md
├── templates/                # 回答模板
│   ├── diagnosis_answer.md
│   ├── followup_questions.md
│   └── expert_report.md
├── scripts/                  # 工具脚本
│   ├── search_pest.py
│   └── normalize_pest_name.py
└── tests/                    # 测试目录
    └── README.md
```

## 后续知识注入方案

当框架验证通过后，可通过以下方式注入真实知识：

### 方案 A：结构化数据导入

向 `data/` 目录填充符合 `schemas/` 定义的结构化 JSON 数据：

- 将害虫本体条目写入 `pest_ontology.json`
- 将作物-害虫关联写入 `crop_pest_map.json`
- 将相似害虫鉴别规则写入 `similar_pests.json`
- 在 `pest_cards/` 下为每个害虫创建独立 JSON/Markdown 卡片

### 方案 B：接入外部知识源

- **AP162 label map** — 作为字段映射基础，通过脚本转换为 pest_ontology 条目
- **InsectAgent 摘要知识** — 结构化导入或作为 RAG 检索源
- **官方病虫害资料** — 中国农业农村部、各省植保站发布的病虫害图谱与防治建议
- **RAG 检索** — 将知识卡片向量化，支持语义检索

### 方案 C：社区贡献

按照 `schemas/` 定义和 `templates/` 规范，任何人都可以贡献新的害虫知识卡片或鉴别规则。

## 约束与排除

- 不爬取网站
- 不导入 AP162、InsectAgent 或任何大型数据集（当前框架阶段）
- 不创建真实害虫知识内容
- 所有文件使用 UTF-8 编码
- 工程保持轻量，不引入 Python 之外的复杂依赖

## 面向的 Agent 平台

- DeepSeek Agent
- Codex (OpenAI)
- Claude Code / Claude (Anthropic)
- 其他支持 Skill 机制或自定义指令的 AI Agent 平台
