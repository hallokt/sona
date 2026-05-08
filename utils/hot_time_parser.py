"""Utilities for parsing natural-language hot-topic lookback windows."""

from __future__ import annotations

import os
import re
from typing import Optional


def infer_hot_lookback_hours(text: str) -> Optional[int]:
    """Infer hot-topics lookback hours from natural-language text."""
    s = str(text or "").strip().lower()
    if not s:
        return None

    if "一周" in s or "七天" in s or "7天" in s:
        return 7 * 24
    if "三天" in s or "3天" in s:
        return 3 * 24
    if "两天" in s or "2天" in s:
        return 2 * 24
    if "一天" in s or "24小时" in s:
        return 24
    if "半天" in s or "12小时" in s:
        return 12

    m_day = re.search(r"最近\s*(\d+)\s*天", s)
    if m_day:
        try:
            return int(m_day.group(1)) * 24
        except Exception:
            return None

    m_hour = re.search(r"最近\s*(\d+)\s*小时", s)
    if m_hour:
        try:
            return int(m_hour.group(1))
        except Exception:
            return None

    m_week = re.search(r"最近\s*(\d+)\s*周", s)
    if m_week:
        try:
            return int(m_week.group(1)) * 7 * 24
        except Exception:
            return None

    return None


def apply_hot_lookback_hours(hours: Optional[int]) -> Optional[int]:
    """Apply inferred hot-topic lookback hours to environment variables."""
    if hours is None:
        return None
    normalized = max(1, min(int(hours), 720))
    os.environ["HOT_LOOKBACK_HOURS"] = str(normalized)
    os.environ["HOT_SNAPSHOT_LOOKBACK_HOURS"] = str(max(24, min(normalized, 720)))
    os.environ["HOT_RANK_LOOKBACK_HOURS"] = str(max(24, min(normalized * 2, 1440)))
    return normalized

