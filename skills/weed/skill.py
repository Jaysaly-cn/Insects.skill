"""
Weed Skill — 草害诊断子 Skill

职责：
- 识别杂草类问题
- 支持杂草形态描述、作物田场景、除草剂风险
"""

from graph.state import PlantProtectionState
from skills.base import SkillOutput
from graph.edges.routing_rules import WEED_KEYWORDS


def run_weed_skill(state: PlantProtectionState) -> dict:
    """执行草害 Skill"""
    output = SkillOutput(domain="weed")
    text = state.get("user_input", "")

    if not any(kw in text for kw in WEED_KEYWORDS):
        output.status = "skipped"
        return output.to_dict()

    output.add_candidate(
        name="杂草（待确定种类）",
        candidate_type="weed",
        confidence=0.4,
        evidence=["用户描述了杂草相关问题"],
        against_evidence=["缺乏杂草形态细节和田间分布"],
        need_more_info=True,
        recommended_observations=[
            "描述杂草形态（叶型/茎型/根系）",
            "拍摄杂草全株照片",
            "确认杂草在田间的分布密度",
        ],
    )

    output.status = "completed"
    return output.to_dict()
