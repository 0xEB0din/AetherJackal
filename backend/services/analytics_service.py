import logging
from services.migration_service import get_migration_stats
from services.resource_service import get_resource_summary

logger = logging.getLogger(__name__)

# Rough cost model for estimation purposes.
# In production, pull real pricing from the AWS Price List API.
_HOURLY_COST = {
    "ec2_instance": 0.0416,     # t3.medium on-demand
    "rds_database": 0.096,      # db.t3.medium postgres
    "s3_bucket": 0.023,         # per GB/month, simplified
    "lambda_function": 0.0,     # pay-per-invoke, negligible idle
    "ecs_service": 0.05,        # fargate vCPU-hour estimate
    "elasticache_cluster": 0.068,
    "load_balancer": 0.0225,
    "api_gateway": 0.0,         # pay-per-request
}

_SERVERLESS_SAVINGS_FACTOR = {
    "rehost": 0.10,
    "replatform": 0.25,
    "refactor": 0.55,
    "repurchase": 0.30,
    "retain": 0.0,
    "retire": 1.0,
}


def estimate_costs(resources, strategy="replatform"):
    """Produce a cost estimate for migrating the given resources."""
    current_monthly = 0.0
    for r in resources:
        rtype = r.get("resource_type", "")
        hourly = _HOURLY_COST.get(rtype, 0.0)
        current_monthly += hourly * 730  # avg hours/month

    savings_pct = _SERVERLESS_SAVINGS_FACTOR.get(strategy, 0.0)
    projected_monthly = current_monthly * (1 - savings_pct)

    return {
        "current_monthly_estimate_usd": round(current_monthly, 2),
        "projected_monthly_estimate_usd": round(projected_monthly, 2),
        "estimated_savings_pct": round(savings_pct * 100, 1),
        "estimated_monthly_savings_usd": round(current_monthly - projected_monthly, 2),
        "strategy": strategy,
        "resource_count": len(resources),
    }


def get_dashboard_analytics():
    """Aggregate data for the main dashboard view."""
    migration_stats = get_migration_stats()
    resource_summary = get_resource_summary()

    return {
        "migrations": migration_stats,
        "resources": resource_summary,
    }
