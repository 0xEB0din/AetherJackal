from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/healthz")
def healthz():
    return jsonify({"status": "healthy"}), 200


@health_bp.route("/readyz")
def readyz():
    return jsonify({"status": "ready"}), 200
