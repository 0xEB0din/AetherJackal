import React, { useEffect, useState, useCallback } from "react";
import { fetchCostEstimate } from "../services/api";

const STRATEGIES = [
  { key: "rehost", label: "Rehost", desc: "Lift-and-shift" },
  { key: "replatform", label: "Replatform", desc: "Lift, tinker, shift" },
  { key: "refactor", label: "Refactor", desc: "Re-architect for cloud-native" },
  { key: "repurchase", label: "Repurchase", desc: "Move to SaaS" },
  { key: "retain", label: "Retain", desc: "Keep on-premises" },
  { key: "retire", label: "Retire", desc: "Decommission" },
];

function CostEstimator() {
  const [strategy, setStrategy] = useState("replatform");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback((s) => {
    setLoading(true);
    fetchCostEstimate(s)
      .then((res) => setData(res.data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { load(strategy); }, [strategy, load]);

  return (
    <div>
      <div className="page-header">
        <h2>Cost Estimator</h2>
        <p>Estimate potential savings across migration strategies</p>
      </div>

      <div className="section">
        <h3 className="section-title">Select Strategy</h3>
        <div className="strategy-select">
          {STRATEGIES.map((s) => (
            <button
              key={s.key}
              className={`strategy-btn ${strategy === s.key ? "active" : ""}`}
              onClick={() => setStrategy(s.key)}
              title={s.desc}
            >
              {s.label}
            </button>
          ))}
        </div>
      </div>

      {error && <div className="error-msg">{error}</div>}

      {loading ? (
        <div className="loading">Calculating costs...</div>
      ) : data ? (
        <>
          <div className="card-grid">
            <div className="card">
              <div className="card-label">Current Monthly Cost</div>
              <div className="card-value">
                ${data.current_monthly_estimate_usd.toLocaleString()}
              </div>
              <div className="card-sub">{data.resource_count} resources</div>
            </div>
            <div className="card">
              <div className="card-label">Projected Monthly Cost</div>
              <div className="card-value">
                ${data.projected_monthly_estimate_usd.toLocaleString()}
              </div>
              <div className="card-sub">After {strategy}</div>
            </div>
            <div className="card cost-card">
              <div className="card-label">Monthly Savings</div>
              <div className="cost-savings">
                ${data.estimated_monthly_savings_usd.toLocaleString()}
              </div>
              <div className="card-sub">{data.estimated_savings_pct}% reduction</div>
            </div>
          </div>

          <div className="section" style={{ marginTop: "1.5rem" }}>
            <h3 className="section-title">Strategy Comparison</h3>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Strategy</th>
                    <th>Description</th>
                    <th>Typical Savings</th>
                    <th>Complexity</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Rehost</td>
                    <td>Move as-is to cloud infrastructure</td>
                    <td>~10%</td>
                    <td><span className="badge badge-completed">Low</span></td>
                  </tr>
                  <tr>
                    <td>Replatform</td>
                    <td>Minor optimizations during migration</td>
                    <td>~25%</td>
                    <td><span className="badge badge-analyzing">Medium</span></td>
                  </tr>
                  <tr>
                    <td>Refactor</td>
                    <td>Rebuild as cloud-native / serverless</td>
                    <td>~55%</td>
                    <td><span className="badge badge-in_progress">High</span></td>
                  </tr>
                  <tr>
                    <td>Repurchase</td>
                    <td>Replace with managed SaaS solution</td>
                    <td>~30%</td>
                    <td><span className="badge badge-analyzing">Medium</span></td>
                  </tr>
                  <tr>
                    <td>Retire</td>
                    <td>Decommission unused workloads</td>
                    <td>100%</td>
                    <td><span className="badge badge-completed">Low</span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
}

export default CostEstimator;
