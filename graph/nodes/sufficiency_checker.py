"""
Information Sufficiency Checker — 信息充分性检查节点

职责：
判断当前信息是否足够进入诊断流程。
关键槽位（crop、symptoms）缺失时，必须追问。
"""

from graph.state import PlantProtectionState


CRITICAL_SLOTS = {
    "crop": "作物信息",
    "symptoms": "症状描述",
}

HIGH_SLOTS = {
    "region": "地区信息",
    "damaged_parts": "受害部位",
    "pest_seen": "是否看到虫体",
    "insect_morphology": "虫体形态",
}


def sufficiency_checker(state: PlantProtectionState) -> PlantProtectionState:
    """检查信息充分性"""
    missing = []
    critical_missing = []

    # 检查关键槽位
    if not state.get("crop"):
        critical_missing.append("crop")
    if not state.get("symptoms"):
        critical_missing.append("symptoms")

    # 检查高优先级槽位
    if not state.get("region"):
        missing.append("region")
    if not state.get("damaged_parts"):
        missing.append("damaged_parts")

    state["missing_slots"] = missing
    state["critical_missing_slots"] = critical_missing

    # 综合判断
    if critical_missing:
        state["sufficiency_level"] = "insufficient"
        state["need_followup"] = True
    elif len(missing) >= 3:
        state["sufficiency_level"] = "partial"
        state["need_followup"] = True
    else:
        state["sufficiency_level"] = "sufficient"
        state["need_followup"] = False

    return state
