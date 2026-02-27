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

## Current Limitations

This is a **Phase 1 prototype**. Be aware of what it can and cannot do today:

| Limitation | Detail |
|---|---|
| **Demo data only** | Resource discovery returns a hardcoded list of 8 AWS resources. There is no live boto3 integration — no actual AWS account is queried. |
| **Flat-file storage** | Migration state is persisted to a JSON file on disk (`/tmp/migrations`). This means data is lost on container restart, there is no concurrent write safety, and it does not scale beyond a single process. |
| **Hardcoded cost model** | Cost estimates use static hourly rates (e.g., t3.medium = $0.0416/hr) and fixed savings percentages per strategy. These do not reflect real AWS pricing, reserved instance discounts, savings plans, or regional price variation. |
| **No authentication** | The API has zero auth. Anyone with network access can create, modify, or delete migrations. There is no concept of users, roles, or tenants. |
| **No real migration execution** | The platform tracks migration *status* but does not actually move workloads. Status transitions are manual — a human updates the status field via API. |
| **Single-region, single-account** | The demo inventory is locked to `us-east-1` in a single AWS account. Multi-region and multi-account discovery is not implemented. |
| **No dependency mapping** | Resources are treated as independent items. There is no understanding of which EC2 instance talks to which RDS database or which services depend on each other. |
| **No rollback automation** | The `rollback_available` flag is set on completion, but no actual rollback logic exists. |

## Tradeoffs

Decisions made in Phase 1 and their consequences:

- **Flask + JSON files over a real database** — Fastest path to a working prototype, but prevents concurrent access and any real production use. Switching to DynamoDB or PostgreSQL is required before deploying for real teams.
- **Hardcoded demo inventory over boto3** — Removes the need for AWS credentials during development, but means the platform cannot demonstrate real value until live discovery is wired in.
- **Monolithic API over microservices** — Simpler to develop and deploy, but migration execution, resource discovery, and analytics will eventually need independent scaling.
- **Client-side routing only** — No server-side rendering or static pre-rendering. Fine for an internal tool, but limits SEO and initial load performance if this ever becomes a public product.
- **No WebSocket or SSE** — Dashboard data is fetched on page load. There are no real-time updates when migration status changes. Users must refresh to see new data.

## Gaps (What's Missing to Be Production-Ready)

These are not "nice-to-haves" — they are blockers for any real deployment:

1. **Authentication and authorization** — JWT or OAuth2 with role-based access control (admin, operator, viewer)
2. **Real database** — DynamoDB, PostgreSQL, or similar with proper migrations and backup
3. **Live resource discovery** — boto3 integration with assume-role support for cross-account scanning
4. **Real AWS pricing** — Pull from the AWS Price List API or Cost Explorer, factoring in RIs, savings plans, and spot pricing
5. **Input rate limiting** — No protection against API abuse; any client can flood the endpoints
6. **Request logging and audit trail** — No structured logging of who did what and when
7. **Error handling in the frontend** — API failures are not surfaced clearly to the user
8. **Migration validation** — No pre-flight checks before starting a migration (permissions, capacity, connectivity)
9. **Data encryption** — State file is written as plaintext JSON; no encryption at rest
10. **HTTPS enforcement** — The app serves over HTTP; TLS termination is left entirely to the deployment layer

## Security Considerations

Current security posture and what needs to change:

| Area | Current State | Required |
|---|---|---|
| **Authentication** | None | JWT/OAuth2 with token expiry and refresh |
| **Authorization** | None | RBAC — at minimum admin, operator, viewer roles |
| **Input validation** | Marshmallow schemas validate shape/types | Add field-level sanitization, length limits, and reject unexpected fields |
| **CORS** | Open (`*`) via Flask-CORS | Restrict to known frontend origins |
| **Secrets management** | No secrets in use yet | When AWS credentials are added, use IAM roles (not hardcoded keys), or a secrets manager |
| **Data at rest** | Plaintext JSON on disk | Encrypt state files; in production use a database with encryption enabled |
| **Data in transit** | HTTP only | Enforce HTTPS with TLS 1.2+ at the load balancer or API Gateway |
| **Rate limiting** | None | Add per-IP and per-endpoint rate limits (e.g., Flask-Limiter) |
| **Dependency security** | No scanning | Add `pip audit` and `npm audit` to CI pipeline |
| **Container security** | Non-root user in Dockerfile | Add read-only filesystem, drop all capabilities, scan images with Trivy or Snyk |
| **API versioning** | `/api/v1` prefix exists | Maintain versioning discipline as the API evolves |

## Future Improvements

See [ROADMAP.md](ROADMAP.md) for the full plan. The features below are what would make CloudMigrate Pro genuinely different from existing tools like AWS Migration Hub, CloudEndure, or Cloudamize:

### What Would Actually Make This Special

- **Automatic dependency mapping** — Analyze VPC flow logs, security groups, and CloudWatch metrics to build a dependency graph showing which resources talk to each other. This is the single biggest pain point in real migrations and almost no open-source tool does it well.
- **AI-driven strategy recommendations** — Use resource metadata, usage patterns, and cost data to recommend the optimal migration strategy per workload instead of making users guess.
- **Migration risk scoring** — Assign a risk score (low/medium/high/critical) to each planned migration based on resource complexity, dependency count, data volume, and downtime tolerance.
- **Infrastructure-as-Code generation** — After selecting a strategy, auto-generate Terraform or CloudFormation templates for the target architecture so teams can review and apply infrastructure changes directly.
- **Runbook generation** — Auto-produce step-by-step migration runbooks (pre-migration checks, execution steps, validation, rollback plan) customized to each workload and strategy.
- **Real-time migration execution with rollback** — Actually execute migrations (EC2 rehost via AMI copy, RDS via snapshot-restore, S3 via cross-region replication) with automatic rollback on failure.
- **Multi-cloud support with cost normalization** — Discover and compare workloads across AWS, Azure, and GCP with normalized cost metrics so teams can make cloud-agnostic decisions.
- **Slack/Teams integration with approval workflows** — Notify channels on status changes and require explicit approval (thumbs-up reaction or slash command) before proceeding to the next migration phase.
- **Before/after cost actuals** — After migration completes, pull real Cost Explorer data to compare projected savings vs. actual savings and surface where estimates were wrong.
- **Compliance templates** — Pre-built migration checklists for SOC 2, HIPAA, PCI-DSS, and FedRAMP that enforce required steps (data classification, encryption verification, access review) before a migration can proceed.

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
