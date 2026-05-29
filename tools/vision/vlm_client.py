"""
VLM Client — 多模态视觉模型客户端

职责：调用视觉-语言模型进行图片分析。
当前为 Mock 实现，后续可对接 Qwen2.5-VL / InternVL。
"""

from typing import Dict, Any, List, Optional


class VLMClient:
    """多模态模型客户端"""

    def __init__(self, model_name: str = "mock-vlm"):
        self.model_name = model_name

    def analyze_image(self, image_path: str, prompt: Optional[str] = None) -> Dict[str, Any]:
        """分析单张图片

        Args:
            image_path: 图片路径
            prompt: 分析提示（可选）

        Returns:
            结构化观察结果
        """
        return {
            "image_path": image_path,
            "status": "mock",
            "observations": ["Mock VLM: 未接入真实模型"],
            "limitations": ["Mock 模式"],
        }

    def analyze_images(self, image_paths: List[str], prompt: Optional[str] = None) -> List[Dict[str, Any]]:
        """批量分析图片"""
        return [self.analyze_image(p, prompt) for p in image_paths]


def get_vlm_client() -> VLMClient:
    """获取 VLM 客户端单例"""
    return VLMClient()
