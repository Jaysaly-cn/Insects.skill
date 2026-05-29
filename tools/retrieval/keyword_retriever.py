"""
Keyword Retriever — 关键词检索工具

职责：基于关键词匹配的知识检索。
"""

from typing import Dict, Any, List, Optional
import json
import os


def keyword_search(query: str, domain: Optional[str] = None, top_k: int = 5) -> List[Dict[str, Any]]:
    """关键词检索（Mock）"""
    return []


def search_knowledge_base(query: str, domain: str) -> List[Dict[str, Any]]:
    """通用知识库检索"""
    return []
