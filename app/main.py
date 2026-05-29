"""
Plant Protection Agent — 应用入口

提供 CLI 和 API 两种启动方式。
当前阶段使用 Mock 节点，不依赖真实 LLM。
"""

import os
import json
import sys


def run_cli():
    """CLI 交互模式"""
    from graph.build_graph import build_plant_protection_graph
    from graph.state import PlantProtectionState

    print("=" * 50)
    print("🌾 Plant Protection Agent (CLI Mode)")
    print("=" * 50)
    print("输入 'quit' 退出, 'reset' 重置会话")
    print()

    app = build_plant_protection_graph()

    while True:
        user_input = input(">> ").strip()
        if user_input.lower() in ("quit", "exit", "/quit"):
            break
        if user_input.lower() == "reset":
            print("[会话已重置]")
            print()
            continue
        if not user_input:
            continue

        initial_state: PlantProtectionState = {
            "user_input": user_input,
            "image_paths": [],
            "all_domains": [],
            "secondary_domains": [],
            "damaged_parts": [],
            "symptoms": [],
            "insect_morphology": [],
            "disease_signs": [],
            "image_observations": [],
            "visual_candidates": [],
            "missing_slots": [],
            "critical_missing_slots": [],
            "followup_questions": [],
            "candidate_diagnoses": [],
            "safety_warnings": [],
            "unsafe_expressions": [],
            "retrieved_docs": [],
        }

        try:
            result = app.invoke(initial_state)
            final = result.get("final_answer", "(无输出)")
            print()
            print(final)
            print()
        except Exception as e:
            print(f"[Error] {e}", file=sys.stderr)


def run_api():
    """API 服务模式（FastAPI）"""
    try:
        import uvicorn
        from app.api.routes import app as fastapi_app

        host = os.getenv("APP_HOST", "0.0.0.0")
        port = int(os.getenv("APP_PORT", "8000"))
        uvicorn.run(fastapi_app, host=host, port=port)
    except ImportError:
        print("FastAPI 未安装。请运行: pip install fastapi uvicorn")
        sys.exit(1)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "cli"
    if mode == "api":
        run_api()
    else:
        run_cli()
