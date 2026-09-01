#!/usr/bin/env python3
"""Persist and validate pending order confirmations for WEEX trade guard flows."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

from weex_agent_state import config_dir


INTENT_FILENAME = "order-intent.json"


def intent_path() -> Path:
    path = config_dir()
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path / INTENT_FILENAME


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            handle.write(serialized)
            handle.flush()
            os.fsync(handle.fileno())
        temporary_path.chmod(0o600)
        os.replace(temporary_path, path)
        temporary_path = None
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY)
        except OSError:
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except OSError:
                pass


def build_risk_signature(
    *,
    account_id: str,
    market: str,
    trading_mode: str,
    order_preview: dict[str, Any],
    analysis_output: dict[str, Any],
    raw_order: dict[str, Any] | None = None,
    intent_type: str = "order",
    environment: dict[str, Any] | None = None,
    tp_sl_order: dict[str, Any] | None = None,
    intent_id: str | None = None,
    created_at: int | None = None,
    expires_at: int | None = None,
    ttl_seconds: int | None = None,
    confirmation_reply_text: str | None = None,
    confirmation_language: str | None = None,
    freshness_required: bool | None = None,
) -> str:
    alerts = analysis_output.get("alerts", []) if isinstance(analysis_output, dict) else None
    fact_binding = (
        analysis_output.get("fact_binding")
        if isinstance(analysis_output, dict)
        else None
    )
    serialized = json.dumps(
        {
            "intent_id": intent_id,
            "intent_type": intent_type,
            "account_id": account_id,
            "market": market,
            "trading_mode": trading_mode,
            "environment": environment,
            "created_at": created_at,
            "expires_at": expires_at,
            "ttl_seconds": ttl_seconds,
            "confirmation_reply_text": confirmation_reply_text,
            "confirmation_language": confirmation_language,
            "freshness_required": freshness_required,
            "order_preview": order_preview,
            "raw_order": raw_order,
            "tp_sl_order": tp_sl_order,
            "alerts": alerts,
            "fact_binding": fact_binding,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def intent_signature_is_valid(
    payload: dict[str, Any],
    *,
    provided_signature: str | None = None,
) -> bool:
    stored_signature = payload.get("risk_signature")
    if not isinstance(stored_signature, str) or not stored_signature:
        return False
    recomputed_signature = build_risk_signature(
        account_id=str(payload.get("account_id") or ""),
        market=str(payload.get("market") or ""),
        trading_mode=str(payload.get("trading_mode") or ""),
        order_preview=payload.get("order_preview"),
        raw_order=payload.get("raw_order"),
        analysis_output=payload.get("analysis_output"),
        intent_type=str(payload.get("intent_type") or "order"),
        environment=payload.get("environment"),
        tp_sl_order=payload.get("tp_sl_order"),
        intent_id=str(payload.get("intent_id") or ""),
        created_at=payload.get("created_at"),
        expires_at=payload.get("expires_at"),
        ttl_seconds=payload.get("ttl_seconds"),
        confirmation_reply_text=payload.get("confirmation_reply_text"),
        confirmation_language=payload.get("confirmation_language"),
        freshness_required=payload.get("freshness_required"),
    )
    if not hmac.compare_digest(stored_signature, recomputed_signature):
        return False
    if provided_signature is None:
        return True
    return hmac.compare_digest(stored_signature, str(provided_signature))


def build_intent(
    *,
    account_id: str,
    market: str,
    trading_mode: str = "live",
    environment: dict[str, Any] | None = None,
    order_preview: dict[str, Any],
    raw_order: dict[str, Any],
    analysis_output: dict[str, Any],
    now_ms: int | None = None,
    ttl_seconds: int = 300,
    intent_type: str = "order",
    tp_sl_order: dict[str, Any] | None = None,
    confirmation_reply_text: str | None = None,
    confirmation_language: str | None = None,
    freshness_required: bool | None = None,
) -> dict[str, Any]:
    current_ms = now_ms if now_ms is not None else int(time.time() * 1000)
    expires_at = current_ms + (ttl_seconds * 1000)
    intent_id = uuid.uuid4().hex
    payload = {
        "intent_id": intent_id,
        "intent_type": intent_type,
        "account_id": account_id,
        "market": market,
        "trading_mode": trading_mode,
        "created_at": current_ms,
        "expires_at": expires_at,
        "ttl_seconds": ttl_seconds,
        "order_preview": order_preview,
        "raw_order": raw_order,
        "analysis_output": analysis_output,
        "confirmation_reply_text": confirmation_reply_text,
        "confirmation_language": confirmation_language,
        "freshness_required": freshness_required,
    }
    if environment is not None:
        payload["environment"] = environment
    if tp_sl_order is not None:
        payload["tp_sl_order"] = tp_sl_order
    payload["risk_signature"] = build_risk_signature(
        account_id=account_id,
        market=market,
        trading_mode=trading_mode,
        order_preview=order_preview,
        raw_order=raw_order,
        analysis_output=analysis_output,
        intent_type=intent_type,
        environment=environment,
        tp_sl_order=tp_sl_order,
        intent_id=intent_id,
        created_at=current_ms,
        expires_at=expires_at,
        ttl_seconds=ttl_seconds,
        confirmation_reply_text=confirmation_reply_text,
        confirmation_language=confirmation_language,
        freshness_required=freshness_required,
    )
    return payload


def save_intent(payload: dict[str, Any]) -> None:
    _atomic_write_json(intent_path(), payload)


def load_intent() -> dict[str, Any] | None:
    path = intent_path()
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return raw if isinstance(raw, dict) else None


def clear_intent() -> None:
    path = intent_path()
    if path.exists():
        path.unlink()


def intent_is_expired(payload: dict[str, Any], *, now_ms: int | None = None) -> bool:
    current_ms = now_ms if now_ms is not None else int(time.time() * 1000)
    try:
        expires_at = int(payload.get("expires_at") or 0)
    except (TypeError, ValueError, OverflowError):
        return True
    return expires_at <= current_ms
