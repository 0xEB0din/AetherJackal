# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-01

### Added

- Flask REST API with full CRUD for migrations
- Resource discovery service with 8 demo AWS resource types
- Cost estimation engine comparing 6 migration strategies (rehost, replatform, refactor, repurchase, retain, retire)
- React dashboard with sidebar navigation and dark theme
- Dashboard page with migration stats and resource summary
- Migration list page with create, update, and delete functionality
- Resource inventory page with filtering by type, region, and tags
- Cost estimator page with strategy comparison table
- Migration lifecycle tracking through 8 states (pending, analyzing, ready, in_progress, validating, completed, failed, rolled_back)
- Docker multi-stage production build and development compose setup
- Jenkins CI/CD pipeline with parallel lint, test, build, and deploy stages
- Serverless Framework configuration for AWS Lambda + API Gateway + DynamoDB deployment
- Backend test suite with pytest (health, migrations, resources, analytics)
- Health check endpoints (/healthz, /readyz) for container orchestration
- Helper script (scripts/migrate.sh) for local development workflow
