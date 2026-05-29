"""
Comprehensive Skill — 综合诊断子 Skill

职责：
- 处理明显跨领域问题
- 汇总虫害、病害、药害、营养、土壤等多因素假设
- 当 all_domains >= 2 时由 Domain Dispatcher 调用
"""

from graph.state import PlantProtectionState
from skills.base import SkillOutput


def run_comprehensive_skill(state: PlantProtectionState) -> dict:
    """执行综合诊断 Skill"""
    output = SkillOutput(domain="comprehensive")
    domains = state.get("all_domains", [])
    crop = state.get("crop", "未知作物")

    # 收集各 Skill 现有结果
    skill_results = {
        "insect": state.get("insect_result"),
        "disease": state.get("disease_result"),
        "weed": state.get("weed_result"),
        "pesticide": state.get("pesticide_result"),
        "pesticide_injury": state.get("pesticide_injury_result"),
        "soil": state.get("soil_result"),
        "nutrition": state.get("nutrition_result"),
    }

    active_domains = [d for d, r in skill_results.items() if r and r.get("status") != "skipped"]

    # 构建综合假设
    hypotheses = []
    if len(active_domains) > 1:
        hypotheses.append(f"多因素综合: {crop}可能存在{' + '.join(active_domains)}复合问题")
    elif len(active_domains) == 1:
        hypotheses.append(f"{crop}主要问题在{active_domains[0]}领域")
    else:
        hypotheses.append(f"{crop}问题待综合判断")

    output.add_candidate(
        name=hypotheses[0],
        candidate_type="comprehensive",
        confidence=0.5,
        evidence=[
            f"涉及领域: {', '.join(active_domains) if active_domains else '待确定'}",
            f"多领域关联分析需要更多信息",
        ],
        against_evidence=[
            "各领域结果可能相互影响，需交叉验证",
        ],
        need_more_info=True,
        recommended_observations=[
            "优先确认主要矛盾（虫害/病害/药害/营养）",
            "注意多因素之间的关联和时序关系",
            "建议进行田间系统调查",
        ],
    )

    output.status = "completed"
    return output.to_dict()
