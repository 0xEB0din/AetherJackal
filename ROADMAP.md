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

**Honest status:** This phase delivers a working prototype with demo data, flat-file storage, and no authentication. It proves the architecture works but cannot be used in production.

## Phase 2 — Make It Real

Replace demo scaffolding with production-grade components.

- [ ] Replace hardcoded resource inventory with live boto3 discovery (EC2, RDS, S3, Lambda, ECS, ElastiCache, ELB, API Gateway)
- [ ] Add assume-role support for cross-account resource scanning
- [ ] Migrate state persistence from JSON files to DynamoDB (or PostgreSQL)
- [ ] Integrate AWS Price List API for real-time cost data (replace hardcoded hourly rates)
- [ ] Factor in Reserved Instances, Savings Plans, and spot pricing in cost estimates
- [ ] Add JWT-based authentication with role-based access control (admin, operator, viewer)
- [ ] Enforce HTTPS and restrict CORS to known origins
- [ ] Add per-endpoint rate limiting (Flask-Limiter)
- [ ] Add `pip audit` and `npm audit` to CI pipeline
- [ ] Add structured request logging with correlation IDs

## Phase 3 — Dependency Mapping and Risk Scoring

This is the feature that would set CloudMigrate Pro apart from most migration tools.

- [ ] Analyze VPC flow logs to detect resource-to-resource communication patterns
- [ ] Parse security group rules to infer allowed connectivity
- [ ] Build a dependency graph (DAG) showing which resources depend on each other
- [ ] Visualize the dependency graph in the frontend (interactive node-link diagram)
- [ ] Assign a migration risk score (low/medium/high/critical) per resource based on:
  - Number of inbound/outbound dependencies
  - Data volume and storage size
  - Downtime tolerance (stateless vs. stateful)
  - Complexity of the target architecture
- [ ] Suggest a migration order that respects dependency constraints (migrate leaves first)
- [ ] Flag circular dependencies and resources that need coordinated migration

## Phase 4 — AI-Driven Strategy Recommendations

Move from "user picks a strategy" to "the platform recommends one."

- [ ] Collect resource utilization metrics from CloudWatch (CPU, memory, network, disk)
- [ ] Analyze usage patterns to classify workloads (steady-state, bursty, idle, batch)
- [ ] Recommend optimal migration strategy per resource based on utilization, cost, and complexity
- [ ] Generate a confidence score for each recommendation
- [ ] Allow users to override recommendations with justification (captured for audit)
- [ ] Produce a migration readiness report (PDF/HTML) summarizing recommendations, risks, and estimated savings

## Phase 5 — Migration Execution Engine

Move from tracking status to actually executing migrations.

- [ ] Pre-migration validation checks (IAM permissions, capacity, connectivity, DNS)
- [ ] Automated rehost execution: EC2 via AMI copy + launch, with security group cloning
- [ ] Database migration via AWS DMS integration (RDS, Aurora)
- [ ] S3 migration via cross-region replication or S3 Batch Operations
- [ ] Lambda and ECS migration via CloudFormation/Terraform template generation
- [ ] Parallel migration execution with configurable concurrency limits
- [ ] Automatic rollback on failure (restore from snapshot, re-point DNS, clean up target resources)
- [ ] Migration dry-run mode (validate everything but do not execute)

## Phase 6 — Infrastructure-as-Code and Runbook Generation

Auto-generate deployment artifacts so teams do not have to write them from scratch.

- [ ] Generate Terraform modules for the target architecture based on selected strategy
- [ ] Generate CloudFormation templates as an alternative
- [ ] Produce step-by-step migration runbooks per workload:
  - Pre-migration checklist (backups, notifications, maintenance windows)
  - Execution steps with estimated durations
  - Validation steps (health checks, smoke tests, data integrity)
  - Rollback plan with specific commands
- [ ] Export runbooks as Markdown, PDF, or Confluence pages
- [ ] Version-control generated IaC in a linked Git repository

## Phase 7 — Observability and Post-Migration Validation

Measure whether the migration actually delivered what was promised.

- [ ] Migration timeline visualization (Gantt-style chart of all migrations)
- [ ] Before/after cost comparison using real AWS Cost Explorer data
- [ ] Surface where cost projections were wrong and by how much
- [ ] Post-migration health monitoring (compare CloudWatch baselines before vs. after)
- [ ] Slack/Teams notifications on migration status changes
- [ ] Approval workflows — require explicit approval before proceeding to next phase
- [ ] Audit log with full history of who did what and when

## Phase 8 — Multi-Cloud and Compliance

- [ ] Azure resource discovery (VMs, Azure SQL, Blob Storage, AKS)
- [ ] GCP resource discovery (Compute Engine, Cloud SQL, GCS, GKE)
- [ ] Cross-cloud cost normalization (compare equivalent workloads across providers)
- [ ] Compliance templates for SOC 2, HIPAA, PCI-DSS, and FedRAMP
- [ ] Pre-migration compliance checklists that block execution until all checks pass
- [ ] Terraform output for multi-cloud infrastructure-as-code handoff
