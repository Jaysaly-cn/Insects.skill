#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search_pest.py — Search pest ontology data by keyword.

Usage:
    python scripts/search_pest.py <keyword>

The script reads data/pest_ontology.json and searches across pest_id,
name_cn, name_en, name_latin, and aliases fields.

In the current framework version (v0.1.0), the data file is empty.
The script handles this gracefully and reports "no records found".
"""

import json
import sys
import os


def load_ontology(data_path: str) -> list:
    """Load pest ontology data from a JSON file.

    Returns an empty list if the file does not exist or is invalid.
    """
    if not os.path.exists(data_path):
        return []

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, OSError):
        return []


def search_pests(ontology: list, keyword: str) -> list:
    """Search ontology records for a keyword.

    Matches against pest_id, name_cn, name_en, name_latin, and aliases.
    Case-insensitive.
    """
    keyword_lower = keyword.strip().lower()
    if not keyword_lower:
        return []

    results = []
    searchable_fields = ["pest_id", "name_cn", "name_en", "name_latin", "aliases"]

    for entry in ontology:
        for field in searchable_fields:
            value = entry.get(field, "")
            if isinstance(value, list):
                # aliases is a list
                for alias in value:
                    if keyword_lower in alias.lower():
                        results.append(entry)
                        break
                else:
                    continue
                break
            elif isinstance(value, str):
                if keyword_lower in value.lower():
                    results.append(entry)
                    break

    return results


def format_result(entry: dict) -> str:
    """Format a single search result for display."""
    lines = []
    lines.append(f"  pest_id:    {entry.get('pest_id', 'N/A')}")
    lines.append(f"  name_cn:    {entry.get('name_cn', 'N/A')}")
    lines.append(f"  name_en:    {entry.get('name_en', 'N/A')}")
    lines.append(f"  name_latin: {entry.get('name_latin', 'N/A')}")
    aliases = entry.get("aliases", [])
    if aliases:
        lines.append(f"  aliases:    {', '.join(aliases)}")
    lines.append(f"  risk_level: {entry.get('risk_level', 'N/A')}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/search_pest.py <keyword>")
        sys.exit(1)

    keyword = sys.argv[1]

    # Determine data path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "pest_ontology.json")
    data_path = os.path.normpath(data_path)

    ontology = load_ontology(data_path)

    if not ontology:
        print("No records found in the pest ontology database.")
        print(f"Data file: {data_path}")
        print("The knowledge base is currently empty (framework version).")
        return

    results = search_pests(ontology, keyword)

    if not results:
        print(f"No pests found matching keyword: {keyword}")
    else:
        print(f"Found {len(results)} result(s) for '{keyword}':")
        print("-" * 40)
        for i, entry in enumerate(results, 1):
            print(f"[{i}]")
            print(format_result(entry))
            print()


if __name__ == "__main__":
    main()
