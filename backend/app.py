import os
import logging

from flask import Flask
from flask_cors import CORS

from config import config_by_name
from routes.health import health_bp
from routes.migrations import migrations_bp
from routes.resources import resources_bp
from routes.analytics import analytics_bp


def create_app(config_name=None):
    """Application factory for the CloudMigrate Pro backend."""
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"]),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    app.register_blueprint(health_bp)
    app.register_blueprint(migrations_bp, url_prefix="/api/v1/migrations")
    app.register_blueprint(resources_bp, url_prefix="/api/v1/resources")
    app.register_blueprint(analytics_bp, url_prefix="/api/v1/analytics")

    state_dir = app.config["MIGRATION_STATE_DIR"]
    os.makedirs(state_dir, exist_ok=True)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000)
