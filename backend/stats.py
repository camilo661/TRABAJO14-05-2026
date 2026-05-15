"""
stats.py
Compute dashboard statistics from the in-memory AppState history.
Returns plain Python dicts/lists — no UI dependencies.
"""

from collections import defaultdict
from backend.singleton import AppState


def get_summary() -> dict:
    """
    Returns:
        total_requests, total_income, done, pending, rejected, cancelled,
        rejection_rate (0-100 float)
    """
    history = AppState().get_history()
    done = sum(1 for r in history if r["status"] == "hecho")
    pending = sum(1 for r in history if r["status"] == "pendiente")
    rejected = sum(1 for r in history if r["status"] == "rechazado")
    cancelled = sum(1 for r in history if r["status"] == "cancelado")
    total = len(history)
    income = sum(r["plan_price"] for r in history if r["status"] == "hecho")
    rate = round((rejected / total * 100), 1) if total else 0.0

    return {
        "total_requests": total,
        "total_income": income,
        "done": done,
        "pending": pending,
        "rejected": rejected,
        "cancelled": cancelled,
        "rejection_rate": rate,
    }


def sales_by_operator() -> list[dict]:
    """Returns [{"operator": str, "count": int, "income": int}, ...]"""
    data: dict[str, dict] = defaultdict(lambda: {"count": 0, "income": 0})
    for r in AppState().get_history():
        key = r["operator_name"]
        data[key]["count"] += 1
        if r["status"] == "hecho":
            data[key]["income"] += r["plan_price"]
    return [{"operator": k, **v} for k, v in sorted(data.items())]


def sales_by_tier() -> list[dict]:
    """Returns plan tier distribution: [{"tier": int, "count": int}, ...]"""
    from backend.catalog import get_plan
    counts: dict[int, int] = defaultdict(int)
    for r in AppState().get_history():
        plan = get_plan(r["operator_key"], r["plan_id"])
        if plan:
            counts[plan["tier"]] += 1
    tier_names = {1: "Básico (Tier 1)", 2: "Estándar (Tier 2)", 3: "Premium (Tier 3)"}
    return [
        {"tier": t, "label": tier_names.get(t, f"Tier {t}"), "count": counts[t]}
        for t in sorted(counts)
    ]


def income_today() -> int:
    """Total income from 'hecho' requests processed today."""
    import datetime
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return sum(
        r["plan_price"]
        for r in AppState().get_history()
        if r["status"] == "hecho" and r["timestamp"].startswith(today)
    )
