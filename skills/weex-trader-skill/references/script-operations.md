# Script Operations

Run commands from the skill root. Before private work:

```bash
python3 scripts/weex_agent_state.py --command skill.preflight --language en --pretty
```

Pass the current user's language explicitly to every user-facing command with `--language zh` or
`--language en`. If the host cannot determine the user's language, pass `--language en` for that
invocation. Language is per invocation and is never persisted as a preference.

Continue only when runtime requirements and `runtime.env_validation.ok` are valid and `runtime.credentials.complete` is true. Configure `WEEX_API_KEY`, `WEEX_API_SECRET`, and `WEEX_API_PASSPHRASE` together outside argv/chat.

## Market and account

```bash
python3 scripts/weex_contract_api.py ticker --symbol BTCUSDT --pretty
python3 scripts/weex_spot_api.py ticker --symbol BTCUSDT --pretty
python3 scripts/weex_contract_api.py call --endpoint market.get_klines --query '{"symbol":"BTCUSDT","interval":"1m","limit":10}' --pretty
python3 scripts/weex_spot_api.py call --endpoint spot.market.get_depth_data --query '{"symbol":"BTCUSDT","limit":20}' --pretty
```

Private queries are live-only and always use the real environment. Every private summary includes the real-trading prefix and real-funds warning. Demo modes and `sim.*` endpoints are rejected before any request.

## Guarded orders

```bash
python3 scripts/weex_trade_guard.py preview-order --market futures --trading-mode live --order-json '{...}' --language en --pretty
python3 scripts/weex_trade_guard.py confirm-order --intent-id <id> --risk-signature <signature> --trading-mode live --user-reply '<exact-confirmation-text>' --confirm-live --language en --pretty

python3 scripts/weex_trade_guard.py preview-cancel --market futures --order-id <id> --language en --pretty
python3 scripts/weex_trade_guard.py confirm-cancel --intent-id <id> --risk-signature <signature> --user-reply '<exact-confirmation-text>' --confirm-live --language en --pretty
```

Use `preview-tp-sl`/`confirm-tp-sl` for official Futures TP/SL. The latest intent binds order fields, environment account, mode, TTL, and confirmation text. A plain market order may skip a second price comparison after exact confirmation; other safety bindings and uncertain-submission handling remain.

All writes require `--confirm-live`. Demo flags and simulated endpoints are unsupported.

## Automated-strategy authorization

Every request is a JSON object passed through `--input`; none accepts `profile` or raw credential fields.

```bash
python3 scripts/weex_auto_trade.py register-strategy --input @register-strategy.json --pretty
python3 scripts/weex_auto_trade.py list-strategies --input @empty.json --pretty
python3 scripts/weex_auto_trade.py ensure-authorization --input @ensure-authorization.json --pretty
python3 scripts/weex_auto_trade.py show-authorization-request --input @show-request.json --pretty
python3 scripts/weex_auto_trade.py grant-authorization --input @grant.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py list-authorizations --input @empty.json --pretty
python3 scripts/weex_auto_trade.py submit-auto --input @submit.json --language en --confirm-live --pretty
python3 scripts/weex_auto_trade.py revoke-authorization --input @revoke.json --pretty
python3 scripts/weex_auto_trade.py event-list --input @strategy.json --pretty
python3 scripts/weex_auto_trade.py reconcile-auto-order --input @reconcile.json --pretty
python3 scripts/weex_auto_trade.py resolve-auto-usage --input @resolve.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py snapshot-state --input @snapshot.json --pretty
python3 scripts/weex_auto_trade.py restore-state --input @restore.json --pretty
python3 scripts/weex_auto_trade.py enable-auto-trading-after-restore --input @empty.json --confirm-live --pretty
```

Authorization requests require modules, symbol scope, conservative per-leg maximum, cumulative quota, and explicit `valid_hours` up to 720 hours. Granting changes local state but does not submit an order. Automatic writes still require fresh official facts, scope/quota checks, atomic reservations, durable audit, and `--confirm-live`. Uncertain results are never retried.

`submit-auto` requires `language` in the JSON request and the CLI requires `--language zh|en`. It controls manual-fallback confirmation text and the language carried to the delayed local notification worker. The exact selected confirmation word remains bound to the pending intent.

The full user-facing template inventory and zh/en coverage matrix is in [`message-templates.md`](message-templates.md).

Snapshots are owner-only local files, not encrypted or uploaded. Restore enables the kill switch, validates a registered snapshot, revokes restored active authorizations, preserves unresolved usage, and never acts on WEEX orders. Old saved-profile authorizations are intentionally not migrated to the current environment account.
