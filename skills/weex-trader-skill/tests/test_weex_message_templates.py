from __future__ import annotations

import sys
import json
import unittest
from string import Formatter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import weex_message_templates as templates  # noqa: E402
import weex_language  # noqa: E402
import weex_user_presenter as presenter  # noqa: E402


class WeexMessageTemplateTests(unittest.TestCase):
    def test_supported_languages_have_the_same_template_ids(self) -> None:
        self.assertEqual(set(templates.MESSAGE_TEMPLATES), set(weex_language.SUPPORTED_LANGUAGES))
        self.assertEqual(len(templates.MESSAGE_TEMPLATES), 23)
        locale_dir = ROOT / "references" / "locales"
        for locale in weex_language.SUPPORTED_LANGUAGES:
            self.assertTrue((locale_dir / f"{locale}.json").exists(), locale)
            self.assertEqual(json.loads((locale_dir / f"{locale}.json").read_text())["locale"], locale)
        self.assertEqual(
            set(templates.MESSAGE_TEMPLATES["zh-CN"]),
            set(templates.MESSAGE_TEMPLATES["en-US"]),
        )

    def test_supported_languages_have_matching_template_placeholders(self) -> None:
        formatter = Formatter()
        for template_id in templates.MESSAGE_TEMPLATES["en-US"]:
            with self.subTest(template_id=template_id):
                en_fields = {
                    name
                    for _, name, _, _ in formatter.parse(templates.MESSAGE_TEMPLATES["en-US"][template_id])
                    if name
                }
                zh_fields = {
                    name
                    for _, name, _, _ in formatter.parse(templates.MESSAGE_TEMPLATES["zh-CN"][template_id])
                    if name
                }
                self.assertEqual(en_fields, zh_fields)

    def test_manual_fallback_is_localized_and_confirmation_bound(self) -> None:
        with self.assertRaises(weex_language.LanguageRequiredError):
            templates.build_manual_fallback_confirmation(None, authorization_miss=False)
        chinese = templates.build_manual_fallback_confirmation("zh", authorization_miss=True)
        english = templates.build_manual_fallback_confirmation("en", authorization_miss=True)

        self.assertEqual(chinese["language"], "zh-CN")
        self.assertEqual(chinese["reply_text"], "确认")
        self.assertIn("本次订单超过自动交易授权范围，尚未下单", chinese["reply_instruction"])
        self.assertIn("确认后回复：确认", chinese["reply_instruction"])
        self.assertEqual(english["language"], "en-US")
        self.assertEqual(english["reply_text"], "confirm")
        self.assertIn("was not submitted", english["reply_instruction"])
        self.assertIn("After confirming, reply: confirm", english["reply_instruction"])
        self.assertIn("Request automated trading authorization", english["authorization_hint"])

    def test_manual_fallback_without_authorization_hint_is_localized(self) -> None:
        chinese = templates.build_manual_fallback_confirmation("zh", authorization_miss=False)
        english = templates.build_manual_fallback_confirmation("en", authorization_miss=False)

        self.assertNotIn("申请自动交易授权", chinese["reply_instruction"])
        self.assertNotIn("automated trading authorization", english["reply_instruction"])
        self.assertIn("本次订单未进入自动交易执行，尚未下单", chinese["reply_instruction"])
        self.assertIn("was not submitted through automated trading", english["reply_instruction"])

    def test_notification_text_supports_both_languages(self) -> None:
        claim = {
            "kind": "ACCEPTED_SUMMARY",
            "strategy_name": "grid-btc",
            "order_count": 2,
            "modules": ["SPOT"],
            "symbols": ["BTCUSDT"],
            "estimated_amount_u": "12",
            "remaining_amount_u": "88",
        }

        chinese_title, chinese_body = templates.build_notification_text(claim, language="zh")
        english_title, english_body = templates.build_notification_text(claim, language="en")

        self.assertIn("自动交易汇总", chinese_title)
        self.assertIn("2 笔订单", chinese_body)
        self.assertIn("auto-trade summary", english_title)
        self.assertIn("2 orders", english_body)

    def test_exception_notification_text_supports_both_languages(self) -> None:
        claim = {
            "kind": "EXCEPTION",
            "strategy_name": "grid-btc",
            "event_type": "USAGE_REVIEW_REQUIRED",
        }

        chinese_title, chinese_body = templates.build_notification_text(claim, language="zh")
        english_title, english_body = templates.build_notification_text(claim, language="en")

        self.assertIn("自动交易提醒", chinese_title)
        self.assertIn("请检查本地事件时间线", chinese_body)
        self.assertIn("auto-trade attention", english_title)
        self.assertIn("inspect the local event timeline", english_body)

    def test_environment_notice_is_localized_without_moving_structured_fields(self) -> None:
        environment = {"trading_mode": "live", "market": "futures"}
        self.assertIn("真实交易", templates.environment_notice(environment, "zh"))
        self.assertIn("real WEEX futures", templates.environment_notice(environment, "en"))
        with self.assertRaisesRegex(ValueError, "DEMO_MODE_REMOVED"):
            templates.environment_notice({"trading_mode": "demo"}, "en")

    def test_user_presenter_owns_confirmation_text(self) -> None:
        result = presenter.present_user_confirmation(
            "en-US",
            environment={
                "trading_mode": "live",
                "market": "futures",
                "uses_real_funds": True,
            },
            preview_context={"order_preview": {"symbol": "BTCUSDT", "type": "MARKET"}},
        )
        self.assertEqual(result["language"], "en-US")
        self.assertEqual(result["reply_text"], "confirm")
        self.assertIn("real trading", result["reply_instruction"])

    def test_supported_detected_language_renders_native_fixed_text(self) -> None:
        decision = weex_language.resolve_language_decision("ja")
        context = weex_language.language_context_from_decision(decision)
        result = presenter.present_user_confirmation(
            context,
            environment={
                "trading_mode": "live",
                "market": "futures",
                "uses_real_funds": True,
            },
            preview_context={"order_preview": {"symbol": "BTCUSDT", "type": "MARKET"}},
        )
        self.assertEqual(result["language"], "ja")
        self.assertEqual(result["language_source"], "detected")
        self.assertEqual(result["input_language"], "ja")
        self.assertNotIn("fallback_reason", result)
        self.assertEqual(result["reply_text"], "確認")
        self.assertIn("現在の取引モード", result["reply_instruction"])
        self.assertNotIn("真实盘", result["reply_instruction"])

    def test_user_message_contract_contains_language_template_and_text(self) -> None:
        message = presenter.present_user_message(
            "zh",
            "guard.pending_order_expired",
        )
        self.assertEqual(message.language, "zh-CN")
        self.assertEqual(message.template_id, "guard.pending_order_expired")
        self.assertIn("重新生成预览", message.text)


if __name__ == "__main__":
    unittest.main()
