"""Shared user-facing WEEX Trader message templates.

Machine-readable error codes and exchange responses intentionally remain outside
this catalog.  The catalog only owns text shown to an end user and keeps the
language selected before an intent or notification is persisted/dispatched.
"""

from __future__ import annotations

from typing import Any

from weex_language import resolve_language


SUPPORTED_LANGUAGES = ("zh", "en")

MESSAGE_TEMPLATES: dict[str, dict[str, str]] = {
    "zh": {
        "confirmation.reply_text": "确认",
        "confirmation.reply_instruction": "如果确认继续，请回复：确认",
        "authorization.hint": (
            "如需取消二次确认功能，可申请自动交易授权。授权后，在指定交易类型、交易对、"
            "单笔金额和有效期范围内，下单无需逐笔确认。发送“申请自动交易授权”即可开始配置。"
        ),
        "manual_fallback.authorization_miss_notice": "本次订单超过自动交易授权范围，尚未下单。",
        "manual_fallback.generic_notice": "本次订单未进入自动交易执行，尚未下单。",
        "manual_fallback.order_preview": "请核对 order_preview 中的完整订单。",
        "manual_fallback.confirm_line": "确认后回复：确认",
        "environment.mode.live": "真实盘",
        "environment.prefix": "当前交易环境：{mode}",
        "environment.funds.real": "本次操作将使用真实资金，请谨慎确认。",
        "environment.preview": "{mode}订单预览已生成，订单尚未提交。",
        "environment.notice.live": "本次操作将使用 WEEX {market} 真实交易。",
        "environment.confirm.real": "如果确认使用真实资金提交这笔订单，请回复：{reply_text}",
        "label.market.futures": "合约",
        "label.market.spot": "现货",
        "label.market.fallback": "交易",
        "label.order_type.market": "市价",
        "label.order_type.limit": "限价",
        "label.order_type.fallback": "订单",
        "action.open_long": "开多",
        "action.open_short": "开空",
        "action.close_long": "平多",
        "action.close_short": "平空",
        "action.buy": "买入",
        "action.sell": "卖出",
        "action.fallback": "下单",
        "order.none": "订单：详情请以上方订单预览为准。",
        "order.cancel": "操作：撤销{market}订单，标识 {target}。",
        "order.full_position": "全部仓位（quantity 为 0 或省略）",
        "order.summary": "订单：{symbol} {market}，{order_type}{action}，数量 {quantity}{price}{trigger}。",
        "order.price": "，价格 {value}",
        "order.trigger": "，触发价 {value}",
        "price.notice": "价格提示：实际成交价可能随市场波动，请以 WEEX 最终成交结果为准。",
        "value.missing": "未返回",
        "notification.strategy_default": "WEEX 策略",
        "notification.accepted_summary.title": "WEEX 自动交易汇总：{strategy}",
        "notification.accepted_summary.body": (
            "{order_count} 笔订单；{modules}；{symbols}；预计 {estimated} U；剩余 {remaining} U"
        ),
        "notification.exception.title": "WEEX 自动交易提醒：{strategy}",
        "notification.exception.body": "{event_type}；请检查本地事件时间线",
        "url.empty": "{label} 不能为空。",
        "url.shape": "{label} 必须是完整的 https:// URL。",
        "url.userinfo": "{label} 不能包含用户名或密码。",
        "url.query_fragment": "{label} 不能包含查询参数或 fragment。",
        "url.host": "{label} 必须使用 weex.com 或 weex.tech 及其子域名；当前域名为 {host!r}。",
        "guard.order_invalid": "订单参数不完整或无效。",
        "guard.pending_order_missing": "没有找到待确认的订单意图。",
        "guard.pending_order_wrong_type": "待确认意图不是普通订单，请使用 TP/SL 确认命令。",
        "guard.intent_id_mismatch_order": "意图 ID 与已保存的待确认订单不匹配。",
        "guard.pending_order_expired": "待确认订单已过期，请重新生成预览。",
        "guard.intent_mode_mismatch": "请求的交易模式与已保存订单不匹配。",
        "guard.confirm_flag_mismatch": "{mode}确认需要使用 {required_flag}。",
        "guard.reply_mismatch": "用户回复必须与最新确认文本完全一致。",
        "guard.confirm_order_fields_missing": "确认订单需要提供预览返回的 intent_id 和 risk_signature。",
        "guard.risk_signature_order": "待确认订单的风险签名不匹配，请重新生成预览。",
        "guard.order_cleanup_failed": "订单已提交，但本地确认状态无法清理。",
        "guard.pending_tp_sl_missing": "没有找到待确认的 TP/SL 意图。",
        "guard.pending_tp_sl_wrong_type": "待确认意图不是 TP/SL 订单。",
        "guard.intent_id_mismatch_tp_sl": "意图 ID 与已保存的待确认 TP/SL 订单不匹配。",
        "guard.pending_tp_sl_expired": "待确认 TP/SL 意图已过期，请重新生成预览。",
        "guard.tp_sl_mode_unsupported": "TP/SL 确认仅支持真实合约交易。",
        "guard.confirm_tp_sl_flag": "真实 TP/SL 订单确认需要使用 --confirm-live。",
        "guard.confirm_tp_sl_fields_missing": "确认 TP/SL 需要提供预览返回的 intent_id 和 risk_signature。",
        "guard.risk_signature_tp_sl": "待确认 TP/SL 订单的风险签名不匹配，请重新生成预览。",
        "guard.tp_sl_context_missing": "待确认 TP/SL 意图缺少订单上下文。",
        "guard.tp_sl_cleanup_failed": "TP/SL 已提交，但本地确认状态无法清理。",
        "guard.pending_cancel_missing": "没有找到待确认的撤单意图。",
        "guard.pending_cancel_expired": "待确认撤单意图已过期，请重新生成预览。",
        "guard.confirm_cancel_fields_missing": "确认撤单需要匹配的 intent_id 和 risk_signature。",
        "guard.risk_signature_cancel": "待确认撤单的风险签名不匹配。",
        "guard.confirm_cancel_flag": "真实撤单确认需要使用 --confirm-live。",
        "guard.cancel_cleanup_failed": "撤单已成功，但本地确认状态无法清理。",
    },
    "en": {
        "confirmation.reply_text": "confirm",
        "confirmation.reply_instruction": "To continue, reply: confirm",
        "authorization.hint": (
            "To disable per-order confirmation, you can request automated trading authorization. "
            "After authorization, orders within the specified trade types, symbols, single-order amount, "
            'and validity period can be placed without per-order confirmation. Send "Request automated '
            'trading authorization" to start configuration.'
        ),
        "manual_fallback.authorization_miss_notice": (
            "This order exceeded the automated-trading authorization scope and was not submitted."
        ),
        "manual_fallback.generic_notice": "This order was not submitted through automated trading.",
        "manual_fallback.order_preview": "Review the complete order in `order_preview`.",
        "manual_fallback.confirm_line": "After confirming, reply: confirm",
        "environment.mode.live": "real trading",
        "environment.prefix": "Current trading mode: {mode}",
        "environment.funds.real": "This operation uses real funds. Confirm carefully.",
        "environment.preview": "{mode} order preview generated; order has not been submitted.",
        "environment.notice.live": "This operation targets real WEEX {market} trading.",
        "environment.confirm.real": "To submit this order with real funds, reply: {reply_text}",
        "label.market.futures": "futures",
        "label.market.spot": "spot",
        "label.market.fallback": "trading",
        "label.order_type.market": "market",
        "label.order_type.limit": "limit",
        "label.order_type.fallback": "order",
        "action.open_long": "open long",
        "action.open_short": "open short",
        "action.close_long": "close long",
        "action.close_short": "close short",
        "action.buy": "buy",
        "action.sell": "sell",
        "action.fallback": "place order",
        "order.none": "Order: see the order preview above for details.",
        "order.cancel": "Operation: cancel the {market} order identified by {target}.",
        "order.full_position": "the full position (quantity is 0 or omitted)",
        "order.summary": "Order: {symbol} {market}, {order_type} {action}, quantity {quantity}{price}{trigger}.",
        "order.price": ", price {value}",
        "order.trigger": ", trigger price {value}",
        "price.notice": "Price notice: The actual execution price may fluctuate with the market. Please refer to the final WEEX execution result.",
        "value.missing": "not returned",
        "notification.strategy_default": "WEEX strategy",
        "notification.accepted_summary.title": "WEEX auto-trade summary: {strategy}",
        "notification.accepted_summary.body": (
            "{order_count} orders; {modules}; {symbols}; estimated {estimated} U; "
            "remaining {remaining} U"
        ),
        "notification.exception.title": "WEEX auto-trade attention: {strategy}",
        "notification.exception.body": "{event_type}; inspect the local event timeline",
        "url.empty": "{label} cannot be empty.",
        "url.shape": "{label} must be a full https URL.",
        "url.userinfo": "{label} must not include username or password components.",
        "url.query_fragment": "{label} must not include query or fragment components.",
        "url.host": "{label} must use a weex.com or weex.tech host; got {host!r}.",
        "guard.order_invalid": "Order parameters are incomplete or invalid.",
        "guard.pending_order_missing": "No pending order intent was found.",
        "guard.pending_order_wrong_type": "The pending intent is not a regular order. Use the TP/SL confirmation command.",
        "guard.intent_id_mismatch_order": "The intent ID does not match the saved pending order.",
        "guard.pending_order_expired": "The pending order intent has expired. Generate a new preview first.",
        "guard.intent_mode_mismatch": "The requested trading mode does not match the saved order.",
        "guard.confirm_flag_mismatch": "{mode} confirmation requires {required_flag}.",
        "guard.reply_mismatch": "The user reply must exactly match the latest confirmation text.",
        "guard.confirm_order_fields_missing": "confirm-order requires the intent_id and risk_signature returned by preview-order.",
        "guard.risk_signature_order": "The pending order risk signature does not match. Generate a new preview first.",
        "guard.order_cleanup_failed": "The order was submitted, but local confirmation state could not be cleared.",
        "guard.pending_tp_sl_missing": "No pending TP/SL intent was found.",
        "guard.pending_tp_sl_wrong_type": "The pending intent is not a TP/SL order.",
        "guard.intent_id_mismatch_tp_sl": "The intent ID does not match the saved pending TP/SL order.",
        "guard.pending_tp_sl_expired": "The pending TP/SL intent has expired. Generate a new preview first.",
        "guard.tp_sl_mode_unsupported": "TP/SL confirmation is supported only for live futures trading.",
        "guard.confirm_tp_sl_flag": "confirm-tp-sl requires --confirm-live before sending a real TP/SL order.",
        "guard.confirm_tp_sl_fields_missing": "confirm-tp-sl requires the intent_id and risk_signature returned by preview-tp-sl.",
        "guard.risk_signature_tp_sl": "The pending TP/SL risk signature does not match. Generate a new preview first.",
        "guard.tp_sl_context_missing": "The pending TP/SL intent is missing its order context.",
        "guard.tp_sl_cleanup_failed": "The TP/SL order was submitted, but local confirmation state could not be cleared.",
        "guard.pending_cancel_missing": "No pending cancellation intent was found.",
        "guard.pending_cancel_expired": "The pending cancellation intent has expired. Generate a new preview first.",
        "guard.confirm_cancel_fields_missing": "confirm-cancel requires a matching intent_id and risk_signature.",
        "guard.risk_signature_cancel": "The pending cancellation risk signature does not match.",
        "guard.confirm_cancel_flag": "confirm-cancel requires --confirm-live before sending a real cancellation.",
        "guard.cancel_cleanup_failed": "The cancellation succeeded, but local confirmation state could not be cleared.",
    },
}


