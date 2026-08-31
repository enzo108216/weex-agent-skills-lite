# WEEX Spot Endpoints (Lite)

Use `references/spot-api-definitions.json` and `references/spot-api-definitions.md` as the endpoint source. The Lite runtime exposes only `spot.account.*`, `spot.config.*`, `spot.market.*`, `spot.order.*`, and `spot.tax.*` entries.

Base URL: `https://api-spot.weex.com`.

```bash
python3 scripts/weex_spot_api.py list-endpoints --pretty
python3 scripts/weex_spot_api.py call --endpoint spot.market.get_ticker_info --query '{"symbol":"BTCUSDT"}' --pretty
```

Conversational mutating Spot calls must use the formal Trader preview/confirmation flow. Explicit low-level operator/API calls still require `--confirm-live` (and are never used as the conversational path).
