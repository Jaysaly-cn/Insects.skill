# Tests — 测试与评测

## 测试集

| 文件 | 说明 |
|------|------|
| test_cases/text_cases.jsonl | 纯文本诊断用例 |
| test_cases/image_text_cases.jsonl | 图片+文本诊断用例 |
| test_cases/insufficient_info_cases.jsonl | 信息不足场景用例 |
| test_cases/multi_intent_cases.jsonl | 多意图并发场景用例 |
| test_cases/safety_cases.jsonl | 安全合规场景用例 |

## 评测脚本

| 脚本 | 评测模块 |
|------|----------|
| eval/intent_eval.py | 意图识别正确率 |
| eval/slot_eval.py | 槽位抽取准确率 |
| eval/followup_eval.py | 追问机制有效性 |
| eval/diagnosis_eval.py | 综合诊断合理性 |
| eval/safety_eval.py | 安全合规通过率 |

## 评测指标

| 模块 | 指标 |
|------|------|
| 意图识别 | 主意图准确率、次意图召回率 |
| 槽位抽取 | 作物/症状/地区正确率 |
| 图片观察 | 客观描述占比、过度判断占比 |
| 追问机制 | 关键缺失追问率、单次追问数 |
| 子 Skill 调用 | 调用正确率 |
| 综合诊断 | 多领域覆盖率、主因识别正确率 |
| 安全合规 | 禁限用药拦截率、剂量表达拦截率 |
| 最终输出 | 结构化完整度、专业性评分 |

## 运行测试

```bash
# 运行单个评测
python tests/eval/intent_eval.py

# 运行所有评测（待实现）
pytest tests/
```
