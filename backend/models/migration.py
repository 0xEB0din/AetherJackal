import uuid
from datetime import datetime, timezone
from marshmallow import Schema, fields, validate

VALID_STATUSES = [
    "pending",
    "analyzing",
    "ready",
    "in_progress",
    "validating",
    "completed",
    "failed",
    "rolled_back",
]

VALID_STRATEGIES = [
    "rehost",       # lift-and-shift
    "replatform",   # lift-tinker-shift
    "refactor",     # re-architect for cloud-native
    "repurchase",   # move to SaaS
    "retain",       # keep on-prem for now
    "retire",       # decommission
]

VALID_RESOURCE_TYPES = [
    "ec2_instance",
    "rds_database",
    "s3_bucket",
    "lambda_function",
    "ecs_service",
    "elasticache_cluster",
    "load_balancer",
    "api_gateway",
]


def new_migration(name, source_env, target_env, strategy, resources=None):
    """Create a new migration record."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "source_environment": source_env,
        "target_environment": target_env,
        "strategy": strategy,
        "status": "pending",
        "resources": resources or [],
        "created_at": now,
        "updated_at": now,
        "started_at": None,
        "completed_at": None,
        "error_log": [],
        "rollback_available": False,
    }


class ResourceSchema(Schema):
    resource_id = fields.String(required=True)
    resource_type = fields.String(
        required=True,
        validate=validate.OneOf(VALID_RESOURCE_TYPES),
    )
    name = fields.String(required=True)
    region = fields.String(load_default="us-east-1")
    tags = fields.Dict(keys=fields.String(), values=fields.String(), load_default={})


class MigrationCreateSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=128))
    source_environment = fields.String(required=True)
    target_environment = fields.String(required=True)
    strategy = fields.String(
        required=True,
        validate=validate.OneOf(VALID_STRATEGIES),
    )
    resources = fields.List(fields.Nested(ResourceSchema), load_default=[])


class MigrationUpdateSchema(Schema):
    name = fields.String(validate=validate.Length(min=1, max=128))
    status = fields.String(validate=validate.OneOf(VALID_STATUSES))
    strategy = fields.String(validate=validate.OneOf(VALID_STRATEGIES))
    resources = fields.List(fields.Nested(ResourceSchema))