CONFIRMATION_PROMPTS = {
    language: {
        "reply_text": MESSAGE_TEMPLATES[language]["confirmation.reply_text"],
        "reply_instruction": MESSAGE_TEMPLATES[language]["confirmation.reply_instruction"],
    }
    for language in SUPPORTED_LANGUAGES
}
AUTO_TRADE_AUTHORIZATION_HINTS = {
    language: MESSAGE_TEMPLATES[language]["authorization.hint"]
    for language in SUPPORTED_LANGUAGES
}


def _resolved_language(language: str) -> str:
    return resolve_language(language)


def render_message(language: str, template_id: str, **values: Any) -> str:
    resolved = _resolved_language(language)
    try:
        template = MESSAGE_TEMPLATES[resolved][template_id]
    except KeyError as exc:
        raise KeyError(f"unknown message template: {template_id}") from exc
    return template.format(**values)


def build_manual_fallback_confirmation(
    language: str,
    *,
    authorization_miss: bool,
) -> dict[str, str]:
    resolved = _resolved_language(language)
    notice_id = (
        "manual_fallback.authorization_miss_notice"
        if authorization_miss
        else "manual_fallback.generic_notice"
    )
    lines = [
        render_message(resolved, notice_id),
        "",
        render_message(resolved, "manual_fallback.order_preview"),
        "",
        render_message(resolved, "manual_fallback.confirm_line"),
    ]
    authorization_hint = ""
    if authorization_miss:
        authorization_hint = render_message(resolved, "authorization.hint")
        lines.extend(["", authorization_hint])
    return {
        "language": resolved,
        "reply_text": render_message(resolved, "confirmation.reply_text"),
        "reply_instruction": "\n".join(lines),
        "authorization_hint": authorization_hint,
    }


