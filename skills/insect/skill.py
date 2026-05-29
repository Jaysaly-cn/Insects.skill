"""
Insect Skill — 虫害诊断子 Skill

职责：
- 判断是否为虫害
- 结合图片、作物、症状生成候选害虫
- 查询害虫知识卡片（桥接 insect.skill/data/）
- 做相似害虫鉴别
- 给出虫害相关调查建议
"""

from graph.state import PlantProtectionState
from skills.base import SkillOutput
from skills.insect.prompts import INSECT_SKILL_PROMPT
from skills.insect.tools import query_pest_ontology, query_pest_card
from graph.edges.routing_rules import INSECT_KEYWORDS


def run_insect_skill(state: PlantProtectionState) -> dict:
    """执行昆虫/虫害 Skill"""
    output = SkillOutput(domain="insect")
    text = state.get("user_input", "")
    crop = state.get("crop", "未知")
    symptoms = state.get("symptoms", [])

    # 1. 检查是否涉及虫害
    has_insect = any(kw in text for kw in INSECT_KEYWORDS)

    if not has_insect and not state.get("pest_seen"):
        output.status = "skipped"
        output.add_candidate(
            name="未检测到虫害相关描述",
            candidate_type="pest",
            confidence=0.0,
            evidence=["用户输入中未提及虫害特征"],
        )
        return output.to_dict()

    # 2. 查询知识库（桥接 insect.skill）
    pest_candidates = query_pest_ontology(text, crop)

    if pest_candidates:
        for pest in pest_candidates:
            # 检索知识卡片
            card = query_pest_card(pest.get("pest_id", ""))
            evidence = [
                f"作物匹配: {crop}",
                f"症状匹配: {', '.join(symptoms[:2]) if symptoms else '待确认'}",
            ]
            if card:
                evidence.append(f"知识卡片: {card.get('name_cn', '')}")

            output.add_candidate(
                name=pest.get("name_cn", pest.get("pest_id", "未知害虫")),
                candidate_type="pest",
                confidence=0.6,
                evidence=evidence,
                against_evidence=["Mock 模式，未接入完整知识库"],
                need_more_info=True,
                recommended_observations=[
                    "观察虫体形态（大小、颜色、翅型）",
                    "确认虫态（卵/幼虫/若虫/蛹/成虫）",
                    "调查田间分布和发生程度",
                ],
            )
    else:
        # 无匹配候选时给出通用建议
        output.add_candidate(
            name=f"{crop}虫害（待确认具体种类）",
            candidate_type="pest",
            confidence=0.3,
            evidence=[f"用户在{crop}上观察到虫害迹象"],
            against_evidence=["知识库中未找到匹配记录"],
            need_more_info=True,
            recommended_observations=[
                "请提供虫体清晰照片（背面+侧面）",
                "描述虫体大小、颜色、形态",
                "确认是单一种类还是混合发生",
            ],
        )

    output.risk_notes = [f"{crop}虫害需确认发生程度后再决定是否用药"]
    output.status = "completed"

    return output.to_dict()
