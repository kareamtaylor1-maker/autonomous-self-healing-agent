$ErrorActionPreference = "Stop"

Write-Host "Checking Docker..."
try {
    docker version | Out-Null
} catch {
    Write-Error "Docker is not available. Install/start Docker Desktop, then rerun this script."
    exit 1
}

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Edit it and add your API key before using model calls."
}

Write-Host "Starting local starter stack..."
docker compose up -d --build

Write-Host ""
Write-Host "Stack started. Health check:"
try {
    Invoke-RestMethod "http://127.0.0.1:8787/health" | ConvertTo-Json
} catch {
    Write-Host "The service may still be starting. Try: docker compose logs -f coordinator"
}
Write-Host "Local API: http://127.0.0.1:8787"
Write-Host "Stop: docker compose down"
