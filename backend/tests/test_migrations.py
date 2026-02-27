import json
import os
import shutil
import pytest

from app import create_app


@pytest.fixture(autouse=True)
def clean_state(tmp_path):
    """Use a temp dir for migration state so tests are isolated."""
    os.environ["MIGRATION_STATE_DIR"] = str(tmp_path)
    yield
    if tmp_path.exists():
        shutil.rmtree(tmp_path, ignore_errors=True)


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def _create_migration(client, **overrides):
    payload = {
        "name": "Test Migration",
        "source_environment": "on-prem-dc1",
        "target_environment": "aws-us-east-1",
        "strategy": "replatform",
    }
    payload.update(overrides)
    return client.post(
        "/api/v1/migrations",
        data=json.dumps(payload),
        content_type="application/json",
    )


class TestMigrationsCRUD:
    def test_create_migration(self, client):
        resp = _create_migration(client)
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Test Migration"
        assert data["status"] == "pending"
        assert "id" in data

    def test_list_migrations(self, client):
        _create_migration(client, name="Migration A")
        _create_migration(client, name="Migration B")
        resp = client.get("/api/v1/migrations")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_get_single_migration(self, client):
        create_resp = _create_migration(client)
        mid = create_resp.get_json()["id"]

        resp = client.get(f"/api/v1/migrations/{mid}")
        assert resp.status_code == 200
        assert resp.get_json()["id"] == mid

    def test_get_nonexistent_returns_404(self, client):
        resp = client.get("/api/v1/migrations/does-not-exist")
        assert resp.status_code == 404

    def test_update_migration_status(self, client):
        create_resp = _create_migration(client)
        mid = create_resp.get_json()["id"]

        resp = client.patch(
            f"/api/v1/migrations/{mid}",
            data=json.dumps({"status": "in_progress"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "in_progress"
        assert resp.get_json()["started_at"] is not None

    def test_complete_migration(self, client):
        create_resp = _create_migration(client)
        mid = create_resp.get_json()["id"]

        client.patch(
            f"/api/v1/migrations/{mid}",
            data=json.dumps({"status": "in_progress"}),
            content_type="application/json",
        )
        resp = client.patch(
            f"/api/v1/migrations/{mid}",
            data=json.dumps({"status": "completed"}),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "completed"
        assert data["completed_at"] is not None
        assert data["rollback_available"] is True

    def test_delete_migration(self, client):
        create_resp = _create_migration(client)
        mid = create_resp.get_json()["id"]

        resp = client.delete(f"/api/v1/migrations/{mid}")
        assert resp.status_code == 200
        assert resp.get_json()["deleted"] is True

        resp = client.get(f"/api/v1/migrations/{mid}")
        assert resp.status_code == 404

    def test_create_with_invalid_strategy(self, client):
        resp = _create_migration(client, strategy="invalid")
        assert resp.status_code == 400

    def test_filter_by_status(self, client):
        _create_migration(client, name="A")
        create_resp = _create_migration(client, name="B")
        mid = create_resp.get_json()["id"]
        client.patch(
            f"/api/v1/migrations/{mid}",
            data=json.dumps({"status": "in_progress"}),
            content_type="application/json",
        )

        resp = client.get("/api/v1/migrations?status=in_progress")
        assert resp.status_code == 200
        assert resp.get_json()["total"] == 1

    def test_stats_endpoint(self, client):
        _create_migration(client, name="A")
        _create_migration(client, name="B")
        resp = client.get("/api/v1/migrations/stats")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] == 2
