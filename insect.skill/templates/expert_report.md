# Expert Report Template

Use this template for technical reports aimed at agricultural extension
workers, plant protection technicians, or researchers.

---

# 农业害虫诊断报告
## Agricultural Pest Diagnostic Report

---

## 1. 案例信息 Case Information

| 项目 | 内容 |
|------|------|
| 报告编号 | [Report ID] |
| 日期 | [Date] |
| 咨询人类型 | [Farmer / Technician / Other] |
| 作物 | [Crop name, variety] |
| 生育期 | [Growth stage] |
| 地点 | [Province, county] |
| 季节 | [Month / season] |

## 2. 现场症状 Field Symptoms

[Description of symptoms as reported by the user.]

- 受害部位: [Damaged plant parts]
- 症状类型: [Symptom types]
- 发生分布: [Field distribution pattern]
- 发生率: [Reported incidence, if available]

## 3. 图像观察 Image Observations

[If images were provided.]

- 图像质量: [Quality assessment]
- 虫态: [Life stage observed]
- 形态特征: [Morphological features noted]
- 危害痕迹: [Feeding signs observed]

## 4. 诊断候选 Diagnostic Candidates

按可能性排序，Top-N:

| 排名 | 害虫 | 置信度 | 支持依据 | 存疑点 |
|------|------|--------|----------|--------|
| 1 | [Pest] | [Level] | [Evidence] | [Doubts] |
| 2 | [Pest] | [Level] | [Evidence] | [Doubts] |
| ... | ... | ... | ... | ... |

## 5. 鉴别分析 Differential Analysis

[Detailed comparison of top candidates, referencing distinguishing
features from similar_pests.json if available.]

### [Pest A] vs [Pest B]

| 鉴别特征 | [Pest A] | [Pest B] | 现场观察 | 可靠性 |
|----------|----------|----------|----------|--------|
| [Feature] | [Value] | [Value] | [Observed] | [Reliability] |

## 6. 风险等级 Risk Level

- **当前风险**: [Low / Medium / High / Critical]
- **判定依据**: [Justification]
- **趋势预判**: [Expected trend if no action, brief]

## 7. 调查建议 Investigation Recommendations

为进一步确诊，建议开展以下田间调查：

1. [Investigation item 1]
2. [Investigation item 2]
3. [Investigation item 3]

## 8. 防控建议 Management Recommendations

### 8.1 农业防治 Cultural Control
- [Specific measures]

### 8.2 物理防治 Physical Control
- [Specific measures]

### 8.3 生物防治 Biological Control
- [Specific measures]

### 8.4 化学防治 Chemical Control (应急)
- **适用条件**: [Economic threshold exceeded?]
- **可选药剂类别**: [Active ingredient classes, no dosages]
- **注意事项**: [Safety, resistance management, PHI, REI]

## 9. 不确定性说明 Uncertainty Statement

- **置信度**: [Overall confidence level]
- **主要不确定因素**: [Key uncertainties]
- **提升置信度所需信息**: [What additional info would help]
- **替代可能性**: [Other possibilities not ruled out]

## 10. 安全声明 Safety Disclaimer

> **免责声明**: 本报告仅供植保技术参考。农药使用须严格遵循产品标签
> 和当地法规。具体用药方案请咨询当地植保站或农业技术推广部门。
> 报告出具方对因使用本报告信息造成的任何损失不承担责任。

## 11. 参考依据 References

- [Local knowledge base: data/pest_ontology.json, data/crop_pest_map.json]
- [External references cited]
- [Communication records with the user]

---

*报告生成时间: [Timestamp]*
*Skill 版本: [Version from VERSION file]*
