---
description: Use for the WEEX Trader Lite workflow in OpenClaw: natural-language spot/futures trading, market/account queries, and fully authorized automated strategies.
name: weex-trader-skill
---

# WEEX Trader Skill — Lite Edition

The final published project is [weex-agent-skills-lite](https://github.com/weex-labs/weex-agent-skills-lite).

This project is the OpenClaw-only WEEX Trader Lite skill. It keeps the formal Trader trading and account/market behavior, including the complete automated-strategy authorization path, while omitting the separate Analysis, Monitor, and Partner skills.

The repository is the source of truth. Do not infer unsupported endpoints or fall back to another skill. Before any private query, order preview, profile/Vault operation, or automatic-order operation, run the Trader preflight and stop when runtime, environment, profile, or dependency checks are not ready.

## OpenClaw installation

Use the project updater, not `gh skill install` or another host installer:

```bash
bash skills/weex-trader-skill/scripts/update_openclaw_skills.sh
```

For a published release, set `WEEX_OPENCLAW_APPROVED_COMMIT` to the release commit and run without `--dev`. Production mode accepts only the configured Lite repository, `main`, and that immutable commit pin.

For an explicitly selected local development checkout only:

```bash
WEEX_OPENCLAW_REPO_URL=/path/to/weex-agent-skills-lite \
WEEX_OPENCLAW_BRANCH=feature/competition-openclaw \
bash skills/weex-trader-skill/scripts/update_openclaw_skills.sh --dev
```

The updater validates the checkout, refreshes only `~/.openclaw/skills/weex-trader-skill`, keeps a stable updater copy, and rolls back links on failure. This project does not provide Codex, Claude Code, Cursor, GitHub Copilot, or other host installation workflows.

## Core capabilities

- Natural-language spot and futures trading with explicit market, symbol, side, position direction, order type, quantity, price, and TP/SL interpretation.
- Manual order previews expose only the structured order summary and fixed confirmation prompt. A plain market order also includes the concise fixed notice: `价格提示：实际成交价可能随市场波动，请以 WEEX 最终成交结果为准。` An exact confirmation submits the bound preview order without another price-volatility check. Risk-analysis alerts remain internal safety checks, not user-facing dialogue.
- Missing-field and ambiguity questions; never guess a quantity unit, account, symbol, trading mode, or side.
- Product-rule validation, structured order preview, exact independent confirmation, order placement/cancellation, official conditional orders, TP/SL, order status, positions, and trade details.
- Public spot/futures price, K-line, depth, and funding-rate queries.
- Private spot/futures balance, available/frozen balance, positions, open/history orders, and fills, with explicit real-trading or demo-trading mode and an environment prefix.
- Complete saved-profile automated-strategy authorization: stable strategy identity, scope, per-leg and cumulative conservative-amount limits, validity, revocation, audit, guarded submission, reconciliation, snapshots, and restore safety.

The following are intentionally not conversational capabilities of this project: replay collection for analysis, trading-profile generation, deep account-risk interpretation, PnL monitor tasks, local automatic-close loops, Partner/referral queries, or Partner writes. Saved profile/Vault management remains only the credential boundary for Trader and automatic authorization. A price-threshold close must use an official WEEX conditional order through Trader; do not create a local monitor.

## Entry points and routing

- `scripts/weex_contract_api.py`: contract/futures market, private account, order, cancellation, and official simulated-futures REST.
- `scripts/weex_spot_api.py`: spot market, private account, order, and cancellation REST.
- `scripts/weex_trade_guard.py`: `preview-order`, `preview-tp-sl`, `confirm-order`, `confirm-tp-sl`, `preview-cancel`, and `confirm-cancel` for safe order flows.
- `scripts/weex_order_intent_state.py`: pending preview identity, TTL, and risk-signature binding.
- `scripts/weex_auto_trade.py`: stable JSON facade for strategy registration, authorization, guarded automatic submission, reconciliation, events, snapshots, and restore.
- `scripts/weex_auto_trade_state.py`, `weex_auto_trade_amount.py`, `weex_auto_trade_runtime.py`, and `weex_auto_trade_notify.py`: the complete local authorization, valuation, official-fact, audit, notification, and recovery implementation behind the facade.
- `scripts/weex_agent_state.py`: preflight and non-secret runtime/profile summary.
- `scripts/weex_profiles*.py`, `weex_profile_store.py`, and `weex_vault*.py`: saved-profile and application-vault setup. Never put a secret on argv.

Use the matching contract or spot definitions in `references/contract-api-definitions.json` and `references/spot-api-definitions.json`. Unknown operations and paths are rejected.

## Runtime and profile rules

Run `python3 scripts/weex_agent_state.py --command skill.preflight --language zh --pretty` before routing. A complete runtime environment may supply `WEEX_API_KEY`, `WEEX_API_SECRET`, and `WEEX_API_PASSPHRASE` together; a partial set fails closed. An explicit saved profile takes precedence over environment credentials. The selected profile must be unambiguous; never guess from list order or name similarity.

For private account queries, require the user to choose `真实盘` or `模拟盘` before calling private commands. For order previews, follow the formal preview-only default policy when mode is omitted, then show the mode and funds warning in the confirmation block. Demo trading is official futures demo REST, not a local dry-run; spot demo and unsupported demo conditional endpoints fail closed.

## Safe order flow

1. Parse the user intent and ask only for missing or ambiguous fields.
2. Call `preview-order`, `preview-tp-sl`, or `preview-cancel`; never call direct mutating API commands from the conversational path.
3. Return the guard's `user_confirmation.reply_instruction` verbatim, including environment prefix, funds warning, order summary, the concise fixed plain-market price notice when applicable, exact reply text, and any mode-switch text. Do not expand that notice with extra risk-analysis prompts.
4. Submit only after a subsequent independent user message exactly matches the latest `user_confirmation.reply_text`, passing that text to the confirm command as `--user-reply`. Keep `intent_id` and `risk_signature` internal. For a plain `MARKET` order, the exact confirmation authorizes direct submission of the signed preview order parameters without re-fetching or comparing market-price facts; final execution is determined by WEEX. Order fields, profile, mode, TTL, confirmation text, signature, and required live/demo flags remain binding. Limit orders, conditional orders, TP/SL, and manual fallbacks from automatic authorization retain their existing fresh-fact checks.
5. Use `--confirm-live` for real trading and `--trading-mode demo --confirm-demo` for official futures demo writes. A timeout or uncertain response is `review_required`; do not retry, split, or guess.

All private summaries start with the returned `user_environment_prefix` (`真实盘` or `模拟盘`). Do not expose credentials, vault passwords, raw headers, full private snapshots, or internal confirmation signatures.

## Automated-strategy authorization

This is a complete saved-profile, real-trading-only authorization path. It does not authorize demo trading or discover arbitrary scripts.

- Register a stable `strategy_id`; restarts and renames reuse it, while a copied strategy receives a new identity.
- Every request includes `trade_types` (`SPOT`, `FUTURES`, or both), symbols or all symbols, maximum conservative U amount per leg, cumulative conservative U quota, and explicit `valid_hours` (greater than 0 and no more than 720 hours). Do not derive the cumulative quota from frequency, balance, validity, target amount, or expected order count.
- Show the full profile name, masked strategy ID, modules, symbols, per-leg limit, cumulative quota, validity, effect on per-order confirmation, revoke action, and local trust boundary. Grant requires the exact request and `--confirm-live`; a pending request grants no authority and expires after 15 minutes.
- Only explicit official Spot/Futures order operations enter the automatic path. Fresh product, market, depth, fee, leverage, conversion, balance, scope, quota, and risk facts are required as internal authorization guards; they are not exposed as a manual order risk prompt. Missing, stale, degraded, incomplete, unconvertible, or unproven facts return to manual preview and confirmation.
- Reserve all batch legs atomically before any WEEX write. Keep strategy, authorization, usage, submission group, client order ID, and WEEX order ID mappings per leg. Explicit rejection releases a reservation; an uncertain result or mapping remains `REVIEW_REQUIRED` and is never retried.
- Full-position TP/SL and unproven reduce-only orders remain manual. Normal advisories do not block an in-scope automatic order; hard constraints, scope/quota violations, state conflicts, revoked/expired authorization, or unsupported operations block every write.
- Accepted conservative quota is not refunded by later reconciliation. Reconciliation records exchange status, fills, quote amount, and fees separately and never changes accepted authorization usage.
- When an order falls back from automatic authorization to manual confirmation, include the fixed prompt: `如需取消二次确认功能，可申请自动交易授权。授权后，在指定交易类型、交易对、单笔金额和有效期范围内，下单无需逐笔确认。发送“申请自动交易授权”即可开始配置。`
- `snapshot-state` and `restore-state` are explicit local operations through the facade. Restore enables the kill switch before lookup, validates the registered snapshot, revokes restored active authorizations, preserves unresolved usage for manual review, and never merges ledgers or acts on exchange orders. Snapshots are owner-only local files, not password-encrypted backups and never uploaded automatically.
- Authorization and local state checks are misuse/corruption controls, not identity authentication or tamper-proofing against an attacker controlling the same OS user, Agent, Vault session, or API key.

Use `references/script-operations.md` for exact JSON commands and lifecycle details. Strategies must invoke the facade as a subprocess and must not import the state kernel or write its database directly.

## Failure and boundary policy

- Never send a mutating request without the required confirmation flag.
- Never use Analysis, Monitor, or Partner endpoints from this project.
- Never treat missing demo equivalents as live equivalents; report degraded data.
- Never return stale or default account/market data after an API error.
- Never retry an order after an uncertain submission; preserve the result for manual reconciliation.
- Never interpret local permissions, SQLite integrity, or audit events as a remote trust or identity proof.
