import axios from "axios";

const BASE_URL = process.env.REACT_APP_API_URL || "/api/v1";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

// ---- Migrations ----

export function fetchMigrations(params = {}) {
  return api.get("/migrations", { params });
}

export function fetchMigration(id) {
  return api.get(`/migrations/${id}`);
}

export function createMigration(data) {
  return api.post("/migrations", data);
}

export function updateMigration(id, data) {
  return api.patch(`/migrations/${id}`, data);
}

export function deleteMigration(id) {
  return api.delete(`/migrations/${id}`);
}

export function fetchMigrationStats() {
  return api.get("/migrations/stats");
}

// ---- Resources ----

export function fetchResources(params = {}) {
  return api.get("/resources", { params });
}

export function fetchResourceSummary() {
  return api.get("/resources/summary");
}

// ---- Analytics ----

export function fetchDashboard() {
  return api.get("/analytics/dashboard");
}

export function fetchCostEstimate(strategy = "replatform") {
  return api.get("/analytics/cost-estimate/all", { params: { strategy } });
}

export default api;
