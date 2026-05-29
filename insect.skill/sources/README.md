# Sources Directory

本目录用于登记和管理农业昆虫 Skill 的知识来源。

## 目录结构

```
sources/
├── README.md                # 本文件
├── source_registry.json     # 来源登记表
└── staging/                 # 暂存区（未核实的原始资料）
    └── .gitkeep
```

## 用途

### source_registry.json

记录所有可用于知识卡片构建的来源。每条记录包含：

- `source_id` — 唯一标识符（格式: SRC_NNNN）
- `title` — 资料标题
- `source_type` — 资料类型（official_guideline / textbook / paper / dataset / expert_note / website）
- `publisher` — 发布机构
- `url` — 网络链接（如有）
- `accessed_at` — 访问/获取日期
- `license` — 使用许可
- `reliability` — 可信度（high / medium / low / unknown）
- `notes` — 补充说明

Agent 在生成知识卡片时，只能引用已在 `source_registry.json` 中登记的来源。

### staging/

用于暂存未核实的原始资料摘录、待确认的来源信息等。

## 当前状态

- **已登记来源**: 0
- **暂存资料**: 0
- **不存放大型原始数据集** — 仅存储来源元信息和必要的摘录。完整的数据集（如 AP162 图像集、InsectAgent 知识库）应在外部管理。

## 不存放的内容

- 完整 PDF 文件
- 大型图像数据集
- 原始数据库 dump
- 网页完整抓取内容

## 添加来源的流程

1. 确认资料的许可和版权允许引用
2. 在 `source_registry.json` 中添加记录
3. 分配唯一的 `source_id`
4. 评估 `reliability` 等级（参见 `protocols/source_quality_policy.md`）
5. 记录访问日期和 URL
