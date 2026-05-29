# Plant Protection Agent / 植保智能体

基于 **LangGraph** 的多模态、多 Skill、可追问、可仲裁、可安全约束的植保专业智能体。

## 核心能力

| 能力 | 说明 |
|------|------|
| **多意图并发** | 同时识别虫害、病害、药害、营养等多种可能，不等单一路由 |
| **多路由分发** | 同时调用多个子 Skill 进行分析，独立返回候选结果 |
| **综合诊断仲裁** | 汇总多 Skill 结果，交叉比对证据，输出主因+次因+待排除项 |
| **信息充分性检查** | 信息不足时主动追问，不强行诊断 |
| **安全合规检查** | 每轮输出前必须经过 Safety Guard，杜绝禁限用药/无源剂量 |
| **可扩展 Skill 体系** | 8 个子 Skill 遵循统一输入输出协议，可独立开发 |

## 子 Skill 一览

| Skill | 领域 | 说明 |
|-------|------|------|
| Insect | 🐛 虫害 | 害虫识别、形态鉴别、IPM 建议 |
| Disease | 🍂 病害 | 真菌/细菌/病毒/生理性病害 |
| Weed | 🌿 草害 | 杂草识别与防除 |
| Pesticide | 🧪 农药 | 农药知识、作用机制、登记查询 |
| Pesticide Injury | ⚠️ 药害 | 药害判断与排除 |
| Soil | 🪨 土壤 | 板结/盐渍化/酸碱度/根系环境 |
| Nutrition | 🌱 营养 | 缺素诊断（N/P/K/Mg/Fe 等） |
| Comprehensive | 🔗 综合 | 跨领域多因素综合分析 |

## 项目结构

```
├── README.md                    # 本文件
├── pyproject.toml               # 项目配置
├── requirements.txt             # 依赖
├── .env.example                 # 环境变量示例
├── app/                         # 应用入口与 API
├── graph/                       # LangGraph 主图
│   ├── state.py                 # 全局 State（50+ 字段）
│   ├── build_graph.py           # 图编译
│   ├── nodes/                   # 11 个节点函数
│   └── edges/                   # 条件路由
├── skills/                      # 子 Skill 集合
│   ├── base.py                  # SkillBase 抽象
│   ├── insect/                  # 🐛 虫害 Skill
│   ├── disease/                 # 🍂 病害 Skill
│   ├── weed/                    # 🌿 草害 Skill
│   ├── pesticide/               # 🧪 农药 Skill
│   ├── pesticide_injury/        # ⚠️ 药害 Skill
│   ├── soil/                    # 🪨 土壤 Skill
│   ├── nutrition/               # 🌱 营养 Skill
│   └── comprehensive/           # 🔗 综合 Skill
├── tools/                       # 工具层
│   ├── vision/                  # 视觉/多模态
│   ├── retrieval/               # 知识检索
│   ├── database/                # 数据库查询
│   └── safety/                  # 安全检查
├── knowledge/                   # 统一知识库
│   ├── ontology/                # 5 个领域本体
│   ├── cards/                   # 知识卡片目录
│   └── sources/                 # 来源登记
├── prompts/                     # LLM Prompt 模板
├── tests/                       # 测试用例与评测
└── docs/                        # 架构文档
```

## 工作流概览

```
[用户输入] → Input Normalizer → Slot Extractor → Intent Router
    ↓                                                      ↓
[图片分析] ← (有图)                                   (无图)
    ↓                                                      ↓
Information Sufficiency Checker → 不足 → Follow-up Generator → END
    ↓ 充分
Domain Dispatcher → (并发调用多个 Skill)
    ↓
Comprehensive Reasoner → Diagnostic Arbiter → Safety Guard → Answer Formatter → 输出
```

## 当前阶段

**MVP 0 — 文本诊断工作流**：工程骨架已搭建，节点使用 Mock 逻辑，可跑通主链路。

详见 `docs/` 目录下的架构设计文档。
