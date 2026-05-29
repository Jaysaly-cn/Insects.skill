# Skill Protocol — 子 Skill 通信协议

## 统一接口

每个子 Skill 实现 `run(state: PlantProtectionState) -> dict`。

```python
def run_insect_skill(state: PlantProtectionState) -> dict:
    ...
    return output.to_dict()
```

## 统一输出格式

```json
{
  "domain": "insect | disease | weed | ...",
  "status": "completed | skipped | error",
  "candidates": [
    {
      "name": "候选对象名称",
      "type": "pest | disease | weed | nutrition | soil | pesticide_injury",
      "confidence": 0.0-1.0,
      "evidence": ["支持证据列表"],
      "against_evidence": ["不支持证据列表"],
      "need_more_info": true/false,
      "recommended_observations": ["建议补充观察"]
    }
  ],
  "retrieved_evidence": [
    {
      "source_id": "SRC_xxxx",
      "title": "来源标题",
      "snippet": "证据片段"
    }
  ],
  "risk_notes": ["风险提示"],
  "followup_questions": ["追问问题"]
}
```

## 规则

1. 每个 Skill 只输出结构化 candidates，不生成自然语言回答
2. 不输出具体农药剂量
3. 标注 confidence 和 need_more_info
4. 如果没有匹配，返回空 candidates
5. 如果领域不匹配，status = "skipped"
