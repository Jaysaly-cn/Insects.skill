# Slot Extraction Prompt

从用户输入中抽取植保诊断所需的槽位信息。

## 必须抽取的槽位

| 槽位 | 说明 | 示例 |
|------|------|------|
| crop | 作物名称 | 水稻、番茄、柑橘 |
| region | 地区 | 浙江、湖南、长江中下游 |
| season | 季节/月份 | 春季、6月 |
| growth_stage | 生育期 | 苗期、分蘖期、开花期 |
| damaged_parts | 受害部位列表 | ["leaf", "stem"] |
| symptoms | 症状列表 | ["叶片发黄", "枯萎"] |
| pest_seen | 是否看到虫体 | true/false |
| insect_stage | 虫态 | larva、adult |
| insect_morphology | 虫体形态描述 | ["小型", "白色", "有翅"] |
| pesticide_history | 用药史 | text |
| fertilization_history | 施肥史 | text |
| irrigation_history | 灌溉史 | text |
| soil_condition | 土壤状况 | text |
| field_distribution | 田间分布 | sporadic/patchy/uniform |

## 输出 JSON

```json
{
  "crop": "",
  "region": "",
  "season": "",
  "growth_stage": "",
  "damaged_parts": [],
  "symptoms": [],
  "pest_seen": false,
  "insect_stage": "",
  "insect_morphology": [],
  "pesticide_history": "",
  "fertilization_history": "",
  "irrigation_history": "",
  "soil_condition": "",
  "field_distribution": ""
}
```
