"""
Pesticide Skill — 农药知识子 Skill

职责：
- 回答农药知识、作用机制、登记对象
- 安全间隔期、抗药性轮换等
- 必须调用安全检查工具
- 没有可靠登记数据时，不给具体剂量
"""

from graph.state import PlantProtectionState
from skills.base import SkillOutput
from graph.edges.routing_rules import PESTICIDE_KEYWORDS


def run_pesticide_skill(state: PlantProtectionState) -> dict:
    """执行农药 Skill"""
    output = SkillOutput(domain="pesticide")
    text = state.get("user_input", "")

    if not any(kw in text for kw in PESTICIDE_KEYWORDS):
        output.status = "skipped"
        return output.to_dict()

    output.add_candidate(
        name="农药信息查询",
        candidate_type="pesticide",
        confidence=0.5,
        evidence=["用户询问了农药相关信息"],
        against_evidence=["没有查询到具体的农药登记数据（Mock 模式）"],
        need_more_info=True,
        recommended_observations=[
            "确认目标作物和防治对象",
            "查看农药标签确认登记信息",
            "咨询当地植保部门获取具体推荐",
        ],
    )

    output.risk_notes = [
        "不要提供具体农药剂量（ml/mu、g/ha、倍液）",
        "必须提醒查看产品标签和当地植保部门建议",
        "注意禁限用农药清单",
    ]

    output.status = "completed"
    return output.to_dict()
