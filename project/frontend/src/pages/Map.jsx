import { useState, useEffect } from "react";
import { API } from "../constants";
import { LoadingSpinner, PageHeader } from "../components/UI";

export default function MapPage() {
  const [incidents, setIncidents] = useState([]);
  const [vehicles,  setVehicles]  = useState([]);
  const [loading,   setLoading]   = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/incidents/`).then(r => r.json()),
      fetch(`${API}/vehicles/`).then(r => r.json()),
    ]).then(([inc, veh]) => { setIncidents(inc); setVehicles(veh); setLoading(false); });
  }, []);

  if (loading) return <LoadingSpinner />;

  const activeInc      = incidents.filter(i => i.status === "active");
  const deployedVeh    = vehicles.filter(v => v.status === "deployed");

  const mapPoints = [
    ...activeInc.map(i => ({ label: i.id.slice(-4), color: "#ff4444", type: "incident", x: 38 + Math.random() * 30, y: 30 + Math.random() * 40 })),
    ...deployedVeh.map(v => ({ label: v.id, color: "#5ba3d9", type: "vehicle", x: 20 + Math.random() * 50, y: 50 + Math.random() * 35 })),
  ];

  return (
    <div style={{ animation: "fadeSlideIn 0.3s ease both" }}>
      <PageHeader eyebrow="Оперативна" title="Карта" />

      {/* Map canvas */}
      <div style={{
        background: "#070f07", border: "1px solid #142014", borderRadius: 10,
        height: 320, position: "relative", overflow: "hidden", marginBottom: 16,
      }}>
        <div style={{
          position: "absolute", inset: 0,
          backgroundImage: "linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px)",
          backgroundSize: "36px 36px",
        }} />
        <div style={{ position: "absolute", top: 10, left: 12, fontSize: 10, color: "#1a3a1a", letterSpacing: "0.1em" }}>БУРГАС · GPS LIVE</div>

        {mapPoints.map((p, i) => (
          <div key={i} style={{ position: "absolute", left: `${p.x}%`, top: `${p.y}%`, transform: "translate(-50%, -50%)" }}>
            <div style={{
              width: p.type === "vehicle" ? 9 : 13, height: p.type === "vehicle" ? 9 : 13,
              borderRadius: "50%", background: p.color,
              animation: p.type === "incident" ? "pulseMap 1.6s infinite" : "none",
            }} />
            <div style={{ fontSize: 9, color: p.color, textAlign: "center", marginTop: 3, fontFamily: "monospace", whiteSpace: "nowrap" }}>{p.label}</div>
          </div>
        ))}

        <div style={{ position: "absolute", bottom: 10, right: 12, display: "flex", flexDirection: "column", gap: 5 }}>
          {[["#ff4444", "Произшествие"], ["#5ba3d9", "Автомобил"]].map(([c, l]) => (
            <div key={l} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 10, color: "#333" }}>
              <div style={{ width: 7, height: 7, borderRadius: "50%", background: c }} /> {l}
            </div>
          ))}
        </div>
      </div>

      <div style={{ fontSize: 10, color: "#3a3a3a", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 10 }}>Активни единици</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {activeInc.map((inc, i) => (
          <div key={inc.id} style={{ background: "#0d0d0d", border: "1px solid #1e1e1e", borderRadius: 8, padding: "10px 14px",
            display: "flex", justifyContent: "space-between", alignItems: "center",
            animation: "fadeSlideIn 0.3s ease both", animationDelay: `${i * 50}ms` }}>
            <div>
              <div style={{ fontSize: 12, color: "#bbb" }}>{inc.id} — {inc.type}</div>
              <div style={{ fontSize: 10, color: "#444", marginTop: 2 }}>{inc.gps.lat}° N, {inc.gps.lng}° E</div>
            </div>
            <div style={{ width: 7, height: 7, borderRadius: "50%", background: "#ff4444", animation: "pulseMap 1.6s infinite" }} />
          </div>
        ))}
        {deployedVeh.map((v, i) => (
          <div key={v.id} style={{ background: "#0d0d0d", border: "1px solid #1e1e1e", borderRadius: 8, padding: "10px 14px",
            display: "flex", justifyContent: "space-between", alignItems: "center",
            animation: "fadeSlideIn 0.3s ease both", animationDelay: `${(activeInc.length + i) * 50}ms` }}>
            <div>
              <div style={{ fontSize: 12, color: "#bbb" }}>{v.id} — {v.model}</div>
              <div style={{ fontSize: 10, color: "#444", marginTop: 2 }}>GPS активен · {v.crew}</div>
            </div>
            <div style={{ width: 7, height: 7, borderRadius: "50%", background: "#5ba3d9" }} />
          </div>
        ))}
      </div>
    </div>
  );
}
