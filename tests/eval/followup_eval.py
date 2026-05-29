#!/usr/bin/env python3
"""
Follow-up Evaluation — 追问机制评测脚本
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from graph.nodes.followup_generator import followup_generator


def evaluate():
    cases_path = os.path.join(os.path.dirname(__file__), "..", "test_cases", "insufficient_info_cases.jsonl")

    if not os.path.exists(cases_path):
        print("[SKIP] test cases not found")
        return

    total = 0
    correct = 0

    with open(cases_path, "r", encoding="utf-8") as f:
        for line in f:
            case = json.loads(line)
            total += 1

            state = {
                "user_input": case["input"],
                "critical_missing_slots": case["expected"].get("critical_missing", []),
                "missing_slots": [],
            }
            result = followup_generator(state)

            questions = result.get("followup_questions", [])
            expected_followup = case["expected"].get("should_followup", False)
            has_questions = len(questions) > 0

            if has_questions == expected_followup:
                correct += 1
            else:
                print(f"  FAIL id={case['id']}: expected followup={expected_followup}, got {len(questions)} questions")

    print(f"\n=== Follow-up Eval Results ===")
    print(f"Total: {total}, Correct: {correct} ({correct/total*100:.1f}%)")


if __name__ == "__main__":
    evaluate()
