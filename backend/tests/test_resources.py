import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        yield client


class TestResources:
    def test_list_all_resources(self, client):
        resp = client.get("/api/v1/resources")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] == 8
        assert len(data["items"]) == 8

    def test_filter_by_type(self, client):
        resp = client.get("/api/v1/resources?resource_type=ec2_instance")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] == 2
        for item in data["items"]:
            assert item["resource_type"] == "ec2_instance"

    def test_filter_by_region(self, client):
        resp = client.get("/api/v1/resources?region=us-east-1")
        assert resp.status_code == 200
        assert resp.get_json()["total"] == 8

    def test_get_single_resource(self, client):
        resp = client.get("/api/v1/resources/i-0a1b2c3d4e5f60001")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["name"] == "web-server-prod-01"

    def test_get_nonexistent_resource(self, client):
        resp = client.get("/api/v1/resources/nope")
        assert resp.status_code == 404

    def test_resource_summary(self, client):
        resp = client.get("/api/v1/resources/summary")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] == 8
        assert "by_category" in data


class TestAnalytics:
    def test_dashboard(self, client):
        resp = client.get("/api/v1/analytics/dashboard")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "migrations" in data
        assert "resources" in data

    def test_cost_estimate_all(self, client):
        resp = client.get("/api/v1/analytics/cost-estimate/all?strategy=refactor")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["strategy"] == "refactor"
        assert data["estimated_savings_pct"] == 55.0
        assert data["resource_count"] == 8

    def test_cost_estimate_custom(self, client):
        resp = client.post(
            "/api/v1/analytics/cost-estimate",
            json={
                "strategy": "rehost",
                "resources": [
                    {"resource_type": "ec2_instance"},
                    {"resource_type": "rds_database"},
                ],
            },
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["resource_count"] == 2
        assert data["estimated_savings_pct"] == 10.0
