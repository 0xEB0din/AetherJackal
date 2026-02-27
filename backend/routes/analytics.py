from flask import Blueprint, request, jsonify

from services.analytics_service import estimate_costs, get_dashboard_analytics
from services.resource_service import discover_resources

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return jsonify(get_dashboard_analytics()), 200


@analytics_bp.route("/cost-estimate", methods=["POST"])
def cost_estimate():
    body = request.get_json()
    if not body or "resources" not in body:
        return jsonify({"error": "Request body must include 'resources' list"}), 400

    strategy = body.get("strategy", "replatform")
    estimate = estimate_costs(body["resources"], strategy=strategy)
    return jsonify(estimate), 200


@analytics_bp.route("/cost-estimate/all", methods=["GET"])
def cost_estimate_all():
    """Quick estimate using every discovered resource."""
    strategy = request.args.get("strategy", "replatform")
    all_resources = discover_resources(limit=200)["items"]
    estimate = estimate_costs(all_resources, strategy=strategy)
    return jsonify(estimate), 200
