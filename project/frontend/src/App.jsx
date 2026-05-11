import { useState, useEffect } from "react";
import { API } from "./constants";
import Sidebar    from "./components/Sidebar";
import Dashboard  from "./pages/Dashboard";
import Incidents  from "./pages/Incidents";
import Teams      from "./pages/Teams";
import Vehicles   from "./pages/Vehicles";
import MapPage    from "./pages/Map";
import Schedule   from "./pages/Schedule";
import "./index.css";

export default function App() {
  const [page,             setPage]             = useState("dashboard");
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [activeIncidents,  setActiveIncidents]  = useState(0);

  useEffect(() => {
    fetch(`${API}/incidents/summary`)
      .then(r => r.json())
      .then(d => setActiveIncidents(d.active_incidents));
  }, []);

  const pages = {
    dashboard: <Dashboard setPage={setPage} setSelectedIncident={setSelectedIncident} />,
    incidents: <Incidents selectedIncident={selectedIncident} setSelectedIncident={setSelectedIncident} />,
    teams:     <Teams />,
    vehicles:  <Vehicles />,
    map:       <MapPage />,
    schedule:  <Schedule />,
  };

  return (
    <div style={{ display: "flex", height: "100vh", background: "#080808", overflow: "hidden" }}>
      <Sidebar
        page={page} setPage={setPage}
        setSelectedIncident={setSelectedIncident}
        activeIncidents={activeIncidents}
      />
      <main style={{ flex: 1, overflow: "auto", padding: "28px 32px" }}>
        {pages[page]}
      </main>
    </div>
  );
}
