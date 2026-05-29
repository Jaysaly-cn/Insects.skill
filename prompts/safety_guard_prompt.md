# Safety Guard Prompt

## 检查项

1. 是否出现禁限用农药（甲胺磷、六六六、滴滴涕等）
2. 是否出现具体剂量表达（ml/mu、g/ha、倍液）
3. 是否出现"保证防治""一定是"等过强绝对化表述
4. 是否在低置信度时给出高风险操作建议
5. 是否缺少农药标签和当地植保部门提醒
6. 是否缺少安全间隔期和防护措施提醒

## 输出 JSON

```json
{
  "pesticide_safety_checked": true,
  "final_answer_allowed": true,
  "safety_warnings": ["安全警告"],
  "unsafe_expressions": ["不安全表达列表"]
}
```

## 规则

- 如果发现不安全表达，必须要求修改后才能输出
- 涉及农药时必须包含安全声明
- 低置信度时必须警告不要急于用药
