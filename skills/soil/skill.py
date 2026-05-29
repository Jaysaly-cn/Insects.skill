"""
Soil Skill — 土壤诊断子 Skill

职责：
- 处理土壤板结、盐渍化、酸碱度、根系环境、排水等问题
- 与营养缺素和根部病害联动
"""

from graph.state import PlantProtectionState
from skills.base import SkillOutput
from graph.edges.routing_rules import SOIL_KEYWORDS


def run_soil_skill(state: PlantProtectionState) -> dict:
    """执行土壤 Skill"""
    output = SkillOutput(domain="soil")
    text = state.get("user_input", "")

    if not any(kw in text for kw in SOIL_KEYWORDS):
        output.status = "skipped"
        return output.to_dict()

    output.add_candidate(
        name="土壤问题（待确认类型）",
        candidate_type="soil",
        confidence=0.4,
        evidence=["用户描述了土壤或根系相关问题"],
        against_evidence=["缺乏土壤检测数据和根系检查信息"],
        need_more_info=True,
        recommended_observations=[
            "检查土壤质地和结构",
            "测量土壤pH和EC值",
            "检查根系健康状况",
            "调查排水和灌溉条件",
        ],
    )

    output.status = "completed"
    return output.to_dict()
