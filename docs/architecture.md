# Architecture — 架构设计

## 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│              (CLI / API / Agent Platform)                │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              LangGraph 主图 (graph/)                     │
│                                                         │
│  Input Normalizer → Slot Extractor → Intent Router      │
│       │                                        │        │
│  Image Analyzer ← (有图)                  (无图) │         │
│       │                                        │        │
│       └──────── Sufficiency Checker ───────────┘        │
│                    │            │                        │
│           Follow-up (不足)  (充分) Domain Dispatcher     │
│                    │            │                        │
│                    │     ┌──────┼──────┐                │
│                    │     │  Skill 集合  │                │
│                    │     │ insect      │                │
│                    │     │ disease     │                │
│                    │     │ weed        │                │
│                    │     │ pesticide   │                │
│                    │     │ pesticide_  │                │
│                    │     │   injury    │                │
│                    │     │ soil        │                │
│                    │     │ nutrition   │                │
│                    │     │ comprehens- │                │
│                    │     │   ive        │                │
│                    │     └──────┬──────┘                │
│                    │            │                        │
│                    │  Comprehensive Reasoner             │
│                    │  Diagnostic Arbiter                 │
│                    │  Safety Guard                       │
│                    │  Answer Formatter                   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                     Output                               │
│              (结构化诊断报告 / 追问 / 安全提示)          │
└─────────────────────────────────────────────────────────┘
```

## 分层说明

### 1. 图编排层 (graph/)

- `state.py` — 全局共享状态对象（PlantProtectionState）
- `build_graph.py` — LangGraph 图编译
- `nodes/` — 11 个节点函数
- `edges/` — 条件路由函数

### 2. 子 Skill 层 (skills/)

- `base.py` — 统一输入输出协议（SkillOutput）
- 8 个子 Skill，每个独立运行，写回 State 对应字段

### 3. 工具层 (tools/)

- 视觉工具（VLM Client、图像质量评估）
- 检索工具（关键词/向量/混合检索）
- 数据库查询（本体、作物问题、农药登记）
- 安全工具（农药安全、风险表达检查）

### 4. 知识层 (knowledge/)

- 统一本体库（5 个领域）
- 知识卡片（按领域分目录）
- 来源登记

### 5. Prompt 层 (prompts/)

- LLM Prompt 模板（后续 LLM 模式使用）

## 核心设计原则

- **多意图并发**：Intent Router 输出 all_domains 列表，Domain Dispatcher 遍历调用
- **结构化结果**：Skill 不直接生成回答，只返回结构化 candidates
- **安全兜底**：所有输出必须经过 Safety Guard
- **逐步求精**：信息不足时不强行诊断，先追问
