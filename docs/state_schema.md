# State Schema — 全局状态 Schema

## PlantProtectionState 字段分组

### 1. 原始输入 (4 fields)
- `user_input` (str) — 用户文本
- `image_paths` (List[str]) — 图片路径
- `conversation_id` (str) — 会话 ID
- `current_date` (str) — 当前日期

### 2. 用户上下文 (3 fields)
- `user_role` (str) — farmer/technician/researcher
- `location` (str) — 地区
- `language` (str) — zh/en

### 3. 诊断槽位 (15 fields)
- `crop`, `region`, `season`, `growth_stage`
- `damaged_parts`, `symptoms`, `field_distribution`
- `pest_seen`, `insect_stage`, `insect_morphology`
- `disease_signs`, `weed_description`
- `pesticide_history`, `fertilization_history`, `irrigation_history`
- `soil_condition`, `weather_context`

### 4. 意图与路由 (6 fields)
- `task_type`, `primary_domain`, `secondary_domains`, `all_domains`
- `route_confidence`, `need_multi_skill`

### 5. 图片分析 (4 fields)
- `image_quality`, `image_observations`, `visual_candidates`, `image_analysis_summary`

### 6. 信息充分性 (5 fields)
- `missing_slots`, `critical_missing_slots`, `sufficiency_level`
- `need_followup`, `followup_questions`

### 7. 子 Skill 结果 (8 fields)
- `insect_result`, `disease_result`, `weed_result`, `pesticide_result`
- `pesticide_injury_result`, `soil_result`, `nutrition_result`, `comprehensive_result`

### 8. 综合诊断 (4 fields)
- `candidate_diagnoses`, `final_diagnosis`, `uncertainty_level`, `confidence`

### 9. 安全合规 (4 fields)
- `safety_warnings`, `unsafe_expressions`, `pesticide_safety_checked`, `final_answer_allowed`

### 10. 最终输出 (2 fields)
- `final_answer`, `answer_format`

全量共约 55+ 字段。
