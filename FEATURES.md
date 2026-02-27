# Features and Use Cases

## Current State (Phase 1 — Prototype)

CloudMigrate Pro is a **working prototype** of a cloud migration planning platform. It demonstrates the architecture and workflows but uses demo data and has no production-grade infrastructure.

### What Works Today

- **Resource inventory view** — Browse 8 pre-loaded AWS resource types (EC2, RDS, S3, Lambda, ECS, ElastiCache, ALB, API Gateway) with filtering by type, region, and tags
- **Migration CRUD** — Create, update, and delete migration records with lifecycle tracking through 8 states (pending, analyzing, ready, in_progress, validating, completed, failed, rolled_back)
- **Cost estimation** — Compare projected monthly costs across 6 migration strategies with savings percentages
- **Dashboard** — Aggregated view of migration stats and resource counts
- **Flexible deployment** — Same codebase runs locally, in Docker, or on AWS Lambda
- **CI/CD pipeline** — Jenkins pipeline with parallel lint, test, build, and deploy stages

### What Does Not Work Yet

- Resource data is hardcoded — no live AWS discovery
- Cost estimates use static rates — not real AWS pricing
- No authentication or authorization
- No actual migration execution — status is updated manually
- No dependency mapping between resources
- No rollback automation
- State is stored in a JSON file on disk — lost on restart

## What Would Make This Special

The features below are what would differentiate CloudMigrate Pro from existing tools (AWS Migration Hub, CloudEndure, Cloudamize, etc.). None of these exist yet — they are the target.

### 1. Automatic Dependency Mapping

**The problem:** The hardest part of any migration is understanding what talks to what. Teams spend weeks manually tracing connections between services, databases, and load balancers.

**The goal:** Analyze VPC flow logs and security group rules to automatically build a dependency graph. Visualize it as an interactive diagram. Suggest a migration order that respects dependencies (migrate leaf nodes first, avoid breaking connections).

**Why it matters:** Almost no open-source migration tool does this well. AWS Migration Hub requires installing agents on every server. An agentless, API-driven approach using existing AWS telemetry would be a genuine differentiator.

### 2. AI-Driven Strategy Recommendations

**The problem:** Today, CloudMigrate Pro asks the user to pick a strategy. Most users do not know whether their workload should be rehosted, replatformed, or refactored.

**The goal:** Analyze CloudWatch metrics (CPU, memory, network patterns) to classify workloads (steady-state, bursty, idle, batch) and recommend the optimal strategy with a confidence score.

**Why it matters:** Turns the platform from a passive tracker into an active advisor. Recommendations backed by real utilization data are far more useful than a dropdown menu.

### 3. Migration Risk Scoring

**The problem:** Not all migrations carry the same risk. Moving a stateless web server is trivial; migrating a primary database with 500GB of data and 20 dependent services is high-risk.

**The goal:** Score each migration as low/medium/high/critical based on dependency count, data volume, downtime tolerance, and target architecture complexity. Surface high-risk migrations prominently so teams can plan accordingly.

**Why it matters:** Prevents teams from discovering risks mid-migration. Prioritizes planning effort where it matters most.

### 4. Infrastructure-as-Code Generation

**The problem:** After deciding on a strategy, teams still have to manually write Terraform or CloudFormation for the target architecture.

**The goal:** Auto-generate IaC templates based on the source resource, selected strategy, and target environment. Teams review and apply rather than writing from scratch.

**Why it matters:** Bridges the gap between "planning" and "doing." Most migration tools stop at planning; this would carry the user into execution.

### 5. Before/After Cost Actuals

**The problem:** Cost estimates are projections. After migration, nobody goes back to check whether the savings materialized.

**The goal:** After a migration completes, pull real spend data from AWS Cost Explorer and compare it to the pre-migration projection. Surface where estimates were accurate and where they were wrong.

**Why it matters:** Builds trust in the platform's estimates over time and surfaces hidden costs (data transfer, API calls, logging) that projections often miss.

## Use Cases

### Migration Planning and Strategy Selection

A team needs to migrate 50+ workloads to AWS but does not know which strategy to apply to each. CloudMigrate Pro provides a single inventory of all resources, runs cost estimates across all strategies, and (once Phase 4 is built) recommends the optimal approach per workload.

### Cost Forecasting for Budget Approval

A team lead needs to present projected cloud costs to leadership. The platform generates current vs. projected monthly spend per strategy, giving concrete dollar amounts to include in a budget proposal. After migration, actual costs can be compared to validate the projections.

### Migration Execution Tracking

Multiple teams are migrating workloads in parallel. The dashboard shows overall progress (how many pending, in-progress, completed, failed), surfaces blockers, and provides rollback status for completed migrations.

### Resource Inventory and Audit

An organization has accumulated cloud resources over years and lacks a clear inventory. The platform discovers and categorizes all resources by type, region, and tags, giving a clean starting point for migration or cost optimization.

### Compliance-Driven Migration

A regulated organization needs to demonstrate that migrations followed a controlled process. The platform tracks state transitions with timestamps, captures error details on failure, and (once Phase 8 is built) enforces compliance checklists before execution can proceed.

### Team Coordination

A platform engineering team coordinates migrations across multiple application teams. The shared dashboard with filtering and aggregate statistics gives visibility without requiring status meetings.

## Summary

CloudMigrate Pro is not special today — it is a well-structured prototype. What would make it special is building the features in Phases 3-6 of the [roadmap](ROADMAP.md): dependency mapping, AI-driven recommendations, risk scoring, and IaC generation. These are the capabilities that existing migration tools either lack entirely or lock behind expensive enterprise licenses.
