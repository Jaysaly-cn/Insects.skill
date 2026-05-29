"""
Domain Dispatcher — 领域分发节点

职责：
根据 all_domains 列表，并发调用对应子 Skill。
每个 Skill 独立运行、独立写回 State 对应字段。
支持多意图并行（multi-skill dispatch 核心节点）。
"""

from graph.state import PlantProtectionState
from graph.edges.routing_rules import get_dispatcher_domains


def domain_dispatcher(state: PlantProtectionState) -> PlantProtectionState:
    """分发到各领域 Skill"""
    domains = get_dispatcher_domains(state)
    need_multi = state.get("need_multi_skill", False)

    # 按领域列表顺序调用 Skill
    for domain in domains:
        if domain == "insect":
            from skills.insect.skill import run_insect_skill
            state["insect_result"] = run_insect_skill(state)
        elif domain == "disease":
            from skills.disease.skill import run_disease_skill
            state["disease_result"] = run_disease_skill(state)
        elif domain == "weed":
            from skills.weed.skill import run_weed_skill
            state["weed_result"] = run_weed_skill(state)
        elif domain == "pesticide":
            from skills.pesticide.skill import run_pesticide_skill
            state["pesticide_result"] = run_pesticide_skill(state)
        elif domain == "pesticide_injury":
            from skills.pesticide_injury.skill import run_pesticide_injury_skill
            state["pesticide_injury_result"] = run_pesticide_injury_skill(state)
        elif domain == "soil":
            from skills.soil.skill import run_soil_skill
            state["soil_result"] = run_soil_skill(state)
        elif domain == "nutrition":
            from skills.nutrition.skill import run_nutrition_skill
            state["nutrition_result"] = run_nutrition_skill(state)
        elif domain == "comprehensive":
            from skills.comprehensive.skill import run_comprehensive_skill
            state["comprehensive_result"] = run_comprehensive_skill(state)

    # 多 Skill 场景：也调用 Comprehensive Skill 做汇总
    if need_multi or len(domains) > 1:
        from skills.comprehensive.skill import run_comprehensive_skill
        state["comprehensive_result"] = run_comprehensive_skill(state)

    return state
