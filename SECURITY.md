# Security boundaries

- This scaffold is plan-only: no arbitrary command execution or filesystem tools are exposed to the model.
- API binds to 127.0.0.1 only by default.
- Do not expose PostgreSQL or the coordinator publicly.
- Never put API keys in source control, prompts, issue text, or logs.
- Use a dedicated non-admin account and a dedicated test repository.
- Keep production writes, deployments, deletions, permission changes, and purchases approval-gated.
- A model's claim that work is safe is not a security control. Enforce policy in code and CI.
- Before unattended operation, add authentication, rate limits, hard spending limits, idempotency, monitoring, tested backups, and an independent kill switch.
