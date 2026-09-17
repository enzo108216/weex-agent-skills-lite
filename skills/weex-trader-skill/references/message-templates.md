# WEEX Trader 消息模板索引

目标架构、语言边界、机器字段与用户文案的职责划分，以 [`02-技术方案.md`](../../需求分析/language-default-removal/02-技术方案.md) 为唯一方案真源。

本文件只维护运行时模板的审查索引；运行时模板唯一实现位于 [`scripts/weex_message_templates.py`](../scripts/weex_message_templates.py)。

## 语言规则

- 支持语言：`zh`、`en`。
- 宿主只根据最新用户消息生成语言决策；`zh` 使用中文，`en` 使用英文，其他或未知语种固定文案降级为英文。
- `input_language` 与 `language`（渲染语言）是两个不同字段；检测到非支持语种时不得覆盖为 `zh`。
- 英文兜底不写入全局配置。
- 显式无效语言值必须拒绝。
- intent 中的确认语言和确认词属于安全绑定，不是全局偏好。

## 模板覆盖索引

| 模板命名空间 | 中文 | English | 消费方 |
| --- | --- | --- | --- |
| `confirmation.*` | 有 | 有 | Trade Guard、自动交易兜底 |
| `manual_fallback.*` | 有 | 有 | 自动交易 Facade |
| `environment.*` | 有 | 有 | Trade Guard 展示器 |
| `label.*` / `action.*` | 有 | 有 | 订单摘要展示器 |
| `order.*` / `price.notice` | 有 | 有 | Trade Guard 展示器 |
| `guard.*` | 有 | 有 | Trade Guard 展示器 |
| `url.*` | 有 | 有 | URL policy 展示边界 |
| `notification.*` | 有 | 有 | 通知 adapter/worker |

## 维护约束

- 新增用户可见模板时，必须同时添加 `zh` 与 `en` 同名键。
- 两种语言必须使用相同的占位符集合。
- 机器错误码、`next_action`、内部风控诊断和 WEEX 原始错误不放入此目录。
- 内部字段只有在进入用户回复或通知正文前，才转换为模板 ID。
