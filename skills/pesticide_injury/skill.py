"""
Pesticide Injury Skill — 药害诊断子 Skill

职责：
- 判断是否可能为药害
- 重点读取用药史、时间间隔、天气、作物生育期
- 与病害、缺素、虫害进行区分
"""

from graph.state import PlantProtectionState
from skills.base import SkillOutput
from graph.edges.routing_rules import PESTICIDE_INJURY_KEYWORDS


def run_pesticide_injury_skill(state: PlantProtectionState) -> dict:
    """执行药害 Skill"""
    output = SkillOutput(domain="pesticide_injury")
    text = state.get("user_input", "")
    pesticide_hist = state.get("pesticide_history", "")

    has_injury = any(kw in text for kw in PESTICIDE_INJURY_KEYWORDS) or bool(pesticide_hist)

    if not has_injury:
        output.status = "skipped"
        return output.to_dict()

    output.add_candidate(
        name="药害（待确认）",
        candidate_type="pesticide_injury",
        confidence=0.4,
        evidence=[
            "用户提及了用药史",
            "症状出现时间与用药时间可能相关",
        ],
        against_evidence=[
            "需排除病害、缺素等可能性",
            "缺乏用药品种、剂量、时间间隔信息",
        ],
        need_more_info=True,
        recommended_observations=[
            "记录用药品种、剂量、时间",
            "记录施药时的天气条件",
            "对比受害植株和未施药区植株差异",
        ],
    )

    output.status = "completed"
    return output.to_dict()
