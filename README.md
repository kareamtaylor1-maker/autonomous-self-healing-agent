# Autonomous Agent Starter (Windows + Cloud-ready)

A starter scaffold for a self-hosted AI task-planning coordinator. **This is not yet a fully autonomous repair or deployment system.**

> **Repository visibility:** this repository is currently public. Do not commit secrets, private source code, logs, or customer data. Change it to private in GitHub Settings if you want the source restricted.

## Included
- FastAPI task API and a LangGraph investigation → plan → independent review workflow.
- PostgreSQL service placeholder for future durable state (the current workflow does not persist tasks).
- Docker Compose and a Windows PowerShell starter script.
- GitHub Actions CI and basic API tests.
- Security notes and a non-secret environment template.

## Windows setup
1. Install and start Docker Desktop with the WSL 2 backend: https://docs.docker.com/desktop/setup/install/windows-install/
2. Clone this repository and open PowerShell in the cloned folder.
3. Run:
   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\setup-windows.ps1
   ```
4. Edit `.env` locally and set `OPENAI_API_KEY` and a model ID available to your account. Never commit `.env`.
5. Rebuild after editing: `docker compose up -d --build`
6. Check health: `Invoke-RestMethod http://127.0.0.1:8787/health`
7. Submit a test task:
   ```powershell
   $body = @{ task = "Inspect a disposable test project and suggest a minimal fix for a failing test. Do not change production systems."; mode = "plan_only" } | ConvertTo-Json
   Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8787/tasks -ContentType "application/json" -Body $body
   ```

## API
- `GET /health`
- `POST /tasks` JSON: `{"task":"Describe the task in at least 10 characters","mode":"plan_only"}`

The current implementation only creates a plan and review. It does not execute shell commands, modify repositories, run project tests, deploy, or automatically repair production systems.

## Cloud deployment
Do not expose port 8787 or PostgreSQL to the public internet. A cloud deployment needs a hardened Linux VM, firewall rules, authenticated TLS access, private connectivity (VPN or authenticated outbound tunnel), backups, monitoring, and secret management. Do not publish Docker's socket. No cloud server has been provisioned by this repository change.

## Next engineering milestones
1. Add authentication, durable task storage, audit logs, rate limits, and spending limits.
2. Add an isolated disposable workspace and strict tool/command allowlists.
3. Integrate GitHub via least-privilege credentials and use per-task branches.
4. Run tests and security checks in CI; require independent review.
5. Add retries, rollback, alerting, backups, and an external kill switch before unattended use.

## Model strategy
The example calls the OpenAI API directly. A gateway such as LiteLLM can later add provider routing/fallbacks and budget controls. Model IDs and prices change; configure a model you can access.
