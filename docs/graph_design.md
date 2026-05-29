# Graph Design — LangGraph 图设计

## 节点清单

| 节点 | 文件 | 职责 | 输入 | 输出 |
|------|------|------|------|------|
| Input Normalizer | input_normalizer.py | 标准化用户输入 | raw input | state 基础字段 |
| Slot Extractor | slot_extractor.py | 抽取诊断槽位 | user_input | crop/symptoms/damaged_parts等 |
| Intent Router | intent_router.py | 多意图识别路由 | user_input | all_domains/primary_domain |
| Image Analyzer | image_analyzer.py | 图片分析 | image_paths | image_observations |
| Sufficiency Checker | sufficiency_checker.py | 信息充分性检查 | 各槽位 | sufficiency_level/need_followup |
| Follow-up Generator | followup_generator.py | 生成追问 | missing_slots | followup_questions |
| Domain Dispatcher | domain_dispatcher.py | 分发到子 Skill | all_domains | {domain}_result |
| Comprehensive Reasoner | comprehensive_reasoner.py | 综合推理 | 各 domain_result | candidate_diagnoses |
| Diagnostic Arbiter | diagnostic_arbiter.py | 诊断仲裁 | candidate_diagnoses | final_diagnosis |
| Safety Guard | safety_guard.py | 安全合规检查 | final_diagnosis | safety_warnings |
| Answer Formatter | answer_formatter.py | 输出格式化 | 全部结果 | final_answer |

## 条件边

| 条件 | 函数 | 分支 |
|------|------|------|
| has_image | after_intent | yes → image_analyzer, no → sufficiency_checker |
| need_followup | after_sufficiency | followup → followup_generator, dispatch → domain_dispatcher |

## 图流程文本

```
START
  ↓
Input Normalizer
  ↓
Slot Extractor
  ↓
Intent Router
  ↓
{has_image?}
  ├── yes → Image Analyzer → Sufficiency Checker
  └── no  → Sufficiency Checker
            ↓
        {need_followup?}
          ├── yes → Follow-up Generator → END
          └── no  → Domain Dispatcher
                     ↓
                   Comprehensive Reasoner
                     ↓
                   Diagnostic Arbiter
                     ↓
                   Safety Guard
                     ↓
                   Answer Formatter
                     ↓
                   END
```
