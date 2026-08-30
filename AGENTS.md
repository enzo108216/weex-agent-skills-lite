# WEEX Trading Competition Project Guidance

- `skills/weex-trader-skill/` is the only source-of-truth implementation layer.
- This project is OpenClaw-only and ships one skill link: `weex-trader-skill`.
- Keep the complete Trader safety flow, saved-profile/Vault boundary, official Spot/Futures API definitions, preview/confirm binding, and automated-strategy authorization facade.
- Never send mutating requests without the required confirmation flag (`--confirm-live` or official futures demo `--trading-mode demo --confirm-demo`).
- Use official WEEX conditional orders for price-threshold closes; do not add a local monitor task.
- Do not add Analysis, Monitor, Partner, replay, profile-analysis, deep-risk, or non-OpenClaw host support to this project.
- Prefer non-argv secret transport and never print credentials, vault passwords, or raw signed headers.
