#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_pest_name.py — Normalize pest name strings.

Usage:
    python scripts/normalize_pest_name.py "<name>"

Performs basic string cleaning:
    - Strip leading/trailing whitespace
    - Normalise internal spaces (collapse multiple spaces to one)
    - Convert to lower case (optional, via --lower)
    - Placeholder for future alias resolution

In the current framework version (v0.1.0), alias mapping is empty.
"""

import sys


def normalize(name: str, to_lower: bool = False) -> str:
    """Normalise a pest name string.

    Steps:
        1. Strip leading and trailing whitespace.
        2. Collapse multiple consecutive spaces into one.
        3. Optionally convert to lower case.
        4. Placeholder: resolve known aliases (not yet implemented).

    Args:
        name: Raw pest name string.
        to_lower: If True, convert the result to lower case.

    Returns:
        Normalised name string.
    """
    # Step 1 & 2: strip and normalise spaces
    normalised = " ".join(name.strip().split())

    # Step 3: optional lowercasing
    if to_lower:
        normalised = normalised.lower()

    # Step 4: alias resolution (placeholder)
    # In future versions, this will look up a canonical name from an
    # alias mapping stored in data/ or a config file.
    # Example:
    #   alias_map = load_alias_map()
    #   normalised = alias_map.get(normalised, normalised)

    return normalised


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/normalize_pest_name.py <name> [--lower]")
        sys.exit(1)

    name = sys.argv[1]
    to_lower = "--lower" in sys.argv

    result = normalize(name, to_lower=to_lower)

    print(f"Input:    {name!r}")
    print(f"Output:   {result!r}")
    if to_lower:
        print("Options:  lowercased")
    else:
        print("Options:  case preserved (use --lower to convert to lower case)")


if __name__ == "__main__":
    main()
