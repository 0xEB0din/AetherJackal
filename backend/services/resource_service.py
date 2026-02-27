import logging

from models.resource import categorize_resource, build_resource_summary

logger = logging.getLogger(__name__)

# In a real deployment this would call AWS APIs via boto3.
# For the demo we use a static inventory that can be swapped
# out for live discovery once credentials are configured.

_DEMO_RESOURCES = [
    {
        "resource_id": "i-0a1b2c3d4e5f60001",
        "resource_type": "ec2_instance",
        "name": "web-server-prod-01",
        "region": "us-east-1",
        "tags": {"environment": "production", "team": "platform"},
        "specs": {"instance_type": "t3.medium", "state": "running"},
    },
    {
        "resource_id": "i-0a1b2c3d4e5f60002",
        "resource_type": "ec2_instance",
        "name": "web-server-prod-02",
        "region": "us-east-1",
        "tags": {"environment": "production", "team": "platform"},
        "specs": {"instance_type": "t3.medium", "state": "running"},
    },
    {
        "resource_id": "db-cluster-prod-01",
        "resource_type": "rds_database",
        "name": "userdb-primary",
        "region": "us-east-1",
        "tags": {"environment": "production", "team": "data"},
        "specs": {"engine": "postgres", "version": "15.4", "multi_az": True},
    },
    {
        "resource_id": "s3-assets-prod",
        "resource_type": "s3_bucket",
        "name": "cloudmigrate-assets-prod",
        "region": "us-east-1",
        "tags": {"environment": "production"},
        "specs": {"versioning": True, "size_gb": 245},
    },
    {
        "resource_id": "lambda-auth-handler",
        "resource_type": "lambda_function",
        "name": "auth-handler",
        "region": "us-east-1",
        "tags": {"environment": "production", "team": "identity"},
        "specs": {"runtime": "python3.12", "memory_mb": 256, "timeout_s": 30},
    },
    {
        "resource_id": "ecs-api-service",
        "resource_type": "ecs_service",
        "name": "api-gateway-service",
        "region": "us-east-1",
        "tags": {"environment": "production", "team": "platform"},
        "specs": {"launch_type": "FARGATE", "desired_count": 3},
    },
    {
        "resource_id": "cache-sessions-prod",
        "resource_type": "elasticache_cluster",
        "name": "session-cache",
        "region": "us-east-1",
        "tags": {"environment": "production", "team": "platform"},
        "specs": {"engine": "redis", "node_type": "cache.r6g.large", "num_nodes": 2},
    },
    {
        "resource_id": "alb-web-prod",
        "resource_type": "load_balancer",
        "name": "web-alb-prod",
        "region": "us-east-1",
        "tags": {"environment": "production", "team": "platform"},
        "specs": {"type": "application", "scheme": "internet-facing"},
    },
]


def discover_resources(resource_type=None, region=None, tag_key=None,
                       tag_value=None, limit=50, offset=0):
    """Return discovered cloud resources with optional filters."""
    results = list(_DEMO_RESOURCES)

    if resource_type:
        results = [r for r in results if r["resource_type"] == resource_type]
    if region:
        results = [r for r in results if r["region"] == region]
    if tag_key:
        results = [r for r in results if tag_key in r.get("tags", {})]
    if tag_key and tag_value:
        results = [r for r in results if r.get("tags", {}).get(tag_key) == tag_value]

    total = len(results)
    page = results[offset: offset + limit]

    return {"items": page, "total": total, "limit": limit, "offset": offset}


def get_resource(resource_id):
    """Look up a single resource by ID."""
    for r in _DEMO_RESOURCES:
        if r["resource_id"] == resource_id:
            return r
    return None


def get_resource_summary():
    """Return an aggregated summary of all discovered resources."""
    return build_resource_summary(_DEMO_RESOURCES)
