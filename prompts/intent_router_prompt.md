# Intent Router Prompt

分析用户输入，识别属于哪些植保子领域。

## 支持领域

- `insect` — 虫害（害虫、幼虫、成虫、蛀茎、刺吸等）
- `disease` — 病害（病斑、霉层、腐烂、枯萎、病毒等）
- `weed` — 草害（杂草、禾草、阔叶草等）
- `pesticide` — 农药（药剂、登记、抗药性等）
- `pesticide_injury` — 药害（打药后出现异常、药斑等）
- `soil` — 土壤（板结、盐渍、酸化、根系问题等）
- `nutrition` — 营养缺素（缺氮、黄化、叶脉间失绿等）
- `comprehensive` — 综合（跨领域或不确定时）

## 输出 JSON

```json
{
  "task_type": "diagnosis | knowledge_query | control_advice | identification | unknown",
  "primary_domain": "主要领域",
  "secondary_domains": ["次要领域列表"],
  "all_domains": ["所有待调用的领域（primary + secondary）"],
  "route_confidence": 0.0,
  "need_multi_skill": false,
  "reason": "判断理由"
}
```

## 规则

- 不要只输出单个 domain。如果存在多种可能，应保留 secondary_domains
- 如果用户明确询问用药，应包含 pesticide
- 如果用户提到"打药后出现症状"，应包含 pesticide_injury
- 如果用户描述"发黄、缺绿、叶脉间黄化"，应考虑 nutrition
- 多意图时 need_multi_skill = true
