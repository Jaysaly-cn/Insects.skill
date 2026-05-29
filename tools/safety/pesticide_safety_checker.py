"""
Pesticide Safety Checker — 农药安全检查工具

职责：检查回答中的农药安全风险。
"""

from typing import Dict, Any, List
import re


# 禁限用农药清单
BANNED_PESTICIDES = [
    "甲胺磷", "对硫磷", "甲基对硫磷", "久效磷", "磷胺",
    "六六六", "滴滴涕", "毒杀芬", "二溴氯丙烷",
    "杀虫脒", "二溴乙烷", "除草醚", "艾氏剂", "狄氏剂",
    "汞制剂", "砷制剂", "铅制剂",
]

# 剂量表达检测模式
DOSAGE_PATTERNS = [
    r"\d+\s*毫升\s*/\s*亩",
    r"\d+\s*克\s*/\s*亩",
    r"\d+\s*倍液",
    r"\d+\s*ml\s*/\s*(亩|mu|ha)",
    r"\d+\s*g\s*/\s*(亩|mu|ha)",
    r"\d+\s*kg\s*/\s*(亩|mu|ha)",
]


def check_pesticide_safety(answer: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """检查回答中的农药安全风险

    Args:
        answer: 待检查的回答文本
        context: 上下文信息

    Returns:
        检查结果
    """
    warnings = []
    unsafe = []

    # 禁限用药检查
    for pesticide in BANNED_PESTICIDES:
        if pesticide in answer:
            unsafe.append(f"提及禁限用农药: {pesticide}")

    # 剂量表达检查
    for pattern in DOSAGE_PATTERNS:
        if re.search(pattern, answer):
            unsafe.append("包含具体剂量表达，违反安全策略")

    return {
        "safe": len(unsafe) == 0,
        "warnings": warnings,
        "unsafe_expressions": unsafe,
    }
