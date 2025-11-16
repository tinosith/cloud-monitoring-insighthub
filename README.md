# InsightHub (Sprint 1 MVP)

## Prereqs
- Docker Desktop + Compose

## Setup
1. Create a `.env` file (use the sample block below).
2. `make up`
3. Open API docs: http://localhost:8000/docs
4. Open Dashboard: http://localhost:8501

### .env example
```
POSTGRES_DB=insighthub
POSTGRES_USER=insight
POSTGRES_PASSWORD=insightpw
POSTGRES_HOST=db
POSTGRES_PORT=5432
API_PORT=8000
DASHBOARD_PORT=8501
```

## Notes
- Generator pushes metrics every ~2s for 3 sources.
- Dashboard caches for 5s; use sidebar to adjust time window/source.

## Next
- Add CI (GitHub Actions): lint, type-check, build images.
- Add auth (read-only API key) and rate limiting.
- Optional: Prometheus + Grafana compose profile.
- Cloud: push images to ECR, run on ECS Fargate; RDS for Postgres.
