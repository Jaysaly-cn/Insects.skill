# Comprehensive Reasoning Prompt

## 输入

- 各子 Skill 结果（insect_result、disease_result、pesticide_injury_result 等）
- 图片观察结果（image_observations）
- 诊断槽位（crop、symptoms 等）
- 检索到的知识文档（retrieved_docs）

## 任务

1. 汇总各子 Skill 结果
2. 找出一致的证据（多领域相互支持的证据）
3. 找出冲突的证据（相互矛盾的证据）
4. 判断是否可能多因素共同作用
5. 输出候选诊断列表（按置信度排序）
6. 标注每个候选的不确定性

## 输出 JSON

```json
{
  "candidate_diagnoses": [
    {
      "diagnosis": "诊断结论",
      "related_domains": ["涉及领域"],
      "confidence": 0.0,
      "supporting_evidence": ["支持证据"],
      "conflicting_evidence": ["矛盾证据"],
      "needs_followup": false
    }
  ],
  "reasoning_summary": "推理过程摘要"
}
```
