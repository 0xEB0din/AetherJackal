import React from "react";
import { Routes, Route, NavLink } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import MigrationList from "./components/MigrationList";
import ResourceInventory from "./components/ResourceInventory";
import CostEstimator from "./components/CostEstimator";

function App() {
  return (
    <div className="app">
      <nav className="sidebar">
        <div className="sidebar-brand">
          <h1>CloudMigrate</h1>
          <span className="brand-tag">PRO</span>
        </div>
        <ul className="nav-links">
          <li>
            <NavLink to="/" end>Dashboard</NavLink>
          </li>
          <li>
            <NavLink to="/migrations">Migrations</NavLink>
          </li>
          <li>
            <NavLink to="/resources">Resources</NavLink>
          </li>
          <li>
            <NavLink to="/costs">Cost Estimator</NavLink>
          </li>
        </ul>
        <div className="sidebar-footer">
          <p>v0.1.0</p>
        </div>
      </nav>

      <main className="content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/migrations" element={<MigrationList />} />
          <Route path="/resources" element={<ResourceInventory />} />
          <Route path="/costs" element={<CostEstimator />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
