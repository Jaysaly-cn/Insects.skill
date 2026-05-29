"""
Reranker — 检索重排序工具

职责：对检索结果进行重排，提高相关性排序。
"""

from typing import Dict, Any, List


def rerank(query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """重排检索结果（Mock）"""
    return documents
