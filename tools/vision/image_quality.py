"""
Image Quality — 图片质量评估工具

职责：评估图片清晰度、主体可见性、是否适合诊断。
"""

from typing import Dict, Any, List


def assess_image_quality(image_path: str) -> Dict[str, Any]:
    """评估单张图片质量

    Args:
        image_path: 图片路径

    Returns:
        质量评估结果
    """
    return {
        "image_path": image_path,
        "quality": "unknown",
        "issues": [],
        "usable": True,
        "note": "Mock 评估模式",
    }


def assess_batch(image_paths: List[str]) -> List[Dict[str, Any]]:
    """批量评估图片质量"""
    return [assess_image_quality(p) for p in image_paths]
