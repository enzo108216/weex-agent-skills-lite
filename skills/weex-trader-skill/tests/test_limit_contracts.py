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
    def test_spot_kline_limit_is_an_optional_query_field(self) -> None:
        endpoint = weex_spot_api.ENDPOINTS["spot.market.get_k_line_data"]
        self.assertIn("limit", endpoint.query_fields)
        client = weex_spot_api.WeexSpotClient(
            base_url="https://api-spot.weex.com",
            timeout=5.0,
            locale="en-US",
            api_key=None,
            api_secret=None,
            api_passphrase=None,
        )
        client._validate_payload_fields(endpoint, {"symbol": "BTCUSDT", "interval": "1m", "limit": 3}, {})

    def test_spot_kline_limit_validates_official_range(self) -> None:
        endpoint = weex_spot_api.ENDPOINTS["spot.market.get_k_line_data"]
        for value in (1, 3, 1000):
            weex_spot_api.validate_endpoint_constraints(endpoint, {"limit": value}, {})
        for value in (0, 1001, "abc", "3.5"):
            with self.subTest(value=value), self.assertRaisesRegex(SystemExit, "limit"):
                weex_spot_api.validate_endpoint_constraints(endpoint, {"limit": value}, {})

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
