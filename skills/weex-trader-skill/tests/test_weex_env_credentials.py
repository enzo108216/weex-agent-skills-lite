#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import weex_agent_state  # noqa: E402
import weex_api_credentials  # noqa: E402
import weex_auto_trade  # noqa: E402
import weex_contract_api  # noqa: E402
import weex_spot_api  # noqa: E402
import weex_trade_guard  # noqa: E402


COMPLETE_ENV = {
    "WEEX_API_KEY": "test-api-key",
    "WEEX_API_SECRET": "test-api-secret",
    "WEEX_API_PASSPHRASE": "test-api-passphrase",
}


class EnvironmentCredentialBoundaryTests(unittest.TestCase):
    def test_environment_account_is_stable_secret_safe_and_host_bound(self) -> None:
        account = weex_api_credentials.load_environment_account(COMPLETE_ENV)
        same_account = weex_api_credentials.load_environment_account(dict(COMPLETE_ENV))
        staging_account = weex_api_credentials.load_environment_account(
            {
                **COMPLETE_ENV,
                "WEEX_CONTRACT_API_BASE": "https://stg-api-contract.weex.tech",
            }
        )

        self.assertEqual(account.account_id, same_account.account_id)
        self.assertNotEqual(account.account_id, staging_account.account_id)
        self.assertEqual(account.credential_source, "environment")
        self.assertTrue(account.account_id.startswith("env-"))
        rendered = repr(account)
        for secret in COMPLETE_ENV.values():
            self.assertNotIn(secret, rendered)

    def test_environment_account_requires_all_three_credentials(self) -> None:
        with self.assertRaisesRegex(SystemExit, "must set"):
            weex_api_credentials.load_environment_account(
                {"WEEX_API_KEY": "only-one-field"}
            )
        with self.assertRaisesRegex(SystemExit, "required"):
            weex_api_credentials.load_environment_account({})

    def test_public_clis_reject_saved_profile_arguments(self) -> None:
        with self.assertRaises(SystemExit):
            weex_contract_api.build_parser().parse_args(
                ["--profile", "legacy", "list-endpoints"]
            )
        with self.assertRaises(SystemExit):
            weex_spot_api.build_parser().parse_args(
                ["--profile", "legacy", "list-endpoints"]
            )
        with self.assertRaises(SystemExit):
            weex_trade_guard.build_parser().parse_args(
                ["preview-cancel", "--profile", "legacy", "--market", "futures", "--order-id", "1"]
            )

    def test_automated_authorization_rejects_profile_input(self) -> None:
        with self.assertRaisesRegex(weex_auto_trade.FacadeError, "unknown fields: profile"):
            weex_auto_trade._validate_command_payload(
                "register-strategy",
                {"profile": "legacy", "strategy_name": "grid"},
            )

    def test_preflight_exposes_only_environment_credential_readiness(self) -> None:
        payload = weex_agent_state.build_agent_runtime_state()

        self.assertNotIn("profiles", payload)
        self.assertNotIn("vault", payload)
        self.assertEqual(payload["credentials"]["source"], "environment")
        self.assertIn(payload["credentials"]["complete"], (True, False))

    def test_profile_and_vault_credential_entrypoints_are_not_shipped(self) -> None:
        forbidden = (
            "weex_profile_store.py",
            "weex_profiles.py",
            "weex_profiles_cli.py",
            "weex_profiles_en.py",
            "weex_profiles_zh.py",
            "weex_vault.py",
            "weex_vault_agent.py",
            "weex_vault_cli.py",
            "weex_vault_en.py",
            "weex_vault_zh.py",
            "weex_linux_profile_wizard.sh",
            "weex_linux_profile_wizard_common.sh",
            "weex_linux_profile_wizard_en.sh",
            "weex_linux_profile_wizard_zh.sh",
        )
        self.assertEqual(
            [name for name in forbidden if (SCRIPTS / name).exists()],
            [],
        )


if __name__ == "__main__":
    unittest.main()
