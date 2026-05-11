import { useState, useEffect } from "react";
import { API } from "../constants";
import { Badge, StatCard, LoadingSpinner, PageHeader } from "../components/UI";

export default function Schedule() {
  const [data,    setData]    = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/schedule/`).then(r => r.json()).then(d => { setData(d); setLoading(false); });
  }, []);

  if (loading || !data) return <LoadingSpinner />;

  const today = new Date().toLocaleDateString("bg-BG", { weekday: "long", day: "numeric", month: "long" });

  return (
    <div style={{ animation: "fadeSlideIn 0.3s ease both" }}>
      <PageHeader eyebrow="Текуща смяна" title="График" />
      <div style={{ fontSize: 12, color: "#444", marginTop: -14, marginBottom: 20 }}>{today}</div>

      <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
        <StatCard label="На дежурство" value={data.on_duty}  color="#44bb44" />
        <StatCard label="В отпуск"     value={data.on_leave} color="#5ba3d9" />
        <StatCard label="Болничен"     value={data.sick}      color="#f0c040" />
      </div>

      <div style={{ background: "#0d0d0d", border: "1px solid #1e1e1e", borderRadius: 8, overflow: "hidden" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1.2fr 1fr 0.8fr 130px", padding: "9px 16px", borderBottom: "1px solid #141414" }}>
          {["Служител", "Екип", "Смяна", "Статус"].map(h => (
            <div key={h} style={{ fontSize: 10, color: "#333", textTransform: "uppercase", letterSpacing: "0.08em" }}>{h}</div>
          ))}
        </div>
        {data.entries.map((s, i) => (
          <div key={i} style={{
            display: "grid", gridTemplateColumns: "1.2fr 1fr 0.8fr 130px",
            padding: "11px 16px", borderBottom: "1px solid #111", alignItems: "center",
            animation: "fadeSlideIn 0.3s ease both", animationDelay: `${i * 55}ms`,
          }}>
            <div style={{ fontSize: 13, color: "#bbb" }}>{s.name}</div>
            <div style={{ fontSize: 11, color: "#444" }}>{s.team}</div>
            <div style={{ fontFamily: "monospace", fontSize: 12, color: s.shift === "—" ? "#2a2a2a" : "#777" }}>{s.shift}</div>
            <div>
              {s.sick    ? <Badge status="sick"    label="Болничен" /> :
               s.leave   ? <Badge status="leave"   label={`Отпуск`} /> :
               s.shift !== "—" ? <Badge status="standby" label="Дежурен" /> :
               <Badge status="offduty" label="Изключен" />}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
