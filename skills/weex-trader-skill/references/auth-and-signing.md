# Auth and Signing

Official REST origins:

- Futures: `https://api-contract.weex.com`
- Spot: `https://api-spot.weex.com`
- Overrides must use `https://` on an allowed `weex.com` or `weex.tech` host.

Private headers are `ACCESS-KEY`, `ACCESS-PASSPHRASE`, `ACCESS-TIMESTAMP`, and `ACCESS-SIGN`. The signature message is `timestamp + METHOD + requestPath + optional("?" + queryString) + body`, signed as Base64 HMAC-SHA256.

## Only credential source

Every private direct REST, trade-guard, and automated-authorization path reads these runtime variables together:

- `WEEX_API_KEY`
- `WEEX_API_SECRET`
- `WEEX_API_PASSPHRASE`

A missing or partial set fails before a private WEEX request. Credentials are not accepted through argv, JSON input, files, saved profiles, Vaults, or keychains. Public endpoints do not require credentials.

Optional environment configuration:

- `WEEX_TRADER_SKILL_HOME`: local non-secret cache/authorization state directory.
- `WEEX_API_TIMEOUT`: positive HTTP timeout; never authorizes a retry.
- `WEEX_CONTRACT_API_BASE` / `WEEX_SPOT_API_BASE`: product-specific origin.
- `WEEX_API_BASE`: shared fallback origin.
- `WEEX_LOCALE`: locale header.

The runtime derives an opaque HMAC-based environment-account ID from the credential set and selected origins. It binds pending confirmations and automatic authorizations so a credential/origin change fails closed. The ID and credentials are never included in public output.

Main WEEX reference: <https://www.weex.com/api-doc/spot/QuickStart/Signature>
