# weex-agent-skills-competition

OpenClaw-only WEEX trading-competition skill. The project keeps the formal Trader trading and market/account behavior and the complete saved-profile automated-strategy authorization path, while shipping no separate Analysis, Monitor, or Partner skills.

## Install or update in OpenClaw

From a checkout of this project:

```bash
bash skills/weex-trader-skill/scripts/update_openclaw_skills.sh --dev
```

For a published release, run the same script without `--dev` and set `WEEX_OPENCLAW_APPROVED_COMMIT` to the release commit. Production mode accepts only the competition repository, `main`, and that pinned commit. The updater validates the Git checkout, refreshes the single `weex-trader-skill` link, runs OpenClaw checks, and restores the previous link if validation fails.

## What it supports

- Natural-language spot and futures orders with missing-field questions, product checks, preview, exact independent confirmation, cancellation, official conditional orders, TP/SL, order status, positions, and fills.
- Manual confirmations intentionally omit user-facing risk analysis; the fixed automatic-trading authorization prompt remains available.
- Public spot/futures prices, K-lines, depth, and funding rates.
- Private spot/futures balances, available/frozen amounts, positions, orders, and fills with explicit `真实盘` or `模拟盘` separation.
- Complete automated-strategy authorization through the Trader JSON facade: stable strategy IDs, Spot/Futures scope, symbol scope, conservative per-leg and cumulative quotas, validity, revoke, audit, guarded submission, reconciliation, snapshot, and restore.

## Deliberate exclusions

This project does not install or route to replay/profile analysis, deep account-risk interpretation, PnL monitor tasks, local automatic-close loops, Partner/referral queries, or any non-OpenClaw host installer. Price-threshold closes use official WEEX conditional orders, not a local monitor.

## Credentials and safety

Use the saved profile/Application Vault or inject the complete `WEEX_API_KEY`, `WEEX_API_SECRET`, and `WEEX_API_PASSPHRASE` set through the OpenClaw runtime. Never put secrets on argv or in chat. Every conversational order uses a guard preview first and requires the exact confirmation text from the latest preview via `--user-reply`; real trading requires `--confirm-live`, and official futures demo writes require `--trading-mode demo --confirm-demo`.

See [`skills/weex-trader-skill/SKILL.md`](skills/weex-trader-skill/SKILL.md) and [`skills/weex-trader-skill/references/script-operations.md`](skills/weex-trader-skill/references/script-operations.md) for routing and facade commands.
