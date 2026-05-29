# Knowledge Base — 统一知识库

本目录集中管理 Plant Protection Agent 所有领域的结构化知识和参考来源。

## 目录结构

```
knowledge/
├── README.md                       # 本文件
├── ontology/                       # 统一实体本体（JSON）
│   ├── pest_ontology.json          #   害虫本体（桥接 insect.skill）
│   ├── disease_ontology.json       #   病害本体（空骨架）
│   ├── weed_ontology.json          #   草害本体（空骨架）
│   ├── nutrition_ontology.json     #   营养缺素本体（空骨架）
│   └── pesticide_ontology.json     #   农药本体（空骨架）
├── cards/                          # 知识卡片目录
│   ├── pest_cards/                 #   害虫知识卡片
│   ├── disease_cards/              #   病害知识卡片
│   ├── weed_cards/                 #   草害知识卡片
│   ├── nutrition_cards/            #   营养知识卡片
│   └── pesticide_cards/            #   农药知识卡片
└── sources/                        # 来源登记
    ├── source_registry.json        #   来源登记表
    └── staging/                    #   未核实的暂存资料

## 数据来源

- `insect.skill/data/pest_ontology.json` — 现有害虫本体（4 条记录）
- `insect.skill/data/pest_cards/` — 现有害虫知识卡片（4 张 reviewed）
- `insect.skill/sources/source_registry.json` — 现有来源登记（2 个来源）

### 引入方式

```python
# 通过 skills/insect/tools.py 的桥接函数访问现有 insect.skill 数据
from skills.insect.tools import load_pest_ontology, query_pest_card
```

### 后续扩展

各领域的 ontology 和卡片可逐步填充：
1. 添加病害本体（水稻稻瘟病、纹枯病、白叶枯病等）
2. 添加草害本体（稗草、千金子、牛筋草等）
3. 添加营养缺素数据
4. 添加农药登记信息
