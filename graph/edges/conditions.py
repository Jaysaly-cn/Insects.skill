"""
Plant Protection Agent — 条件路由函数

LangGraph 条件边的判断函数，决定图的分支走向。
"""

from graph.state import PlantProtectionState


def has_image(state: PlantProtectionState) -> str:
    """是否有图片需要分析？"""
    image_paths = state.get("image_paths", [])
    if image_paths and len(image_paths) > 0:
        return "yes"
    return "no"


def need_followup(state: PlantProtectionState) -> str:
    """是否需要追问？"""
    if state.get("need_followup") is True:
        sufficiency = state.get("sufficiency_level", "")
        if sufficiency == "insufficient":
            return "yes"
    return "no"


def should_use_multi_skill(state: PlantProtectionState) -> bool:
    """是否需要多 Skill 并发？"""
    domains = state.get("all_domains", [])
    return len(domains) >= 2 or state.get("need_multi_skill") is True


def should_safety_check(state: PlantProtectionState) -> bool:
    """是否应进入安全检查？所有输出都必须检查。"""
    return True


def after_sufficiency(state: PlantProtectionState) -> str:
    """充分性检查后的路由"""
    if state.get("need_followup") is True:
        return "followup"
    return "dispatch"


def after_intent(state: PlantProtectionState) -> str:
    """意图识别后的路由（是否分析图片）"""
    return has_image(state)
