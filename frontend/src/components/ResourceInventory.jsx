import React, { useEffect, useState } from "react";
import { fetchResources, fetchResourceSummary } from "../services/api";

const TYPE_LABELS = {
  ec2_instance: "EC2 Instance",
  rds_database: "RDS Database",
  s3_bucket: "S3 Bucket",
  lambda_function: "Lambda Function",
  ecs_service: "ECS Service",
  elasticache_cluster: "ElastiCache",
  load_balancer: "Load Balancer",
  api_gateway: "API Gateway",
};

function ResourceInventory() {
  const [resources, setResources] = useState([]);
  const [summary, setSummary] = useState(null);
  const [filter, setFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([fetchResources(), fetchResourceSummary()])
      .then(([resRes, sumRes]) => {
        setResources(resRes.data.items);
        setSummary(sumRes.data);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Discovering resources...</div>;
  if (error) return <div className="error-msg">{error}</div>;

  const filtered = filter
    ? resources.filter((r) => r.resource_type === filter)
    : resources;

  return (
    <div>
      <div className="page-header">
        <h2>Resource Inventory</h2>
        <p>Discovered cloud resources available for migration</p>
      </div>

      {summary && (
        <div className="card-grid">
          <div className="card">
            <div className="card-label">Total Discovered</div>
            <div className="card-value">{summary.total}</div>
          </div>
          {Object.entries(summary.by_category)
            .filter(([, count]) => count > 0)
            .map(([cat, count]) => (
              <div className="card" key={cat}>
                <div className="card-label">{cat}</div>
                <div className="card-value">{count}</div>
              </div>
            ))}
        </div>
      )}

      <div style={{ marginBottom: "1rem" }}>
        <select
          className="btn btn-outline"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          style={{ padding: "0.45rem 0.75rem", cursor: "pointer" }}
        >
          <option value="">All Types</option>
          {Object.entries(TYPE_LABELS).map(([val, label]) => (
            <option key={val} value={val}>{label}</option>
          ))}
        </select>
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Resource ID</th>
              <th>Region</th>
              <th>Tags</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((r) => (
              <tr key={r.resource_id}>
                <td>{r.name}</td>
                <td>{TYPE_LABELS[r.resource_type] || r.resource_type}</td>
                <td style={{ fontFamily: "monospace", fontSize: "0.8rem" }}>
                  {r.resource_id}
                </td>
                <td>{r.region}</td>
                <td>
                  {Object.entries(r.tags || {}).map(([k, v]) => (
                    <span
                      key={k}
                      className="badge badge-analyzing"
                      style={{ marginRight: "0.3rem" }}
                    >
                      {k}: {v}
                    </span>
                  ))}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ResourceInventory;
