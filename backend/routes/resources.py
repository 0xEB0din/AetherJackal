from flask import Blueprint, request, jsonify

from services.resource_service import (
    discover_resources,
    get_resource,
    get_resource_summary,
)

resources_bp = Blueprint("resources", __name__)


@resources_bp.route("", methods=["GET"])
def index():
    result = discover_resources(
        resource_type=request.args.get("resource_type"),
        region=request.args.get("region"),
        tag_key=request.args.get("tag_key"),
        tag_value=request.args.get("tag_value"),
        limit=request.args.get("limit", 50, type=int),
        offset=request.args.get("offset", 0, type=int),
    )
    return jsonify(result), 200


@resources_bp.route("/summary", methods=["GET"])
def summary():
    return jsonify(get_resource_summary()), 200


@resources_bp.route("/<resource_id>", methods=["GET"])
def show(resource_id):
    resource = get_resource(resource_id)
    if resource is None:
        return jsonify({"error": "Resource not found"}), 404
    return jsonify(resource), 200
