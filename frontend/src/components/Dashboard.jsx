import React, { useEffect, useState } from "react";
import { fetchDashboard, fetchCostEstimate } from "../services/api";

function Dashboard() {
  const [data, setData] = useState(null);
  const [costs, setCosts] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([fetchDashboard(), fetchCostEstimate("replatform")])
      .then(([dashRes, costRes]) => {
        setData(dashRes.data);
        setCosts(costRes.data);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error-msg">{error}</div>;

  const { migrations, resources } = data;

  return (
    <div>
      <div className="page-header">
        <h2>Dashboard</h2>
        <p>Overview of your cloud migration status</p>
      </div>

      <div className="section">
        <h3 className="section-title">Migration Summary</h3>
        <div className="card-grid">
          <div className="card">
            <div className="card-label">Total Migrations</div>
            <div className="card-value">{migrations.total}</div>
          </div>
          {Object.entries(migrations.by_status).map(([status, count]) => (
            <div className="card" key={status}>
              <div className="card-label">{status.replace("_", " ")}</div>
              <div className="card-value">{count}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <h3 className="section-title">Resource Inventory</h3>
        <div className="card-grid">
          <div className="card">
            <div className="card-label">Total Resources</div>
            <div className="card-value">{resources.total}</div>
          </div>
          {Object.entries(resources.by_category)
            .filter(([, count]) => count > 0)
            .map(([cat, count]) => (
              <div className="card" key={cat}>
                <div className="card-label">{cat}</div>
                <div className="card-value">{count}</div>
              </div>
            ))}
        </div>
      </div>

      {costs && (
        <div className="section">
          <h3 className="section-title">Cost Snapshot (Replatform)</h3>
          <div className="card-grid">
            <div className="card">
              <div className="card-label">Current Monthly</div>
              <div className="card-value">
                ${costs.current_monthly_estimate_usd.toLocaleString()}
              </div>
            </div>
            <div className="card">
              <div className="card-label">Projected Monthly</div>
              <div className="card-value">
                ${costs.projected_monthly_estimate_usd.toLocaleString()}
              </div>
            </div>
            <div className="card cost-card">
              <div className="card-label">Estimated Savings</div>
              <div className="card-value">{costs.estimated_savings_pct}%</div>
              <div className="card-sub">
                ${costs.estimated_monthly_savings_usd.toLocaleString()}/mo
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
