"""
Plant Protection Agent — 配置管理

从环境变量读取所有配置项，提供统一的配置入口。
"""

import os
from typing import Optional


class Settings:
    """应用全局配置"""

    # LLM
    llm_api_key: Optional[str] = os.getenv("LLM_API_KEY")
    llm_model_name: str = os.getenv("LLM_MODEL_NAME", "qwen2.5-vl-72b-instruct")
    llm_base_url: Optional[str] = os.getenv("LLM_BASE_URL")

    # LangGraph
    langgraph_debug: bool = os.getenv("LANGGRAPH_DEBUG", "false").lower() == "true"
    langgraph_max_recursion: int = int(os.getenv("LANGGRAPH_MAX_RECURSION", "25"))

    # Vision
    vlm_enabled: bool = os.getenv("VLM_ENABLED", "false").lower() == "true"
    vlm_model_path: str = os.getenv("VLM_MODEL_PATH", "models/vlm/")

    # Retrieval
    retriever_type: str = os.getenv("RETRIEVER_TYPE", "keyword")
    vector_db_path: str = os.getenv("VECTOR_DB_PATH", "data/vectors/")

    # App
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "info")


settings = Settings()
