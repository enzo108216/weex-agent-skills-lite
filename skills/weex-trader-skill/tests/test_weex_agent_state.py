#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import weex_agent_state as agent_state  # noqa: E402


class AgentStateEnvironmentOnlyTests(unittest.TestCase):
    def test_init_routes_every_private_flow_to_complete_environment_credentials(self) -> None:
        payload = agent_state.build_agent_init_state("zh")

        self.assertNotIn("profiles", payload)
        self.assertNotIn("vault", payload)
        self.assertEqual(
            payload["routes"]["private_api_requires"],
            [
                "direct_contract_spot:complete_environment_credentials",
                "trade_guard:complete_environment_credentials",
                "automated_authorization:complete_environment_credentials",
            ],
        )
        self.assertEqual(payload["credentials"]["source"], "environment")

    def test_preflight_without_language_clears_previous_cached_preference(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            init_path = Path(tempdir) / agent_state.AGENT_INIT_FILENAME
            init_path.write_text(
                json.dumps({"language": {"preferred": "zh"}}),
                encoding="utf-8",
            )
            with mock.patch.dict(
                os.environ,
                {"WEEX_TRADER_SKILL_HOME": tempdir},
                clear=True,
            ):
                records = agent_state.refresh_agent_records(command="skill.preflight")

                self.assertEqual(
                    records["init"]["language"],
                    {"preferred": None, "source": "unset"},
                )
                self.assertEqual(agent_state.resolve_language_with_source(), ("en", "default"))

    def test_runtime_reports_presence_without_exposing_values(self) -> None:
        credentials = {
            "WEEX_API_KEY": "env-api-key",
            "WEEX_API_SECRET": "env-api-secret",
            "WEEX_API_PASSPHRASE": "env-api-passphrase",
        }
        with mock.patch.dict(os.environ, credentials, clear=True):
            payload = agent_state.build_agent_runtime_state()

        self.assertTrue(payload["credentials"]["complete"])
        self.assertEqual(
            payload["credentials"]["present"],
            {name: True for name in credentials},
        )
        serialized = json.dumps(payload)
        for value in credentials.values():
            self.assertNotIn(value, serialized)

    def test_blank_or_partial_environment_credentials_are_not_complete(self) -> None:
        with mock.patch.dict(
            os.environ,
            {
                "WEEX_API_KEY": " ",
                "WEEX_API_SECRET": "present",
                "WEEX_API_PASSPHRASE": "\t",
            },
            clear=True,
        ):
            payload = agent_state.build_agent_runtime_state()

        self.assertFalse(payload["credentials"]["complete"])
        self.assertEqual(
            payload["credentials"]["present"],
            {
                "WEEX_API_KEY": False,
                "WEEX_API_SECRET": True,
                "WEEX_API_PASSPHRASE": False,
            },
        )

    def test_runtime_environment_validation_rejects_partial_credentials_and_invalid_overrides(self) -> None:
        partial = agent_state.validate_runtime_environment({"WEEX_API_KEY": "only-key"})
        self.assertFalse(partial["ok"])
        self.assertTrue(any("provided together" in item for item in partial["issues"]))

        invalid = agent_state.validate_runtime_environment(
            {
                "WEEX_API_TIMEOUT": "0",
                "WEEX_SPOT_API_BASE": "http://example.com",
            }
        )
        self.assertFalse(invalid["ok"])
        self.assertEqual(len(invalid["issues"]), 2)

    def test_refresh_writes_owner_only_non_secret_cache_files(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            env = {
                "WEEX_TRADER_SKILL_HOME": tempdir,
                "WEEX_API_KEY": "key",
                "WEEX_API_SECRET": "secret",
                "WEEX_API_PASSPHRASE": "passphrase",
            }
            with mock.patch.dict(os.environ, env, clear=True):
                records = agent_state.refresh_agent_records(
                    preferred_language="en",
                    command="test.preflight",
                )
                init_path = agent_state.agent_init_path()
                runtime_path = agent_state.agent_runtime_path()

            self.assertEqual(records["runtime"]["command"], "test.preflight")
            self.assertEqual(stat.S_IMODE(init_path.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(runtime_path.stat().st_mode), 0o600)
            combined = init_path.read_text() + runtime_path.read_text()
            self.assertNotIn("secret", combined)
            self.assertNotIn("passphrase", combined)

    def test_private_runtime_preflight_preserves_dependency_and_environment_fail_closed_checks(self) -> None:
        with mock.patch.object(agent_state, "_probe_required_modules", return_value=(False, ["requests"])):
            with mock.patch.object(
                agent_state,
                "validate_runtime_environment",
                return_value={"ok": False, "issues": ["bad environment"]},
            ):
                with self.assertRaises(agent_state.RuntimePreflightError) as raised:
                    agent_state.ensure_private_runtime_ready(command="private.test")

        self.assertEqual(raised.exception.missing_modules, ("requests",))
        self.assertEqual(raised.exception.env_issues, ("bad environment",))


if __name__ == "__main__":
    unittest.main()
