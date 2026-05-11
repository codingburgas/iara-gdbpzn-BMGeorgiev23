export const API = "http://localhost:5000/api";

export const STATUS_STYLES = {
  active:      { bg: "#3d1a1a", text: "#ff6b6b", border: "#8b2020" },
  closed:      { bg: "#1a2d1a", text: "#6bcb77", border: "#1f5e25" },
  deployed:    { bg: "#3d2a10", text: "#ffb347", border: "#7a4e0d" },
  standby:     { bg: "#1a2535", text: "#5ba3d9", border: "#1e4876" },
  offduty:     { bg: "#1e1e1e", text: "#666",    border: "#2a2a2a" },
  maintenance: { bg: "#2a1f35", text: "#b87fcc", border: "#5e3475" },
  leave:       { bg: "#1e2535", text: "#5ba3d9", border: "#1e4876" },
  sick:        { bg: "#2d2810", text: "#f0c040", border: "#6b5a10" },
};

export const SEVERITY_COLOR = { high: "#ff4444", medium: "#ffaa00", low: "#44bb44" };
export const SEVERITY_LABEL = { high: "Висока",  medium: "Средна",  low: "Ниска"  };

export const STATUS_LABEL = {
  active: "Активно", closed: "Приключено",
  deployed: "Разгърнат", standby: "Готовност",
  offduty: "Изключен", maintenance: "Сервиз",
  leave: "В отпуск", sick: "Болничен",
};
