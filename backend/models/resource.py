from marshmallow import Schema, fields, validate

RESOURCE_CATEGORIES = {
    "compute": ["ec2_instance", "lambda_function", "ecs_service"],
    "database": ["rds_database", "elasticache_cluster"],
    "storage": ["s3_bucket"],
    "networking": ["load_balancer", "api_gateway"],
}


def categorize_resource(resource_type):
    """Return the category for a given resource type."""
    for category, types in RESOURCE_CATEGORIES.items():
        if resource_type in types:
            return category
    return "other"


def build_resource_summary(resources):
    """Build a summary of resources grouped by category."""
    summary = {cat: [] for cat in RESOURCE_CATEGORIES}
    summary["other"] = []

    for resource in resources:
        cat = categorize_resource(resource.get("resource_type", ""))
        summary[cat].append(resource)

    return {
        "total": len(resources),
        "by_category": {k: len(v) for k, v in summary.items()},
        "details": summary,
    }


class ResourceQuerySchema(Schema):
    resource_type = fields.String()
    region = fields.String()
    tag_key = fields.String()
    tag_value = fields.String()
    limit = fields.Integer(load_default=50, validate=validate.Range(min=1, max=200))
    offset = fields.Integer(load_default=0, validate=validate.Range(min=0))
