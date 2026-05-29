# Evaluation Plan — 评测计划

## 评测目标

构建标准化的测试集和评测脚本，量化评估 Agent 各模块的性能。

## 评测维度

| 维度 | 指标 | 当前目标 |
|------|------|----------|
| 意图识别 | 主意图准确率 ≥ 80% | 关键词 Mock ≥ 70% |
| 槽位抽取 | 关键槽位（作物/症状）准确率 ≥ 85% | Mock ≥ 60% |
| 多意图并发 | 多领域识别召回率 ≥ 75% | Mock ≥ 60% |
| 追问机制 | 关键缺失追问率 100% | Mock ≥ 90% |
| 信息充分性 | 正确分类 sufficient/insufficient ≥ 80% | Mock ≥ 70% |
| 综合诊断 | 主因识别正确率 ≥ 60% | 待建立基线 |
| 安全合规 | 禁限用药拦截率 100% | 待建立基线 |
| 输出质量 | 结构化完整度 ≥ 90% | 待建立基线 |

## 测试集建设

| 阶段 | 测试集 | 数量 | 覆盖范围 |
|------|--------|------|----------|
| MVP 0 | text_cases.jsonl | 10-20 | 基本诊断场景 |
| MVP 0 | insufficient_info_cases.jsonl | 5-10 | 信息不足场景 |
| MVP 0 | multi_intent_cases.jsonl | 5-10 | 多意图场景 |
| MVP 1 | 扩展 text_cases | 30-50 | 水稻/蔬菜/果树常见病虫害 |
| MVP 2 | image_text_cases | 10-20 | 图文混合场景 |
| MVP 3 | safety_cases | 10-20 | 安全违规场景 |

## 评测流程

```bash
# 运行意图评测
python tests/eval/intent_eval.py

# 运行槽位评测
python tests/eval/slot_eval.py

# 运行追问评测
python tests/eval/followup_eval.py
```
