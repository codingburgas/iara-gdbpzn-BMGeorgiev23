import { useState, useEffect } from "react";
import { API } from "../constants";
import { Badge, StatCard, Card, BackButton, LoadingSpinner, PageHeader } from "../components/UI";

function TeamDetail({ team, onBack }) {
  const [detail, setDetail] = useState(null);

  useEffect(() => {
    fetch(`${API}/teams/${team.id}`).then(r => r.json()).then(setDetail);
  }, [team.id]);

  if (!detail) return <LoadingSpinner />;

  return (
    <div style={{ animation: "fadeSlideIn 0.25s ease both" }}>
      <BackButton onClick={onBack} />
      <div style={{ fontSize: 20, fontWeight: 700, color: "#e0e0e0", marginBottom: 4 }}>{detail.name}</div>
      <div style={{ fontSize: 12, color: "#444", marginBottom: 20 }}>{detail.vehicle}</div>

      <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
        <StatCard label="Общо"    value={detail.members} />
        <StatCard label="Налични" value={detail.available} color="#5ba3d9" />
        <StatCard label="Статус"
          value={detail.status === "deployed" ? "Разгърнат" : "Готовност"}
          color={detail.status === "deployed" ? "#ffb347" : "#5ba3d9"} />
      </div>

      {detail.incident && (
        <div style={{ background: "#1c0f0f", border: "1px solid #5a1818", borderRadius: 8, padding: "10px 14px", marginBottom: 14, fontSize: 12, color: "#bb7777" }}>
          Активно произшествие: <strong style={{ color: "#ff8888" }}>{detail.incident}</strong>
        </div>
      )}

      <Card>
        <div style={{ fontSize: 10, color: "#3a3a3a", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 12 }}>Членове на екипа</div>
        {detail.staff.map((m, i) => (
          <div key={m.id} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid #141414",
            animation: "fadeSlideIn 0.3s ease both", animationDelay: `${i * 60}ms` }}>
            <div>
              <div style={{ fontSize: 13, color: "#c0c0c0" }}>{m.name}</div>
              <div style={{ fontSize: 10, color: "#444", marginTop: 2 }}>{m.role}</div>
            </div>
            <Badge status={m.status} label={
              { deployed: "Разгърнат", standby: "Готовност", leave: "В отпуск", sick: "Болничен", offduty: "Изключен" }[m.status]
            } />
          </div>
        ))}
      </Card>
    </div>
  );
}

export default function Teams() {
  const [teams,    setTeams]    = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading,  setLoading]  = useState(true);

  useEffect(() => {
    fetch(`${API}/teams/`).then(r => r.json()).then(d => { setTeams(d); setLoading(false); });
  }, []);

  if (loading)  return <LoadingSpinner />;
  if (selected) return <TeamDetail team={selected} onBack={() => setSelected(null)} />;

  return (
    <div style={{ animation: "fadeSlideIn 0.3s ease both" }}>
      <PageHeader eyebrow="Управление" title="Екипи" />

      <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
        <StatCard label="Разгърнати" value={teams.filter(t => t.status === "deployed").length}  color="#ffb347" />
        <StatCard label="В готовност" value={teams.filter(t => t.status === "standby").length}  color="#5ba3d9" />
        <StatCard label="Изкл."       value={teams.filter(t => t.status === "offduty").length}  color="#444" />
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 7 }}>
        {teams.map((t, i) => (
          <Card key={t.id} onClick={() => setSelected(t)}
            style={{ animation: "fadeSlideIn 0.3s ease both", animationDelay: `${i * 50}ms` }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
              <span style={{ fontSize: 14, fontWeight: 600, color: "#c0c0c0" }}>{t.name}</span>
              <Badge status={t.status} label={t.status === "deployed" ? "Разгърнат" : t.status === "standby" ? "Готовност" : "Изкл."} />
            </div>
            <div style={{ fontSize: 12, color: "#444" }}>{t.vehicle}</div>
            <div style={{ fontSize: 11, color: "#333", marginTop: 4 }}>
              {t.available}/{t.members} налични{t.incident ? ` · ${t.incident}` : ""}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
