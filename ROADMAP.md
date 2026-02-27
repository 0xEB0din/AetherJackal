# Roadmap

Planned features and improvements for CloudMigrate Pro.

## Phase 1 — Foundation (current)

- [x] Flask REST API with full CRUD for migrations
- [x] Resource discovery service with filtering
- [x] Cost estimation engine with multi-strategy comparison
- [x] React dashboard with navigation and dark theme
- [x] Docker multi-stage build (production) and dev compose setup
- [x] Jenkins CI/CD pipeline with parallel lint/test stages
- [x] Serverless Framework config for AWS Lambda deployment
- [x] Backend test suite with pytest

## Phase 2 — Live AWS Integration

- [ ] Replace demo resource inventory with live boto3 discovery
- [ ] Persist migration state in DynamoDB instead of local JSON
- [ ] Add IAM role-based authentication for API endpoints
- [ ] Pull real-time pricing from the AWS Price List API
- [ ] CloudWatch metrics integration for resource health data

## Phase 3 — Migration Execution Engine

- [ ] Automated migration execution for rehost (EC2 → EC2) workloads
- [ ] Database migration support via AWS DMS integration
- [ ] Pre-migration validation checks (connectivity, permissions, capacity)
- [ ] Rollback automation with state snapshots
- [ ] Parallel migration execution with concurrency limits

## Phase 4 — Observability and Reporting

- [ ] Migration timeline visualization
- [ ] Cost comparison reports (before/after with actuals)
- [ ] Export migration plans as PDF
- [ ] Slack/email notifications on status changes
- [ ] Audit log for compliance tracking

## Phase 5 — Multi-Cloud

- [ ] Azure resource discovery and migration support
- [ ] GCP resource discovery and migration support
- [ ] Cross-cloud cost normalization
- [ ] Terraform output for infrastructure-as-code handoff
