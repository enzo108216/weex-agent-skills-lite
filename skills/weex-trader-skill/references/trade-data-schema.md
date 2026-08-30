# Trader Internal Fact Schema

This schema is used internally by the trade guard and automated-authorization runtime. It is not a conversational analysis or monitoring interface.

## Environment

```json
{
  "trading_mode": "live",
  "environment": {
    "trading_mode": "live",
    "market": "futures",
    "uses_real_funds": true
  }
}
```

`live` and `demo` are internal values. User-facing text must use `真实盘` and `模拟盘`. Demo facts are only from official simulated futures endpoints.

## Account and order facts

- `balances[*]`: asset, total, available, frozen/locked and account scope.
- `positions[*]`: market, symbol, side/position side, quantity, entry/open value, current notional/mark price, leverage, margin and liquidation fields when official facts are available.
- `orders[*]`: official order ID, client ID, symbol, side, type, quantity, price, status, mode and timestamps.
- `fills[*]`: official trade/order IDs, quantity, quote amount, fee and fee asset when complete.
- `partial` and `degraded_reasons` are required when a response cannot prove complete coverage. Never replace missing facts with an entry price, default balance, stale response or guessed fee.

## Authorization facts

Automatic authorization uses Decimal strings for conservative per-leg and cumulative U estimates. The state facade binds strategy, authorization, usage, submission group, client order ID, WEEX order ID and durable events. Accepted quota is not changed by later fill reconciliation; uncertain mappings remain `REVIEW_REQUIRED`.
