#!/usr/bin/env python3
"""Language validation and input-to-render routing for localized WEEX flows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SUPPORTED_LANGUAGES = ("zh", "en")
MIN_DETECTED_LANGUAGE_CONFIDENCE = 0.8
LanguageSource = Literal["explicit", "detected", "fallback"]


@dataclass(frozen=True)
class LanguageContext:
    language: str
    source: LanguageSource
    input_language: str | None = None
    confidence: float | None = None
    fallback_reason: str | None = None

    def __post_init__(self) -> None:
        if self.source == "fallback" and self.language != "en":
            raise LanguageMismatchError("fallback language context must render English")


@dataclass(frozen=True)
class LanguageDecision:
    """Invocation-scoped language routing decision for an OpenClaw request."""

    input_language: str | None
    render_language: str
    source: LanguageSource
    confidence: float | None = None
    fallback_reason: str | None = None


class LanguageRequiredError(ValueError):
    """Raised when a localized operation does not receive an explicit language."""


class LanguageMismatchError(ValueError):
    """Raised when a requested render language conflicts with detected input language."""


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


def normalize_detected_language(value: str | None) -> str | None:
    """Normalize a host-detected language without treating unsupported languages as zh."""
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip().lower().replace("-", "_")
    if raw in {"unknown", "und", "auto", "uncertain"}:
        return None
    if raw.startswith("zh") or raw in {"cn", "chinese"}:
        return "zh"
    if raw.startswith("en") or raw in {"english"}:
        return "en"
    return raw


def _validate_confidence(confidence: float | None) -> float | None:
    if confidence is None:
        return None
    try:
        normalized = float(confidence)
    except (TypeError, ValueError) as exc:
        raise ValueError("language confidence must be between 0 and 1") from exc
    if not 0 <= normalized <= 1:
        raise ValueError("language confidence must be between 0 and 1")
    return normalized


def resolve_language_decision(
    input_language: str | None,
    *,
    render_language: str | None = None,
    confidence: float | None = None,
) -> LanguageDecision:
    """Resolve host-detected input language to the zh/en template language."""
    detected = normalize_detected_language(input_language)
    has_input_signal = isinstance(input_language, str) and bool(input_language.strip())
    normalized_confidence = _validate_confidence(confidence)
    if normalized_confidence is not None and normalized_confidence < MIN_DETECTED_LANGUAGE_CONFIDENCE:
        expected = "en"
        source = "fallback"
        fallback_reason = "low_confidence"
    elif detected in SUPPORTED_LANGUAGES:
        expected = detected
        source: LanguageSource = "detected"
        fallback_reason = None
    elif detected is None and render_language is not None and not has_input_signal:
        expected = normalize_language(render_language)
        if expected == "zh":
            raise LanguageMismatchError(
                "input language is required before selecting Chinese render language"
            )
        source = "explicit"
        fallback_reason = None
    elif detected is None:
        expected = "en"
        source = "fallback"
        fallback_reason = "language_undetermined"
    else:
        expected = "en"
        source = "fallback"
        fallback_reason = "unsupported_language"

    if render_language is None:
        selected = expected
    else:
        selected = normalize_language(render_language)
        if selected != expected:
            raise LanguageMismatchError(
                f"render language {selected!r} conflicts with detected input language "
                f"{input_language!r}; expected {expected!r}"
            )

    return LanguageDecision(
        input_language=detected,
        render_language=selected,
        source=source,
        confidence=normalized_confidence,
        fallback_reason=fallback_reason,
    )


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


def language_context_from_decision(decision: LanguageDecision) -> LanguageContext:
    """Convert a host decision into the context consumed by the presenter."""
    return LanguageContext(
        language=decision.render_language,
        source=decision.source,
        input_language=decision.input_language,
        confidence=decision.confidence,
        fallback_reason=decision.fallback_reason,
    )
