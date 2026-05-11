import { useState, useEffect } from "react";
import { API } from "../constants";
import { Badge, StatCard, FuelBar, Card, LoadingSpinner, PageHeader } from "../components/UI";

export default function Vehicles() {
  const [vehicles, setVehicles] = useState([]);
  const [loading,  setLoading]  = useState(true);

  useEffect(() => {
    fetch(`${API}/vehicles/`).then(r => r.json()).then(d => { setVehicles(d); setLoading(false); });
  }, []);

  if (loading) return <LoadingSpinner />;

  const avgFuel = Math.round(vehicles.reduce((a, v) => a + v.fuel, 0) / vehicles.length);

  return (
    <div style={{ animation: "fadeSlideIn 0.3s ease both" }}>
      <PageHeader eyebrow="Флот" title="Пожарни автомобили" />

      <div style={{ display: "flex", gap: 10, marginBottom: 20, flexWrap: "wrap" }}>
        <StatCard label="Разгърнати"  value={vehicles.filter(v => v.status === "deployed").length}    color="#ffb347" />
        <StatCard label="В готовност" value={vehicles.filter(v => v.status === "standby").length}     color="#5ba3d9" />
        <StatCard label="Сервиз"      value={vehicles.filter(v => v.status === "maintenance").length} color="#b87fcc" />
        <StatCard label="Средно гориво" value={`${avgFuel}%`} />
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
        {vehicles.map((v, i) => (
          <Card key={v.id} style={{ animation: "fadeSlideIn 0.3s ease both", animationDelay: `${i * 50}ms` }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 4 }}>
                  <span style={{ fontFamily: "monospace", fontSize: 13, color: "#cc5522", fontWeight: 700 }}>{v.id}</span>
                  <span style={{ fontSize: 14, fontWeight: 600, color: "#c0c0c0" }}>{v.model}</span>
                </div>
                <div style={{ fontSize: 11, color: "#444" }}>{v.type} · {v.year}</div>
                {v.crew && <div style={{ fontSize: 11, color: "#333", marginTop: 2 }}>Екип: {v.crew}</div>}
              </div>
              <Badge status={v.status} label={
                { deployed: "Разгърнат", standby: "Готовност", maintenance: "Сервиз" }[v.status]
              } />
            </div>
            <div style={{ fontSize: 10, color: "#3a3a3a", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 6 }}>Гориво</div>
            <FuelBar pct={v.fuel} />
          </Card>
        ))}
      </div>
    </div>
  );
}
