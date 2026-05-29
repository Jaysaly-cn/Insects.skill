"""
Image Analyzer — 图片分析节点

职责：
当用户提供图片时，调用多模态模型或图像工具进行客观观察。
输出结构化观察结果，作为诊断证据之一。

Mock 实现：当前返回占位结果。
"""

from graph.state import PlantProtectionState


def image_analyzer(state: PlantProtectionState) -> PlantProtectionState:
    """分析用户提供的图片"""
    image_paths = state.get("image_paths", [])

    if not image_paths:
        state["image_quality"] = None
        state["image_observations"] = []
        state["visual_candidates"] = []
        return state

    observations = []
    candidates = []

    for img_path in image_paths:
        obs = {
            "image_id": img_path,
            "visible_parts": [],
            "observed_features": [],
            "limitations": ["Mock 分析模式，未接入真实 VLM"],
        }
        observations.append(obs)

    state["image_quality"] = "unknown"
    state["image_observations"] = observations
    state["visual_candidates"] = candidates
    state["image_analysis_summary"] = f"分析了 {len(image_paths)} 张图片（Mock 模式）"

    return state
