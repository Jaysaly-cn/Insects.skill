# Tool Protocol — 工具调用协议

## 工具分类

### 视觉工具 (tools/vision/)
- `VLMClient.analyze_image(path)` — 调用多模态模型分析图片
- `assess_image_quality(path)` — 评估图片质量
- `detect_pest_candidate(path)` — 专用害虫检测模型

### 检索工具 (tools/retrieval/)
- `vector_search(query, domain, top_k)` — 向量检索
- `keyword_search(query, domain, top_k)` — 关键词检索
- `hybrid_search(query, filters)` — 混合检索
- `rerank(query, docs)` — 检索重排

### 数据库工具 (tools/database/)
- `query_ontology(name, domain)` — 本体查询
- `query_crop_problems(crop, region)` — 作物问题查询
- `query_pesticide_registration(crop, target)` — 农药登记查询
- `query_occurrence_calendar(pest_id, region)` — 发生历查询

### 安全工具 (tools/safety/)
- `check_pesticide_safety(answer, context)` — 农药安全风险检查
- `check_risk_expressions(text)` — 风险表达检查

## 调用原则

1. 所有工具应为纯函数，不维护全局状态
2. Mock 实现返回空/默认值，不依赖外部服务
3. 工具调用结果写入 State 对应字段
