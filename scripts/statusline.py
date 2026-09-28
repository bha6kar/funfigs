"""Render Claude's context occupancy using only its supplied session JSON."""

import json
import math
import os
import sys


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) else None


def clean(value):
    return "".join(c for c in str(value) if c.isprintable())[:60]


def render(data, colour=True):
    if not isinstance(data, dict):
        return "Funfigs | context unavailable"
    model = data.get("model") or {}
    context = data.get("context_window") or {}
    if not isinstance(model, dict) or not isinstance(context, dict):
        return "Funfigs | context unavailable"
    label = clean(model.get("display_name") or "Claude")
    pct = number(context.get("used_percentage"))
    size = number(context.get("context_window_size"))
    used = None
    usage = context.get("current_usage")
    if isinstance(usage, dict):
        counts = [number(usage.get(k)) for k in
                  ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")]
        if all(v is not None and v >= 0 for v in counts):
            used = sum(counts)
    if pct is None and used is not None and size and size > 0:
        pct = used / size * 100
    if pct is None:
        occupancy = "context unavailable"
    else:
        pct = max(0, min(100, pct))
        filled = int(pct // 10)
        level = "low" if pct < 50 else "medium" if pct < 80 else "high"
        occupancy = f"context [{'#' * filled}{'-' * (10 - filled)}] {pct:.0f}% used ({level})"
        if colour:
            code = 32 if pct < 50 else 33 if pct < 80 else 31
            occupancy = f"\033[{code}m{occupancy}\033[0m"
        if used is not None and size and size > 0:
            occupancy += f" {used / 1000:.1f}k/{size / 1000:.0f}k tokens"
    parts = [label, occupancy]
    cost = data.get("cost") or {}
    dollars = number(cost.get("total_cost_usd")) if isinstance(cost, dict) else None
    if dollars is not None and dollars >= 0:
        parts.append(f"est. session ${dollars:.2f}")
    return " | ".join(parts)


if __name__ == "__main__":
    try:
        payload = json.load(sys.stdin)
    except (ValueError, UnicodeError):
        payload = None
    print(render(payload, colour=not bool(os.environ.get("NO_COLOR"))))
