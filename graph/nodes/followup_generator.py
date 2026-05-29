"""
Follow-up Generator — 追问生成节点

职责：
当信息不足时，生成简洁、优先级明确的追问问题。
一次最多问 3 个关键问题，优先影响最大的信息。
"""

from graph.state import PlantProtectionState


def followup_generator(state: PlantProtectionState) -> PlantProtectionState:
    """根据缺失槽位生成追问问题"""
    critical_missing = state.get("critical_missing_slots", [])
    missing = state.get("missing_slots", [])
    questions = []

    # 关键缺失优先
    if "crop" in critical_missing:
        questions.append("请问这是什么作物？如果能告知品种和当前生育期，可以帮助缩小可疑病虫害范围。")

    if "symptoms" in critical_missing:
        questions.append("请问作物出现了哪些具体症状？比如叶片发黄、枯萎、斑点等？")

    # 高位缺失
    if "region" in missing and "crop" not in critical_missing:
        questions.append("请问您的田块在哪个省/县？目前大概什么季节？")

    if "damaged_parts" in missing and "symptoms" not in critical_missing:
        questions.append("请问植株哪个部位受害最明显？叶片、茎秆、根部还是果实？")

    if not questions:
        # 兜底
        questions.append("当前信息还不足以做高置信判断。请补充更多细节，如作物种类、症状描述、发生地区等。")

    # 限制最多 3 个
    state["followup_questions"] = questions[:3]

    return state
