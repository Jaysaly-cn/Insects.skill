"""
Pest Detector — 害虫检测专用工具

职责：可选调用专用害虫识别模型，输出 Top-K 候选。
"""

from typing import Dict, Any, List


def detect_pest_candidate(image_path: str) -> Dict[str, Any]:
    """检测图片中的害虫候选

    Args:
        image_path: 图片路径

    Returns:
        Top-K 候选列表
    """
    return {
        "image_path": image_path,
        "candidates": [],
        "status": "mock",
        "note": "Mock 检测模式，未接入专用模型",
    }
