# Troubleshooting

## Missing or partial credentials

Symptoms include `environment credentials ... required`, `must be provided together`, or `runtime.credentials.complete: false`.

Set all three non-empty variables in the OpenClaw runtime:

- `WEEX_API_KEY`
- `WEEX_API_SECRET`
- `WEEX_API_PASSPHRASE`

Do not pass values on argv or in facade JSON. Do not mix fields from different WEEX API credentials. Re-run preflight after changing the process environment.

## Authentication or signature rejection

- Confirm the three variables belong to one API credential and have the required WEEX permissions.
- Confirm `WEEX_CONTRACT_API_BASE`, `WEEX_SPOT_API_BASE`, or `WEEX_API_BASE` points to the origin where that credential was issued.
- Check clock accuracy and `references/auth-and-signing.md`.
- Never print signed headers while debugging.

## Invalid runtime override

`WEEX_API_TIMEOUT` must be a positive finite number. API origins must be full allowed WEEX HTTPS URLs. Fix or unset the invalid override, run preflight, and retry only after `runtime.env_validation.ok` is true.

## Environment account changed

If confirmation reports that the environment account changed, the credential set or API origin differs from the preview. Generate a new preview. Do not copy the old intent/account ID or bypass the check.

Automatic strategies and authorizations are isolated by the same binding. After a deliberate credential/origin change, register or select the strategy visible to the new environment account and grant a new authorization. Existing saved-profile authorizations are not migrated.

## Missing Python dependency

Run `python3 scripts/weex_runtime_setup.py --pretty`, then retry with the same interpreter. Installation uses the hashed `requirements.lock`.

## Order rejected or uncertain

- Re-check balance, API permissions, symbol/product rules, mode, and order fields.
- If the result is uncertain or `REVIEW_REQUIRED`, inspect/reconcile the exchange state; never retry automatically.

Useful non-secret checks:

```bash
python3 scripts/weex_agent_state.py --command skill.preflight --pretty
python3 scripts/weex_contract_api.py list-endpoints --pretty
python3 scripts/weex_spot_api.py list-endpoints --pretty
```
