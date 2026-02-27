import React, { useEffect, useState, useCallback } from "react";
import {
  fetchMigrations,
  createMigration,
  updateMigration,
  deleteMigration,
} from "../services/api";

const STRATEGIES = [
  "rehost",
  "replatform",
  "refactor",
  "repurchase",
  "retain",
  "retire",
];

const EMPTY_FORM = {
  name: "",
  source_environment: "",
  target_environment: "",
  strategy: "replatform",
};

function MigrationList() {
  const [migrations, setMigrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);

  const load = useCallback(() => {
    setLoading(true);
    fetchMigrations()
      .then((res) => setMigrations(res.data.items))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleCreate = (e) => {
    e.preventDefault();
    createMigration(form)
      .then(() => {
        setForm(EMPTY_FORM);
        setShowForm(false);
        load();
      })
      .catch((err) => setError(err.message));
  };

  const handleStatusChange = (id, status) => {
    updateMigration(id, { status })
      .then(() => load())
      .catch((err) => setError(err.message));
  };

  const handleDelete = (id) => {
    deleteMigration(id)
      .then(() => load())
      .catch((err) => setError(err.message));
  };

  if (loading) return <div className="loading">Loading migrations...</div>;

  return (
    <div>
      <div className="page-header">
        <h2>Migrations</h2>
        <p>Manage and track your cloud migration workloads</p>
      </div>

      {error && <div className="error-msg">{error}</div>}

      <div style={{ marginBottom: "1.5rem" }}>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "Cancel" : "+ New Migration"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="card" style={{ marginBottom: "1.5rem" }}>
          <div className="form-row">
            <div className="form-group">
              <label>Migration Name</label>
              <input
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                placeholder="e.g. Migrate user-service to ECS"
                required
              />
            </div>
            <div className="form-group">
              <label>Strategy</label>
              <select
                value={form.strategy}
                onChange={(e) => setForm({ ...form, strategy: e.target.value })}
              >
                {STRATEGIES.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Source Environment</label>
              <input
                value={form.source_environment}
                onChange={(e) => setForm({ ...form, source_environment: e.target.value })}
                placeholder="e.g. on-prem-dc1"
                required
              />
            </div>
            <div className="form-group">
              <label>Target Environment</label>
              <input
                value={form.target_environment}
                onChange={(e) => setForm({ ...form, target_environment: e.target.value })}
                placeholder="e.g. aws-us-east-1"
                required
              />
            </div>
          </div>
          <button type="submit" className="btn btn-primary">Create Migration</button>
        </form>
      )}

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Strategy</th>
              <th>Source</th>
              <th>Target</th>
              <th>Status</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {migrations.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ textAlign: "center", color: "var(--text-secondary)" }}>
                  No migrations yet. Create one to get started.
                </td>
              </tr>
            ) : (
              migrations.map((m) => (
                <tr key={m.id}>
                  <td>{m.name}</td>
                  <td>{m.strategy}</td>
                  <td>{m.source_environment}</td>
                  <td>{m.target_environment}</td>
                  <td>
                    <span className={`badge badge-${m.status}`}>{m.status.replace("_", " ")}</span>
                  </td>
                  <td>{new Date(m.created_at).toLocaleDateString()}</td>
                  <td>
                    {m.status === "pending" && (
                      <button
                        className="btn btn-outline"
                        onClick={() => handleStatusChange(m.id, "in_progress")}
                      >
                        Start
                      </button>
                    )}
                    {m.status === "in_progress" && (
                      <button
                        className="btn btn-outline"
                        onClick={() => handleStatusChange(m.id, "completed")}
                      >
                        Complete
                      </button>
                    )}
                    {" "}
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDelete(m.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default MigrationList;
