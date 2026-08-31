# weex-trader-skill (Competition / OpenClaw)

This is the only skill shipped by `weex-agent-skills-competition`. It is installed and updated through the OpenClaw updater at `scripts/update_openclaw_skills.sh`.

## Supported workflows

- Spot and futures market data: price, K-line, depth, and funding rate.
- Spot and futures private account data: balances, available/frozen amounts, positions, orders, and fills.
- Natural-language orders: missing-field questions, product validation, preview, exact confirmation, official conditional orders, TP/SL, cancellation, status, and position queries.
- Manual confirmation responses contain only the order summary, mode/funds notice, and the fixed confirmation/automatic-authorization prompt; risk analysis remains internal.
- Complete automated-strategy authorization through `scripts/weex_auto_trade.py`, including stable strategy IDs, Spot/Futures scope, symbol scope, conservative per-leg and cumulative quotas, expiry, revocation, audit, guarded submission, reconciliation, snapshots, and restore.

## Not shipped

There are no Analysis, Monitor, or Partner skills in this project. Replay/profile analysis, deep risk interpretation, PnL monitor loops, local automatic close tasks, Partner queries, and non-OpenClaw host installers are out of scope.

## Safety

Refresh preflight before private work. Use a saved profile/Application Vault or the complete runtime credential set; never put secrets on argv. Conversational orders must use `weex_trade_guard.py preview-order` first and pass the exact independent confirmation returned by the latest preview as `--user-reply`. Real trading requires `--confirm-live`; official futures demo writes require `--trading-mode demo --confirm-demo`. Unknown operations, stale data, mode mismatches, and uncertain submissions fail closed.

## References

- `SKILL.md`: Agent routing and safety contract.
- `references/script-operations.md`: CLI and automated-authorization facade commands.
- `references/contract-api-definitions.json` and `references/spot-api-definitions.json`: REST endpoint source.
