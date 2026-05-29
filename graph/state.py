"""
Plant Protection Agent — 全局 State 定义

PlantProtectionState 是整个 Agent 的共享状态对象，贯穿所有节点。
设计原则：
  - 每个节点只读取自己需要的字段，写入自己负责的字段
  - 多意图并发通过 all_domains 列表驱动，每个 Skill 结果独立存储
  - 综合诊断仲裁通过 candidate_diagnoses → final_diagnosis 两阶段完成
"""

from typing import TypedDict, Optional, List, Dict, Any


class PlantProtectionState(TypedDict, total=False):
    # ===================== 原始输入 =====================
    user_input: str
    """用户原始文本输入"""
    image_paths: List[str]
    """用户提供的图片路径列表"""
    conversation_id: str
    """会话唯一标识"""
    user_id: Optional[str]
    """用户标识（可选）"""
    current_date: Optional[str]
    """当前日期（系统填充）"""

    # ===================== 用户上下文 =====================
    user_role: Optional[str]
    """用户角色: farmer | technician | researcher | unknown"""
    location: Optional[str]
    """用户提供的地区信息"""
    language: Optional[str]
    """语言: zh | en"""

    # ===================== 诊断槽位（Slot Extractor 填充） =====================
    crop: Optional[str]
    """作物名称"""
    region: Optional[str]
    """发生地区"""
    season: Optional[str]
    """发生季节/月份"""
    growth_stage: Optional[str]
    """作物生育期: 苗期 | 分蘖期 | 拔节期 | 孕穗期 | 抽穗期 | 灌浆期 | 成熟期"""

    damaged_parts: List[str]
    """受害部位: leaf | stem | root | fruit | flower | seed | seedling | whole_plant"""
    symptoms: List[str]
    """症状描述列表"""
    field_distribution: Optional[str]
    """田间分布: sporadic | patchy | edge_effect | uniform"""

    pest_seen: Optional[bool]
    """是否看到虫体"""
    insect_stage: Optional[str]
    """虫态: egg | larva | nymph | pupa | adult"""
    insect_morphology: List[str]
    """虫体形态描述"""

    disease_signs: List[str]
    """病害特征: 病斑颜色/形状/霉层/菌核等"""
    weed_description: Optional[str]
    """杂草描述"""

    pesticide_history: Optional[str]
    """用药史"""
    fertilization_history: Optional[str]
    """施肥史"""
    irrigation_history: Optional[str]
    """灌溉史"""
    soil_condition: Optional[str]
    """土壤状况"""
    weather_context: Optional[str]
    """天气/气候背景"""

    # ===================== 意图与路由（Intent Router 填充） =====================
    task_type: Optional[str]
    """任务类型: diagnosis | knowledge_query | control_advice | identification | unknown"""
    primary_domain: Optional[str]
    """主要领域: insect | disease | weed | pesticide | pesticide_injury | soil | nutrition | comprehensive"""
    secondary_domains: List[str]
    """次要领域列表（多意图时填充）"""
    all_domains: List[str]
    """所有待调用的领域列表（primary + secondary）"""
    route_confidence: Optional[float]
    """路由置信度 0-1"""
    need_multi_skill: Optional[bool]
    """是否需要多 Skill 并发（all_domains >= 2 时自动启用）"""

    # ===================== 图片分析结果（Image Analyzer 填充） =====================
    image_quality: Optional[str]
    """图片质量: high | medium | low | unusable"""
    image_observations: List[Dict[str, Any]]
    """每张图片的客观观察结果"""
    visual_candidates: List[Dict[str, Any]]
    """基于视觉的候选列表"""
    image_analysis_summary: Optional[str]
    """图片分析文本摘要"""

    # ===================== 信息充分性（Sufficiency Checker 填充） =====================
    missing_slots: List[str]
    """缺失的非关键槽位"""
    critical_missing_slots: List[str]
    """缺失的关键槽位（crop、symptoms）"""
    sufficiency_level: Optional[str]
    """信息充分程度: sufficient | partial | insufficient"""
    need_followup: Optional[bool]
    """是否需要追问"""
    followup_questions: List[str]
    """追问问题列表"""

    # ===================== 各子 Skill 结果（Domain Dispatcher 填充） =====================
    insect_result: Optional[Dict[str, Any]]
    """Insect Skill 输出"""
    disease_result: Optional[Dict[str, Any]]
    """Disease Skill 输出"""
    weed_result: Optional[Dict[str, Any]]
    """Weed Skill 输出"""
    pesticide_result: Optional[Dict[str, Any]]
    """Pesticide Skill 输出"""
    pesticide_injury_result: Optional[Dict[str, Any]]
    """Pesticide Injury Skill 输出"""
    soil_result: Optional[Dict[str, Any]]
    """Soil Skill 输出"""
    nutrition_result: Optional[Dict[str, Any]]
    """Nutrition Skill 输出"""
    comprehensive_result: Optional[Dict[str, Any]]
    """Comprehensive Skill 输出（多 Skill 汇总时使用）"""

    # ===================== 证据与检索 =====================
    retrieved_docs: List[Dict[str, Any]]
    """检索到的知识文档列表"""
    evidence_summary: Optional[str]
    """证据摘要"""

    # ===================== 综合诊断（Comprehensive Reasoner + Diagnostic Arbiter 填充） =====================
    candidate_diagnoses: List[Dict[str, Any]]
    """候选诊断列表（Comprehensive Reasoner 输出）"""
    final_diagnosis: Optional[Dict[str, Any]]
    """最终诊断（Diagnostic Arbiter 输出）"""
    uncertainty_level: Optional[str]
    """不确定度: low | medium | high | insufficient"""
    confidence: Optional[float]
    """整体置信度 0-1"""

    # ===================== 安全合规（Safety Guard 填充） =====================
    safety_warnings: List[str]
    """安全警告列表"""
    unsafe_expressions: List[str]
    """不安全表达列表"""
    pesticide_safety_checked: Optional[bool]
    """是否已完成农药安全检查"""
    final_answer_allowed: Optional[bool]
    """是否允许输出最终回答"""

    # ===================== 最终输出（Answer Formatter 填充） =====================
    final_answer: Optional[str]
    """格式化后的最终回答文本"""
    answer_format: Optional[str]
    """输出格式: concise | expert_report | followup"""
