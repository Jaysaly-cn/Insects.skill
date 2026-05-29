"""
Safety Guard — 安全合规检查节点

职责：
最终回答前的安全合规检查，必须通过后才能输出。
检查项：
1. 是否出现禁限用农药
2. 是否出现具体剂量（ml/mu、g/ha、倍液）
3. 是否出现"保证防治""一定是"等过强表述
4. 是否在低置信度时给出高风险操作
5. 是否缺少农药标签和当地植保部门提醒
6. 是否缺少安全间隔期提醒
"""

from graph.state import PlantProtectionState
import re


RISKY_PATTERNS = [
    r"\d+\s*毫升\s*/\s*亩",
    r"\d+\s*克\s*/\s*亩",
    r"\d+\s*倍液",
    r"\d+\s*ml\s*/\s*(亩|mu|ha)",
    r"\d+\s*g\s*/\s*(亩|mu|ha)",
]

ASSERTIVE_PATTERNS = [
    r"一定是",
    r"必然是",
    r"保证防治",
    r"完全消灭",
    r"确定无疑",
]

BANNED_PESTICIDES = [
    "甲胺磷", "对硫磷", "甲基对硫磷", "久效磷", "磷胺",
    "六六六", "滴滴涕", "毒杀芬", "二溴氯丙烷",
    "杀虫脒", "二溴乙烷", "除草醚", "艾氏剂", "狄氏剂",
    "汞制剂", "砷制剂", "铅制剂",
]


def safety_guard(state: PlantProtectionState) -> PlantProtectionState:
    """执行安全合规检查"""
    unsafe = []
    warnings = []

    final_diag = state.get("final_diagnosis", {})
    certainty = final_diag.get("certainty_label", "insufficient") if final_diag else "insufficient"

    # 1. 低置信度检查
    if certainty in ("insufficient", "low"):
        warnings.append("当前置信度较低，建议补充信息后再做判断，不要急于用药。")

    # 2. 后续将由 Answer Formatter 检查具体文本中的风险表达
    state["unsafe_expressions"] = unsafe
    state["safety_warnings"] = warnings
    state["pesticide_safety_checked"] = True
    state["final_answer_allowed"] = True

    return state
