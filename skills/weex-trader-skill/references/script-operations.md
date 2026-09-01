# Script Operations

All commands in this reference are for the OpenClaw checkout. Run them from the skill root or use absolute paths. Python 3 and the pinned `requirements.lock` are required for saved profiles, Vault, trade guard, aggregation, and automated authorization.

## Preflight and runtime

```bash
python3 scripts/weex_agent_state.py --command skill.preflight --language zh --pretty
python3 scripts/weex_runtime_setup.py --pretty
python3 scripts/weex_doctor.py gui --pretty
```

Stop when `runtime.host.requirements_ready` is false, dependencies are missing, or `runtime.env_validation.ok` is false. Do not print secret values.

## Profiles and Vault

Use `scripts/weex_profiles_zh.py`/`scripts/weex_profiles_en.py` or the `scripts/weex_profiles.py` wrapper. Use `scripts/weex_vault_cli.py`, `scripts/weex_vault_zh.py`, or `scripts/weex_vault_en.py` for the application Vault. Prefer `--prompt-secrets`, environment secret names, or `--secrets-stdin-json`; never put API secrets or Vault passwords directly on argv.

Before editing, deleting, or changing a default profile, run the localized `list --pretty` command. A saved profile contains a name, stable profile ID, API key/secret/passphrase, optional note, and optional validated contract/spot base URLs. Profile and Vault state is local; it is not part of this project checkout.

## Market, account, and trading commands

```bash
python3 scripts/weex_contract_api.py ticker --symbol BTCUSDT --pretty
python3 scripts/weex_spot_api.py ticker --symbol BTCUSDT --pretty
python3 scripts/weex_contract_api.py call --endpoint market.get_klines --query '{"symbol":"BTCUSDT","interval":"1m","limit":10}' --pretty
python3 scripts/weex_spot_api.py call --endpoint spot.market.get_depth_data --query '{"symbol":"BTCUSDT","limit":20}' --pretty
```

Private account commands require an explicit trading mode (`live`/`demo` internally, displayed as `真实盘`/`模拟盘`) and a selected saved profile or a complete runtime credential set. Demo private futures use only documented `sim.*` endpoints; demo spot and missing demo equivalents fail closed.

Natural-language orders must use the guard:

```bash
python3 scripts/weex_trade_guard.py preview-order --profile <name> --language zh --order-json '{...}' --pretty
python3 scripts/weex_trade_guard.py confirm-order --profile <name> --language zh --user-reply '确认' --confirm-live --pretty
```

Use `preview-tp-sl`/`confirm-tp-sl` for official futures TP/SL. The confirmation command must consume the exact reply text from the latest independent preview via `--user-reply`; changed fields, mode, expired intents, stale facts, and mismatches are rejected. Real writes require `--confirm-live`; official futures demo writes require `--trading-mode demo --confirm-demo`.

A plain `MARKET` preview includes the concise fixed notice: `价格提示：实际成交价可能随市场波动，请以 WEEX 最终成交结果为准。` Once the user sends the exact independent confirmation, the guard submits the signed preview order parameters without re-fetching or comparing market-price facts. This exception does not change the 300-second TTL, intent signature, profile/mode binding, confirmation flags, uncertain-submission handling, or the fresh-fact checks for limit orders, conditional orders, TP/SL, and automatic-authorization fallbacks.

Order cancellation uses the same binding:

```bash
python3 scripts/weex_trade_guard.py preview-cancel --profile <name> --market futures --order-id <id> --language zh --pretty
python3 scripts/weex_trade_guard.py confirm-cancel --profile <name> --intent-id <id> --risk-signature <signature> --user-reply '确认' --pretty
```

## Automated-strategy authorization

The JSON facade is the only supported automatic-order boundary. Strategies call it as a subprocess and never import the SQLite state kernel.

```bash
python3 scripts/weex_auto_trade.py register-strategy --input @register-strategy.json --pretty
python3 scripts/weex_auto_trade.py list-strategies --input @profile.json --pretty
python3 scripts/weex_auto_trade.py ensure-authorization --input @ensure-authorization.json --pretty
python3 scripts/weex_auto_trade.py show-authorization-request --input @show-authorization-request.json --pretty
python3 scripts/weex_auto_trade.py grant-authorization --input @grant-authorization.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py list-authorizations --input @profile.json --pretty
python3 scripts/weex_auto_trade.py submit-auto --input @submit-auto.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py revoke-authorization --input @revoke-authorization.json --pretty
python3 scripts/weex_auto_trade.py retire-strategy --input @retire-strategy.json --pretty
python3 scripts/weex_auto_trade.py event-list --input @strategy.json --pretty
python3 scripts/weex_auto_trade.py reconcile-auto-order --input @reconcile-auto-order.json --pretty
python3 scripts/weex_auto_trade.py resolve-auto-usage --input @resolve-auto-usage.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py snapshot-state --input @snapshot-state.json --pretty
python3 scripts/weex_auto_trade.py restore-state --input @restore-state.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py enable-auto-trading-after-restore --input @enable-auto-trading.json --confirm-live --pretty
```

Every authorization request includes Spot/Futures modules, selected symbols or all symbols, conservative per-leg U maximum, cumulative conservative U quota, and `valid_hours` greater than 0 and no more than 720 hours. Never derive the cumulative quota. Granting changes local authorization state and does not submit an order. Automatic submissions still require fresh official facts, product/risk/balance checks, scope/quota checks, atomic reservations, and durable per-leg audit. Unknown or uncertain results become `REVIEW_REQUIRED` and are never retried.

Use `event-list`, `reconcile-auto-order`, and `resolve-auto-usage` for read-only audit/reconciliation. Accepted conservative usage is never refunded by later fills or lower fees. Full-position TP/SL, unproven reduce-only behavior, missing conversion/depth/leverage/fee facts, and unsupported operations return to manual preview.

## Snapshot and restore

```bash
python3 scripts/weex_auto_trade.py snapshot-state --profile <name> --pretty
python3 scripts/weex_auto_trade.py restore-state --profile <name> --snapshot-id <registered-id> --pretty
```

Snapshots are owner-only local files in the Trader-managed directory, not encrypted backups and never uploaded automatically. Restore enables the kill switch first, validates a registered snapshot, revokes restored active authorizations, preserves unresolved usage for manual reconciliation, and never merges ledgers or acts on exchange orders.
