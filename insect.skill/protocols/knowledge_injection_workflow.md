# Knowledge Injection Workflow

本文档定义从原始资料到正式知识卡片的标准化注入流程。

## 流程概览

```
[资料来源收集]
      │
      ▼
[来源登记] ──────────────→ sources/source_registry.json
      │
      ▼
[事实抽取] ──────────────→ data/staging/fact_extracts/{pest_id}.facts.json
      │
      ▼
[实体规范化] ────────────→ protocols/entity_normalization_policy.md
      │
      ▼
[生成 draft 知识卡] ────→ data/staging/pest_cards/{pest_id}.draft.md
      │
      ▼
[自动校验] ──────────────→ scripts/validate_pest_card.py
      │
      ▼
[人工/专家审核]
      │
      ▼
[进入正式知识库] ────────→ data/pest_cards/{pest_id}.md
```

## 阶段 1: 来源登记

### 1.1 收集资料

可接受的资料类型：

- **official_guideline** — 官方植保资料（农业农村部、各省植保站发布的病虫害防治指南、检疫公告）
- **textbook** — 正式出版的教材、专著
- **paper** — 经同行评审的学术论文
- **dataset** — 已发布的结构化数据集
- **expert_note** — 经专家确认的笔记或鉴定记录
- **website** — 权威机构网站资料（如 FAO、CABI、中国农业科学院）

### 1.2 登记来源

每个来源在 `sources/source_registry.json` 中登记一条记录：

```json
{
  "source_id": "SRC_0001",
  "title": "",
  "source_type": "official_guideline",
  "publisher": "",
  "url": "",
  "accessed_at": "YYYY-MM-DD",
  "license": "",
  "reliability": "high",
  "notes": ""
}
```

**reliability 分级**详见 `protocols/source_quality_policy.md`。

### 1.3 未登记来源不得使用

Agent 在生成知识卡片时，只能引用已在 `source_registry.json` 中登记的来源。如需使用新来源，须先登记。

## 阶段 2: 事实抽取

### 2.1 抽取原则

- 逐字段抽取，不做自由概括
- 每个事实标注来源编号和原文/摘要证据
- 标注抽取置信度
- 不同来源冲突时记录冲突

### 2.2 抽取格式

输出文件: `data/staging/fact_extracts/{pest_id}.facts.json`

```json
{
  "pest_id": "genus_species",
  "extracted_at": "YYYY-MM-DD",
  "extracted_by": "agent",
  "facts": [
    {
      "field": "name_cn",
      "claim": "",
      "source_id": "SRC_0001",
      "evidence": "",
      "confidence": "medium",
      "notes": ""
    }
  ]
}
```

### 2.3 字段覆盖检查

抽取完成后，对照 `templates/pest_card.md` 检查必填字段是否有来源支持。未覆盖字段在知识卡片中标注「待补充」。

## 阶段 3: 实体规范化

### 3.1 确定 pest_id

按照 `protocols/entity_normalization_policy.md` 的规则，为害虫分配统一的 `pest_id`。

### 3.2 名称规范

- 中文名：以官方资料或权威教材为准
- 英文名：以 CABI、FAO 等国际资料为准
- 拉丁名：严格遵循二名法，含命名人和年份
- 别名：收集常见俗名、历史名称、数据集标签名

### 3.3 映射登记

如涉及 AP162 label、InsectAgent label 等外部标识符，在 `aliases` 中记录，格式如：

```
"aliases": ["ap162:xxxx", "insectagent:yyyy"]
```

## 阶段 4: 生成 draft 知识卡

### 4.1 使用模板

使用 `templates/pest_card.md` 作为模板，将事实抽取结果填入。

### 4.2 生成工具

可使用 `scripts/create_pest_card_stub.py` 生成空白卡片骨架，然后手动或由 Agent 填入内容。

### 4.3 输出位置

draft 卡片统一输出到 `data/staging/pest_cards/{pest_id}.draft.md`。

### 4.4 YAML frontmatter 要求

- `status` 必须为 `draft`
- `source_quality.confidence` 如实填写
- `source_quality.source_count` 填写实际引用的来源数量
- `reviewed_by` 留空

## 阶段 5: 自动校验

### 5.1 运行校验脚本

```bash
python scripts/validate_pest_card.py data/staging/pest_cards/{pest_id}.draft.md
```

### 5.2 校验项目

详见 `scripts/validate_pest_card.py`，包括：

1. YAML frontmatter 存在性
2. pest_id 非空
3. status 合法值
4. 必要章节完整性
5. 风险表达检测
6. 疑似剂量表达检测

### 5.3 校验不通过处理

- 标注 error 的项目必须修正
- 标注 warning 的项目建议修正或补充说明

## 阶段 6: 人工/专家审核

### 6.1 审核要点

- 每条关键事实是否有来源支持
- 是否存在过度推断
- 相似害虫鉴别是否准确
- 防控建议是否安全合规
- 不确定性是否充分说明

### 6.2 审核后操作

- 通过 → 更新 `status: reviewed`，填写 `reviewed_by`
- 需修改 → 返回修改，保持 `status: draft`
- 不可用 → 标记 `status: deprecated`

## 阶段 7: 进入正式知识库

审核通过的卡片从 `data/staging/pest_cards/` 移动到 `data/pest_cards/`。

同时更新 `data/pest_ontology.json`、`data/crop_pest_map.json`、`data/similar_pests.json` 等索引文件。

## 当前状态

- 框架已就绪
- 无已登记来源
- 无已抽取事实
- 无 draft 卡片
- 无正式卡片
