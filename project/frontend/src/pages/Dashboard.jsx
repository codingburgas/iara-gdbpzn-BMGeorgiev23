import { useState, useEffect } from "react";
import { API, SEVERITY_COLOR } from "../constants";
import { StatCard, Badge, FuelBar, Card, LoadingSpinner, PageHeader } from "../components/UI";

export default function Dashboard({ setPage, setSelectedIncident }) {
  const [summary,   setSummary]   = useState(null);
  const [incidents, setIncidents] = useState([]);
  const [vehicles,  setVehicles]  = useState([]);
  const [teams,     setTeams]     = useState([]);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/incidents/summary`).then(r => r.json()),
      fetch(`${API}/incidents/`).then(r => r.json()),
      fetch(`${API}/vehicles/`).then(r => r.json()),
      fetch(`${API}/teams/`).then(r => r.json()),
    ]).then(([sum, inc, veh, tm]) => {
      setSummary(sum); setIncidents(inc); setVehicles(veh); setTeams(tm);
    });
  }, []);

  if (!summary) return <LoadingSpinner />;

  return (
    <div style={{ animation: "fadeSlideIn 0.3s ease both" }}>
      <PageHeader eyebrow="Оперативен Център" title="Табло за управление" />

      <div style={{ display: "flex", gap: 10, marginBottom: 22, flexWrap: "wrap" }}>
        <StatCard label="Активни произшествия" value={summary.active_incidents}  color="#ff6b6b" />
        <StatCard label="Разгърнати екипи"      value={summary.deployed_teams}    color="#ffb347" />
        <StatCard label="Екипи в готовност"     value={summary.standby_teams}     color="#5ba3d9" />
        <StatCard label="Налични служители"     value={`${summary.available_staff}/${summary.total_staff}`} />
      </div>

      <div style={{ fontSize: 10, color: "#3a3a3a", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 10 }}>Последни произшествия</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 7, marginBottom: 22 }}>
        {incidents.map((inc, i) => (
          <Card key={inc.id} onClick={() => { setSelectedIncident(inc); setPage("incidents"); }}
            style={{ animation: "fadeSlideIn 0.3s ease both", animationDelay: `${i * 50}ms` }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{ width: 7, height: 7, borderRadius: "50%", background: SEVERITY_COLOR[inc.severity], flexShrink: 0 }} />
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 13, fontWeight: 600, color: "#c0c0c0", marginBottom: 2 }}>{inc.id} — {inc.type}</div>
                <div style={{ fontSize: 11, color: "#444", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{inc.address}</div>
              </div>
              <span style={{ fontSize: 11, color: "#444", marginRight: 8 }}>{inc.time}</span>
              <Badge status={inc.status} label={inc.status === "active" ? "Активно" : "Приключено"} />
            </div>
          </Card>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
        <Card>
          <div style={{ fontSize: 10, color: "#3a3a3a", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 12 }}>Статус на екипи</div>
          {teams.map(t => (
            <div key={t.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "7px 0", borderBottom: "1px solid #141414" }}>
              <span style={{ fontSize: 12, color: "#888" }}>{t.name}</span>
              <Badge status={t.status} label={t.status === "deployed" ? "Разгърнат" : t.status === "standby" ? "Готовност" : "Изкл."} />
            </div>
          ))}
        </Card>
        <Card>
          <div style={{ fontSize: 10, color: "#3a3a3a", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 12 }}>Горивни нива</div>
          {vehicles.map(v => (
            <div key={v.id} style={{ padding: "6px 0", borderBottom: "1px solid #141414" }}>
              <div style={{ fontSize: 11, color: "#555", marginBottom: 5 }}>{v.id} — {v.type}</div>
              <FuelBar pct={v.fuel} />
            </div>
          ))}
        </Card>
      </div>
    </div>
  );
}
