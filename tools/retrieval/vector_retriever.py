"""
Vector Retriever — 向量检索工具

职责：基于语义向量的知识检索。
Mock 实现，后续接入 bge-m3 + Qdrant/Milvus。
"""

from typing import Dict, Any, List, Optional


def vector_search(query: str, domain: Optional[str] = None, top_k: int = 5) -> List[Dict[str, Any]]:
    """向量检索知识卡片"""
    return []
