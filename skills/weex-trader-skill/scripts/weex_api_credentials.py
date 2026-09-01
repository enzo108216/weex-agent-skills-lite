#!/usr/bin/env python3
"""Lightweight credential loading for container-based WEEX API access."""

from __future__ import annotations

import os
import hashlib
import hmac
from dataclasses import dataclass, field
from typing import Mapping, Optional


API_KEY_ENV = "WEEX_API_KEY"
API_SECRET_ENV = "WEEX_API_SECRET"
API_PASSPHRASE_ENV = "WEEX_API_PASSPHRASE"
ENVIRONMENT_CREDENTIAL_NAMES = (API_KEY_ENV, API_SECRET_ENV, API_PASSPHRASE_ENV)
DEFAULT_CONTRACT_API_BASE = "https://api-contract.weex.com"
DEFAULT_SPOT_API_BASE = "https://api-spot.weex.com"


@dataclass(frozen=True, repr=False)
class ApiCredentials:
    api_key: str
    api_secret: str
    api_passphrase: str


@dataclass(frozen=True, repr=False)
class EnvironmentAccount:
    """Opaque local identity for the currently injected WEEX credentials."""

    account_id: str = field(repr=False)
    credentials: ApiCredentials = field(repr=False)
    credential_source: str = "environment"

    def __repr__(self) -> str:
        return "EnvironmentAccount(credential_source='environment')"


def load_environment_credentials(
    env: Optional[Mapping[str, str]] = None,
) -> Optional[ApiCredentials]:
    """Return the standard WEEX environment credentials or fail on a partial set."""

    source = os.environ if env is None else env
    present = [name for name in ENVIRONMENT_CREDENTIAL_NAMES if name in source]
    if not present:
        return None

    values = {
        name: str(source.get(name) or "").strip()
        for name in ENVIRONMENT_CREDENTIAL_NAMES
    }

    missing = [name for name, value in values.items() if not value]
    if missing:
        raise SystemExit(
            "WEEX environment credentials must set WEEX_API_KEY, WEEX_API_SECRET, "
            "and WEEX_API_PASSPHRASE together. Missing: " + ", ".join(missing)
        )

    return ApiCredentials(
        api_key=values[API_KEY_ENV],
        api_secret=values[API_SECRET_ENV],
        api_passphrase=values[API_PASSPHRASE_ENV],
    )


def load_environment_account(
    env: Optional[Mapping[str, str]] = None,
) -> EnvironmentAccount:
    """Load the only supported private credential source and derive a safe account binding."""

    source = os.environ if env is None else env
    credentials = load_environment_credentials(source)
    if credentials is None:
        raise SystemExit(
            "WEEX_API_KEY, WEEX_API_SECRET, and WEEX_API_PASSPHRASE are required "
            "in the runtime environment for private WEEX commands."
        )
    shared_base = str(source.get("WEEX_API_BASE") or "").strip()
    contract_base = str(
        source.get("WEEX_CONTRACT_API_BASE") or shared_base or DEFAULT_CONTRACT_API_BASE
    ).strip().rstrip("/")
    spot_base = str(
        source.get("WEEX_SPOT_API_BASE") or shared_base or DEFAULT_SPOT_API_BASE
    ).strip().rstrip("/")
    binding = "\0".join(
        (
            "weex-environment-account-v1",
            credentials.api_key,
            credentials.api_passphrase,
            contract_base,
            spot_base,
        )
    ).encode("utf-8")
    digest = hmac.new(
        credentials.api_secret.encode("utf-8"),
        binding,
        hashlib.sha256,
    ).hexdigest()
    return EnvironmentAccount(
        account_id=f"env-{digest}",
        credentials=credentials,
    )
