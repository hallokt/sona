"""Rules facade for scorer status aggregation."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from tests.evals.scorers.core import evaluate_case


def score_with_rules(case: Any, output: Dict[str, Any], latency_ms: int) -> Tuple[str, Dict[str, float], List[str]]:
    """Apply Day3 pass/warning/fail rules."""
    return evaluate_case(case, output, latency_ms)

