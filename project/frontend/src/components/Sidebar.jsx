const NAV_ITEMS = [
  { id: "dashboard", label: "Табло" },
  { id: "incidents", label: "Произшествия" },
  { id: "teams",     label: "Екипи" },
  { id: "vehicles",  label: "Автомобили" },
  { id: "map",       label: "Карта" },
  { id: "schedule",  label: "График" },
];

export default function Sidebar({ page, setPage, setSelectedIncident, activeIncidents }) {
  const now = new Date().toLocaleTimeString("bg-BG", { hour: "2-digit", minute: "2-digit" });

  return (
    <aside style={{
      width: 210, background: "#080808", borderRight: "1px solid #161616",
      display: "flex", flexDirection: "column", flexShrink: 0,
    }}>
      {/* Logo */}
      <div style={{ padding: "18px 14px 14px", borderBottom: "1px solid #161616" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
          <div style={{
            width: 30, height: 30, background: "#b81c00", borderRadius: 5,
            display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16,
            boxShadow: "0 0 12px #b81c0044",
          }}>🔥</div>
          <div>
            <div style={{ fontSize: 12, fontWeight: 700, color: "#cc3300", letterSpacing: "0.1em" }}>ГДПБЗН</div>
            <div style={{ fontSize: 9, color: "#2e2e2e", letterSpacing: "0.06em" }}>МВР · БЪЛГАРИЯ</div>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <div style={{ width: 5, height: 5, borderRadius: "50%", background: "#44bb44", boxShadow: "0 0 6px #44bb4488" }} />
          <span style={{ fontSize: 10, color: "#2e2e2e" }}>Система активна · {now}</span>
        </div>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: "10px 6px" }}>
        {NAV_ITEMS.map((item, i) => {
          const active = page === item.id;
          return (
            <button key={item.id}
              onClick={() => { setPage(item.id); if (item.id !== "incidents") setSelectedIncident(null); }}
              style={{
                width: "100%", display: "flex", alignItems: "center", justifyContent: "space-between",
                padding: "9px 12px", marginBottom: 2, borderRadius: 6, cursor: "pointer",
                border: "none", fontFamily: "inherit", fontSize: 12, textAlign: "left",
                background: active ? "#141414" : "transparent",
                color: active ? "#d0d0d0" : "#3a3a3a",
                borderLeft: active ? "2px solid #cc3300" : "2px solid transparent",
                transition: "all 0.15s",
                animation: `fadeSlideIn 0.3s ease both`,
                animationDelay: `${i * 40}ms`,
              }}
              onMouseEnter={e => { if (!active) { e.currentTarget.style.color = "#777"; e.currentTarget.style.background = "#0e0e0e"; } }}
              onMouseLeave={e => { if (!active) { e.currentTarget.style.color = "#3a3a3a"; e.currentTarget.style.background = "transparent"; } }}
            >
              <span style={{ letterSpacing: "0.04em" }}>{item.label}</span>
              {item.id === "incidents" && activeIncidents > 0 && (
                <span style={{
                  background: "#6e1010", color: "#ff7777", borderRadius: 10,
                  padding: "1px 7px", fontSize: 10, fontWeight: 700,
                }}>{activeIncidents}</span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer */}
      <div style={{ padding: "10px 14px", borderTop: "1px solid #161616" }}>
        <div style={{ fontSize: 10, color: "#252525" }}>Оперативен дежурен</div>
        <div style={{ fontSize: 11, color: "#383838", marginTop: 2 }}>ст. комисар Начев</div>
      </div>
    </aside>
  );
}
