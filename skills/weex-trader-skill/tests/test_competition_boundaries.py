from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


class CompetitionBoundaryTests(unittest.TestCase):
    def test_project_contains_only_the_trader_skill(self) -> None:
        skill_dirs = sorted(
            path.name
            for path in (ROOT.parent).iterdir()
            if path.is_dir() and (path / "SKILL.md").exists()
        )
        self.assertEqual(skill_dirs, ["weex-trader-skill"])

    def test_manifest_is_openclaw_only_and_keeps_auto_authorization(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["host_support"]["openclaw"]["supported"])
        self.assertFalse(manifest["host_support"]["other_hosts"]["supported"])
        self.assertEqual(manifest["host_support"]["openclaw"]["linked_skills"], ["weex-trader-skill"])
        self.assertIn("submit-auto", manifest["routing"]["automated_strategy_authorization"]["commands"])

    def test_spot_registry_excludes_partner_rebate_endpoints(self) -> None:
        sys.path.insert(0, str(SCRIPTS))
        import weex_spot_api  # type: ignore

        self.assertTrue(weex_spot_api.ENDPOINTS)
        self.assertFalse(any(key.startswith("spot.rebate.") for key in weex_spot_api.ENDPOINTS))

    def test_openclaw_updater_links_one_skill(self) -> None:
        updater = (SCRIPTS / "update_openclaw_skills.sh").read_text(encoding="utf-8")
        self.assertIn('WEEX_SKILLS=("weex-trader-skill")', updater)
        self.assertNotIn("weex-analysis-skill", updater)
        self.assertNotIn("weex-monitor-skill", updater)
        self.assertNotIn("weex-partner-skill", updater)

    def test_core_cli_help_is_available(self) -> None:
        for script in (
            "weex_contract_api.py",
            "weex_spot_api.py",
            "weex_trade_guard.py",
            "weex_auto_trade.py",
        ):
            completed = subprocess.run(
                [sys.executable, str(SCRIPTS / script), "--help"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, f"{script}: {completed.stderr}")


if __name__ == "__main__":
    unittest.main()
