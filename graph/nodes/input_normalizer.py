"""
Input Normalizer — 输入标准化节点

职责：
1. 接收原始用户输入
2. 标准化文本、图片路径、会话 ID、时间等
3. 合并历史对话上下文
4. 输出标准化 State

Mock 实现：当前直接透传，仅填充基础字段。
"""

from datetime import datetime
from graph.state import PlantProtectionState


def input_normalizer(state: PlantProtectionState) -> PlantProtectionState:
    """标准化用户输入"""
    state["current_date"] = datetime.now().strftime("%Y-%m-%d")
    state["language"] = detect_language(state.get("user_input", ""))
    return state


def detect_language(text: str) -> str:
    """简单语言检测"""
    if not text:
        return "zh"
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff":
            return "zh"
    return "en"
