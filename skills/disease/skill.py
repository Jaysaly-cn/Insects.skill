"""
Disease Skill — 病害诊断子 Skill

职责：
- 判断真菌、细菌、病毒、生理性病害可能
- 结合病斑形态、部位、扩展方式、环境条件
- 输出候选病害
- 与虫害、药害、缺素进行区分
"""

from graph.state import PlantProtectionState
from skills.base import SkillOutput
from graph.edges.routing_rules import DISEASE_KEYWORDS


def run_disease_skill(state: PlantProtectionState) -> dict:
    """执行病害 Skill"""
    output = SkillOutput(domain="disease")
    text = state.get("user_input", "")
    crop = state.get("crop", "未知")

    has_disease = any(kw in text for kw in DISEASE_KEYWORDS)

    if not has_disease:
        output.status = "skipped"
        return output.to_dict()

    # 病害类型判断（Mock）
    disease_types = []
    if any(kw in text for kw in ["霉", "粉", "锈"]):
        disease_types.append("真菌性病害")
    if any(kw in text for kw in ["腐", "烂", "萎蔫"]):
        disease_types.append("真菌/细菌性病害")
    if any(kw in text for kw in ["花叶", "矮缩", "黄化"]):
        disease_types.append("病毒病")
    if any(kw in text for kw in ["斑点", "穿孔", "溃疡"]):
        disease_types.append("细菌性病害")

    disease_label = "/".join(disease_types) if disease_types else "病害（待确定类型）"

    output.add_candidate(
        name=f"{crop}{disease_label}",
        candidate_type="disease",
        confidence=0.5,
        evidence=[
            f"用户描述的症状符合{disease_label}特征",
        ],
        against_evidence=[
            "需排除虫害、药害和缺素可能性",
            "缺乏病斑形态和扩展方式细节",
        ],
        need_more_info=True,
        recommended_observations=[
            "拍摄病斑特写（正面+背面）",
            "描述病斑形状、颜色、是否有霉层",
            "记录发病部位（新叶/老叶/茎基部）",
            "调查田间分布和发病环境",
        ],
    )

    output.status = "completed"
    return output.to_dict()
