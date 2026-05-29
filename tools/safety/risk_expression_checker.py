"""
Risk Expression Checker — 风险表达检查工具

职责：检查回答中是否包含过强或不当的表达。
"""

from typing import Dict, Any, List
import re


RISKY_PATTERNS = [
    (r"一定是", "绝对化表达: '一定是'"),
    (r"必然是", "绝对化表达: '必然是'"),
    (r"保证防治", "保证性表达: '保证防治'"),
    (r"完全消灭", "绝对化表达: '完全消灭'"),
    (r"确定无疑", "绝对化表达: '确定无疑'"),
    (r"无需进一步确认", "绝对化表达: '无需进一步确认'"),
]


def check_risk_expressions(text: str) -> List[str]:
    """检查风险表达

    Returns:
        风险表达列表
    """
    issues = []
    for pattern, description in RISKY_PATTERNS:
        if re.search(pattern, text):
            issues.append(description)
    return issues
