# Data Directory

本目录存放农业昆虫 Skill 的结构化知识数据。当前为框架版本（0.1.0），所有数据文件均为空结构。

## 文件说明

### pest_ontology.json

害虫本体数据，每条记录描述一种农业害虫。数据结构由 `schemas/pest_ontology.schema.json` 定义。

字段包括但不限于：
- `pest_id` — 唯一标识符
- `name_cn` — 中文名
- `name_en` — 英文名
- `name_latin` — 拉丁学名
- `aliases` — 别名/俗称
- `taxonomy` — 分类信息（目、科、属）
- `major_hosts` — 主要寄主作物
- `damaging_stages` — 为害虫态
- `damaged_parts` — 为害部位
- `typical_symptoms` — 典型症状
- `diagnostic_features` — 鉴别特征
- `similar_pests` — 相似害虫列表
- `risk_level` — 风险等级
- `references` — 参考来源

当前为空数组 `[]`，等待后续知识注入。

### crop_pest_map.json

作物-害虫关联映射表。数据结构由 `schemas/crop_pest_map.schema.json` 定义。

字段包括但不限于：
- `crop` — 作物名称
- `region` — 适用地区
- `growth_stage` — 生育期
- `common_pests` — 常见害虫列表
- `notes` — 备注
- `references` — 参考来源

当前为空数组 `[]`。

### similar_pests.json

相似害虫鉴别表，用于区分外观或症状相似的害虫。数据结构由 `schemas/similar_pests.schema.json` 定义。

字段包括但不限于：
- `pest_id` — 害虫标识符
- `similar_to` — 与之相似的害虫标识符
- `distinguishing_points` — 区分要点
- `confidence_notes` — 置信度说明
- `references` — 参考来源

当前为空数组 `[]`。

### pest_cards/

单独害虫知识卡片目录。每个害虫可在此目录下存放独立的 JSON 或 Markdown 文件，便于按需加载。

当前仅包含 `.gitkeep` 占位文件，无实际内容。

## 注意事项

- 所有 JSON 数据需符合 `schemas/` 中对应 Schema 的定义。
- 添加真实数据前请确认数据来源的准确性和版权合规性。
- 建议使用 UTF-8 编码保存所有文件。
