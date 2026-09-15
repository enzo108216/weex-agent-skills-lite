#!/usr/bin/env python3
"""Strict language validation for the localized WEEX Trader CLI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SUPPORTED_LANGUAGES = ("zh", "en")
LanguageSource = Literal["explicit", "detected", "fallback"]


@dataclass(frozen=True)
class LanguageContext:
    language: str
    source: LanguageSource


class LanguageRequiredError(ValueError):
    """Raised when a localized operation does not receive an explicit language."""


def normalize_language(value: str | None) -> str:
    """Normalize an explicit language value without a cached or fallback preference."""
    if not isinstance(value, str) or not value.strip():
        raise LanguageRequiredError("--language is required; choose zh or en")

    raw = value.strip().lower().replace("-", "_")
    if raw.startswith("zh") or raw in {"cn", "zh_cn", "zh_tw", "zh_hk"} or "chinese" in raw:
        return "zh"
    if raw.startswith("en") or raw in {"english", "en_us", "en_gb"}:
        return "en"
    raise LanguageRequiredError("language must be zh or en")


def resolve_language(language: str | None) -> str:
    """Validate and return the explicitly selected language."""
    return normalize_language(language)


def resolve_language_context(
    language: str | None,
    *,
    source: LanguageSource = "explicit",
) -> LanguageContext:
    """Build the per-invocation language context; never reads persisted preferences."""
    return LanguageContext(language=resolve_language(language), source=source)
