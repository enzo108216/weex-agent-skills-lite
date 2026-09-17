# OpenClaw Language Contract

OpenClaw must decide language from the latest user message before invoking any user-facing
WEEX command. Previous assistant messages, memory results, persisted state, and tool output are
not language evidence.

## Decision fields

```json
{
  "input_language": "ja",
  "render_language": "en",
  "source": "fallback",
  "fallback_reason": "unsupported_language"
}
```

- `input_language` is the detected language family or `unknown`.
- `render_language` is the template language and is limited to `zh` or `en`.
- `source` is `detected`, `explicit`, or `fallback`.
- `fallback_reason` is present for unsupported or undetermined input.
- Detection confidence below `0.8` is treated as undetermined and falls back to English.

## Resolution rules

1. `zh`, `zh-CN`, and other Chinese variants render with `zh`.
2. `en`, `en-US`, and other English variants render with `en`.
3. Unsupported languages such as Japanese, Korean, or French render fixed templates with `en`.
4. An undetermined language renders fixed templates with `en`.
5. Low-confidence detection renders fixed templates with `en`.
6. A caller must not override an unsupported/undetermined decision with `zh`; selecting `zh` requires a detected Chinese input language.
7. Preflight is machine-only and has no language parameter.

For strict single-language responses, OpenClaw should render the surrounding explanation in the
same `render_language`. If the product intentionally keeps an unsupported-language explanation,
the fixed confirmation block must remain explicitly English and its `reply_text` must be treated as
an opaque exact token.

## Confirmation binding

The language decision, render language, confirmation word, intent, account binding, TTL, and risk
signature belong to one invocation. If the language decision changes between preview and confirm,
OpenClaw must generate a new preview instead of reusing the old intent.