def build_notification_text(
    claim: dict[str, Any],
    language: str | None = None,
) -> tuple[str, str]:
    resolved = _resolved_language(language or claim.get("language"))
    strategy_default = render_message(resolved, "notification.strategy_default")
    strategy = str(claim.get("strategy_name") or strategy_default)
    if claim.get("kind") == "ACCEPTED_SUMMARY":
        modules = ", ".join(str(item) for item in claim.get("modules", []))
        symbols = ", ".join(str(item) for item in claim.get("symbols", []))
        return (
            render_message(resolved, "notification.accepted_summary.title", strategy=strategy),
            render_message(
                resolved,
                "notification.accepted_summary.body",
                order_count=claim.get("order_count", 0),
                modules=modules,
                symbols=symbols,
                estimated=claim.get("estimated_amount_u", "unknown"),
                remaining=claim.get("remaining_amount_u", "unknown"),
            ),
        )
    return (
        render_message(resolved, "notification.exception.title", strategy=strategy),
        render_message(
            resolved,
            "notification.exception.body",
            event_type=claim.get("event_type", "UNKNOWN_EVENT"),
        ),
    )


def environment_label(environment: dict[str, Any], language: str) -> str:
    resolved = _resolved_language(language)
    mode = str(environment.get("trading_mode") or "live").strip().lower()
    if mode != "live":
        raise ValueError("DEMO_MODE_REMOVED")
    return render_message(resolved, "environment.mode.live")


