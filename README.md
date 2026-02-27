# CloudMigrate Pro

A full-stack cloud migration platform that helps teams plan, execute, and monitor the migration of on-premises workloads to AWS serverless infrastructure.

Built with **Flask** (Python) on the backend and **React** on the frontend, containerized with **Docker**, and deployable through a **Jenkins** CI/CD pipeline or the **Serverless Framework**.

---

## What It Does

CloudMigrate Pro gives engineering teams a single dashboard to manage cloud migrations end-to-end:

- **Resource Discovery** — inventory existing cloud resources (EC2, RDS, S3, Lambda, ECS, ElastiCache, ALB, API Gateway) with filtering by type, region, and tags
- **Migration Tracking** — create, update, and monitor migrations through their full lifecycle (pending → analyzing → in progress → completed / rolled back)
- **Cost Estimation** — compare monthly spend across six migration strategies (rehost, replatform, refactor, repurchase, retain, retire) with projected savings
- **Strategy Comparison** — side-by-side view of complexity vs. savings trade-offs to guide decision-making

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, React Router, Axios |
| Backend | Python 3.12, Flask, Flask-CORS, Marshmallow |
| Infrastructure | Docker, Docker Compose, Serverless Framework |
| CI/CD | Jenkins (parallel lint + test stages, Docker build, ECR push) |
| Cloud | AWS (Lambda, API Gateway, DynamoDB, ECR, ECS) |
| Testing | pytest, pytest-cov, React Testing Library |
| Linting | pylint, ESLint |

## Project Structure

```
.
├── backend/
│   ├── app.py                  # Flask application factory
│   ├── config.py               # Environment-based configuration
│   ├── serverless.yml          # Serverless Framework deployment config
│   ├── requirements.txt
│   ├── models/
│   │   ├── migration.py        # Migration schemas and validation
│   │   └── resource.py         # Resource categorization and schemas
│   ├── routes/
│   │   ├── health.py           # /healthz and /readyz endpoints
│   │   ├── migrations.py       # CRUD + stats for migrations
│   │   ├── resources.py        # Resource discovery and filtering
│   │   └── analytics.py        # Dashboard analytics and cost estimation
│   ├── services/
│   │   ├── migration_service.py
│   │   ├── resource_service.py
│   │   └── analytics_service.py
│   └── tests/
│       ├── conftest.py
│       ├── test_health.py
│       ├── test_migrations.py
│       └── test_resources.py
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js
│       ├── App.js
│       ├── components/
│       │   ├── Dashboard.jsx
│       │   ├── MigrationList.jsx
│       │   ├── ResourceInventory.jsx
│       │   └── CostEstimator.jsx
│       ├── services/
│       │   └── api.js
│       └── styles/
│           └── global.css
├── docker/
│   ├── Dockerfile              # Multi-stage production build
│   └── Dockerfile.dev          # Lightweight dev image
├── ci-cd/
│   └── Jenkinsfile             # Full CI/CD pipeline
├── scripts/
│   └── migrate.sh              # Local dev helper script
├── docker-compose.yml
├── ROADMAP.md
└── LICENSE
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose (optional, for containerized setup)

### Quick Start (local)

```bash
# clone the repo
git clone https://github.com/0xEB0din/AetherJackal.git
cd AetherJackal

# install everything and start dev servers
./scripts/migrate.sh setup
./scripts/migrate.sh dev
```

The backend runs on `http://localhost:5000` and the frontend on `http://localhost:3000`.

### Quick Start (Docker)

```bash
docker-compose up --build
```

### Running Tests

```bash
# backend tests with coverage
cd backend && python -m pytest tests/ -v --cov=.

# or use the helper script
./scripts/migrate.sh test
```

## API Reference

All endpoints are prefixed with `/api/v1`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/healthz` | Health check |
| `GET` | `/api/v1/migrations` | List all migrations (supports `?status=` filter) |
| `POST` | `/api/v1/migrations` | Create a new migration |
| `GET` | `/api/v1/migrations/:id` | Get migration details |
| `PATCH` | `/api/v1/migrations/:id` | Update migration (status, strategy, etc.) |
| `DELETE` | `/api/v1/migrations/:id` | Delete a migration |
| `GET` | `/api/v1/migrations/stats` | Aggregate migration statistics |
| `GET` | `/api/v1/resources` | Discover resources (supports type/region/tag filters) |
| `GET` | `/api/v1/resources/summary` | Resource summary by category |
| `GET` | `/api/v1/resources/:id` | Single resource details |
| `GET` | `/api/v1/analytics/dashboard` | Combined dashboard data |
| `POST` | `/api/v1/analytics/cost-estimate` | Cost estimate for given resources |
| `GET` | `/api/v1/analytics/cost-estimate/all` | Estimate for all discovered resources |

### Example: Create a Migration

```bash
curl -X POST http://localhost:5000/api/v1/migrations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Migrate user-service to ECS Fargate",
    "source_environment": "on-prem-dc1",
    "target_environment": "aws-us-east-1",
    "strategy": "replatform"
  }'
```

## CI/CD Pipeline

The Jenkins pipeline (`ci-cd/Jenkinsfile`) runs:

1. **Lint** — pylint (backend) + ESLint (frontend) in parallel
2. **Test** — pytest with coverage + React Testing Library in parallel
3. **Build** — multi-stage Docker image
4. **Deploy to Staging** — automatic on `develop` branch
5. **Deploy to Production** — manual approval gate on `main`, pushes to ECR

## Serverless Deployment

For AWS Lambda + API Gateway deployment:

```bash
cd backend
npx serverless deploy --stage prod --region us-east-1
```

This provisions a DynamoDB table, Lambda function, and HTTP API Gateway endpoint.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and milestones.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit using [Conventional Commits](https://www.conventionalcommits.org) (`git commit -m "feat: add resource tagging"`)
4. Push to your branch (`git push origin feature/my-feature`)
5. Open a pull request

## License

MIT License — see [LICENSE](LICENSE) for details.

## Contact

**Ahmed Ebrahim** — [@0xEB0din](https://twitter.com/0xEB0din)

Project: [github.com/0xEB0din/AetherJackal](https://github.com/0xEB0din/AetherJackal)
