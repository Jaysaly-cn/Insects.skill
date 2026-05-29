#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
create_pest_card_stub.py — Generate a blank draft pest knowledge card.

Usage:
    python scripts/create_pest_card_stub.py --pest-id <id> --name-cn <name> [--name-latin <latin>]

The script generates a draft card from the standard template
(templates/pest_card.md) and writes it to:
    data/staging/pest_cards/<pest_id>.draft.md

No real pest knowledge is injected — only user-supplied identifiers
and placeholder sections are written.
"""

import argparse
import os
import sys
from datetime import datetime


TEMPLATE_CONTENT = """---
pest_id: "{pest_id}"
card_version: "0.1.0"
status: "draft"
updated_at: "{updated_at}"
reviewed_by: ""

names:
  name_cn: "{name_cn}"
  name_en: ""
  name_latin: "{name_latin}"
  aliases: []

taxonomy:
  order: ""
  family: ""
  genus: ""
  species: ""

hosts:
  major_hosts: []
  occasional_hosts: []

damage:
  damaging_stages: []
  damaged_parts: []
  typical_symptoms: []

diagnosis:
  diagnostic_features: []
  similar_pests: []

occurrence:
  regions: []
  seasons: []
  notes: ""

risk:
  risk_level: "unknown"
  quarantine_status: "unknown"

source_quality:
  citation_required: true
  source_count: 0
  confidence: "unreviewed"
---

# {name_cn}

> **卡片状态**: draft
> **最后更新**: {updated_at}
> **审核人**: 待指定

---

## 1. 基本信息

| 字段 | 内容 |
|------|------|
| 中文名 | {name_cn} |
| 英文名 | 待补充 |
| 拉丁学名 | {name_latin} |
| 分类地位 | 待补充（目 / 科 / 属） |
| 主要寄主 | 待补充 |
| 偶发寄主 | 待补充 |
| 主要危害虫态 | 待补充 |

---

## 2. 形态识别特征

### 2.1 卵

待补充。

### 2.2 幼虫 / 若虫

待补充。

### 2.3 蛹

待补充（不适用则注明）。

### 2.4 成虫

待补充。

---

## 3. 危害症状

| 危害部位 | 症状描述 | 典型田间表现 |
|----------|----------|-------------|
| 待补充 | 待补充 | 待补充 |

---

## 4. 发生规律

- **发生世代**: 待补充
- **越冬虫态与场所**: 待补充
- **发生盛期**: 待补充
- **影响因素**: 待补充

---

## 5. 诊断要点

识别该害虫的关键特征：

1. 待补充
2. 待补充
3. 待补充

> 诊断置信度提示：当前来源不足，需进一步确认。

---

## 6. 相似害虫鉴别

| 相似害虫 | 相似点 | 区别点 | 需补充观察 |
|----------|--------|--------|-----------|
| 待补充 | 待补充 | 待补充 | 待补充 |

---

## 7. 田间调查建议

1. 待补充
2. 待补充
3. 待补充

---

## 8. 综合防控原则

> 以下为通用原则，非针对本害虫的专用方案。

- **农业防治**: 待补充
- **物理防治**: 待补充
- **生物防治**: 待补充
- **化学防治（应急）**: 待补充。仅在达到防治指标且其他措施不足时考虑。

> **用药安全提示**: 具体农药选择和使用剂量须严格遵循产品标签及当地植保部门指导。不推荐禁限用农药。

---

## 9. 不确定性与注意事项

- 当前卡片状态为 draft，未经专家审核。
- 以下字段缺乏足够来源支持：待补充。
- 以下字段可能存在争议：待补充。
- 若田间症状与本文描述不符，建议咨询当地植保技术人员。

---

## 10. 参考来源

| 编号 | 来源类型 | 标题/描述 | 可靠性 | 备注 |
|------|----------|----------|--------|------|
| [R1] | 待补充 | 待补充 | 待补充 | 待补充 |

---

*本卡片由 create_pest_card_stub.py 自动生成。*
*本卡片遵循 `insect.skill` 知识卡片构建标准。*
*审核流程: draft → reviewed → 进入正式 pest_cards/。*
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate a blank draft pest knowledge card."
    )
    parser.add_argument(
        "--pest-id",
        required=True,
        help="Unique pest identifier (e.g. genus_species)."
    )
    parser.add_argument(
        "--name-cn",
        required=True,
        help="Chinese common name of the pest."
    )
    parser.add_argument(
        "--name-latin",
        default="",
        help="Latin scientific name (Genus species Author, Year)."
    )
    args = parser.parse_args()

    pest_id = args.pest_id.strip()
    name_cn = args.name_cn.strip()
    name_latin = args.name_latin.strip()

    if not pest_id:
        print("Error: --pest-id must not be empty.", file=sys.stderr)
        sys.exit(1)
    if not name_cn:
        print("Error: --name-cn must not be empty.", file=sys.stderr)
        sys.exit(1)

    # Determine output path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(
        script_dir, "..", "data", "staging", "pest_cards"
    )
    output_dir = os.path.normpath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{pest_id}.draft.md")
    output_path = os.path.normpath(output_path)

    if os.path.exists(output_path):
        print(f"Warning: File already exists: {output_path}")
        print("Remove or rename the existing file before regenerating.")
        sys.exit(1)

    updated_at = datetime.now().strftime("%Y-%m-%d")
    content = TEMPLATE_CONTENT.format(
        pest_id=pest_id,
        name_cn=name_cn,
        name_latin=name_latin if name_latin else "待补充",
        updated_at=updated_at,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Draft card generated: {output_path}")
    print(f"  pest_id:   {pest_id}")
    print(f"  name_cn:   {name_cn}")
    print(f"  name_latin: {name_latin if name_latin else '(not provided)'}")
    print(f"  status:    draft")
    print(f"  date:      {updated_at}")


if __name__ == "__main__":
    main()