def environment_prefix(environment: dict[str, Any], language: str) -> str:
    resolved = _resolved_language(language)
    return render_message(
        resolved,
        "environment.prefix",
        mode=environment_label(environment, resolved),
    )


def environment_notice(environment: dict[str, Any], language: str) -> str:
    resolved = _resolved_language(language)
    mode = str(environment.get("trading_mode") or "live").strip().lower()
    if mode != "live":
        raise ValueError("DEMO_MODE_REMOVED")
    market = str(environment.get("market") or "trading").strip().lower()
    market_key = market if market in {"spot", "futures"} else "fallback"
    return render_message(
        resolved,
        "environment.notice.live",
        market=render_message(resolved, f"label.market.{market_key}"),
    )


def _format_value(value: Any, *, missing: str) -> str:
    if value is None or value == "":
        return missing
    return str(value)


def _market_label(market: Any, language: str) -> str:
    normalized = str(market or "").strip().lower()
    key = normalized if normalized in {"spot", "futures"} else "fallback"
    return render_message(language, f"label.market.{key}")


def _order_type_label(order_type: Any, language: str) -> str:
    normalized = str(order_type or "").strip().upper()
    key = {"MARKET": "market", "LIMIT": "limit"}.get(normalized, "fallback")
    return render_message(language, f"label.order_type.{key}")


