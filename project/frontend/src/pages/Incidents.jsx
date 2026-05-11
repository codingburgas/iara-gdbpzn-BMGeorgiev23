import { useState, useEffect } from "react";
import { API, SEVERITY_COLOR, SEVERITY_LABEL } from "../constants";
import { Badge, Card, BackButton, LoadingSpinner, PageHeader } from "../components/UI";

function IncidentDetail({ inc, onBack }) {
  return (
    <div style={{ animation: "fadeSlideIn 0.25s ease both" }}>
      <BackButton onClick={onBack} />
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: 20 }}>
        <div>
          <div style={{ fontSize: 10, color: "#444", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 4 }}>{inc.id}</div>
          <div style={{ fontSize: 20, fontWeight: 700, color: "#e0e0e0" }}>{inc.type}</div>
          <div style={{ fontSize: 12, color: "#555", marginTop: 4 }}>{inc.address}</div>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <span style={{ fontSize: 11, color: SEVERITY_COLOR[inc.severity], border: `1px solid ${SEVERITY_COLOR[inc.severity]}`, padding: "2px 8px", borderRadius: 4, fontWeight: 700 }}>
            {SEVERITY_LABEL[inc.severity]} опасност
          </span>
          <Badge status={inc.status} label={inc.status === "active" ? "Активно" : "Приключено"} />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 14 }}>
        {[
          ["Час на регистрация", inc.time],
          ["GPS координати", `${inc.gps.lat}° N, ${inc.gps.lng}° E`],
          ["Отговорен екип", inc.team],
          ["Опасни вещества", inc.hazmat || "Не са установени"],
        ].map(([lbl, val]) => (
          <div key={lbl} style={{ background: "#0d0d0d", border: "1px solid #1e1e1e", borderRadius: 8, padding: "12px 14px" }}>
            <div style={{ fontSize: 10, color: "#3a3a3a", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 6 }}>{lbl}</div>
            <div style={{ fontSize: 13, color: "#bbb" }}>{val}</div>
          </div>
        ))}
      </div>

      <div style={{ background: "#0d0d0d", border: "1px solid #1e1e1e", borderRadius: 8, padding: "14px 16px", marginBottom: 14 }}>
        <div style={{ fontSize: 10, color: "#3a3a3a", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12 }}>Задачи</div>
        {inc.tasks.map((task, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "8px 0", borderBottom: "1px solid #141414",
            animation: "fadeSlideIn 0.3s ease both", animationDelay: `${i * 60}ms` }}>
            <div style={{
              width: 15, height: 15, borderRadius: 3, flexShrink: 0,
              border: `1px solid ${task.done ? "#2d5c2d" : "#2a2a2a"}`,
              background: task.done ? "#1a2d1a" : "transparent",
              display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              {task.done && <span style={{ fontSize: 9, color: "#44bb44" }}>✓</span>}
            </div>
            <span style={{ fontSize: 13, color: task.done ? "#444" : "#aaa", textDecoration: task.done ? "line-through" : "none" }}>{task.label}</span>
          </div>
        ))}
      </div>

      {inc.hazmat && (
        <div style={{ background: "#241408", border: "1px solid #6b3010", borderRadius: 8, padding: "14px 16px" }}>
          <div style={{ fontSize: 10, color: "#aa5520", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 8 }}>⚠ Опасни вещества</div>
          <div style={{ fontSize: 13, color: "#bb7744" }}>
            Установено: <strong style={{ color: "#ffaa55" }}>{inc.hazmat}</strong><br />
            Протокол: Евакуационна зона 200м. Избягвайте вдишване. Без открит пламък.
          </div>
        </div>
      )}
    </div>
  );
}

export default function Incidents({ selectedIncident, setSelectedIncident }) {
  const [incidents, setIncidents] = useState([]);
  const [filter, setFilter]       = useState("all");
  const [loading, setLoading]     = useState(true);

  useEffect(() => {
    fetch(`${API}/incidents/`).then(r => r.json()).then(d => { setIncidents(d); setLoading(false); });
  }, []);

  if (selectedIncident) return <IncidentDetail inc={selectedIncident} onBack={() => setSelectedIncident(null)} />;
  if (loading) return <LoadingSpinner />;

  const filtered = filter === "all" ? incidents : incidents.filter(i => i.status === filter);

  return (
    <div style={{ animation: "fadeSlideIn 0.3s ease both" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20 }}>
        <PageHeader eyebrow="Регистър" title="Произшествия" />
        <div style={{ display: "flex", gap: 5 }}>
          {[["all", "Всички"], ["active", "Активни"], ["closed", "Приключени"]].map(([val, lbl]) => (
            <button key={val} onClick={() => setFilter(val)} style={{
              background: filter === val ? "#161616" : "none",
              border: `1px solid ${filter === val ? "#3a3a3a" : "#1a1a1a"}`,
              borderRadius: 6, color: filter === val ? "#ccc" : "#444",
              padding: "5px 12px", cursor: "pointer", fontSize: 11,
              fontFamily: "inherit", transition: "all 0.15s",
            }}>{lbl}</button>
          ))}
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
        {filtered.map((inc, i) => (
          <Card key={inc.id} onClick={() => setSelectedIncident(inc)}
            style={{ animation: "fadeSlideIn 0.3s ease both", animationDelay: `${i * 50}ms` }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 7 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                <div style={{ width: 7, height: 7, borderRadius: "50%", background: SEVERITY_COLOR[inc.severity] }} />
                <span style={{ fontSize: 11, color: "#444", fontFamily: "monospace" }}>{inc.id}</span>
                <span style={{ fontSize: 14, fontWeight: 600, color: "#c0c0c0" }}>{inc.type}</span>
              </div>
              <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
                <span style={{ fontSize: 11, color: "#444" }}>{inc.time}</span>
                <Badge status={inc.status} label={inc.status === "active" ? "Активно" : "Приключено"} />
              </div>
            </div>
            <div style={{ fontSize: 12, color: "#444" }}>{inc.address}</div>
            <div style={{ fontSize: 11, color: "#333", marginTop: 4 }}>
              Екип: {inc.team}{inc.hazmat ? ` · ⚠ ${inc.hazmat}` : ""}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
