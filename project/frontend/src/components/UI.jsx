import { STATUS_STYLES } from "../constants";

export function Badge({ status, label }) {
  const s = STATUS_STYLES[status] || STATUS_STYLES.offduty;
  return (
    <span style={{
      background: s.bg, color: s.text, border: `1px solid ${s.border}`,
      borderRadius: 4, padding: "2px 8px", fontSize: 11, fontWeight: 700,
      letterSpacing: "0.06em", textTransform: "uppercase", whiteSpace: "nowrap",
    }}>{label}</span>
  );
}

export function StatCard({ label, value, color }) {
  return (
    <div className="stat-card" style={{ flex: 1, minWidth: 110 }}>
      <div style={{ fontSize: 10, color: "#4a4a4a", letterSpacing: "0.1em", textTransform: "uppercase", marginBottom: 8 }}>{label}</div>
      <div style={{ fontSize: 26, fontWeight: 700, color: color || "#d8d8d8", fontFamily: "monospace" }}>{value}</div>
    </div>
  );
}

export function FuelBar({ pct }) {
  const color = pct > 60 ? "#44bb44" : pct > 30 ? "#ffaa00" : "#ff4444";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      <div style={{ flex: 1, height: 5, background: "#1e1e1e", borderRadius: 3, overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, height: "100%", background: color, borderRadius: 3, transition: "width 0.6s ease" }} />
      </div>
      <span style={{ fontSize: 11, color: "#555", minWidth: 32 }}>{pct}%</span>
    </div>
  );
}

export function BackButton({ onClick }) {
  return (
    <button onClick={onClick} style={{
      background: "none", border: "1px solid #2a2a2a", borderRadius: 6,
      color: "#666", padding: "6px 14px", cursor: "pointer", fontSize: 12,
      marginBottom: 20, fontFamily: "inherit", transition: "border-color 0.15s, color 0.15s",
    }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = "#555"; e.currentTarget.style.color = "#aaa"; }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = "#2a2a2a"; e.currentTarget.style.color = "#666"; }}
    >← Назад</button>
  );
}

export function PageHeader({ eyebrow, title }) {
  return (
    <div style={{ marginBottom: 22 }}>
      {eyebrow && <div style={{ fontSize: 10, color: "#444", letterSpacing: "0.14em", textTransform: "uppercase", marginBottom: 4 }}>{eyebrow}</div>}
      <div style={{ fontSize: 20, fontWeight: 700, color: "#e0e0e0" }}>{title}</div>
    </div>
  );
}

export function Card({ children, onClick, style = {} }) {
  const base = {
    background: "#0d0d0d", border: "1px solid #1e1e1e", borderRadius: 8,
    padding: "14px 18px", transition: "border-color 0.15s",
    ...(onClick ? { cursor: "pointer" } : {}),
    ...style,
  };
  return (
    <div style={base}
      onClick={onClick}
      onMouseEnter={onClick ? e => e.currentTarget.style.borderColor = "#3a3a3a" : undefined}
      onMouseLeave={onClick ? e => e.currentTarget.style.borderColor = "#1e1e1e" : undefined}
    >{children}</div>
  );
}

export function LoadingSpinner() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10, color: "#444", fontSize: 13, padding: "40px 0" }}>
      <div style={{ width: 16, height: 16, border: "2px solid #2a2a2a", borderTopColor: "#cc3300", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
      Зареждане…
    </div>
  );
}