def _order_action(order_preview: dict[str, Any], language: str) -> str:
    side = str(order_preview.get("side") or "").strip().upper()
    position_side = str(
        order_preview.get("position_side") or order_preview.get("positionSide") or ""
    ).strip().upper()
    action_key = {
        ("LONG", "BUY"): "open_long",
        ("SHORT", "SELL"): "open_short",
        ("LONG", "SELL"): "close_long",
        ("SHORT", "BUY"): "close_short",
    }.get((position_side, side))
    if action_key is None:
        action_key = {"BUY": "buy", "SELL": "sell"}.get(side, "fallback")
    return render_message(language, f"action.{action_key}")


def _is_full_position_tp_sl(order_preview: dict[str, Any]) -> bool:
    if not order_preview.get("planType"):
        return False
    quantity = order_preview.get("quantity")
    if quantity is None or str(quantity).strip() == "":
        return True
    try:
        from decimal import Decimal, InvalidOperation

        return Decimal(str(quantity)) == 0
    except (InvalidOperation, ValueError):
        return False


def format_order_summary(preview_context: dict[str, Any] | None, language: str) -> str:
    resolved = _resolved_language(language)
    order_preview = (preview_context or {}).get("order_preview")
    if not isinstance(order_preview, dict) or not order_preview:
        return render_message(resolved, "order.none")
    if order_preview.get("operation") == "cancel_order":
        target = order_preview.get("order_id") or order_preview.get("client_oid") or (
            render_message(resolved, "value.missing")
        )
        return render_message(
            resolved,
            "order.cancel",
            market=_market_label(order_preview.get("market"), resolved),
            target=target,
        )
    symbol = _format_value(
        order_preview.get("symbol"),
        missing=render_message(resolved, "value.missing"),
    )
    market = _market_label(order_preview.get("market"), resolved)
    order_type = _order_type_label(
        order_preview.get("order_type") or order_preview.get("orderType"), resolved
    )
    action = _order_action(order_preview, resolved)
    if _is_full_position_tp_sl(order_preview):
        quantity = render_message(resolved, "order.full_position")
    else:
        quantity = _format_value(
            order_preview.get("quantity") or order_preview.get("size"),
            missing=render_message(resolved, "value.missing"),
        )
    price = order_preview.get("price")
    price_text = "" if price in (None, "") else render_message(
        resolved,
        "order.price",
        value=_format_value(price, missing=render_message(resolved, "value.missing")),
    )
    trigger_price = order_preview.get("trigger_price") or order_preview.get("triggerPrice")
    trigger_text = "" if trigger_price in (None, "") else render_message(
        resolved,
        "order.trigger",
        value=_format_value(
            trigger_price,
            missing=render_message(resolved, "value.missing"),
        ),
    )
    return render_message(
        resolved,
        "order.summary",
        symbol=symbol,
        market=market,
        order_type=order_type,
        action=action,
        quantity=quantity,
        price=price_text,
        trigger=trigger_text,
    )


def market_price_warning(language: str) -> str:
    return render_message(_resolved_language(language), "price.notice")


def build_confirmation_instruction(
    language: str,
    *,
    environment: dict[str, Any],
    preview_context: dict[str, Any] | None,
    auto_trade_authorization_hint: str | None,
    reply_text: str,
    market_price_recheck_skipped: bool,
) -> tuple[str, str | None]:
    resolved = _resolved_language(language)
    mode = environment_label(environment, resolved)
    preview_mode = mode.capitalize() if resolved == "en" else mode
    lines = [
        environment_prefix(environment, resolved),
        render_message(resolved, "environment.funds.real"),
        "",
        render_message(resolved, "environment.preview", mode=preview_mode),
        "",
        format_order_summary(preview_context, resolved),
    ]
    if market_price_recheck_skipped:
        lines.extend(["", market_price_warning(resolved)])
    lines.extend(
        [
            "",
            render_message(
                resolved,
                "environment.confirm.real",
                mode=mode,
                reply_text=reply_text,
            ),
        ]
    )
    if auto_trade_authorization_hint is not None:
        lines.extend(["", auto_trade_authorization_hint])
    return "\n".join(lines), None
