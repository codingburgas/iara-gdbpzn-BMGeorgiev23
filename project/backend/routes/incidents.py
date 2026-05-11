from flask import Blueprint, jsonify
from data import INCIDENTS, TEAMS, STAFF, VEHICLES

incidents_bp = Blueprint("incidents", __name__)


@incidents_bp.route("/", methods=["GET"])
def get_incidents():
    return jsonify(INCIDENTS)


@incidents_bp.route("/<incident_id>", methods=["GET"])
def get_incident(incident_id):
    inc = next((i for i in INCIDENTS if i["id"] == incident_id), None)
    if not inc:
        return jsonify({"error": "Not found"}), 404
    return jsonify(inc)


@incidents_bp.route("/summary", methods=["GET"])
def get_summary():
    active    = [i for i in INCIDENTS if i["status"] == "active"]
    deployed  = [t for t in TEAMS    if t["status"] == "deployed"]
    standby   = [t for t in TEAMS    if t["status"] == "standby"]
    available = [s for s in STAFF    if s["status"] in ("standby", "deployed")]

    avg_fuel = round(
        sum(v["fuel"] for v in VEHICLES) / len(VEHICLES)
    ) if VEHICLES else 0

    return jsonify({
        "active_incidents":  len(active),
        "deployed_teams":    len(deployed),
        "standby_teams":     len(standby),
        "available_staff":   len(available),
        "total_staff":       len(STAFF),
        "average_fuel_pct":  avg_fuel,
    })
