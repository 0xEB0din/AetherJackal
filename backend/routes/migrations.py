from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from models.migration import (
    MigrationCreateSchema,
    MigrationUpdateSchema,
    new_migration,
)
from services.migration_service import (
    list_migrations,
    get_migration,
    create_migration,
    update_migration,
    delete_migration,
    get_migration_stats,
)

migrations_bp = Blueprint("migrations", __name__)

_create_schema = MigrationCreateSchema()
_update_schema = MigrationUpdateSchema()


@migrations_bp.route("", methods=["GET"])
def index():
    status = request.args.get("status")
    limit = request.args.get("limit", 50, type=int)
    offset = request.args.get("offset", 0, type=int)
    result = list_migrations(status_filter=status, limit=limit, offset=offset)
    return jsonify(result), 200


@migrations_bp.route("/<migration_id>", methods=["GET"])
def show(migration_id):
    migration = get_migration(migration_id)
    if migration is None:
        return jsonify({"error": "Migration not found"}), 404
    return jsonify(migration), 200


@migrations_bp.route("", methods=["POST"])
def create():
    try:
        data = _create_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    record = new_migration(
        name=data["name"],
        source_env=data["source_environment"],
        target_env=data["target_environment"],
        strategy=data["strategy"],
        resources=data.get("resources", []),
    )
    created = create_migration(record)
    return jsonify(created), 201


@migrations_bp.route("/<migration_id>", methods=["PATCH"])
def update(migration_id):
    try:
        data = _update_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    updated = update_migration(migration_id, data)
    if updated is None:
        return jsonify({"error": "Migration not found"}), 404
    return jsonify(updated), 200


@migrations_bp.route("/<migration_id>", methods=["DELETE"])
def destroy(migration_id):
    if delete_migration(migration_id):
        return jsonify({"deleted": True}), 200
    return jsonify({"error": "Migration not found"}), 404


@migrations_bp.route("/stats", methods=["GET"])
def stats():
    return jsonify(get_migration_stats()), 200
