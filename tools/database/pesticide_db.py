"""
Pesticide DB — 农药数据库查询工具

职责：查询农药登记信息。
Mock 实现，后续接入官方农药登记数据库。
"""

from typing import Dict, Any, List, Optional


def query_pesticide_registration(crop: str, target: str) -> List[Dict[str, Any]]:
    """查询农药登记信息

    Args:
        crop: 作物名称
        target: 防治对象

    Returns:
        已登记农药列表
    """
    return []


def query_pesticide_info(pesticide_name: str) -> Dict[str, Any]:
    """查询单个农药信息"""
    return {}
