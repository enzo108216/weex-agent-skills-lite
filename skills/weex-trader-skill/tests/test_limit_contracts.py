from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import weex_contract_api  # noqa: E402
import weex_spot_api  # noqa: E402
import weex_trade_data_aggregator  # noqa: E402


class LimitContractTests(unittest.TestCase):
    def test_contract_depth_limit_accepts_only_documented_values(self) -> None:
        endpoint = weex_contract_api.ENDPOINTS["market.get_depth_data"]
        for value in (15, 200):
            weex_contract_api.validate_endpoint_constraints(endpoint, {"limit": value}, {})
        with self.assertRaisesRegex(SystemExit, "limit"):
            weex_contract_api.validate_endpoint_constraints(endpoint, {"limit": 20}, {})

    def test_spot_depth_limit_accepts_only_documented_values(self) -> None:
        endpoint = weex_spot_api.ENDPOINTS["spot.market.get_depth_data"]
        for value in (15, 200):
            weex_spot_api.validate_endpoint_constraints(endpoint, {"limit": value}, {})
        with self.assertRaisesRegex(SystemExit, "limit"):
            weex_spot_api.validate_endpoint_constraints(endpoint, {"limit": 20}, {})

    def test_spot_history_uses_official_maximum_and_retries_explicit_parameter_error(self) -> None:
        self.assertLessEqual(weex_trade_data_aggregator.SPOT_ORDER_LIMIT, 200)
        self.assertTrue(
            weex_trade_data_aggregator._should_retry_spot_history_orders_with_safe_limit(
                ValueError("spot.order.history_orders returned {'code': -1142, 'msg': 'limit must be between 1 and 200'}"),
                limit=1000,
            )
        )


if __name__ == "__main__":
    unittest.main()
