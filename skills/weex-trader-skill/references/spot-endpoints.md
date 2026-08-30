# WEEX Spot Endpoints (Competition)

Use `references/spot-api-definitions.json` and `references/spot-api-definitions.md` as the endpoint source. The competition runtime exposes only `spot.account.*`, `spot.config.*`, `spot.market.*`, `spot.order.*`, and `spot.tax.*` entries; `weex_spot_api.py` rejects the Partner rebate category.

Base URL: `https://api-spot.weex.com`.

```bash
python3 scripts/weex_spot_api.py list-endpoints --pretty
python3 scripts/weex_spot_api.py call --endpoint spot.market.get_ticker_info --query '{"symbol":"BTCUSDT"}' --pretty
```

All mutating Spot calls require the formal Trader preview/confirmation flow and `--confirm-live`.
