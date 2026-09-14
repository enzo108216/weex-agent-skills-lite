---
description: Use for the WEEX Trader Lite workflow in OpenClaw: natural-language spot/futures trading, market/account queries, and fully authorized automated strategies.
name: weex-trader-skill
---

# WEEX Trader Skill — Lite Edition

This repository is the only source of truth. The skill is OpenClaw-only and keeps formal Trader trading/account behavior and complete automated-strategy authorization while omitting separate Analysis, Monitor, and Partner skills.

Before every private query, order preview/confirmation, or automatic-order operation, run:

```bash
python3 scripts/weex_agent_state.py --command skill.preflight --pretty
```

The host should pass the current user's language explicitly to user-facing commands with
`--language zh` or `--language en`; the preflight command above does not select a default language.
If the host provides no language and no cached preference exists, the user-facing fallback is English (`en`).

Stop if runtime requirements are not ready, modules are missing, environment validation fails, or `runtime.credentials.complete` is false.

## Credential boundary

The only private credential source is the complete runtime environment set `WEEX_API_KEY`, `WEEX_API_SECRET`, and `WEEX_API_PASSPHRASE`. All three must be non-empty; missing or partial sets fail closed before a WEEX request. Do not accept credentials from argv, JSON payloads, files, saved profiles, Vaults, keychains, chat, or another fallback.

Optional `WEEX_CONTRACT_API_BASE`, `WEEX_SPOT_API_BASE`, `WEEX_API_BASE`, `WEEX_API_TIMEOUT`, and `WEEX_LOCALE` remain environment-only configuration. Base URLs must pass the WEEX HTTPS allowlist.

The runtime derives an opaque account binding from the credentials and selected Spot/Futures origins. It may be stored only as a non-reversible local state key; never return or print it. Credential or origin changes invalidate pending confirmations and isolate automated authorizations from the previous environment account.

## Routing

- `scripts/weex_contract_api.py`: Futures market/private account/order/cancel and official Futures demo REST.
- `scripts/weex_spot_api.py`: Spot market/private account/order/cancel REST.
- `scripts/weex_trade_guard.py`: `preview-order`, `preview-tp-sl`, `confirm-order`, `confirm-tp-sl`, `preview-cancel`, `confirm-cancel`.
- `scripts/weex_order_intent_state.py`: preview identity, TTL, environment-account and risk-signature binding.
- `scripts/weex_auto_trade.py`: stable JSON facade for strategy registration, authorization, guarded submission, reconciliation, events, snapshots, and restore.
- `scripts/weex_auto_trade_state.py`, `weex_auto_trade_amount.py`, `weex_auto_trade_runtime.py`, `weex_auto_trade_notify.py`: authorization state, conservative valuation, official facts, notification, and recovery implementation.
- `scripts/weex_trade_data_aggregator.py`: internal official account/market facts for guards; not a conversational analysis/replay surface.
- `scripts/weex_agent_state.py`: non-secret preflight and environment readiness summary.
- `scripts/weex_api_credentials.py`: the sole account credential loader and environment-account binding implementation.

Use only operations in `references/contract-api-definitions.json` and `references/spot-api-definitions.json`. Unknown operations and paths are rejected.

## Account queries and safe order flow

Private account queries require the user to choose `真实盘` or `模拟盘` before calling private commands. Demo trading means official Futures demo REST; Spot demo and unsupported demo endpoints fail closed. Every private summary starts with the returned `user_environment_prefix`.

1. Parse intent and ask only for missing/ambiguous fields; never guess quantity unit, symbol, side, or mode.
2. Call the appropriate preview command; never call a direct mutating API command from conversation.
3. Return `user_confirmation.reply_instruction` verbatim.
4. Submit only after a later independent message exactly matches `user_confirmation.reply_text`, using the current intent ID/risk signature internally. Order fields, environment account, mode, TTL, confirmation text, and required flags remain bound.
5. Use `--confirm-live` for real trading and `--trading-mode demo --confirm-demo` for official Futures demo writes. A timeout or uncertain response is `REVIEW_REQUIRED`; never retry, split, or guess.

A plain market order may skip a second price comparison after exact confirmation, but all other confirmation, account, mode, TTL, and submission-uncertainty guards remain. Limit, conditional, TP/SL, and automatic-fallback paths retain fresh-fact checks.

## Automated-strategy authorization

Automatic authorization is environment-account-bound and real-trading-only. It never accepts raw credentials or an account/profile selector in its JSON requests.

- Register a stable `strategy_id`; every authorization specifies `trade_types`, symbols/all-symbols, maximum conservative U per leg, cumulative conservative U quota, and explicit `valid_hours` greater than 0 and no more than 720 hours.
- Never infer cumulative quota or validity. Show credential source, masked strategy ID, modules, symbols, limits, validity, per-order-confirmation effect, revoke action, and local trust boundary. Grant requires the exact request and `--confirm-live`.
- Only explicit official Spot/Futures order operations enter automatic submission. Fresh product, market, depth, fee, leverage, conversion, balance, scope, quota, and internal risk facts are mandatory.
- Batch reservations are atomic before any WEEX write. Explicit rejections release reservations; uncertain results remain `REVIEW_REQUIRED` and are never retried.
- Full-position TP/SL and unproven reduce-only paths remain manual. Hard constraints, state conflicts, expired/revoked authorization, unsupported operations, or incomplete facts block every write.
- Reconciliation never changes accepted conservative quota. Snapshots/restores remain owner-only local controls; restore revokes active authorizations, preserves unresolved usage, and never acts on exchange orders.
- Existing saved-profile authorizations are not migrated. After upgrading, register and explicitly authorize the current environment account.

Local state controls misuse/corruption; they are not identity authentication or tamper-proofing against an attacker controlling the same OS user, Agent, process environment, or API key.

## Exclusions and failure policy

Do not expose Analysis, Monitor, Partner, replay, profile analysis, deep account-risk reports, local price/PnL monitor loops, or non-OpenClaw installation. Price-threshold closes use official WEEX conditional orders.

Never send a mutating request without its required confirmation flag. Never return stale/default private data after an API error, retry an uncertain order, expose credentials/internal account IDs/raw headers, or treat a missing demo equivalent as a real-trading equivalent.
