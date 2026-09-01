# Script Operations

Run commands from the skill root. Before private work:

```bash
python3 scripts/weex_agent_state.py --command skill.preflight --language zh --pretty
```

Continue only when runtime requirements and `runtime.env_validation.ok` are valid and `runtime.credentials.complete` is true. Configure `WEEX_API_KEY`, `WEEX_API_SECRET`, and `WEEX_API_PASSPHRASE` together outside argv/chat.

## Market and account

```bash
python3 scripts/weex_contract_api.py ticker --symbol BTCUSDT --pretty
python3 scripts/weex_spot_api.py ticker --symbol BTCUSDT --pretty
python3 scripts/weex_contract_api.py call --endpoint market.get_klines --query '{"symbol":"BTCUSDT","interval":"1m","limit":10}' --pretty
python3 scripts/weex_spot_api.py call --endpoint spot.market.get_depth_data --query '{"symbol":"BTCUSDT","limit":20}' --pretty
```

Private queries require an explicit internal `live`/`demo` mode, displayed to users as `真实盘`/`模拟盘`. Demo private data is limited to documented Futures `sim.*` endpoints; Spot demo and missing equivalents fail closed.

## Guarded orders

```bash
python3 scripts/weex_trade_guard.py preview-order --market futures --trading-mode live --order-json '{...}' --language zh --pretty
python3 scripts/weex_trade_guard.py confirm-order --intent-id <id> --risk-signature <signature> --trading-mode live --user-reply '确认' --confirm-live --language zh --pretty

python3 scripts/weex_trade_guard.py preview-cancel --market futures --order-id <id> --language zh --pretty
python3 scripts/weex_trade_guard.py confirm-cancel --intent-id <id> --risk-signature <signature> --user-reply '确认' --confirm-live --pretty
```

Use `preview-tp-sl`/`confirm-tp-sl` for official Futures TP/SL. The latest intent binds order fields, environment account, mode, TTL, and confirmation text. A plain market order may skip a second price comparison after exact confirmation; other safety bindings and uncertain-submission handling remain.

Real writes require `--confirm-live`. Official Futures demo writes require `--trading-mode demo --confirm-demo`.

## Automated-strategy authorization

Every request is a JSON object passed through `--input`; none accepts `profile` or raw credential fields.

```bash
python3 scripts/weex_auto_trade.py register-strategy --input @register-strategy.json --pretty
python3 scripts/weex_auto_trade.py list-strategies --input @empty.json --pretty
python3 scripts/weex_auto_trade.py ensure-authorization --input @ensure-authorization.json --pretty
python3 scripts/weex_auto_trade.py show-authorization-request --input @show-request.json --pretty
python3 scripts/weex_auto_trade.py grant-authorization --input @grant.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py list-authorizations --input @empty.json --pretty
python3 scripts/weex_auto_trade.py submit-auto --input @submit.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py revoke-authorization --input @revoke.json --pretty
python3 scripts/weex_auto_trade.py event-list --input @strategy.json --pretty
python3 scripts/weex_auto_trade.py reconcile-auto-order --input @reconcile.json --pretty
python3 scripts/weex_auto_trade.py resolve-auto-usage --input @resolve.json --confirm-live --pretty
python3 scripts/weex_auto_trade.py snapshot-state --input @snapshot.json --pretty
python3 scripts/weex_auto_trade.py restore-state --input @restore.json --pretty
python3 scripts/weex_auto_trade.py enable-auto-trading-after-restore --input @empty.json --confirm-live --pretty
```

Authorization requests require modules, symbol scope, conservative per-leg maximum, cumulative quota, and explicit `valid_hours` up to 720 hours. Granting changes local state but does not submit an order. Automatic writes still require fresh official facts, scope/quota checks, atomic reservations, durable audit, and `--confirm-live`. Uncertain results are never retried.

Snapshots are owner-only local files, not encrypted or uploaded. Restore enables the kill switch, validates a registered snapshot, revokes restored active authorizations, preserves unresolved usage, and never acts on WEEX orders. Old saved-profile authorizations are intentionally not migrated to the current environment account.
